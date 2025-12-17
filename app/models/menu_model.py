from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class MenuItem(BaseModel):
    name: str = Field(..., description="Name of the menu item")
    description: Optional[str] = Field(None, description="Item description")
    price: Optional[float] = Field(None, description="Price in local currency")
    is_healthy: Optional[bool] = Field(None, description="Whether this item is healthy")
    category: Optional[str] = Field(None, description="Category (e.g., Appetizer, Main Course)")
    calories: Optional[int] = Field(None, description="Calorie count")
    source: Optional[str] = Field(None, description="Source of the menu item")

class MenuIn(BaseModel):
    place_id: str = Field(..., description="Google Place ID")
    place_name: str = Field(..., description="Name of the restaurant/location")
    items: List[MenuItem] = Field(default=[], description="List of menu items")
    source: str = Field("google", description="Source of menu data")
    last_updated: datetime = Field(default_factory=datetime.now)

class MenuOut(MenuIn):
    id: str = Field(..., alias="_id")
    
    class Config:
        populate_by_name = True
        from_attributes = True