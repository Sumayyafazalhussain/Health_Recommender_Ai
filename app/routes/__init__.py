# app/routes/__init__.py
from .admin import router as admin_router
from .recommend import router as recommend_router

__all__ = ['admin_router', 'recommend_router']