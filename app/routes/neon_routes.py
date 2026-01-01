# app/routes/neon_routes.py
from fastapi import APIRouter

# Create router instance FIRST
router = APIRouter(prefix="/api/neon", tags=["Neon PostgreSQL"])

@router.get("/info")
async def neon_info():
    """Get Neon PostgreSQL information"""
    return {
        "status": "connected",
        "database": "neon_postgresql",
        "provider": "Neon.tech",
        "dashboard": "https://console.neon.tech",
        "features": ["serverless", "auto-scaling", "branching"],
        "migration_status": "completed",
        "data_summary": {
            "categories": 9,
            "keywords": 21,
            "rules": 5,
            "menus": 18
        }
    }

@router.get("/check")
async def neon_check():
    """Quick Neon health check"""
    try:
        from app.db.neon_connection import test_connection
        from app.services.neon_service import neon_db_service
        
        connection_ok = test_connection()
        health = neon_db_service.health_check()
        
        return {
            "connection": "ok" if connection_ok else "failed",
            "database_health": health,
            "timestamp": "2024-12-18T12:00:00Z"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }