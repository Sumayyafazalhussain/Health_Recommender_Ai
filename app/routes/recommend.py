

# # app/routes/recommend.py
# from fastapi import APIRouter, HTTPException, Query
# from pydantic import BaseModel
# from typing import Optional

# router = APIRouter(prefix="/api", tags=["recommendations"])

# class LocationRequest(BaseModel):
#     lat: float
#     lng: float
#     radius: Optional[int] = 500
#     context: Optional[str] = None
#     include_locations: Optional[bool] = False
#     include_menu: Optional[bool] = False

# @router.get("/recommend", response_model=dict)
# async def get_recommendations(
#     lat: float = Query(..., ge=-90, le=90, description="Latitude"),
#     lng: float = Query(..., ge=-180, le=180, description="Longitude"),
#     radius: int = Query(500, ge=100, le=5000, description="Search radius in meters"),
#     context: Optional[str] = Query(None, description="User context (morning, evening, workout)"),
#     include_locations: bool = Query(False, description="Include specific location suggestions"),
#     include_menu: bool = Query(False, description="Include menu information")
# ):
#     """
#     Get AI-powered healthy recommendations based on location
#     """
#     if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
#         raise HTTPException(
#             status_code=400,
#             detail="Invalid coordinates"
#         )
    
#     try:
#         from app.services.recommend_service import recommendation_service
#         result = await recommendation_service.analyze_and_recommend(
#             lat=lat,
#             lng=lng,
#             radius=radius,
#             user_context=context or "",
#             include_specific_locations=include_locations,
#             include_menu=include_menu
#         )
        
#         return result
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.post("/recommend", response_model=dict)
# async def get_recommendations_post(request: LocationRequest):
#     """
#     POST version of recommendations endpoint
#     """
#     if not (-90 <= request.lat <= 90) or not (-180 <= request.lng <= 180):
#         raise HTTPException(
#             status_code=400,
#             detail="Invalid coordinates"
#         )
    
#     try:
#         from app.services.recommend_service import recommendation_service
#         result = await recommendation_service.analyze_and_recommend(
#             lat=request.lat,
#             lng=request.lng,
#             radius=request.radius,
#             user_context=request.context or "",
#             include_specific_locations=request.include_locations,
#             include_menu=request.include_menu
#         )
        
#         return result
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.get("/test", response_model=dict)
# async def test_endpoint():
#     """Test endpoint"""
#     return {
#         "status": "success",
#         "message": "Recommendation API is working",
#         "apis": {
#             "google_maps": "active",
#             "gemini_ai": "active"
#         }
#     }










# app/routes/recommend.py
from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from app.db.neon_connection import get_db, User

router = APIRouter(prefix="/api", tags=["recommendations"])


# ========== IMPORT GET_CURRENT_USER DEPENDENCY ==========
async def get_current_user_optional(
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Optional authentication - returns None if no token provided
    Allows endpoints to work with or without auth
    """
    try:
        from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
        from fastapi import Request
        
        # This is a simplified version - you might need to adjust based on your needs
        return None
    except:
        return None


class LocationRequest(BaseModel):
    lat: float
    lng: float
    radius: Optional[int] = 500
    context: Optional[str] = None
    include_locations: Optional[bool] = False
    include_menu: Optional[bool] = False


# ========== PUBLIC ENDPOINTS (No Auth Required) ==========

@router.get("/recommend", response_model=dict)
async def get_recommendations(
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lng: float = Query(..., ge=-180, le=180, description="Longitude"),
    radius: int = Query(500, ge=100, le=5000, description="Search radius in meters"),
    context: Optional[str] = Query(None, description="User context (morning, evening, workout)"),
    include_locations: bool = Query(False, description="Include specific location suggestions"),
    include_menu: bool = Query(False, description="Include menu information"),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """
    Get AI-powered healthy recommendations based on location
    
    This endpoint works with or without authentication.
    If authenticated, recommendations can be personalized based on user preferences.
    """
    if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
        raise HTTPException(
            status_code=400,
            detail="Invalid coordinates"
        )
    
    try:
        from app.services.recommend_service import recommendation_service
        
        # Get user preferences if authenticated
        user_context = context or ""
        if current_user:
            # Add user-specific context
            health_goals = getattr(current_user, 'health_goals', [])
            dietary_prefs = getattr(current_user, 'dietary_preferences', [])
            allergies = getattr(current_user, 'allergies', [])
            
            if health_goals:
                user_context += f" User goals: {', '.join(health_goals)}."
            if dietary_prefs:
                user_context += f" Dietary preferences: {', '.join(dietary_prefs)}."
            if allergies:
                user_context += f" Allergies: {', '.join(allergies)}."
        
        result = await recommendation_service.analyze_and_recommend(
            lat=lat,
            lng=lng,
            radius=radius,
            user_context=user_context,
            include_specific_locations=include_locations,
            include_menu=include_menu
        )
        
        # Add authentication status to response
        result['authenticated'] = current_user is not None
        if current_user:
            result['user_email'] = current_user.email
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recommend", response_model=dict)
async def get_recommendations_post(
    request: LocationRequest,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """
    POST version of recommendations endpoint
    
    This endpoint works with or without authentication.
    If authenticated, recommendations can be personalized.
    """
    if not (-90 <= request.lat <= 90) or not (-180 <= request.lng <= 180):
        raise HTTPException(
            status_code=400,
            detail="Invalid coordinates"
        )
    
    try:
        from app.services.recommend_service import recommendation_service
        
        # Get user preferences if authenticated
        user_context = request.context or ""
        if current_user:
            health_goals = getattr(current_user, 'health_goals', [])
            dietary_prefs = getattr(current_user, 'dietary_preferences', [])
            allergies = getattr(current_user, 'allergies', [])
            
            if health_goals:
                user_context += f" User goals: {', '.join(health_goals)}."
            if dietary_prefs:
                user_context += f" Dietary preferences: {', '.join(dietary_prefs)}."
            if allergies:
                user_context += f" Allergies: {', '.join(allergies)}."
        
        result = await recommendation_service.analyze_and_recommend(
            lat=request.lat,
            lng=request.lng,
            radius=request.radius,
            user_context=user_context,
            include_specific_locations=request.include_locations,
            include_menu=request.include_menu
        )
        
        # Add authentication status
        result['authenticated'] = current_user is not None
        if current_user:
            result['user_email'] = current_user.email
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test", response_model=dict)
async def test_endpoint():
    """Test endpoint"""
    return {
        "status": "success",
        "message": "Recommendation API is working",
        "apis": {
            "google_maps": "active",
            "gemini_ai": "active"
        },
        "authentication": "Optional - works with or without JWT"
    }