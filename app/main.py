
# # app/main.py
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# app = FastAPI(
#     title="Health Recommender AI - Neon PostgreSQL",
#     description="Backend with Neon Serverless PostgreSQL Database",
#     version="2.0.0",
#     docs_url="/docs",
#     redoc_url="/redoc"
# )

# # CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ========== IMPORT ROUTERS ==========
# # Import all routers at the top level (not inside functions)
# from app.routes.admin import router as admin_router
# from app.routes.image import router as image_router
# from app.routes.locations import router as locations_router
# from app.routes.neon_routes import router as neon_router
# from app.routes.recommend import router as recommend_router

# # Include routers
# app.include_router(admin_router)
# app.include_router(image_router)
# app.include_router(locations_router)
# app.include_router(neon_router)
# app.include_router(recommend_router)

# # ========== ENDPOINTS ==========
# @app.get("/")
# async def root():
#     return {
#         "status": "ok",
#         "app": "Health Recommender AI",
#         "version": "2.0.0",
#         "database": "Neon PostgreSQL",
#         "endpoints": {
#             "docs": "/docs",
#             "health": "/health",
#             "admin": "/admin/health",
#             "neon": "/api/neon/info",
#             "image": "/api/image/health",
#             "locations": "/api/locations/search",
#             "recommend": "/api/recommend"
#         }
#     }

# @app.get("/health")
# async def health():
#     try:
#         from app.services.neon_service import neon_db_service
#         db_health = neon_db_service.health_check()
#         return {
#             "status": "healthy",
#             "database": "neon_postgresql",
#             "database_status": db_health["status"],
#             "data_counts": db_health.get("counts", {}),
#             "timestamp": "2024-12-18T12:00:00Z"
#         }
#     except Exception as e:
#         return {
#             "status": "degraded",
#             "database": "neon_postgresql",
#             "error": str(e)
#         }

# # ========== STARTUP EVENT ==========
# @app.on_event("startup")
# async def startup_event():
#     print("\n" + "="*60)
#     print("🚀 HEALTH RECOMMENDER AI BACKEND")
#     print("📊 Database: Neon PostgreSQL (Serverless)")
#     print("="*60)
    
#     # Initialize services (they auto-initialize when imported)
#     try:
#         from app.services.ai_service import ai_service
#         print("✅ AI Service: Ready")
#     except Exception as e:
#         print(f"⚠️ AI Service: {e}")
    
#     try:
#         from app.services.google_service import google_service
#         print("✅ Google Maps Service: Ready")
#     except Exception as e:
#         print(f"⚠️ Google Maps Service: {e}")
    
#     try:
#         from app.services.neon_service import neon_db_service
#         print("✅ Neon Service: Ready")
#     except Exception as e:
#         print(f"⚠️ Neon Service: {e}")
    
#     # Test Neon connection
#     try:
#         from app.db.neon_connection import test_connection
#         if test_connection():
#             print("✅ Neon PostgreSQL: CONNECTED")
#         else:
#             print("❌ Neon PostgreSQL: FAILED")
#     except Exception as e:
#         print(f"⚠️ Connection test error: {e}")
    
#     print("\n🌐 API Endpoints:")
#     print("   • Swagger UI: http://localhost:8000/docs")
#     print("   • Health: http://localhost:8000/health")
#     print("   • Admin: http://localhost:8000/admin/health")
#     print("   • Neon Info: http://localhost:8000/api/neon/info")
#     print("="*60)# app/main.py - UPDATE to include auth router


# # app/main.py
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# app = FastAPI(
#     title="Health Recommender AI",
#     description="Health food recommendation system with JWT Auth",
#     version="3.0.0",
#     docs_url="/docs",
#     redoc_url="/redoc"
# )

# # CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ========== MANUALLY IMPORT AND INCLUDE ROUTERS ==========
# print("\n" + "="*60)
# print("🚀 LOADING ROUTERS")
# print("="*60)

# # 1. Admin routes
# try:
#     from app.routes.admin import router as admin_router
#     app.include_router(admin_router)
#     print("✅ Admin routes loaded")
# except ImportError as e:
#     print(f"⚠️  Admin routes: {e}")

# # 2. Auth routes - MOST IMPORTANT!
# try:
#     from app.routes.auth import router as auth_router
#     app.include_router(auth_router)
#     print("✅ Auth routes loaded - JWT Authentication READY")
# except ImportError as e:
#     print(f"❌ Auth routes FAILED: {e}")
#     print("   Creating basic auth router...")
    
#     # Create basic auth router if import fails
#     from fastapi import APIRouter
#     auth_router = APIRouter(prefix="/api/auth", tags=["authentication"])
    
#     @auth_router.get("/health")
#     async def auth_health():
#         return {"status": "setup-needed", "message": "Complete auth setup required"}
    
#     app.include_router(auth_router)

# # 3. Image routes
# try:
#     from app.routes.image import router as image_router
#     app.include_router(image_router)
#     print("✅ Image routes loaded")
# except ImportError as e:
#     print(f"⚠️  Image routes: {e}")

# # 4. Location routes
# try:
#     from app.routes.locations import router as locations_router
#     app.include_router(locations_router)
#     print("✅ Location routes loaded")
# except ImportError as e:
#     print(f"⚠️  Location routes: {e}")

# # 5. Neon routes
# try:
#     from app.routes.neon_routes import router as neon_router
#     app.include_router(neon_router)
#     print("✅ Neon routes loaded")
# except ImportError as e:
#     print(f"⚠️  Neon routes: {e}")

# # 6. Recommend routes
# try:
#     from app.routes.recommend import router as recommend_router
#     app.include_router(recommend_router)
#     print("✅ Recommend routes loaded")
# except ImportError as e:
#     print(f"⚠️  Recommend routes: {e}")

# print("="*60)
# print("🎯 All routers loaded successfully!")
# print("="*60)

# # ========== BASIC ENDPOINTS ==========
# @app.get("/")
# async def root():
#     return {
#         "status": "running",
#         "app": "Health Recommender AI",
#         "version": "3.0.0",
#         "message": "Backend is running with JWT Authentication",
#         "endpoints": {
#             "swagger": "/docs",
#             "health": "/health",
#             "auth_health": "/api/auth/health",
#             "register": "/api/auth/register",
#             "login": "/api/auth/login-json"
#         }
#     }

# @app.get("/health")
# async def health():
#     return {
#         "status": "healthy",
#         "database": "neon_postgresql",
#         "timestamp": "2024-12-18T12:00:00Z"
#     }

# # ========== STARTUP EVENT ==========
# @app.on_event("startup")
# async def startup():
#     print("\n" + "="*60)
#     print("🏥 HEALTH RECOMMENDER AI BACKEND")
#     print("📊 Database: Neon PostgreSQL")
#     print("🔐 Authentication: JWT")
#     print("="*60)
    
#     print("\n🌐 AVAILABLE ENDPOINTS:")
#     print("   • Swagger UI: http://localhost:8000/docs")
#     print("   • Health: http://localhost:8000/health")
#     print("   • Auth Health: http://localhost:8000/api/auth/health")
#     print("   • Register: http://localhost:8000/api/auth/register")
#     print("   • Login: http://localhost:8000/api/auth/login-json")
#     print("\n📞 Test endpoints:")
#     print("   curl http://localhost:8000/api/auth/health")
#     print("   curl -X POST http://localhost:8000/api/auth/register \\")
#     print('        -H "Content-Type: application/json" \\')
#     print('        -d \'{"email":"test@example.com","full_name":"Test User","password":"123"}\'')
#     print("="*60)













# # app/main.py
# """
# Health Recommender AI - Main Application
# FastAPI Backend with JWT Authentication
# """

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# import logging
# import sys
# import os

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
# logger = logging.getLogger(__name__)

# # Create FastAPI application
# app = FastAPI(
#     title="Health Recommender AI",
#     description="AI-powered health recommendations with JWT authentication",
#     version="2.0.0",
#     docs_url="/docs",
#     redoc_url="/redoc"
# )

# # CORS Middleware Configuration
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # In production, specify your frontend domain
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ============================================================
# # ROUTER LOADING - CRITICAL SECTION
# # ============================================================

# print("\n" + "="*70)
# print("🔧 LOADING APPLICATION ROUTERS")
# print("="*70)

# # Counter for successfully loaded routers
# routers_loaded = 0
# routers_failed = 0

# # ============================================================
# # 1. AUTHENTICATION ROUTER (HIGHEST PRIORITY)
# # ============================================================
# try:
#     print("\n📍 Loading Authentication Router...")
    
#     # Import the auth module
#     from app.routes import auth
    
#     # Register the router
#     app.include_router(auth.router)
    
#     routers_loaded += 1
#     logger.info("✅ Authentication router loaded successfully")
#     print("✅ Authentication router loaded: /api/auth")
#     print("   • GET  /api/auth/health")
#     print("   • GET  /api/auth/test")
#     print("   • POST /api/auth/register")
#     print("   • POST /api/auth/login")
#     print("   • GET  /api/auth/me (protected)")
#     print("   • PUT  /api/auth/me (protected)")
#     print("   • POST /api/auth/logout (protected)")
#     print("   • POST /api/auth/verify (protected)")
#     print("   • DELETE /api/auth/me (protected)")
    
# except ImportError as e:
#     routers_failed += 1
#     logger.error(f"❌ Failed to import auth router: {e}")
#     print(f"❌ AUTH ROUTER IMPORT FAILED: {e}")
#     print("   Check: app/routes/auth.py exists and has no syntax errors")
    
# except Exception as e:
#     routers_failed += 1
#     logger.error(f"❌ Failed to load auth router: {e}")
#     print(f"❌ AUTH ROUTER LOADING FAILED: {e}")
#     import traceback
#     traceback.print_exc()

# # ============================================================
# # 2. ADMIN ROUTER
# # ============================================================
# try:
#     print("\n📍 Loading Admin Router...")
#     from app.routes import admin
#     app.include_router(admin.router)
#     routers_loaded += 1
#     logger.info("✅ Admin router loaded")
#     print("✅ Admin router loaded: /admin")
# except Exception as e:
#     routers_failed += 1
#     logger.warning(f"⚠️  Admin router: {str(e)[:50]}")
#     print(f"⚠️  Admin router: {str(e)[:50]}")

# # ============================================================
# # 3. IMAGE ANALYSIS ROUTER
# # ============================================================
# try:
#     print("\n📍 Loading Image Analysis Router...")
#     from app.routes import image
#     app.include_router(image.router)
#     routers_loaded += 1
#     logger.info("✅ Image router loaded")
#     print("✅ Image router loaded: /api/image")
# except Exception as e:
#     routers_failed += 1
#     logger.warning(f"⚠️  Image router: {str(e)[:50]}")
#     print(f"⚠️  Image router: {str(e)[:50]}")

# # ============================================================
# # 4. LOCATIONS ROUTER
# # ============================================================
# try:
#     print("\n📍 Loading Locations Router...")
#     from app.routes import locations
#     app.include_router(locations.router)
#     routers_loaded += 1
#     logger.info("✅ Locations router loaded")
#     print("✅ Locations router loaded: /api/locations")
# except Exception as e:
#     routers_failed += 1
#     logger.warning(f"⚠️  Locations router: {str(e)[:50]}")
#     print(f"⚠️  Locations router: {str(e)[:50]}")

# # ============================================================
# # 5. NEON DATABASE ROUTER
# # ============================================================
# try:
#     print("\n📍 Loading Neon Database Router...")
#     from app.routes import neon_routes
#     app.include_router(neon_routes.router)
#     routers_loaded += 1
#     logger.info("✅ Neon router loaded")
#     print("✅ Neon router loaded: /api/neon")
# except Exception as e:
#     routers_failed += 1
#     logger.warning(f"⚠️  Neon router: {str(e)[:50]}")
#     print(f"⚠️  Neon router: {str(e)[:50]}")

# # ============================================================
# # 6. RECOMMENDATION ROUTER
# # ============================================================
# try:
#     print("\n📍 Loading Recommendation Router...")
#     from app.routes import recommend
#     app.include_router(recommend.router)
#     routers_loaded += 1
#     logger.info("✅ Recommend router loaded")
#     print("✅ Recommend router loaded: /api/recommend")
# except Exception as e:
#     routers_failed += 1
#     logger.warning(f"⚠️  Recommend router: {str(e)[:50]}")
#     print(f"⚠️  Recommend router: {str(e)[:50]}")

# # ============================================================
# # ROUTER LOADING SUMMARY
# # ============================================================
# print("\n" + "="*70)
# print(f"📊 ROUTER LOADING SUMMARY")
# print(f"   ✅ Loaded: {routers_loaded}")
# print(f"   ❌ Failed: {routers_failed}")
# print("="*70)

# if routers_failed > 0:
#     print("\n⚠️  WARNING: Some routers failed to load!")
#     print("   Check the error messages above for details")

# if routers_loaded == 0:
#     print("\n❌ CRITICAL: No routers loaded! Server may not work correctly!")
# else:
#     print(f"\n✅ Server ready with {routers_loaded} active router(s)")

# print("="*70 + "\n")

# # ============================================================
# # ROOT ENDPOINTS
# # ============================================================

# @app.get("/")
# async def root():
#     """Root endpoint - API information"""
#     return {
#         "status": "running",
#         "service": "Health Recommender AI",
#         "version": "2.0.0",
#         "authentication": "JWT (Bearer Token)",
#         "routers_loaded": routers_loaded,
#         "routers_failed": routers_failed,
#         "documentation": {
#             "swagger_ui": "http://localhost:8000/docs",
#             "redoc": "http://localhost:8000/redoc"
#         },
#         "quick_tests": {
#             "health": "GET /health",
#             "auth_health": "GET /api/auth/health",
#             "auth_test": "GET /api/auth/test"
#         },
#         "authentication_endpoints": {
#             "register": "POST /api/auth/register",
#             "login": "POST /api/auth/login",
#             "profile": "GET /api/auth/me (requires token)",
#             "update": "PUT /api/auth/me (requires token)"
#         }
#     }


# @app.get("/health")
# async def health_check():
#     """System health check"""
#     db_status = "unknown"
    
#     try:
#         from app.db.neon_connection import test_connection
#         db_healthy = test_connection()
#         db_status = "connected" if db_healthy else "disconnected"
#     except Exception as e:
#         db_status = f"error: {str(e)[:50]}"
#         logger.error(f"Database health check failed: {e}")
    
#     return {
#         "status": "healthy",
#         "service": "main",
#         "database": db_status,
#         "authentication": "active" if routers_loaded > 0 else "inactive",
#         "routers_loaded": routers_loaded,
#         "routers_failed": routers_failed
#     }


# @app.get("/api/status")
# async def api_status():
#     """Detailed API status"""
#     try:
#         from app.services.neon_service import neon_db_service
#         db_health = neon_db_service.health_check()
#     except Exception as e:
#         db_health = {"status": "error", "message": str(e)}
    
#     return {
#         "api": "online",
#         "version": "2.0.0",
#         "database": db_health,
#         "routers": {
#             "loaded": routers_loaded,
#             "failed": routers_failed,
#             "total": routers_loaded + routers_failed
#         },
#         "features": {
#             "jwt_authentication": routers_loaded > 0,
#             "image_analysis": True,
#             "recommendations": True,
#             "google_maps": True,
#             "gemini_ai": True
#         }
#     }


# # ============================================================
# # STARTUP EVENT
# # ============================================================

# @app.on_event("startup")
# async def startup_event():
#     """Application startup tasks"""
#     print("\n" + "="*70)
#     print("🚀 HEALTH RECOMMENDER AI - SERVER STARTED")
#     print("="*70)
    
#     # Test database connection
#     try:
#         from app.db.neon_connection import test_connection
#         if test_connection():
#             print("✅ Database: Connected to Neon PostgreSQL")
#             logger.info("Database connection successful")
#         else:
#             print("⚠️  Database: Connection failed")
#             logger.warning("Database connection failed")
#     except Exception as e:
#         print(f"❌ Database Error: {e}")
#         logger.error(f"Database connection error: {e}")
    
#     print("\n🔐 JWT AUTHENTICATION:")
#     if routers_loaded > 0:
#         print("   ✅ Status: ACTIVE")
#         print("\n📋 AUTHENTICATION ENDPOINTS:")
#         print("   • GET    /api/auth/health       - Health check")
#         print("   • GET    /api/auth/test         - Test setup")
#         print("   • POST   /api/auth/register     - Register user")
#         print("   • POST   /api/auth/login        - Login user")
#         print("   • GET    /api/auth/me           - Get profile (protected)")
#         print("   • PUT    /api/auth/me           - Update profile (protected)")
#         print("   • POST   /api/auth/logout       - Logout (protected)")
#         print("   • POST   /api/auth/verify       - Verify token (protected)")
#         print("   • DELETE /api/auth/me           - Delete account (protected)")
#     else:
#         print("   ❌ Status: INACTIVE - Auth router failed to load")
    
#     print("\n🔗 QUICK TESTS:")
#     print("   curl http://localhost:8000/")
#     print("   curl http://localhost:8000/health")
#     print("   curl http://localhost:8000/api/auth/health")
#     print("   curl http://localhost:8000/api/auth/test")
    
#     print("\n📚 DOCUMENTATION:")
#     print("   • Swagger UI: http://localhost:8000/docs")
#     print("   • ReDoc:      http://localhost:8000/redoc")
    
#     print("\n🧪 TESTING:")
#     print("   Run: python test_jwt_auth.py")
    
#     print("="*70 + "\n")
    
#     logger.info("Application startup complete")


# @app.on_event("shutdown")
# async def shutdown_event():
#     """Application shutdown tasks"""
#     logger.info("Server shutting down...")
#     print("\n" + "="*70)
#     print("🛑 SERVER SHUTDOWN")
#     print("="*70)


# # ============================================================
# # EXCEPTION HANDLERS
# # ============================================================

# @app.exception_handler(404)
# async def not_found_handler(request, exc):
#     """Custom 404 handler"""
#     return {
#         "error": "Not Found",
#         "message": f"Endpoint {request.url.path} not found",
#         "tip": "Check /docs for available endpoints"
#     }


# @app.exception_handler(500)
# async def internal_error_handler(request, exc):
#     """Custom 500 handler"""
#     logger.error(f"Internal server error: {exc}")
#     return {
#         "error": "Internal Server Error",
#         "message": "An unexpected error occurred",
#         "tip": "Check server logs for details"
#     }


# # ============================================================
# # MAIN ENTRY POINT (for direct execution)
# # ============================================================

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(
#         "app.main:app",
#         host="0.0.0.0",
#         port=8000,
#         reload=True,
#         log_level="info"
#     )










# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    
    print("\n🔗 IMPORTANT ENDPOINTS:")
    print("   📍 API Root:        http://localhost:8000/")
    print("   🔐 Authentication:  http://localhost:8000/auth/register")
    print("   📋 Documentation:   http://localhost:8000/docs")
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

# Import routers
print("\n📡 Loading routers...")

try:
    # Load auth router first
    from app.routes.auth import router as auth_router
    app.include_router(auth_router)
    print("✅ Authentication routes loaded")
except Exception as e:
    print(f"❌ Failed to load auth router: {e}")
    # Create minimal auth endpoints
    from fastapi import APIRouter
    fallback_auth = APIRouter(prefix="/auth", tags=["Authentication"])
    
    @fallback_auth.get("/health")
    async def auth_health():
        return {"status": "fallback", "message": "Auth router failed to load"}
    
    app.include_router(fallback_auth)

# Load other routers
routers = [
    ("admin", "/admin"),
    ("image", "/api/image"),
    ("locations", "/api/locations"),
    ("neon_routes", "/api/neon"),
    ("recommend", "/api")
]

for router_name, prefix in routers:
    try:
        module = __import__(f"app.routes.{router_name}", fromlist=["router"])
        router = getattr(module, "router")
        app.include_router(router)
        print(f"✅ {router_name} routes loaded")
    except Exception as e:
        print(f"⚠️  Failed to load {router_name}: {str(e)[:50]}")

print("="*60)

# Root endpoint
@app.get("/")
async def root():
    return {
        "status": "running",
        "service": "Health Recommender AI",
        "version": "2.0.0",
        "authentication": "JWT Enabled",
        "endpoints": {
            "auth_register": "POST /auth/register",
            "auth_login": "POST /auth/login",
            "auth_profile": "GET /auth/me (requires JWT)",
            "image_analysis": "GET /api/image/analyze-quick",
            "recommendations": "GET /api/recommend",
            "documentation": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    try:
        from app.services.neon_service import neon_db_service
        db_health = neon_db_service.health_check()
        return {
            "status": "healthy",
            "database": db_health.get("status", "unknown"),
            "auth": "jwt_enabled",
            "services": {
                "image_analysis": "active",
                "recommendations": "active",
                "google_maps": "active"
            }
        }
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e)
        }

# Test endpoint to verify auth is working
@app.get("/test-auth-setup")
async def test_auth_setup():
    from app.config import settings
    
    return {
        "jwt_secret_set": bool(settings.SECRET_KEY),
        "jwt_secret_length": len(settings.SECRET_KEY) if settings.SECRET_KEY else 0,
        "database_url_set": bool(settings.DATABASE_URL),
        "auth_endpoints": [
            "http://localhost:8000/auth/health",
            "http://localhost:8000/auth/register",
            "http://localhost:8000/auth/login"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)