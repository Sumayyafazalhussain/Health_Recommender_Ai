# app/__init__.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def create_app() -> FastAPI:
    app = FastAPI(
        title="Healthy Recommender Backend",
        description="AI-powered healthy alternative recommendations",
        version="1.0.0"
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Routes
    @app.get("/")
    def root():
        return {"message": "Healthy Recommender API"}
    
    @app.get("/health")
    def health():
        return {"status": "healthy"}
    
    # Import and include routers
    try:
        from app.routes.recommend import router as recommend_router
        app.include_router(recommend_router)
    except ImportError:
        pass
    
    try:
        from app.routes.admin import router as admin_router
        app.include_router(admin_router)
    except ImportError:
        pass
    
    return app

# Create app instance
app = create_app()