
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.admin import router as admin_router
from app.routes.recommend import router as recommend_router
from app.routes.locations import router as locations_router
from app.routes.image import router as image_router  # ADDED
from app.config import settings

app = FastAPI(
    title="Healthy Recommender Backend",
    description="AI-powered healthy alternative recommendations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(admin_router)
app.include_router(recommend_router)
app.include_router(locations_router)
app.include_router(image_router)  # ADDED

@app.get("/")
def root():
    return {
        "status": "ok", 
        "app": "Healthy Recommender Backend",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "recommendations": "/api/recommend",
            "location_search": "/api/locations/search",
            "healthy_alternatives": "/api/locations/healthy-alternatives",
            "image_analysis": "/api/analyze-image",  # UPDATED
            "admin": "/admin"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}