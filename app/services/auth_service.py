# # app/services/auth_service.py
# """
# Authentication Service - JWT token management and password hashing
# """

# from datetime import datetime, timedelta
# from typing import Optional
# from jose import JWTError, jwt
# from passlib.context import CryptContext
# from app.config import settings
# from app.models.user_model import TokenData
# import logging

# logger = logging.getLogger(__name__)

# # ============================================================
# # PASSWORD HASHING CONFIGURATION
# # ============================================================
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# # ============================================================
# # JWT CONFIGURATION
# # ============================================================
# SECRET_KEY = settings.SECRET_KEY
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


# # ============================================================
# # PASSWORD FUNCTIONS
# # ============================================================

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     """
#     Verify a plain password against a hashed password
    
#     Args:
#         plain_password: The plain text password
#         hashed_password: The hashed password from database
        
#     Returns:
#         True if password matches, False otherwise
#     """
#     try:
#         return pwd_context.verify(plain_password, hashed_password)
#     except Exception as e:
#         logger.error(f"Error verifying password: {e}")
#         return False


# def get_password_hash(password: str) -> str:
#     """
#     Hash a plain password using bcrypt
    
#     Args:
#         password: Plain text password
        
#     Returns:
#         Hashed password string
#     """
#     try:
#         return pwd_context.hash(password)
#     except Exception as e:
#         logger.error(f"Error hashing password: {e}")
#         raise


# # ============================================================
# # JWT TOKEN FUNCTIONS
# # ============================================================

# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
#     """
#     Create a JWT access token
    
#     Args:
#         data: Dictionary containing token payload (must include 'sub' and 'user_id')
#         expires_delta: Optional expiration time delta
        
#     Returns:
#         Encoded JWT token string
#     """
#     try:
#         to_encode = data.copy()
        
#         # Set expiration time
#         if expires_delta:
#             expire = datetime.utcnow() + expires_delta
#         else:
#             expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
#         # Add expiration to token
#         to_encode.update({"exp": expire})
        
#         # Encode JWT
#         encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
#         logger.debug(f"Created token for user: {data.get('sub')}")
#         return encoded_jwt
        
#     except Exception as e:
#         logger.error(f"Error creating access token: {e}")
#         raise


# def verify_token(token: str) -> Optional[TokenData]:
#     """
#     Verify and decode a JWT token
    
#     Args:
#         token: JWT token string
        
#     Returns:
#         TokenData object if valid, None if invalid
#     """
#     try:
#         # Decode JWT
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
#         # Extract data
#         email: str = payload.get("sub")
#         user_id: str = payload.get("user_id")
        
#         # Validate required fields
#         if email is None or user_id is None:
#             logger.warning("Token missing required fields")
#             return None
        
#         # Return token data
#         return TokenData(email=email, user_id=user_id)
        
#     except JWTError as e:
#         logger.warning(f"JWT verification failed: {e}")
#         return None
#     except Exception as e:
#         logger.error(f"Error verifying token: {e}")
#         return None


# def decode_token(token: str) -> Optional[dict]:
#     """
#     Decode a JWT token without verification (for debugging)
    
#     Args:
#         token: JWT token string
        
#     Returns:
#         Decoded payload dictionary or None
#     """
#     try:
#         payload = jwt.decode(
#             token, 
#             SECRET_KEY, 
#             algorithms=[ALGORITHM],
#             options={"verify_signature": False}
#         )
#         return payload
#     except Exception as e:
#         logger.error(f"Error decoding token: {e}")
#         return None




# app/services/auth_service.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings
from app.models.user_model import TokenData
import logging

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[TokenData]:
    """Verify and decode a JWT token"""
    try:
        logger.info(f"Verifying token: {token[:50]}...")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        email: str = payload.get("sub")
        user_id: str = payload.get("user_id")
        
        logger.info(f"Token payload: email={email}, user_id={user_id}")
        
        if email is None or user_id is None:
            logger.warning("Token missing email or user_id")
            return None
            
        return TokenData(email=email, user_id=user_id)
    except JWTError as e:
        logger.error(f"JWT verification error: {e}")
        return None
    except Exception as e:
        logger.error(f"Token verification error: {e}")
        return None