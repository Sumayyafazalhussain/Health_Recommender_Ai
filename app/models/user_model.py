# app/models/user_model.py
"""
User Models - Pydantic schemas for user authentication
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    """Base user model with common fields"""
    email: str = Field(
        ..., 
        pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        description="Valid email address"
    )
    full_name: str = Field(
        ..., 
        min_length=2, 
        max_length=100,
        description="User's full name"
    )


class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(
        ..., 
        min_length=6,
        description="Password (minimum 6 characters)"
    )
    health_goals: Optional[List[str]] = Field(
        default=["general_health"],
        description="List of health goals"
    )
    dietary_preferences: Optional[List[str]] = Field(
        default=[],
        description="Dietary preferences (e.g., vegetarian, vegan)"
    )
    allergies: Optional[List[str]] = Field(
        default=[],
        description="List of allergies"
    )


class UserLogin(BaseModel):
    """Schema for user login"""
    email: str = Field(
        ..., 
        pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        description="User's email"
    )
    password: str = Field(
        ...,
        description="User's password"
    )


class UserUpdate(BaseModel):
    """Schema for updating user profile"""
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    health_goals: Optional[List[str]] = None
    dietary_preferences: Optional[List[str]] = None
    allergies: Optional[List[str]] = None


class UserOut(UserBase):
    """Schema for user output (response)"""
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    health_goals: List[str]
    dietary_preferences: List[str]
    allergies: List[str]
    
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """JWT Token response schema"""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(..., description="Token type (bearer)")
    user: UserOut = Field(..., description="User data")


class TokenData(BaseModel):
    """Data extracted from JWT token"""
    email: Optional[str] = None
    user_id: Optional[str] = None