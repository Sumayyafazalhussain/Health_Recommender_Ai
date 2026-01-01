# app/routes/__init__.py
# This file makes routes a package and exports all routers

from .auth import router as auth_router
from .admin import router as admin_router
from .image import router as image_router
from .locations import router as locations_router
from .neon_routes import router as neon_routes_router
from .recommend import router as recommend_router

# Try to import protected router
try:
    from .protected import router as protected_router
    __all__ = [
        'auth_router',
        'admin_router',
        'image_router',
        'locations_router',
        'neon_routes_router',
        'recommend_router',
        'protected_router'
    ]
except ImportError:
    __all__ = [
        'auth_router',
        'admin_router',
        'image_router',
        'locations_router',
        'neon_routes_router',
        'recommend_router'
    ]

print(f"✅ Routes package loaded with {len(__all__)} routers")