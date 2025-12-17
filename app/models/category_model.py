
from pydantic import BaseModel, Field
from typing import Optional

class CategoryBase(BaseModel):
    name: str = Field(..., description="Category name")
    description: Optional[str] = Field(None, description="Category description")
    is_unhealthy: bool = Field(True, description="Whether this category is unhealthy")

class CategoryIn(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: str = Field(..., alias="_id")
    
    class Config:
        populate_by_name = True
        from_attributes = True