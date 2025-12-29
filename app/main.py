# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Health Recommender AI - Neon PostgreSQL",
    description="Backend with Neon Serverless PostgreSQL Database",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== SIMPLE IMPORTS ==========
try:
    from app.routes.admin import router as admin_router
    app.include_router(admin_router)
    print("✅ Admin routes loaded")
except Exception as e:
    print(f"⚠️ Admin routes error: {e}")

try:
    from app.routes.image import router as image_router
    app.include_router(image_router)
    print("✅ Image routes loaded")
except Exception as e:
    print(f"⚠️ Image routes error: {e}")

try:
    from app.routes.locations import router as locations_router
    app.include_router(locations_router)
    print("✅ Locations routes loaded")
except Exception as e:
    print(f"⚠️ Locations routes error: {e}")

try:
    from app.routes.neon_routes import router as neon_router
    app.include_router(neon_router)
    print("✅ Neon routes loaded")
except Exception as e:
    print(f"⚠️ Neon routes error: {e}")

try:
    from app.routes.recommend import router as recommend_router
    app.include_router(recommend_router)
    print("✅ Recommend routes loaded")
except Exception as e:
    print(f"⚠️ Recommend routes error: {e}")

# ========== ENDPOINTS ==========
@app.get("/")
async def root():
    return {
        "status": "ok",
        "app": "Health Recommender AI",
        "version": "2.0.0",
        "database": "Neon PostgreSQL",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "admin": "/admin/health",
            "neon": "/api/neon/info",
            "image": "/api/image/health",
            "locations": "/api/locations/search",
            "recommend": "/api/recommend"
        }
    }

@app.get("/health")
async def health():
    try:
        from app.services.neon_service import neon_db_service
        db_health = neon_db_service.health_check()
        return {
            "status": "healthy",
            "database": "neon_postgresql",
            "database_status": db_health["status"],
            "data_counts": db_health.get("counts", {}),
            "timestamp": "2024-12-18T12:00:00Z"
        }
    except Exception as e:
        return {
            "status": "degraded",
            "database": "neon_postgresql",
            "error": str(e)
        }

# ========== STARTUP ==========
@app.on_event("startup")
async def startup_event():
    print("\n" + "="*60)
    print("🚀 HEALTH RECOMMENDER AI BACKEND")
    print("📊 Database: Neon PostgreSQL (Serverless)")
    print("="*60)
    
    # Test Neon connection
    try:
        from app.db.neon_connection import test_connection
        if test_connection():
            print("✅ Neon PostgreSQL: CONNECTED")
        else:
            print("❌ Neon PostgreSQL: FAILED")
    except Exception as e:
        print(f"⚠️ Connection test error: {e}")
    
    print("\n🌐 API Endpoints:")
    print("   • Swagger UI: http://localhost:8000/docs")
    print("   • Health: http://localhost:8000/health")
    print("   • Admin: http://localhost:8000/admin/health")
    print("   • Neon Info: http://localhost:8000/api/neon/info")
    print("="*60)
