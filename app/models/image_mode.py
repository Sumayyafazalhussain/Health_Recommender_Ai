from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ImageAnalysisRequest(BaseModel):
    image_url: str = Field(..., description="URL of the food/restaurant image")
    user_lat: Optional[float] = Field(None, description="User's latitude")
    user_lng: Optional[float] = Field(None, description="User's longitude")
    radius: int = Field(1000, description="Search radius in meters")
    include_menu: bool = Field(False, description="Include menu analysis")

class FoodItem(BaseModel):
    name: str = Field(..., description="Food item name")
    confidence: float = Field(..., description="Detection confidence (0-100)")
    category: str = Field(..., description="Food category")
    calories: Optional[int] = Field(None, description="Estimated calories")
    health_score: int = Field(5, description="Health score 1-10")
    is_healthy: bool = Field(False, description="Whether item is healthy")

class ImageAnalysisResponse(BaseModel):
    status: str = Field(..., description="Analysis status")
    detected_items: List[FoodItem] = Field([], description="Detected food items")
    unhealthy_items: List[FoodItem] = Field([], description="Unhealthy items found")
    restaurant_suggestion: Optional[Dict[str, Any]] = Field(None, description="Detected restaurant")
    healthy_alternatives: List[Dict[str, Any]] = Field([], description="Nearby healthy alternatives")
    ai_message: str = Field(..., description="AI recommendation message")
    total_items_detected: int = Field(0, description="Total items detected")