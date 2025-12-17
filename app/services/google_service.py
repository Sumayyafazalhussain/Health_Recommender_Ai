
# import googlemaps
# from app.config import settings
# from typing import List, Dict, Optional
# import logging

# logger = logging.getLogger(__name__)

# class GoogleMapsService:
#     def __init__(self):
#         """Initialize Google Maps client with real API"""
#         if not settings.GOOGLE_API_KEY:
#             raise ValueError("GOOGLE_API_KEY is required")
        
#         self.client = googlemaps.Client(key=settings.GOOGLE_API_KEY)
#         logger.info("✅ Google Maps API initialized")
    
#     def get_nearby_places(
#         self, 
#         lat: float, 
#         lng: float, 
#         radius: int = 500,
#         place_type: Optional[str] = None
#     ) -> List[Dict]:
#         """
#         Get nearby places from Google Places API
        
#         Args:
#             lat: Latitude
#             lng: Longitude
#             radius: Search radius in meters
#             place_type: Optional Google Places type filter

        
#         Returns:
#             List of place dictionaries from Google API
#         """
#         try:
#             params = {
#                 'location': (lat, lng),
#                 'radius': radius,
#                 'language': 'en'
#             }
            
#             if place_type:
#                 params['type'] = place_type
            
#             places_result = self.client.places_nearby(**params)
#             places = places_result.get('results', [])
            
#             logger.info(f"📍 Google Maps API found {len(places)} places near ({lat}, {lng})")
            
#             # Log first few places for debugging
#             if places and logger.isEnabledFor(logging.DEBUG):
#                 for i, place in enumerate(places[:3]):
#                     logger.debug(f"  {i+1}. {place.get('name')} - {place.get('types', [])[:3]}")
            
#             return places
            
#         except googlemaps.exceptions.ApiError as e:
#             logger.error(f"Google Maps API error: {e}")
#             raise Exception(f"Google Maps API error: {e}")
#         except Exception as e:
#             logger.error(f"Error in get_nearby_places: {e}")
#             raise
    
#     def get_place_details(self, place_id: str) -> Optional[Dict]:
#         """Get detailed information about a place"""
#         try:
#             return self.client.place(place_id)
#         except Exception as e:
#             logger.error(f"Error getting place details: {e}")
#             return None

# # Singleton instance
# google_service = GoogleMapsService()import googlemaps
# import googlemaps
# from app.config import settings
# from typing import List, Dict, Optional, Any, Tuple
# import logging
# import time

# logger = logging.getLogger(__name__)

# class GoogleMapsService:
#     def __init__(self):
#         """Initialize Google Maps client with real API"""
#         if not settings.GOOGLE_API_KEY:
#             raise ValueError("GOOGLE_API_KEY is required")
        
#         self.client = googlemaps.Client(key=settings.GOOGLE_API_KEY)
#         self.cache = {}  # Simple cache to avoid duplicate API calls
#         logger.info("✅ Google Maps API initialized")
    
#     def get_nearby_places(
#         self, 
#         lat: float, 
#         lng: float, 
#         radius: int = 500,
#         place_type: Optional[str] = None,
#         keyword: Optional[str] = None,
#         min_rating: float = 3.0
#     ) -> List[Dict[str, Any]]:
#         """
#         Get nearby places from Google Places API with enriched data
        
#         Args:
#             lat: Latitude
#             lng: Longitude
#             radius: Search radius in meters (max 50000)
#             place_type: Google Places type (restaurant, cafe, park, etc.)
#             keyword: Search keyword
#             min_rating: Minimum rating to include
        
#         Returns:
#             List of enriched place dictionaries
#         """
#         try:
#             cache_key = f"{lat},{lng},{radius},{place_type},{keyword}"
#             if cache_key in self.cache:
#                 logger.info(f"📦 Using cached results for: {cache_key}")
#                 return self.cache[cache_key]
            
#             logger.info(f"📍 Searching Google Places: ({lat}, {lng}), radius: {radius}m, type: {place_type}")
            
#             params = {
#                 'location': (lat, lng),
#                 'radius': min(radius, 50000),  # Google max is 50000
#                 'language': 'en'
#             }
            
#             if place_type:
#                 params['type'] = place_type
            
#             if keyword:
#                 params['keyword'] = keyword
            
#             # Make API call
#             places_result = self.client.places_nearby(**params)
#             places = places_result.get('results', [])
            
#             # Enrich places with more details
#             enriched_places = []
#             for place in places[:20]:  # Limit to 20 places for performance
#                 enriched = self._enrich_place_details(place)
                
#                 # Filter by minimum rating
#                 if enriched.get('rating', 0) >= min_rating:
#                     enriched_places.append(enriched)
            
#             # Sort by rating (highest first)
#             enriched_places.sort(key=lambda x: x.get('rating', 0), reverse=True)
            
#             logger.info(f"✅ Found {len(enriched_places)} places (filtered from {len(places)})")
            
#             # Cache for 5 minutes
#             self.cache[cache_key] = enriched_places
#             if len(self.cache) > 50:  # Limit cache size
#                 self.cache.pop(next(iter(self.cache)))
            
#             return enriched_places
            
#         except googlemaps.exceptions.ApiError as e:
#             logger.error(f"Google Maps API error: {e}")
#             # Return sample data if API fails (for testing)
#             return self._get_sample_places(lat, lng, place_type)
#         except Exception as e:
#             logger.error(f"Error in get_nearby_places: {e}")
#             return self._get_sample_places(lat, lng, place_type)
    
#     def get_nearby_restaurants(
#         self,
#         lat: float,
#         lng: float,
#         radius: int = 1000,
#         include_fast_food: bool = True
#     ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
#         """
#         Get nearby restaurants categorized by healthiness
        
#         Returns:
#             Tuple of (unhealthy_restaurants, healthy_restaurants)
#         """
#         try:
#             logger.info(f"🍽️ Searching restaurants near: ({lat}, {lng})")
            
#             # Search for restaurants
#             all_restaurants = self.get_nearby_places(
#                 lat=lat,
#                 lng=lng,
#                 radius=radius,
#                 place_type="restaurant"
#             )
            
#             # Also search for food places
#             food_places = self.get_nearby_places(
#                 lat=lat,
#                 lng=lng,
#                 radius=radius,
#                 place_type="food"
#             )
            
#             # Combine and deduplicate
#             all_places = all_restaurants + food_places
#             unique_places = []
#             seen_ids = set()
            
#             for place in all_places:
#                 place_id = place.get('place_id')
#                 if place_id and place_id not in seen_ids:
#                     seen_ids.add(place_id)
#                     unique_places.append(place)
            
#             # Categorize by healthiness
#             unhealthy_restaurants = []
#             healthy_restaurants = []
            
#             for restaurant in unique_places:
#                 # Determine if it's unhealthy
#                 is_unhealthy = self._is_unhealthy_restaurant(restaurant)
#                 restaurant['is_unhealthy'] = is_unhealthy
#                 restaurant['is_restaurant'] = True
                
#                 if is_unhealthy and include_fast_food:
#                     unhealthy_restaurants.append(restaurant)
#                 else:
#                     healthy_restaurants.append(restaurant)
            
#             # Sort unhealthy by rating (highest first)
#             unhealthy_restaurants.sort(key=lambda x: x.get('rating', 0), reverse=True)
            
#             # Sort healthy by health score then rating
#             for restaurant in healthy_restaurants:
#                 restaurant['health_score'] = self._calculate_health_score(restaurant)
            
#             healthy_restaurants.sort(
#                 key=lambda x: (x.get('health_score', 0), x.get('rating', 0)), 
#                 reverse=True
#             )
            
#             logger.info(f"✅ Found {len(unhealthy_restaurants)} unhealthy and {len(healthy_restaurants)} healthy restaurants")
#             return unhealthy_restaurants, healthy_restaurants
            
#         except Exception as e:
#             logger.error(f"Error getting restaurants: {e}")
#             return [], []
    
#     def _enrich_place_details(self, place: Dict[str, Any]) -> Dict[str, Any]:
#         """Enrich place data with additional fields and formatting"""
#         # Extract basic info
#         place_id = place.get('place_id', '')
#         name = place.get('name', 'Unknown Place')
#         rating = place.get('rating', 0)
#         vicinity = place.get('vicinity', 'Address not available')
#         types = place.get('types', [])
        
#         # Get geometry for distance calculation
#         geometry = place.get('geometry', {})
#         location = geometry.get('location', {})
#         lat = location.get('lat')
#         lng = location.get('lng')
        
#         # Get opening hours
#         opening_hours = place.get('opening_hours', {})
#         open_now = opening_hours.get('open_now')
        
#         # Get price level
#         price_level = place.get('price_level')
#         price_map = {
#             0: 'Free',
#             1: 'Inexpensive',
#             2: 'Moderate',
#             3: 'Expensive',
#             4: 'Very Expensive'
#         }
#         price_level_text = price_map.get(price_level, 'Unknown') if price_level is not None else 'Unknown'
        
#         # Get photos if available
#         photos = place.get('photos', [])
#         photo_url = None
#         if photos:
#             # Get first photo reference
#             photo_ref = photos[0].get('photo_reference')
#             if photo_ref:
#                 photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_ref}&key={settings.GOOGLE_API_KEY}"
        
#         # Create enriched place object
#         enriched = {
#             'place_id': place_id,
#             'name': name,
#             'rating': float(rating) if rating else 0.0,
#             'vicinity': vicinity,
#             'types': types,
#             'geometry': geometry,
#             'latitude': lat,
#             'longitude': lng,
#             'open_now': open_now,
#             'price_level': price_level,
#             'price_level_text': price_level_text,
#             'user_ratings_total': place.get('user_ratings_total', 0),
#             'photo_url': photo_url,
#             'plus_code': place.get('plus_code', {}),
#             'business_status': place.get('business_status', 'OPERATIONAL')
#         }
        
#         return enriched
    
#     def _is_unhealthy_restaurant(self, restaurant: Dict[str, Any]) -> bool:
#         """Determine if a restaurant is unhealthy"""
#         name = restaurant.get('name', '').lower()
#         types = [t.lower() for t in restaurant.get('types', [])]
        
#         # Unhealthy keywords
#         unhealthy_keywords = [
#             'mcdonald', 'kfc', 'burger king', 'pizza hut', 'domino',
#             'fast food', 'fried chicken', 'burger', 'pizza', 'donut',
#             'fried', 'crispy', 'cheese', 'cream', 'butter', 'sugar'
#         ]
        
#         # Unhealthy types
#         unhealthy_types = [
#             'fast_food', 'hamburger', 'pizza', 'fried_chicken',
#             'donut', 'ice_cream', 'dessert'
#         ]
        
#         # Check name
#         for keyword in unhealthy_keywords:
#             if keyword in name:
#                 return True
        
#         # Check types
#         for unhealthy_type in unhealthy_types:
#             if unhealthy_type in types:
#                 return True
        
#         return False
    
#     def _calculate_health_score(self, restaurant: Dict[str, Any]) -> int:
#         """Calculate health score from 1-10"""
#         name = restaurant.get('name', '').lower()
#         types = [t.lower() for t in restaurant.get('types', [])]
#         rating = restaurant.get('rating', 0)
        
#         score = 5  # Base score
        
#         # Healthy keywords
#         healthy_keywords = [
#             'salad', 'healthy', 'fresh', 'organic', 'juice', 'smoothie',
#             'cafe', 'coffee', 'grill', 'vegetarian', 'vegan', 'fit',
#             'fruit', 'yogurt', 'green', 'natural', 'lean', 'protein',
#             'whole food', 'plant based'
#         ]
        
#         # Healthy types
#         healthy_types = [
#             'cafe', 'health', 'vegetarian', 'vegan', 'salad', 'juice_bar',
#             'smoothie', 'health_food', 'organic'
#         ]
        
#         # Add points for healthy keywords
#         for keyword in healthy_keywords:
#             if keyword in name:
#                 score += 1
        
#         # Add points for healthy types
#         for healthy_type in healthy_types:
#             if healthy_type in types:
#                 score += 2
        
#         # Add points for high rating
#         if rating >= 4.5:
#             score += 2
#         elif rating >= 4.0:
#             score += 1
        
#         # Ensure score is between 1-10
#         return max(1, min(10, score))
    
#     def get_place_details(self, place_id: str) -> Optional[Dict[str, Any]]:
#         """Get detailed information about a place"""
#         try:
#             cache_key = f"details_{place_id}"
#             if cache_key in self.cache:
#                 return self.cache[cache_key]
            
#             result = self.client.place(place_id)
#             details = result.get('result', {})
            
#             # Cache for 10 minutes
#             self.cache[cache_key] = details
#             return details
            
#         except Exception as e:
#             logger.error(f"Error getting place details: {e}")
#             return None
    
#     def search_places_by_query(
#         self, 
#         query: str, 
#         location: Optional[Tuple[float, float]] = None,
#         radius: int = 5000
#     ) -> List[Dict[str, Any]]:
#         """Search places by text query"""
#         try:
#             params = {
#                 'query': query,
#                 'language': 'en'
#             }
            
#             if location:
#                 params['location'] = location
#                 params['radius'] = radius
            
#             result = self.client.places(**params)
#             places = result.get('results', [])
            
#             enriched_places = []
#             for place in places[:10]:  # Limit to 10
#                 enriched = self._enrich_place_details(place)
#                 enriched_places.append(enriched)
            
#             return enriched_places
            
#         except Exception as e:
#             logger.error(f"Error searching places: {e}")
#             return []
    
#     def calculate_distance(
#         self, 
#         origin: Tuple[float, float], 
#         destination: Tuple[float, float],
#         mode: str = 'walking'
#     ) -> Optional[Dict[str, Any]]:
#         """Calculate distance and duration between two points"""
#         try:
#             result = self.client.distance_matrix(
#                 origins=[origin],
#                 destinations=[destination],
#                 mode=mode
#             )
            
#             elements = result.get('rows', [{}])[0].get('elements', [{}])
#             if elements and elements[0].get('status') == 'OK':
#                 return elements[0]
            
#             return None
            
#         except Exception as e:
#             logger.error(f"Error calculating distance: {e}")
#             return None
    
#     def _get_sample_places(self, lat: float, lng: float, place_type: str = None) -> List[Dict[str, Any]]:
#         """Return sample places for testing when API fails"""
#         logger.warning("⚠️ Using sample data (API may be failing)")
        
#         # Sample unhealthy restaurants
#         unhealthy_samples = [
#             {
#                 'place_id': 'ChIJMcDonalds_Karachi',
#                 'name': "McDonald's Gulshan",
#                 'rating': 3.9,
#                 'vicinity': "Gulshan-e-Iqbal, Block 7, Karachi",
#                 'types': ['restaurant', 'fast_food', 'food', 'point_of_interest'],
#                 'geometry': {'location': {'lat': lat + 0.001, 'lng': lng + 0.001}},
#                 'price_level': 2,
#                 'user_ratings_total': 1250,
#                 'open_now': True
#             },
#             {
#                 'place_id': 'ChIJKFC_Karachi',
#                 'name': "KFC Tariq Road",
#                 'rating': 3.7,
#                 'vicinity': "Tariq Road, Karachi",
#                 'types': ['restaurant', 'fast_food', 'food', 'point_of_interest'],
#                 'geometry': {'location': {'lat': lat + 0.002, 'lng': lng - 0.001}},
#                 'price_level': 2,
#                 'user_ratings_total': 980,
#                 'open_now': True
#             }
#         ]
        
#         # Sample healthy places
#         healthy_samples = [
#             {
#                 'place_id': 'ChIJCafe_Espresso',
#                 'name': "Espresso Coffee Shop",
#                 'rating': 4.3,
#                 'vicinity': "Main University Road, Karachi",
#                 'types': ['cafe', 'food', 'point_of_interest'],
#                 'geometry': {'location': {'lat': lat - 0.001, 'lng': lng + 0.002}},
#                 'price_level': 1,
#                 'user_ratings_total': 850,
#                 'open_now': True
#             },
#             {
#                 'place_id': 'ChIJSalad_Bar',
#                 'name': "The Salad Bar",
#                 'rating': 4.5,
#                 'vicinity': "DHA Phase 6, Karachi",
#                 'types': ['restaurant', 'food', 'health', 'point_of_interest'],
#                 'geometry': {'location': {'lat': lat + 0.003, 'lng': lng + 0.001}},
#                 'price_level': 2,
#                 'user_ratings_total': 620,
#                 'open_now': True
#             },
#             {
#                 'place_id': 'ChIJFresh_Juice',
#                 'name': "Fresh Juice Corner",
#                 'rating': 4.2,
#                 'vicinity': "Bahadurabad, Karachi",
#                 'types': ['cafe', 'food', 'point_of_interest'],
#                 'geometry': {'location': {'lat': lat - 0.002, 'lng': lng - 0.002}},
#                 'price_level': 1,
#                 'user_ratings_total': 420,
#                 'open_now': True
#             }
#         ]
        
#         # Return based on requested type
#         if place_type == 'restaurant' or place_type == 'food':
#             samples = unhealthy_samples + healthy_samples
#         elif 'unhealthy' in str(place_type):
#             samples = unhealthy_samples
#         else:
#             samples = healthy_samples
        
#         # Enrich all samples
#         enriched_samples = []
#         for sample in samples:
#             enriched = self._enrich_place_details(sample)
#             enriched_samples.append(enriched)
        
#         return enriched_samples

# # Singleton instance
# google_service = GoogleMapsService()

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