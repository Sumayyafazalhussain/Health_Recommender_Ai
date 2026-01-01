# app/routes/auth.py
"""
JWT Authentication Routes
Complete implementation with all endpoints
"""

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import timedelta
import logging

# Import database
from app.db.neon_connection import get_db, User

# Import models
from app.models.user_model import (
    UserCreate, 
    UserLogin, 
    UserOut, 
    UserUpdate, 
    Token
)

# Import auth services
from app.services.auth_service import (
    get_password_hash,
    verify_password,
    create_access_token,
    verify_token
)

# Import settings
from app.config import settings

# Setup logging
logger = logging.getLogger(__name__)

# ============================================================
# ROUTER SETUP - This is crucial for main.py to find it
# ============================================================
router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

# Security scheme
security = HTTPBearer()

# ============================================================
# HELPER FUNCTION: Get Current User
# ============================================================
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to extract and validate JWT token
    Returns the current authenticated user
    """
    try:
        # Extract token from Authorization header
        token = credentials.credentials
        
        # Verify and decode token
        token_data = verify_token(token)
        
        if token_data is None:
            logger.warning("Invalid token provided")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Get user from database
        user = db.query(User).filter(User.email == token_data.email).first()
        
        if user is None:
            logger.warning(f"User not found: {token_data.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if user is active
        if not user.is_active:
            logger.warning(f"Inactive user attempted access: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user"
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_current_user: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ============================================================
# PUBLIC ENDPOINTS (No authentication required)
# ============================================================

@router.get("/health")
async def health_check():
    """
    Health check endpoint
    Test: curl http://localhost:8000/api/auth/health
    """
    return {
        "status": "healthy",
        "service": "authentication",
        "message": "JWT Authentication is active",
        "endpoints": {
            "register": "POST /api/auth/register",
            "login": "POST /api/auth/login",
            "me": "GET /api/auth/me (protected)"
        }
    }


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user
    
    Request body:
    {
        "email": "user@example.com",
        "password": "password123",
        "full_name": "John Doe",
        "health_goals": ["weight_loss"],
        "dietary_preferences": ["vegetarian"],
        "allergies": ["peanuts"]
    }
    
    Returns: JWT token and user data
    """
    try:
        # Check if email already exists
        existing_user = db.query(User).filter(
            User.email == user_data.email
        ).first()
        
        if existing_user:
            logger.warning(f"Registration attempt with existing email: {user_data.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash the password
        hashed_password = get_password_hash(user_data.password)
        
        # Create new user
        new_user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            health_goals=user_data.health_goals or ['general_health'],
            dietary_preferences=user_data.dietary_preferences or [],
            allergies=user_data.allergies or []
        )
        
        # Save to database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        logger.info(f"✅ New user registered: {user_data.email}")
        
        # Create JWT token
        access_token = create_access_token(
            data={"sub": new_user.email, "user_id": new_user.id},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        # Return token and user data
        user_out = UserOut.model_validate(new_user)
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=user_out
        )
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login_user(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login user with email and password
    
    Request body:
    {
        "email": "user@example.com",
        "password": "password123"
    }
    
    Returns: JWT token and user data
    """
    try:
        # Find user by email
        user = db.query(User).filter(User.email == credentials.email).first()
        
        if not user:
            logger.warning(f"Login attempt with non-existent email: {credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verify password
        if not verify_password(credentials.password, user.hashed_password):
            logger.warning(f"Failed login attempt for: {credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if user is active
        if not user.is_active:
            logger.warning(f"Inactive user login attempt: {credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive"
            )
        
        logger.info(f"✅ User logged in: {credentials.email}")
        
        # Create JWT token
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        # Return token and user data
        user_out = UserOut.model_validate(user)
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=user_out
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


# ============================================================
# PROTECTED ENDPOINTS (Authentication required)
# ============================================================

@router.get("/me", response_model=UserOut)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current logged-in user information
    
    Requires: Authorization header with Bearer token
    
    Example:
    curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/api/auth/me
    """
    return UserOut.model_validate(current_user)


@router.put("/me", response_model=UserOut)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user profile
    
    Requires: Authorization header with Bearer token
    
    Request body (all fields optional):
    {
        "full_name": "New Name",
        "health_goals": ["fitness", "weight_loss"],
        "dietary_preferences": ["vegan"],
        "allergies": ["nuts"]
    }
    """
    try:
        # Update only provided fields
        update_data = user_update.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(current_user, field, value)
        
        # Commit changes
        db.commit()
        db.refresh(current_user)
        
        logger.info(f"✅ User profile updated: {current_user.email}")
        
        return UserOut.model_validate(current_user)
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Update error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Profile update failed"
        )


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user)
):
    """
    Logout user
    
    Note: With JWT, logout is handled client-side by removing the token.
    This endpoint just confirms the token is valid.
    """
    logger.info(f"✅ User logged out: {current_user.email}")
    
    return {
        "message": "Logged out successfully",
        "tip": "Remove the JWT token from your client storage"
    }


@router.delete("/me", status_code=status.HTTP_200_OK)
async def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Soft delete user account (deactivate)
    
    Requires: Authorization header with Bearer token
    """
    try:
        # Soft delete - just deactivate
        current_user.is_active = False
        db.commit()
        
        logger.info(f"✅ User account deleted: {current_user.email}")
        
        return {
            "message": "Account deleted successfully"
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Delete error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Account deletion failed"
        )


@router.post("/verify")
async def verify_token_endpoint(
    current_user: User = Depends(get_current_user)
):
    """
    Verify if JWT token is still valid
    
    Requires: Authorization header with Bearer token
    
    Returns user data if token is valid
    """
    return {
        "valid": True,
        "message": "Token is valid",
        "user": UserOut.model_validate(current_user)
    }


# ============================================================
# TESTING ENDPOINT
# ============================================================

@router.get("/test")
async def test_auth_setup():
    """
    Test endpoint to verify authentication module is loaded
    """
    return {
        "status": "success",
        "message": "Authentication routes are working!",
        "available_endpoints": [
            "GET  /api/auth/health",
            "POST /api/auth/register",
            "POST /api/auth/login",
            "GET  /api/auth/me (protected)",
            "PUT  /api/auth/me (protected)",
            "POST /api/auth/logout (protected)",
            "POST /api/auth/verify (protected)",
            "DELETE /api/auth/me (protected)"
        ],
        "jwt_config": {
            "token_expiration": f"{settings.ACCESS_TOKEN_EXPIRE_MINUTES} minutes",
            "algorithm": "HS256"
        }
    }







# # app/routes/auth.py
# from fastapi import APIRouter, HTTPException, status, Depends
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
# from typing import Annotated
# import logging

# from app.db.neon_connection import get_db
# from app.models.user_model import UserCreate, UserLogin, Token, UserOut
# from app.services.user_service import user_service
# from app.services.auth_service import verify_password, create_access_token, verify_token
# from app.config import settings

# logger = logging.getLogger(__name__)

# router = APIRouter(prefix="/auth", tags=["Authentication"])

# # OAuth2 scheme
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# @router.get("/health")
# async def auth_health():
#     """Health check for auth service"""
#     return {
#         "status": "healthy",
#         "service": "authentication",
#         "message": "JWT authentication is active",
#         "endpoints": [
#             "POST /auth/register",
#             "POST /auth/login",
#             "GET /auth/me",
#             "GET /auth/health"
#         ]
#     }

# @router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
# async def register(
#     user_data: UserCreate,
#     db: Session = Depends(get_db)
# ):
#     """Register a new user"""
#     try:
#         logger.info(f"Registering user: {user_data.email}")
        
#         # Check if user already exists
#         existing_user = user_service.get_user_by_email(db, user_data.email)
#         if existing_user:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="User with this email already exists"
#             )
        
#         # Create user
#         user = user_service.create_user(db, user_data)
#         logger.info(f"User registered successfully: {user.email}")
        
#         return UserOut.model_validate(user)
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"Registration error: {e}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Registration failed: {str(e)}"
#         )

# @router.post("/login", response_model=Token)
# async def login(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
#     db: Session = Depends(get_db)
# ):
#     """Login user and return JWT token"""
#     try:
#         logger.info(f"Login attempt for: {form_data.username}")
        
#         # Authenticate user
#         user = user_service.authenticate_user(db, form_data.username, form_data.password)
#         if not user:
#             logger.warning(f"Failed login for: {form_data.username}")
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Incorrect email or password",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
        
#         # Create access token
#         from datetime import timedelta
#         access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#         access_token = create_access_token(
#             data={"sub": user.email, "user_id": user.id},
#             expires_delta=access_token_expires
#         )
        
#         # Convert user to output format
#         user_out = UserOut.model_validate(user)
        
#         logger.info(f"Successful login for: {user.email}")
        
#         return Token(
#             access_token=access_token,
#             token_type="bearer",
#             user=user_out
#         )
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"Login error: {e}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Login failed: {str(e)}"
#         )

# # Dependency to get current user
# async def get_current_user(
#     token: Annotated[str, Depends(oauth2_scheme)],
#     db: Session = Depends(get_db)
# ):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
    
#     try:
#         token_data = verify_token(token)
#         if token_data is None:
#             raise credentials_exception
        
#         user = user_service.get_user_by_email(db, email=token_data.email)
#         if user is None:
#             raise credentials_exception
        
#         return UserOut.model_validate(user)
#     except Exception as e:
#         logger.error(f"Token validation error: {e}")
#         raise credentials_exception

# async def get_current_active_user(
#     current_user: Annotated[UserOut, Depends(get_current_user)]
# ):
#     if not current_user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user

# @router.get("/me", response_model=UserOut)
# async def get_current_user_info(
#     current_user: Annotated[UserOut, Depends(get_current_active_user)]
# ):
#     """Get current user information"""
#     return current_user

# @router.get("/test-token")
# async def test_token(
#     current_user: Annotated[UserOut, Depends(get_current_active_user)]
# ):
#     """Test endpoint to verify token works"""
#     return {
#         "status": "success",
#         "message": "Token is valid",
#         "user": current_user
#     }