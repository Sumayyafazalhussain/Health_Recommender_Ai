
from fastapi import APIRouter, HTTPException, Query  # ADDED APIRouter here
from pydantic import BaseModel
from typing import Optional
from app.services.recommend_service import recommendation_service

# Create router instance
router = APIRouter(prefix="/api", tags=["recommendations"])

class LocationRequest(BaseModel):
    lat: float
    lng: float
    radius: Optional[int] = 500
    context: Optional[str] = None
    include_locations: Optional[bool] = False
    include_menu: Optional[bool] = False

@router.get("/recommend", response_model=dict)
async def get_recommendations(
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lng: float = Query(..., ge=-180, le=180, description="Longitude"),
    radius: int = Query(500, ge=100, le=5000, description="Search radius in meters"),
    context: Optional[str] = Query(None, description="User context (morning, evening, workout)"),
    include_locations: bool = Query(False, description="Include specific location suggestions"),
    include_menu: bool = Query(False, description="Include menu information")
):
    """
    Get AI-powered healthy recommendations based on location
    """
    if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
        raise HTTPException(
            status_code=400,
            detail="Invalid coordinates"
        )
    
    result = await recommendation_service.analyze_and_recommend(
        lat=lat,
        lng=lng,
        radius=radius,
        user_context=context or "",
        include_specific_locations=include_locations,
        include_menu=include_menu
    )
    
    return result

@router.post("/recommend", response_model=dict)
async def get_recommendations_post(request: LocationRequest):
    """
    POST version of recommendations endpoint
    """
    if not (-90 <= request.lat <= 90) or not (-180 <= request.lng <= 180):
        raise HTTPException(
            status_code=400,
            detail="Invalid coordinates"
        )
    
    result = await recommendation_service.analyze_and_recommend(
        lat=request.lat,
        lng=request.lng,
        radius=request.radius,
        user_context=request.context or "",
        include_specific_locations=request.include_locations,
        include_menu=request.include_menu
    )
    
    return result

@router.get("/test", response_model=dict)
async def test_endpoint():
    """Test endpoint"""
    return {
        "status": "success",
        "message": "Recommendation API is working",
        "apis": {
            "google_maps": "active",
            "gemini_ai": "active"
        }
    }

# Export router
__all__ = ["router"]
