# app/services/user_service.py
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timedelta

from app.db.neon_connection import SessionLocal, User
from app.services.auth_service import get_password_hash, verify_password, create_access_token
from models.user_model import UserCreate, UserUpdate, UserOut, Token
import logging

logger = logging.getLogger(__name__)

class UserService:
    
    @staticmethod
    def get_db():
        """Get database session"""
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        """Create a new user"""
        # Check if user already exists
        db_user = UserService.get_user_by_email(db, user.email)
        if db_user:
            raise ValueError("User with this email already exists")
        
        # Create new user
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            full_name=user.full_name,
            hashed_password=hashed_password,
            health_goals=user.health_goals or ['general_health'],
            dietary_preferences=user.dietary_preferences or [],
            allergies=user.allergies or []
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        logger.info(f"User created: {user.email}")
        return db_user
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = UserService.get_user_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    @staticmethod
    def login_user(db: Session, email: str, password: str) -> Optional[Token]:
        """Login user and return token"""
        user = UserService.authenticate_user(db, email, password)
        if not user:
            return None
        
        # Create access token
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id},
            expires_delta=access_token_expires
        )
        
        # Convert user to output format
        user_out = UserOut.model_validate(user)
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=user_out
        )
    
    @staticmethod
    def update_user(db: Session, user_id: str, user_update: UserUpdate) -> Optional[User]:
        """Update user information"""
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            return None
        
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db_user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    @staticmethod
    def delete_user(db: Session, user_id: str) -> bool:
        """Delete a user (soft delete)"""
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            return False
        
        db_user.is_active = False
        db.commit()
        
        return True

# Create global instance
user_service = UserService()