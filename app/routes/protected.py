# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("\n" + "="*60)
    print("🚀 HEALTH RECOMMENDER AI - Starting Server")
    print("="*60)
    
    # Test database connection
    try:
        from app.db.neon_connection import test_connection
        db_ok = test_connection()
        if db_ok:
            print("✅ Database connection successful")
        else:
            print("⚠️  Database connection issue")
    except Exception as e:
        print(f"⚠️  Database connection error: {e}")
    
    # Check JWT configuration
    from app.config import settings
    if settings.SECRET_KEY and settings.SECRET_KEY != "your-fallback-secret-key-for-development-12345":
        print("✅ JWT authentication configured")
    else:
        print("⚠️  Using development JWT secret - change in production!")
    
    print("\n🔗 AVAILABLE ENDPOINTS:")
    print("   📍 API Root:        http://localhost:8000/")
    print("   🔐 Authentication:  http://localhost:8000/api/auth/register")
    print("   📋 Documentation:   http://localhost:8000/docs")
    print("   🖼️  Image Analysis: http://localhost:8000/api/image/analyze-quick")
    print("   🗺️  Recommendations: http://localhost:8000/api/recommend")
    print("="*60)
    print("💡 Use /docs for interactive API testing")
    print("="*60)
    
    yield
    
    # Shutdown
    print("\n🛑 SERVER SHUTTING DOWN...")

app = FastAPI(
    title="Health Recommender AI",
    version="2.0.0",
    description="JWT-enabled health recommendation system with AI-powered food analysis",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
from app.routes.auth import router as auth_router
from app.routes.admin import router as admin_router
from app.routes.image import router as image_router
from app.routes.locations import router as locations_router
from app.routes.neon_routes import router as neon_routes_router
from app.routes.recommend import router as recommend_router

# Include routers
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(image_router)
app.include_router(locations_router)
app.include_router(neon_routes_router)
app.include_router(recommend_router)

# Try to include protected routes if they exist
try:
    from app.routes.protected import router as protected_router
    app.include_router(protected_router)
    print("✅ Protected routes loaded")
except ImportError:
    pass

# Root endpoint
@app.get("/")
async def root():
    return {
        "status": "running",
        "service": "Health Recommender AI",
        "version": "2.0.0",
        "features": {
            "jwt_auth": True,
            "image_analysis": True,
            "ai_recommendations": True,
            "google_maps": True,
            "postgresql": True
        },
        "authentication": {
            "register": "POST /api/auth/register",
            "login": "POST /api/auth/login",
            "profile": "GET /api/auth/me"
        },
        "endpoints": {
            "image_analysis": "GET /api/image/analyze-quick",
            "recommendations": "GET /api/recommend",
            "locations": "GET /api/locations/search",
            "admin": "GET /admin/categories"
        },
        "documentation": "/docs"
    }

@app.get("/health")
async def health_check():
    from app.services.neon_service import neon_db_service
    
    try:
        db_health = neon_db_service.health_check()
        return {
            "status": "healthy",
            "services": {
                "database": db_health.get("status", "unknown"),
                "authentication": "jwt_enabled",
                "image_processing": "available",
                "ai_service": "available"
            },
            "database_stats": db_health.get("counts", {}),
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e),
            "services": {
                "database": "unavailable",
                "authentication": "jwt_enabled",
                "image_processing": "available"
            }
        }

# Error handlers
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "status": "error",
            "message": f"Route {request.url.path} not found",
            "available_routes": [
                "/",
                "/health",
                "/docs",
                "/api/auth/register",
                "/api/auth/login",
                "/api/auth/me",
                "/api/auth/health",
                "/api/image/analyze-quick",
                "/api/recommend",
                "/api/locations/search",
                "/admin/categories"
            ]
        }
    )

@app.exception_handler(401)
async def unauthorized_handler(request: Request, exc):
    return JSONResponse(
        status_code=401,
        content={
            "status": "error",
            "message": "Authentication required",
            "solution": "Login at /api/auth/login or register at /api/auth/register"
        },
        headers={"WWW-Authenticate": "Bearer"}
    )

@app.get("/test-auth")
async def test_auth_setup():
    """Test if authentication is properly configured"""
    from app.config import settings
    
    return {
        "jwt_configured": bool(settings.SECRET_KEY),
        "database_url_set": bool(settings.DATABASE_URL),
        "google_api_set": bool(settings.GOOGLE_API_KEY),
        "gemini_api_set": bool(settings.GEMINI_API_KEY),
        "token_expiry_minutes": settings.ACCESS_TOKEN_EXPIRE_MINUTES
    }