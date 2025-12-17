# # app/models/category_model.py
# from pydantic import BaseModel

# class CategoryIn(BaseModel):
#     id: str
#     name: str
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class CategoryBase(BaseModel):
    name: str = Field(..., description="Category name (e.g., 'Fast Food')")
    description: Optional[str] = Field(None, description="Category description")
    is_unhealthy: bool = Field(True, description="Whether this category triggers recommendations")

class CategoryIn(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: str = Field(..., alias="_id")
    
    class Config:
        populate_by_name = True
        from_attributes = True