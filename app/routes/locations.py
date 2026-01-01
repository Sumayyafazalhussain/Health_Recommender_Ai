
# app/routes/locations.py
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Dict, Any
import logging
import math

logger = logging.getLogger(__name__)

# Create router FIRST
router = APIRouter(prefix="/api/locations", tags=["locations"])

def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> int:
    """Calculate distance between two coordinates in meters"""
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

@router.get("/search")
async def search_nearby_locations(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    radius: int = Query(1500, description="Search radius in meters"),
    search_type: str = Query("all", description="Type to search: all, restaurants, cafes, gyms, bars")
):
    """
    Search for specific nearby locations
    """
    try:
        # Import inside function to avoid circular imports
        from app.services.google_service import google_service
        
        # Map search type to Google place types
        type_mapping = {
            "all": ["restaurant", "cafe", "gym", "bar", "park", "food"],
            "restaurants": ["restaurant", "food", "meal_takeaway"],
            "cafes": ["cafe", "coffee"],
            "gyms": ["gym", "fitness", "health"],
            "bars": ["bar", "night_club", "pub"],
            "healthy": ["cafe", "health", "park", "gym"]
        }
        
        place_types = type_mapping.get(search_type.lower(), ["restaurant", "cafe"])
        
        # Get places
        places = google_service.get_nearby_places_by_types(
            lat=lat,
            lng=lng,
            radius=radius,
            place_types=place_types
        )
        
        # Add distance to each place
        for place in places:
            place_lat = place.get('geometry', {}).get('location', {}).get('lat')
            place_lng = place.get('geometry', {}).get('location', {}).get('lng')
            
            if place_lat and place_lng:
                distance = calculate_distance(lat, lng, place_lat, place_lng)
                place['distance'] = distance
                place['distance_text'] = f"{distance}m" if distance < 1000 else f"{distance/1000:.1f}km"
        
        # Sort by distance
        places.sort(key=lambda x: x.get('distance', 99999))
        
        return {
            "status": "success",
            "location": {"lat": lat, "lng": lng, "radius": radius},
            "search_type": search_type,
            "count": len(places),
            "places": places[:20],  # Limit to 20
            "top_recommendations": places[:5]  # Top 5 closest
        }
        
    except Exception as e:
        logger.error(f"Location search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/healthy-alternatives")
async def get_healthy_alternatives(
    lat: float = Query(...),
    lng: float = Query(...),
    radius: int = 1500
):
    """
    Get healthy alternatives near a location
    """
    try:
        # Import inside function to avoid circular imports
        from app.services.google_service import google_service
        from app.services.ai_service import ai_service
        
        # Search for healthy places
        healthy_results = google_service.search_healthy_places_nearby(lat, lng, radius)
        
        # Generate AI message
        ai_message = await ai_service.generate_recommendation_message(
            trigger_place_name="your current location",
            trigger_category="any place",
            recommendations=["Cafes", "Gyms", "Parks", "Healthy Restaurants"],
            user_context="Looking for healthy options"
        )
        
        return {
            "status": "success",
            "location": {"lat": lat, "lng": lng},
            "healthy_options": healthy_results,
            "ai_message": ai_message,
            "summary": {
                "total_cafes": len(healthy_results.get("healthy_cafes", [])),
                "total_gyms": len(healthy_results.get("gyms", [])),
                "total_parks": len(healthy_results.get("parks", [])),
                "total_healthy_restaurants": len(healthy_results.get("healthy_restaurants", []))
            }
        }
        
    except Exception as e:
        logger.error(f"Healthy alternatives error: {e}")
        raise HTTPException(status_code=500, detail=str(e))














