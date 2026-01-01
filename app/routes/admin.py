
# app/routes/admin.py
from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/admin", tags=["admin"])

# ==================== CATEGORIES ====================
@router.post("/categories", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_category(category: dict):
    """Create a new category"""
    try:
        from app.services.neon_service import neon_db_service
        result = neon_db_service.create_category(category)
        
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories", response_model=dict)
async def list_categories():
    """Get all categories"""
    try:
        from app.services.neon_service import neon_db_service
        categories = neon_db_service.get_categories()
        return {
            "status": "success",
            "count": len(categories),
            "categories": categories
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== KEYWORDS ====================
@router.post("/keywords", response_model=dict)
async def create_keyword(keyword: dict):
    """Add a keyword for category detection"""
    try:
        from app.services.neon_service import neon_db_service
        result = neon_db_service.create_keyword(keyword)
        
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/keywords", response_model=dict)
async def list_keywords():
    """Get all keywords"""
    try:
        from app.services.neon_service import neon_db_service
        keywords = neon_db_service.get_keywords()
        return {
            "status": "success",
            "count": len(keywords),
            "keywords": keywords
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== RULES ====================
@router.post("/rules", response_model=dict)
async def create_rule(rule: dict):
    """Create a recommendation rule"""
    try:
        from app.services.neon_service import neon_db_service
        result = neon_db_service.create_rule(rule)
        
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/rules", response_model=dict)
async def list_rules():
    """Get all rules with details"""
    try:
        from app.services.neon_service import neon_db_service
        rules = neon_db_service.get_rules()
        return {
            "status": "success",
            "count": len(rules),
            "rules": rules
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== STATISTICS ====================
@router.get("/stats", response_model=dict)
async def get_stats():
    """Get database statistics"""
    try:
        from app.services.neon_service import neon_db_service
        result = neon_db_service.health_check()
        return {
            "status": "success",
            "database": "neon_postgresql",
            "counts": result.get("counts", {})
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health", response_model=dict)
async def admin_health():
    """Admin health check"""
    try:
        from app.services.neon_service import neon_db_service
        result = neon_db_service.health_check()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

@router.get("/test-neon")
async def test_neon_connection():
    """Test Neon PostgreSQL connection"""
    try:
        from app.services.neon_service import neon_db_service
        result = neon_db_service.health_check()
        return {
            "status": "success",
            "database": "neon_postgresql",
            "connection": "healthy" if result.get("status") == "healthy" else "unhealthy",
            "details": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))








# from fastapi import APIRouter, HTTPException, status, Depends
# from sqlalchemy.orm import Session

# from app.db.neon_connection import get_db
# from app.routes.auth import get_current_active_user
# from models.user_model import UserOut

# router = APIRouter(prefix="/admin", tags=["admin"])

# # Add authentication dependency to admin routes
# @router.get("/categories", response_model=dict)
# async def list_categories(
#     current_user: UserOut = Depends(get_current_active_user),
#     db: Session = Depends(get_db)
# ):
#     """Get all categories (protected)"""
#     try:
#         from app.services.neon_service import neon_db_service
#         categories = neon_db_service.get_categories()
#         return {
#             "status": "success",
#             "count": len(categories),
#             "categories": categories
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # Similarly add @router.post("/categories") and other admin routes with authentication