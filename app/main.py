
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.routes.admin import router as admin_router
# from app.routes.recommend import router as recommend_router
# from app.routes.locations import router as locations_router
# from app.routes.image import router as image_router  # ADDED
# from app.config import settings

# app = FastAPI(
#     title="Healthy Recommender Backend",
#     description="AI-powered healthy alternative recommendations",
#     version="1.0.0"
# )

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Include routers
# app.include_router(admin_router)
# app.include_router(recommend_router)
# app.include_router(locations_router)
# app.include_router(image_router)  # ADDED

# @app.get("/")
# def root():
#     return {
#         "status": "ok", 
#         "app": "Healthy Recommender Backend",
#         "version": "1.0.0",
#         "docs": "/docs",
#         "endpoints": {
#             "recommendations": "/api/recommend",
#             "location_search": "/api/locations/search",
#             "healthy_alternatives": "/api/locations/healthy-alternatives",
#             "image_analysis": "/api/analyze-image",  # UPDATED
#             "admin": "/admin"
#         }
#     }

# @app.get("/health")
# def health_check():
#     return {"status": "healthy"}


# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.admin import router as admin_router
from app.routes.recommend import router as recommend_router
from app.routes.locations import router as locations_router
from app.routes.image import router as image_router
from app.config import settings  # Changed from 'app.config' to '.config'

app = FastAPI(
    title="Healthy Recommender Backend",
    description="AI-powered healthy alternative recommendations",
    version="1.0.0",
    docs_url="/docs",  # Explicitly enable Swagger
    redoc_url="/redoc"  # Enable ReDoc as well
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers with prefixes
app.include_router(admin_router, prefix="/api", tags=["Admin"])
app.include_router(recommend_router, prefix="/api", tags=["Recommendations"])
app.include_router(locations_router, prefix="/api", tags=["Locations"])
app.include_router(image_router, prefix="/api", tags=["Image Analysis"])

@app.get("/", tags=["Root"])
def root():
    """Root endpoint with API information"""
    return {
        "status": "ok", 
        "app": "Healthy Recommender Backend",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "recommendations": "/api/recommend",
            "location_search": "/api/locations/search",
            "healthy_alternatives": "/api/locations/healthy-alternatives",
            "image_analysis": "/api/image/analyze",
            "image_analysis_quick": "/api/image/analyze-quick",
            "admin": "/admin"
        }
    }

@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": "2024-12-18"}

@app.get("/api/info", tags=["API Info"])
def api_info():
    """Detailed API information"""
    return {
        "name": "Healthy Recommender API",
        "version": "1.0.0",
        "description": "AI-powered food image analysis and healthy recommendations",
        "contact": {
            "name": "API Support",
            "email": "support@example.com"
        },
        "license": {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT"
        }
    }