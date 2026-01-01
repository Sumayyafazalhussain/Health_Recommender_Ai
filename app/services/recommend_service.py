
# app/services/recommend_service.py
from typing import Any, Dict, List, Optional
import logging
import math

logger = logging.getLogger(__name__)

class RecommendationService:
    def __init__(self):
        """Initialize recommendation service"""
        logger.info("✅ RecommendationService initialized")
    
    async def analyze_and_recommend(
        self, 
        lat: float, 
        lng: float, 
        radius: int = 500,
        user_context: str = "",
        include_specific_locations: bool = False,
        include_menu: bool = False
    ) -> Dict[str, Any]:
        """
        Main recommendation pipeline
        """
        try:
            # Import here to avoid circular imports
            from app.services.google_service import google_service
            from app.services.rule_engine import rule_engine
            from app.services.ai_service import ai_service
            
            logger.info(f"📍 Searching restaurants/cafes/gyms near: ({lat}, {lng}), radius: {radius}m")
            
            # 1. Search ONLY for restaurants, cafes, gyms
            target_place_types = ['restaurant', 'cafe', 'gym', 'food', 'bar', 'meal_takeaway']
            
            nearby_places = google_service.get_nearby_places_by_types(
                lat=lat,
                lng=lng,
                radius=radius,
                place_types=target_place_types
            )
            
            if not nearby_places:
                return {
                    "status": "no_food_places",
                    "message": "No restaurants, cafes, or gyms found in this area",
                    "total_places_found": 0
                }
            
            logger.info(f"🍽️ Found {len(nearby_places)} restaurants/cafes/gyms")
            
            # 2. Analyze places (only restaurants/cafes/gyms)
            unhealthy_places = []
            all_analyzed_places = []
            
            for place in nearby_places:
                place_name = place.get('name', '')
                place_types = place.get('types', [])
                
                result = rule_engine.analyze_place(place_name, place_types)
                
                if result['triggered']:
                    place['analysis'] = result
                    all_analyzed_places.append(place)
                    
                    if result.get('is_unhealthy', False):
                        unhealthy_places.append(place)
            
            logger.info(f"🚨 Unhealthy places: {len(unhealthy_places)}, 🥗 All analyzed: {len(all_analyzed_places)}")
            
            # 3. Select target
            target_place = None
            target_result = None
            
            if unhealthy_places:
                # Use first unhealthy place
                target_place = unhealthy_places[0]
                target_result = target_place['analysis']
                logger.info(f"🚨 Targeting unhealthy: {target_place.get('name')}")
            elif all_analyzed_places:
                # Use first analyzed place
                target_place = all_analyzed_places[0]
                target_result = target_place['analysis']
                logger.info(f"📍 Targeting: {target_place.get('name')}")
            else:
                # No restaurants/cafes/gyms detected
                return {
                    "status": "all_healthy",
                    "message": "No unhealthy restaurants, cafes, or gyms detected nearby.",
                    "nearby_food_places": [
                        {
                            "name": p.get('name'),
                            "types": p.get('types', [])[:2],
                            "rating": p.get('rating', 'N/A')
                        } for p in nearby_places[:3]
                    ],
                    "total_places_found": len(nearby_places)
                }
            
            # 4. Get healthy alternatives (ONLY restaurants, cafes, gyms)
            healthy_alternatives = []
            if include_specific_locations:
                healthy_alternatives = await self._get_healthy_alternatives(lat, lng, radius)
            else:
                # Even if include_specific_locations is false, try to get SOME alternatives
                healthy_alternatives = await self._get_minimal_alternatives(lat, lng, radius)
            
            # 5. Generate AI message - ALWAYS try to include specific places
            ai_message = await self._generate_ai_message(
                target_place,
                target_result,
                healthy_alternatives,
                user_context,
                ai_service
            )
            
            # 6. Build response
            response = {
                "status": "recommendation_generated",
                "detected_place": {
                    "name": target_place.get('name'),
                    "rating": target_place.get('rating', 'N/A'),
                    "vicinity": target_place.get('vicinity', 'Address not available'),
                    "types": target_place.get('types', []),
                    "category": target_result['category_name'],
                    "category_id": target_result['category_id'],
                    "is_unhealthy": target_result.get('is_unhealthy', False),
                    "price_level": target_place.get('price_level_text', 'Unknown'),
                    "place_id": target_place.get('place_id', '')
                },
                "recommendations": target_result['recommendations'],
                "total_places_found": len(nearby_places)
            }
            
            # Add healthy alternatives if we have them
            if healthy_alternatives:
                response["healthy_alternatives"] = healthy_alternatives
            
            # Add AI message
            response["ai_message"] = ai_message
            
            logger.info(f"🎯 Recommendation generated for: {target_place.get('name')}")
            return response
            
        except Exception as e:
            logger.error(f"❌ Error: {e}", exc_info=True)
            return {
                "status": "error",
                "message": "Unable to generate recommendations",
                "error": str(e)
            }
    
    async def _get_healthy_alternatives(
        self,
        lat: float,
        lng: float,
        radius: int
    ) -> List[Dict[str, Any]]:
        """Get healthy alternatives - ONLY cafes, gyms, healthy restaurants"""
        try:
            from app.services.google_service import google_service
            
            # Get healthy places from Google service
            healthy_places = google_service.get_healthy_alternatives_nearby(lat, lng, radius)
            
            if not healthy_places:
                return await self._get_minimal_alternatives(lat, lng, radius)
            
            # Format alternatives
            alternatives = []
            for place in healthy_places[:5]:  # Top 5
                # Calculate distance
                distance = self._calculate_distance(
                    lat, lng,
                    place.get('geometry', {}).get('location', {}).get('lat'),
                    place.get('geometry', {}).get('location', {}).get('lng')
                )
                
                # Skip if too far
                if distance > radius * 1.5:  # Allow 50% extra
                    continue
                
                # Determine category
                name = place.get('name', '').lower()
                types = [t.lower() for t in place.get('types', [])]
                
                if 'gym' in name or 'fitness' in name or 'muscle' in name or 'gym' in types:
                    category = 'Gym'
                elif 'cafe' in name or 'coffee' in name or 'tea' in name or 'juice' in name or 'cafe' in types:
                    category = 'Cafe'
                elif 'restaurant' in name or 'food' in name or 'restaurant' in types:
                    category = 'Restaurant'
                elif 'healthy' in name or 'salad' in name or 'organic' in name:
                    category = 'Healthy Restaurant'
                else:
                    category = 'Healthy Place'
                
                alternative = {
                    'name': place.get('name'),
                    'category': category,
                    'rating': place.get('rating', 'N/A'),
                    'vicinity': place.get('vicinity', 'Address not available'),
                    'distance': distance,
                    'distance_text': f"{distance}m" if distance < 1000 else f"{distance/1000:.1f}km",
                    'price_level': place.get('price_level_text', 'Unknown'),
                    'types': place.get('types', [])[:2]
                }
                alternatives.append(alternative)
            
            # Sort by distance
            alternatives.sort(key=lambda x: x.get('distance', 99999))
            
            return alternatives[:3]  # Return top 3
            
        except Exception as e:
            logger.error(f"Error getting alternatives: {e}")
            return []
    
    async def _get_minimal_alternatives(
        self,
        lat: float,
        lng: float,
        radius: int
    ) -> List[Dict[str, Any]]:
        """Get at least some alternatives for AI message"""
        try:
            from app.services.google_service import google_service
            
            # Search for any nearby places
            places = google_service.get_nearby_places_by_types(
                lat=lat,
                lng=lng,
                radius=radius,
                place_types=['cafe', 'gym', 'food']
            )
            
            if len(places) < 2:
                return []
            
            alternatives = []
            for i, place in enumerate(places[:3]):  # Get top 3
                if i >= 2:  # Only need 2 for message
                    break
                    
                # Calculate distance
                distance = self._calculate_distance(
                    lat, lng,
                    place.get('geometry', {}).get('location', {}).get('lat'),
                    place.get('geometry', {}).get('location', {}).get('lng')
                )
                
                # Determine category
                name = place.get('name', '').lower()
                if 'gym' in name or 'fitness' in name:
                    category = 'Gym'
                elif 'cafe' in name or 'coffee' in name or 'tea' in name:
                    category = 'Cafe'
                else:
                    category = 'Restaurant'
                
                alternative = {
                    'name': place.get('name'),
                    'category': category,
                    'rating': place.get('rating', 'N/A'),
                    'vicinity': place.get('vicinity', 'Address not available'),
                    'distance': distance,
                    'distance_text': f"{distance}m" if distance < 1000 else f"{distance/1000:.1f}km",
                    'price_level': place.get('price_level_text', 'Unknown')
                }
                alternatives.append(alternative)
            
            return alternatives
            
        except Exception as e:
            logger.error(f"Error getting minimal alternatives: {e}")
            return []
    
    async def _generate_ai_message(
        self,
        target_place: Dict,
        target_result: Dict,
        healthy_alternatives: List[Dict],
        user_context: str,
        ai_service
    ) -> str:
        """Generate AI message - ALWAYS try to include specific places"""
        try:
            # If we have healthy alternatives, use specific locations
            if healthy_alternatives and len(healthy_alternatives) >= 2:
                return await ai_service.generate_recommendation_with_specific_locations(
                    trigger_place_name=target_place.get('name'),
                    trigger_category=target_result['category_name'],
                    specific_alternatives=healthy_alternatives[:2],  # Use top 2
                    user_context=user_context
                )
            else:
                # Try to get at least 2 alternatives
                lat = target_place.get('geometry', {}).get('location', {}).get('lat')
                lng = target_place.get('geometry', {}).get('location', {}).get('lng')
                
                if lat and lng:
                    from app.services.google_service import google_service
                    # Get nearby places for this specific location
                    nearby = google_service.get_nearby_places_by_types(
                        lat=lat,
                        lng=lng,
                        radius=500,
                        place_types=['cafe', 'gym', 'food']
                    )
                    
                    if nearby and len(nearby) >= 2:
                        # Format alternatives
                        formatted_alts = []
                        for i, place in enumerate(nearby[:2]):
                            if place.get('name') == target_place.get('name'):
                                continue  # Skip the target place
                                
                            distance = self._calculate_distance(
                                lat, lng,
                                place.get('geometry', {}).get('location', {}).get('lat'),
                                place.get('geometry', {}).get('location', {}).get('lng')
                            )
                            
                            alt = {
                                'name': place.get('name'),
                                'distance': distance,
                                'distance_text': f"{distance}m" if distance < 1000 else f"{distance/1000:.1f}km",
                                'rating': place.get('rating', 'N/A')
                            }
                            formatted_alts.append(alt)
                        
                        if len(formatted_alts) >= 2:
                            return await ai_service.generate_recommendation_with_specific_locations(
                                trigger_place_name=target_place.get('name'),
                                trigger_category=target_result['category_name'],
                                specific_alternatives=formatted_alts[:2],
                                user_context=user_context
                            )
            
            # Fallback to generic message
            return await ai_service.generate_recommendation_message(
                trigger_place_name=target_place.get('name'),
                trigger_category=target_result['category_name'],
                recommendations=target_result['recommendations'],
                user_context=user_context
            )
            
        except Exception as e:
            logger.error(f"AI message error: {e}")
            # Simple fallback
            place_name = target_place.get('name', 'this place')
            if healthy_alternatives:
                alt = healthy_alternatives[0]
                return f"Instead of {place_name}, try {alt['name']} ({alt['distance_text']} away). It's a {alt.get('category', 'healthy place')} with {alt['rating']}★ rating!"
            return f"Consider healthier restaurant, cafe, or gym options instead of {place_name}!"
    
    def _calculate_distance(
        self,
        lat1: float,
        lng1: float,
        lat2: Optional[float],
        lng2: Optional[float]
    ) -> int:
        """Calculate distance in meters"""
        if not lat2 or not lng2:
            return 99999
        
        try:
            lat1, lng1, lat2, lng2 = map(math.radians, [lat1, lng1, lat2, lng2])
            dlat = lat2 - lat1
            dlng = lng2 - lng1
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng/2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            R = 6371000
            return int(R * c)
        except:
            return 99999

# Create singleton instance
recommendation_service = RecommendationService()