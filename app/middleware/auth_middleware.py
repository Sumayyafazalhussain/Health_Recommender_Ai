# app/middleware/auth_middleware.py
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List, Optional
import time

# List of public routes that don't require authentication
PUBLIC_ROUTES = [
    "/",
    "/health",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/api/auth/register",
    "/api/auth/login",
    "/api/auth/health",
    "/api/image/",
    "/api/recommend",
    "/api/locations/",
    "/api/neon/",
    "/test-auth"
]

async def auth_middleware(request: Request, call_next):
    """Middleware to check JWT tokens for protected routes"""
    start_time = time.time()
    
    # Skip middleware for public routes
    path = request.url.path
    if any(path.startswith(public) for public in PUBLIC_ROUTES):
        response = await call_next(request)
        return response
    
    # Check for Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "status": "error",
                "message": "Missing Authorization header",
                "required": "Bearer token"
            }
        )
    
    # Check if it's a Bearer token
    if not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "status": "error",
                "message": "Invalid Authorization header format",
                "required": "Bearer <token>"
            }
        )
    
    # Extract token
    token = auth_header.split(" ")[1] if len(auth_header.split(" ")) > 1 else ""
    
    if not token:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "status": "error",
                "message": "Missing token"
            }
        )
    
    # Verify token (simplified - actual verification happens in dependencies)
    try:
        from app.services.auth_service import verify_token
        token_data = verify_token(token)
        if not token_data:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "status": "error",
                    "message": "Invalid or expired token"
                }
            )
        
        # Add user info to request state for use in endpoints
        request.state.user_id = token_data.user_id
        request.state.user_email = token_data.email
        
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "status": "error",
                "message": f"Token verification failed: {str(e)}"
            }
        )
    
    # Process request
    response = await call_next(request)
    
    # Add request time to headers
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    return response