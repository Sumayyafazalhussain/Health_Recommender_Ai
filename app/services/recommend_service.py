
# from typing import Dict, List, Optional
# from app.services.google_service import google_service
# from app.services.ai_service import ai_service
# from app.services.rule_engine import RuleEngine
# import logging

# logger = logging.getLogger(__name__)

# class RecommendationService:
#     def __init__(self):
#         """Initialize recommendation service with real APIs"""
#         self.rule_engine = RuleEngine()
#         logger.info("✅ RecommendationService initialized")
    
#     async def analyze_and_recommend(
#         self, 
#         lat: float, 
#         lng: float, 
#         radius: int = 500,
#         user_context: str = ""
#     ) -> Dict:
#         """
#         Main recommendation pipeline
        
#         1. Get nearby places from Google Maps API
#         2. Analyze each place using rule engine
#         3. Generate AI message using Gemini API
#         4. Return recommendations
        
#         Args:
#             lat: Latitude
#             lng: Longitude
#             radius: Search radius
#             user_context: Optional context
        
#         Returns:
#             Dictionary with recommendations
#         """
#         try:
#             logger.info(f"📍 Analyzing location: ({lat}, {lng}), radius: {radius}m")
            
#             # 1. Get places from Google Maps API
#             nearby_places = google_service.get_nearby_places(lat, lng, radius)
            
#             if not nearby_places:
#                 return {
#                     "status": "no_places",
#                     "message": "No nearby places found in this area",
#                     "recommendations": []
#                 }
            
#             logger.info(f"📊 Found {len(nearby_places)} places to analyze")
            
#             # 2. Analyze each place
#             for place in nearby_places:
#                 place_name = place.get('name', '')
#                 place_types = place.get('types', [])
                
#                 # Analyze using rule engine
#                 result = self.rule_engine.analyze_place(place_name, place_types)
                
#                 if result['triggered']:
#                     recommendations = result['recommendations']
                    
#                     # 3. Generate AI message
#                     ai_message = await ai_service.generate_recommendation_message(
#                         trigger_category=result['category_name'],
#                         recommendations=recommendations,
#                         user_context=user_context
#                     )
                    
#                     logger.info(f"🎯 Recommendation generated for: {place_name}")
                    
#                     return {
#                         "status": "recommendation_generated",
#                         "detected_place": {
#                             "name": place_name,
#                             "types": place_types,
#                             "category": result['category_name'],
#                             "category_id": result['category_id']
#                         },
#                         "recommendations": recommendations,
#                         "ai_message": ai_message,
#                         "nearby_raw": nearby_places[:10],
#                         "total_places_found": len(nearby_places)
#                     }
            
#             # 4. No triggers found
#             return {
#                 "status": "all_healthy",
#                 "message": "Great! No unhealthy places detected nearby.",
#                 "detected_places": [
#                     {"name": p.get('name'), "types": p.get('types')} 
#                     for p in nearby_places[:5]
#                 ],
#                 "total_places_found": len(nearby_places)
#             }
            
#         except Exception as e:
#             logger.error(f"❌ Recommendation error: {e}", exc_info=True)
#             return {
#                 "status": "error",
#                 "message": "Unable to generate recommendations",
#                 "error": str(e)
#             }

# # Singleton instance
# recommendation_service = RecommendationService()

# from typing import Dict, List, Optional
# from app.services.google_service import google_service
# from app.services.ai_service import ai_service
# from app.services.rule_engine import RuleEngine
# import logging
# import math

# logger = logging.getLogger(__name__)

# class RecommendationService:
#     def __init__(self):
#         """Initialize recommendation service with real APIs"""
#         self.rule_engine = RuleEngine()
#         logger.info("✅ RecommendationService initialized")
    
#     async def analyze_and_recommend(
#         self, 
#         lat: float, 
#         lng: float, 
#         radius: int = 500,
#         user_context: str = "",
#         include_specific_locations: bool = False  # ✅ FIXED PARAMETER NAME
#     ) -> Dict:
#         """
#         Main recommendation pipeline
#         """
#         try:
#             logger.info(f"📍 Analyzing location: ({lat}, {lng}), radius: {radius}m")
            
#             # 1. Get places from Google Maps API
#             nearby_places = google_service.get_nearby_places(lat, lng, radius)
            
#             if not nearby_places:
#                 return {
#                     "status": "no_places",
#                     "message": "No nearby places found in this area",
#                     "recommendations": []
#                 }
            
#             logger.info(f"📊 Found {len(nearby_places)} places to analyze")
            
#             # 2. Analyze each place
#             for place in nearby_places:
#                 place_name = place.get('name', '')
#                 place_types = place.get('types', [])
                
#                 # Analyze using rule engine
#                 result = self.rule_engine.analyze_place(place_name, place_types)
                
#                 if result['triggered']:
#                     recommendations = result['recommendations']
                    
#                     # 3. Generate AI message
#                     if include_specific_locations:  # ✅ FIXED
#                         # Find actual healthy places
#                         healthy_places = self._find_healthy_places_from_nearby(
#                             nearby_places, result['category_id']
#                         )
                        
#                         # Calculate distances
#                         healthy_with_details = self._add_location_details(
#                             lat, lng, healthy_places
#                         )
                        
#                         ai_message = await ai_service.generate_recommendation_with_specific_locations(
#                             trigger_place_name=place_name,
#                             trigger_category=result['category_name'],
#                             specific_alternatives=healthy_with_details[:3],
#                             user_context=user_context
#                         )
                        
#                         return {
#                             "status": "recommendation_generated",
#                             "detected_place": {
#                                 "name": place_name,
#                                 "types": place_types,
#                                 "category": result['category_name'],
#                                 "category_id": result['category_id']
#                             },
#                             "recommendations": recommendations,
#                             "healthy_alternatives": healthy_with_details[:5],
#                             "ai_message": ai_message,
#                             "total_places_found": len(nearby_places)
#                         }
#                     else:
#                         # OLD: General AI message
#                         ai_message = await ai_service.generate_recommendation_message(
#                             trigger_place_name=place_name,
#                             trigger_category=result['category_name'],
#                             recommendations=recommendations,
#                             user_context=user_context
#                         )
                        
#                         logger.info(f"🎯 Recommendation generated for: {place_name}")
                        
#                         return {
#                             "status": "recommendation_generated",
#                             "detected_place": {
#                                 "name": place_name,
#                                 "types": place_types,
#                                 "category": result['category_name'],
#                                 "category_id": result['category_id']
#                             },
#                             "recommendations": recommendations,
#                             "ai_message": ai_message,
#                             "total_places_found": len(nearby_places)
#                         }
            
#             # 4. No triggers found
#             return {
#                 "status": "all_healthy",
#                 "message": "Great! No unhealthy places detected nearby.",
#                 "detected_places": [
#                     {"name": p.get('name'), "types": p.get('types')} 
#                     for p in nearby_places[:5]
#                 ],
#                 "total_places_found": len(nearby_places)
#             }
            
#         except Exception as e:
#             logger.error(f"❌ Recommendation error: {e}", exc_info=True)
#             return {
#                 "status": "error",
#                 "message": "Unable to generate recommendations",
#                 "error": str(e)
#             }
    
#     def _find_healthy_places_from_nearby(
#         self, 
#         nearby_places: List[Dict], 
#         trigger_category_id: str
#     ) -> List[Dict]:
#         """
#         Find actual healthy places from nearby places
#         """
#         try:
#             # Get recommended categories
#             recommended_categories = self.rule_engine.get_recommended_category_names(trigger_category_id)
            
#             if not recommended_categories:
#                 return []
            
#             healthy_places = []
            
#             # Simple keyword matching
#             for place in nearby_places:
#                 place_name = place.get('name', '').lower()
                
#                 # Check if place matches any healthy category
#                 is_healthy = False
                
#                 # Check category names in place name
#                 for category in recommended_categories:
#                     if category.lower() in place_name:
#                         is_healthy = True
#                         break
                
#                 # Check for common healthy keywords
#                 healthy_keywords = ['cafe', 'coffee', 'juice', 'smoothie', 'salad', 'gym', 'fitness', 'yoga', 'park']
#                 for keyword in healthy_keywords:
#                     if keyword in place_name:
#                         is_healthy = True
#                         break
                
#                 if is_healthy:
#                     healthy_places.append(place)
            
#             return healthy_places
            
#         except Exception as e:
#             logger.error(f"Error finding healthy places: {e}")
#             return []
    
#     def _add_location_details(
#         self, 
#         user_lat: float, 
#         user_lng: float, 
#         places: List[Dict]
#     ) -> List[Dict]:
#         """
#         Add distance and other details to places
#         """
#         def calculate_distance(lat1, lon1, lat2, lon2):
#             """Calculate distance between two coordinates in meters"""
#             # Convert to radians
#             lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
            
#             # Haversine formula
#             dlat = lat2 - lat1
#             dlon = lon2 - lon1
#             a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
#             c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            
#             # Earth radius in meters
#             R = 6371000
#             return int(R * c)
        
#         places_with_details = []
        
#         for place in places:
#             place_lat = place.get('geometry', {}).get('location', {}).get('lat')
#             place_lng = place.get('geometry', {}).get('location', {}).get('lng')
            
#             details = {
#                 'name': place.get('name', 'Unknown'),
#                 'types': place.get('types', []),
#                 'rating': place.get('rating'),
#                 'vicinity': place.get('vicinity', ''),
#                 'open_now': place.get('opening_hours', {}).get('open_now'),
#                 'place_id': place.get('place_id')
#             }
            
#             # Calculate distance if coordinates available
#             if place_lat and place_lng:
#                 distance = calculate_distance(user_lat, user_lng, place_lat, place_lng)
#                 details['distance'] = distance
                
#                 # Add human-readable distance
#                 if distance < 1000:
#                     details['distance_text'] = f"{distance}m away"
#                 else:
#                     details['distance_text'] = f"{distance/1000:.1f}km away"
            
#             places_with_details.append(details)
        
#         # Sort by distance (nearest first)
#         return sorted(
#             places_with_details, 
#             key=lambda x: x.get('distance', 99999)
#         )

# # Singleton instance
# recommendation_service = RecommendationService()\from typing import Dict, List, Optional, Any, Tuplefrom typing import Dict, List, Optional, Any


# from typing import Any, Dict, List, Optional
# from app.services.google_service import google_service
# from app.services.ai_service import ai_service
# from app.services.rule_engine import RuleEngine
# import logging
# import math

# logger = logging.getLogger(__name__)

# class RecommendationService:
#     def __init__(self):
#         """Initialize recommendation service"""
#         self.rule_engine = RuleEngine()
#         logger.info("✅ RecommendationService initialized")
    
#     async def analyze_and_recommend(
#         self, 
#         lat: float, 
#         lng: float, 
#         radius: int = 500,
#         user_context: str = "",
#         include_specific_locations: bool = False,
#         include_menu: bool = False
#     ) -> Dict[str, Any]:
#         """
#         Main recommendation pipeline
#         """
#         try:
#             logger.info(f"📍 Searching restaurants/cafes/gyms near: ({lat}, {lng})")
            
#             # 1. Search ONLY for restaurants, cafes, gyms
#             target_place_types = ['restaurant', 'cafe', 'gym', 'food', 'bar']
            
#             nearby_places = google_service.get_nearby_places_by_types(
#                 lat=lat,
#                 lng=lng,
#                 radius=radius,
#                 place_types=target_place_types
#             )
            
#             if not nearby_places:
#                 return {
#                     "status": "no_food_places",
#                     "message": "No restaurants, cafes, or gyms found in this area",
#                     "total_places_found": 0
#                 }
            
#             logger.info(f"🍽️ Found {len(nearby_places)} restaurants/cafes/gyms")
            
#             # 2. Analyze places (only restaurants/cafes/gyms)
#             unhealthy_places = []
#             all_analyzed_places = []
            
#             for place in nearby_places:
#                 place_name = place.get('name', '')
#                 place_types = place.get('types', [])
                
#                 result = self.rule_engine.analyze_place(place_name, place_types)
                
#                 if result['triggered']:
#                     place['analysis'] = result
#                     all_analyzed_places.append(place)
                    
#                     if result.get('is_unhealthy', False):
#                         unhealthy_places.append(place)
            
#             # 3. Select target
#             if unhealthy_places:
#                 target_place = unhealthy_places[0]
#                 target_result = target_place['analysis']
#                 logger.info(f"🚨 Unhealthy place: {target_place.get('name')}")
#             elif all_analyzed_places:
#                 target_place = all_analyzed_places[0]
#                 target_result = target_place['analysis']
#                 logger.info(f"📍 Place: {target_place.get('name')}")
#             else:
#                 # No restaurants/cafes/gyms detected
#                 return {
#                     "status": "all_healthy",
#                     "message": "No unhealthy restaurants, cafes, or gyms detected nearby.",
#                     "nearby_food_places": [
#                         {
#                             "name": p.get('name'),
#                             "types": p.get('types', [])[:2],
#                             "rating": p.get('rating', 'N/A')
#                         } for p in nearby_places[:3]
#                     ],
#                     "total_places_found": len(nearby_places)
#                 }
            
#             # 4. Get healthy alternatives (ONLY restaurants, cafes, gyms)
#             healthy_alternatives = []
#             if include_specific_locations:
#                 healthy_alternatives = await self._get_healthy_alternatives(lat, lng, radius)
            
#             # 5. Generate AI message
#             ai_message = await self._generate_ai_message(
#                 target_place,
#                 target_result,
#                 healthy_alternatives,
#                 user_context,
#                 include_specific_locations
#             )
            
#             # 6. Build response
#             response = {
#                 "status": "recommendation_generated",
#                 "detected_place": {
#                     "name": target_place.get('name'),
#                     "rating": target_place.get('rating', 'N/A'),
#                     "vicinity": target_place.get('vicinity', 'Address not available'),
#                     "types": target_place.get('types', []),
#                     "category": target_result['category_name'],
#                     "category_id": target_result['category_id'],
#                     "is_unhealthy": target_result.get('is_unhealthy', False),
#                     "price_level": target_place.get('price_level_text', 'Unknown'),
#                     "place_id": target_place.get('place_id', '')
#                 },
#                 "recommendations": target_result['recommendations'],
#                 "total_places_found": len(nearby_places)
#             }
            
#             # Add healthy alternatives if requested
#             if healthy_alternatives and include_specific_locations:
#                 response["healthy_alternatives"] = healthy_alternatives
            
#             # Add AI message
#             response["ai_message"] = ai_message
            
#             logger.info(f"🎯 Recommendation for: {target_place.get('name')}")
#             return response
            
#         except Exception as e:
#             logger.error(f"❌ Error: {e}", exc_info=True)
#             return {
#                 "status": "error",
#                 "message": "Unable to generate recommendations",
#                 "error": str(e)
#             }
    
#     async def _get_healthy_alternatives(
#         self,
#         lat: float,
#         lng: float,
#         radius: int
#     ) -> List[Dict[str, Any]]:
#         """Get healthy alternatives - ONLY cafes, gyms, healthy restaurants"""
#         try:
#             # Get healthy places from Google service
#             healthy_places = google_service.get_healthy_alternatives_nearby(lat, lng, radius)
            
#             if not healthy_places:
#                 return []
            
#             # Format alternatives
#             alternatives = []
#             for place in healthy_places[:5]:  # Top 5
#                 # Calculate distance
#                 distance = self._calculate_distance(
#                     lat, lng,
#                     place.get('geometry', {}).get('location', {}).get('lat'),
#                     place.get('geometry', {}).get('location', {}).get('lng')
#                 )
                
#                 # Determine category
#                 name = place.get('name', '').lower()
#                 if 'cafe' in name or 'coffee' in name:
#                     category = 'Cafe'
#                 elif 'gym' in name or 'fitness' in name:
#                     category = 'Gym'
#                 elif 'restaurant' in name or 'food' in name:
#                     category = 'Restaurant'
#                 else:
#                     category = 'Healthy Place'
                
#                 alternative = {
#                     'name': place.get('name'),
#                     'category': category,
#                     'rating': place.get('rating', 'N/A'),
#                     'vicinity': place.get('vicinity', 'Address not available'),
#                     'distance': distance,
#                     'distance_text': f"{distance}m" if distance < 1000 else f"{distance/1000:.1f}km",
#                     'price_level': place.get('price_level_text', 'Unknown'),
#                     'types': place.get('types', [])[:2]
#                 }
#                 alternatives.append(alternative)
            
#             # Sort by distance
#             alternatives.sort(key=lambda x: x.get('distance', 99999))
            
#             return alternatives[:3]  # Return top 3
            
#         except Exception as e:
#             logger.error(f"Error getting alternatives: {e}")
#             return []
    
#     async def _generate_ai_message(
#         self,
#         target_place: Dict,
#         target_result: Dict,
#         healthy_alternatives: List[Dict],
#         user_context: str,
#         include_specific: bool
#     ) -> str:
#         """Generate AI message"""
#         try:
#             if include_specific and healthy_alternatives:
#                 # Message with specific restaurant/cafe/gym suggestions
#                 return await ai_service.generate_recommendation_with_specific_locations(
#                     trigger_place_name=target_place.get('name'),
#                     trigger_category=target_result['category_name'],
#                     specific_alternatives=healthy_alternatives[:2],
#                     user_context=user_context
#                 )
#             else:
#                 # General message
#                 return await ai_service.generate_recommendation_message(
#                     trigger_place_name=target_place.get('name'),
#                     trigger_category=target_result['category_name'],
#                     recommendations=target_result['recommendations'],
#                     user_context=user_context
#                 )
#         except Exception as e:
#             logger.error(f"AI message error: {e}")
#             # Simple fallback
#             place_name = target_place.get('name', 'this place')
#             if healthy_alternatives:
#                 alt = healthy_alternatives[0]
#                 return f"Instead of {place_name}, try {alt['name']} ({alt['distance_text']} away). It's a {alt['category']} with {alt['rating']}★ rating!"
#             return f"Consider healthier restaurant, cafe, or gym options instead of {place_name}!"
    
#     def _calculate_distance(
#         self,
#         lat1: float,
#         lng1: float,
#         lat2: Optional[float],
#         lng2: Optional[float]
#     ) -> int:
#         """Calculate distance in meters"""
#         if not lat2 or not lng2:
#             return 99999
        
#         try:
#             lat1, lng1, lat2, lng2 = map(math.radians, [lat1, lng1, lat2, lng2])
#             dlat = lat2 - lat1
#             dlng = lng2 - lng1
#             a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng/2)**2
#             c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
#             R = 6371000
#             return int(R * c)
#         except:
#             return 99999

# # Singleton instance
# recommendation_service = RecommendationService()








# from typing import Any, Dict, List, Optional
# from app.services.google_service import google_service
# from app.services.ai_service import ai_service
# from app.services.rule_engine import RuleEngine
# import logging
# import math

# logger = logging.getLogger(__name__)

# class RecommendationService:
#     def __init__(self):
#         """Initialize recommendation service"""
#         self.rule_engine = RuleEngine()
#         logger.info("✅ RecommendationService initialized")
    
#     async def analyze_and_recommend(
#         self, 
#         lat: float, 
#         lng: float, 
#         radius: int = 500,
#         user_context: str = "",
#         include_specific_locations: bool = False,
#         include_menu: bool = False
#     ) -> Dict[str, Any]:
#         """
#         Main recommendation pipeline
#         """
#         try:
#             logger.info(f"📍 Searching restaurants/cafes/gyms near: ({lat}, {lng})")
            
#             # 1. Search ONLY for restaurants, cafes, gyms
#             target_place_types = ['restaurant', 'cafe', 'gym', 'food', 'bar']
            
#             nearby_places = google_service.get_nearby_places_by_types(
#                 lat=lat,
#                 lng=lng,
#                 radius=radius,
#                 place_types=target_place_types
#             )
            
#             if not nearby_places:
#                 return {
#                     "status": "no_food_places",
#                     "message": "No restaurants, cafes, or gyms found in this area",
#                     "total_places_found": 0
#                 }
            
#             logger.info(f"🍽️ Found {len(nearby_places)} restaurants/cafes/gyms")
            
#             # 2. Analyze places (only restaurants/cafes/gyms)
#             unhealthy_places = []
#             all_analyzed_places = []
            
#             for place in nearby_places:
#                 place_name = place.get('name', '')
#                 place_types = place.get('types', [])
                
#                 result = self.rule_engine.analyze_place(place_name, place_types)
                
#                 if result['triggered']:
#                     place['analysis'] = result
#                     all_analyzed_places.append(place)
                    
#                     if result.get('is_unhealthy', False):
#                         unhealthy_places.append(place)
            
#             # 3. Select target
#             if unhealthy_places:
#                 target_place = unhealthy_places[0]
#                 target_result = target_place['analysis']
#                 logger.info(f"🚨 Unhealthy place: {target_place.get('name')}")
#             elif all_analyzed_places:
#                 target_place = all_analyzed_places[0]
#                 target_result = target_place['analysis']
#                 logger.info(f"📍 Place: {target_place.get('name')}")
#             else:
#                 # No restaurants/cafes/gyms detected
#                 return {
#                     "status": "all_healthy",
#                     "message": "No unhealthy restaurants, cafes, or gyms detected nearby.",
#                     "nearby_food_places": [
#                         {
#                             "name": p.get('name'),
#                             "types": p.get('types', [])[:2],
#                             "rating": p.get('rating', 'N/A')
#                         } for p in nearby_places[:3]
#                     ],
#                     "total_places_found": len(nearby_places)
#                 }
            
#             # 4. Get healthy alternatives (ONLY restaurants, cafes, gyms)
#             healthy_alternatives = []
#             if include_specific_locations:
#                 healthy_alternatives = await self._get_healthy_alternatives(lat, lng, radius)
            
#             # 5. Generate AI message
#             ai_message = await self._generate_ai_message(
#                 target_place,
#                 target_result,
#                 healthy_alternatives,
#                 user_context,
#                 include_specific_locations
#             )
            
#             # 6. Build response
#             response = {
#                 "status": "recommendation_generated",
#                 "detected_place": {
#                     "name": target_place.get('name'),
#                     "rating": target_place.get('rating', 'N/A'),
#                     "vicinity": target_place.get('vicinity', 'Address not available'),
#                     "types": target_place.get('types', []),
#                     "category": target_result['category_name'],
#                     "category_id": target_result['category_id'],
#                     "is_unhealthy": target_result.get('is_unhealthy', False),
#                     "price_level": target_place.get('price_level_text', 'Unknown'),
#                     "place_id": target_place.get('place_id', '')
#                 },
#                 "recommendations": target_result['recommendations'],
#                 "total_places_found": len(nearby_places)
#             }
            
#             # Add healthy alternatives if requested
#             if healthy_alternatives and include_specific_locations:
#                 response["healthy_alternatives"] = healthy_alternatives
            
#             # Add AI message
#             response["ai_message"] = ai_message
            
#             logger.info(f"🎯 Recommendation for: {target_place.get('name')}")
#             return response
            
#         except Exception as e:
#             logger.error(f"❌ Error: {e}", exc_info=True)
#             return {
#                 "status": "error",
#                 "message": "Unable to generate recommendations",
#                 "error": str(e)
#             }
    
#     async def _get_healthy_alternatives(
#         self,
#         lat: float,
#         lng: float,
#         radius: int
#     ) -> List[Dict[str, Any]]:
#         """Get healthy alternatives - ONLY cafes, gyms, healthy restaurants"""
#         try:
#             # Get healthy places from Google service
#             healthy_places = google_service.get_healthy_alternatives_nearby(lat, lng, radius)
            
#             if not healthy_places:
#                 return []
            
#             # Format alternatives
#             alternatives = []
#             for place in healthy_places[:5]:  # Top 5
#                 # Calculate distance
#                 distance = self._calculate_distance(
#                     lat, lng,
#                     place.get('geometry', {}).get('location', {}).get('lat'),
#                     place.get('geometry', {}).get('location', {}).get('lng')
#                 )
                
#                 # Determine category
#                 name = place.get('name', '').lower()
#                 types = [t.lower() for t in place.get('types', [])]

#                 if 'gym' in name or 'fitness' in name or 'muscle' in name or 'gym' in types:
#                     category = 'Gym'
#                 elif 'cafe' in name or 'coffee' in name or 'tea' in name or 'juice' in name or 'cafe' in types:
#                     category = 'Cafe'
#                 elif 'restaurant' in name or 'food' in name or 'restaurant' in types:
#                     category = 'Restaurant'
#                 elif 'healthy' in name or 'salad' in name or 'organic' in name:
#                     category = 'Healthy Restaurant'
#                 else:
#                     category = 'Healthy Place'
                
#                 alternative = {
#                     'name': place.get('name'),
#                     'category': category,
#                     'rating': place.get('rating', 'N/A'),
#                     'vicinity': place.get('vicinity', 'Address not available'),
#                     'distance': distance,
#                     'distance_text': f"{distance}m" if distance < 1000 else f"{distance/1000:.1f}km",
#                     'price_level': place.get('price_level_text', 'Unknown'),
#                     'types': place.get('types', [])[:2]
#                 }
#                 alternatives.append(alternative)
            
#             # Sort by distance
#             alternatives.sort(key=lambda x: x.get('distance', 99999))
            
#             return alternatives[:3]  # Return top 3
            
#         except Exception as e:
#             logger.error(f"Error getting alternatives: {e}")
#             return []
    
#     async def _generate_ai_message(
#         self,
#         target_place: Dict,
#         target_result: Dict,
#         healthy_alternatives: List[Dict],
#         user_context: str,
#         include_specific: bool
#     ) -> str:
#         """Generate AI message"""
#         try:
#             if include_specific and healthy_alternatives:
#                 # Message with specific restaurant/cafe/gym suggestions
#                 return await ai_service.generate_recommendation_with_specific_locations(
#                     trigger_place_name=target_place.get('name'),
#                     trigger_category=target_result['category_name'],
#                     specific_alternatives=healthy_alternatives[:2],
#                     user_context=user_context
#                 )
#             else:
#                 # General message
#                 return await ai_service.generate_recommendation_message(
#                     trigger_place_name=target_place.get('name'),
#                     trigger_category=target_result['category_name'],
#                     recommendations=target_result['recommendations'],
#                     user_context=user_context
#                 )
#         except Exception as e:
#             logger.error(f"AI message error: {e}")
#             # Simple fallback
#             place_name = target_place.get('name', 'this place')
#             if healthy_alternatives:
#                 alt = healthy_alternatives[0]
#                 return f"Instead of {place_name}, try {alt['name']} ({alt['distance_text']} away). It's a {alt['category']} with {alt['rating']}★ rating!"
#             return f"Consider healthier restaurant, cafe, or gym options instead of {place_name}!"
    
#     def _calculate_distance(
#         self,
#         lat1: float,
#         lng1: float,
#         lat2: Optional[float],
#         lng2: Optional[float]
#     ) -> int:
#         """Calculate distance in meters"""
#         if not lat2 or not lng2:
#             return 99999
        
#         try:
#             lat1, lng1, lat2, lng2 = map(math.radians, [lat1, lng1, lat2, lng2])
#             dlat = lat2 - lat1
#             dlng = lng2 - lng1
#             a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng/2)**2
#             c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
#             R = 6371000
#             return int(R * c)
#         except:
#             return 99999

# # Singleton instance
# recommendation_service = RecommendationService()




from typing import Any, Dict, List, Optional
from app.services.google_service import google_service
from app.services.ai_service import ai_service
from app.services.rule_engine import RuleEngine
import logging
import math

logger = logging.getLogger(__name__)

class RecommendationService:
    def __init__(self):
        """Initialize recommendation service"""
        self.rule_engine = RuleEngine()
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
                
                result = self.rule_engine.analyze_place(place_name, place_types)
                
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
                user_context
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
        user_context: str
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
                    # Get nearby places for this specific location
                    from app.services.google_service import google_service
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

# Singleton instance
recommendation_service = RecommendationService()