
import googlemaps
from app.config import settings
from typing import List, Dict, Optional, Any, Tuple
import logging
import time

logger = logging.getLogger(__name__)

class GoogleMapsService:
    def __init__(self):
        """Initialize Google Maps client"""
        if not settings.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is required")
        
        self.client = googlemaps.Client(key=settings.GOOGLE_API_KEY)
        logger.info("✅ Google Maps API initialized")
    
    def get_nearby_places_by_types(
        self, 
        lat: float, 
        lng: float, 
        radius: int = 500,
        place_types: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get nearby places - ONLY restaurants, cafes, gyms, bars
        """
        # ONLY search for these types
        if place_types is None:
            place_types = ['restaurant', 'cafe', 'gym', 'bar', 'food', 'meal_takeaway']
        
        all_places = []
        
        for place_type in place_types:
            try:
                logger.info(f"🔍 Searching for {place_type} near ({lat}, {lng})")
                
                places_result = self.client.places_nearby(
                    location=(lat, lng),
                    radius=radius,
                    type=place_type,
                    language='en'
                )
                
                places = places_result.get('results', [])
                
                for place in places:
                    enriched = self._enrich_place(place, place_type)
                    all_places.append(enriched)
                
                logger.info(f"   Found {len(places)} {place_type}(s)")
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error searching {place_type}: {e}")
                continue
        
        # Remove duplicates
        unique_places = []
        seen_ids = set()
        
        for place in all_places:
            place_id = place.get('place_id')
            if place_id and place_id not in seen_ids:
                seen_ids.add(place_id)
                unique_places.append(place)
        
        logger.info(f"📍 Total restaurants/cafes/gyms found: {len(unique_places)}")
        return unique_places
    
    def _enrich_place(self, place: Dict, place_type: str) -> Dict[str, Any]:
        """Enrich place data"""
        result = {
            'place_id': place.get('place_id'),
            'name': place.get('name', 'Unknown'),
            'types': place.get('types', []),
            'rating': place.get('rating', 0),
            'vicinity': place.get('vicinity', 'Address not available'),
            'geometry': place.get('geometry', {}),
            'price_level': place.get('price_level'),
            'user_ratings_total': place.get('user_ratings_total', 0),
            'search_source': place_type
        }
        
        # Price level
        price_map = {0: 'Free', 1: 'Inexpensive', 2: 'Moderate', 3: 'Expensive', 4: 'Very Expensive'}
        result['price_level_text'] = price_map.get(result['price_level'], 'Unknown')
        
        return result
    
    def get_healthy_alternatives_nearby(
        self,
        lat: float,
        lng: float,
        radius: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Get healthy alternatives nearby - ONLY cafes, gyms, healthy restaurants
        """
        try:
            # Search for healthy places
            healthy_types = ['cafe', 'gym', 'food']  # Only these
            
            all_places = []
            for h_type in healthy_types:
                places = self.get_nearby_places_by_types(lat, lng, radius, [h_type])
                all_places.extend(places[:5])  # Get top 5 per type
            
            # Filter for healthy names
            healthy_places = []
            for place in all_places:
                name = place.get('name', '').lower()
                
                # Skip unhealthy names
                if any(word in name for word in ['fast food', 'fried', 'burger', 'pizza', 'kfc', 'mcdonald']):
                    continue
                
                # Prefer healthy names
                if any(word in name for word in ['cafe', 'coffee', 'healthy', 'salad', 'juice', 'smoothie', 'gym', 'fitness']):
                    healthy_places.append(place)
                elif place.get('rating', 0) >= 4.0:  # High-rated places
                    healthy_places.append(place)
            
            return healthy_places[:10]  # Return top 10
            
        except Exception as e:
            logger.error(f"Error getting healthy alternatives: {e}")
            return []

# Singleton instance
google_service = GoogleMapsService()