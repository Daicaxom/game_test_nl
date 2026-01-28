"""
API v1 Router - Aggregates all API endpoints
"""
from fastapi import APIRouter

from app.api.v1 import auth, heroes, battles

api_router = APIRouter()

# Include routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(heroes.router, prefix="/heroes", tags=["Heroes"])
api_router.include_router(battles.router, prefix="/battles", tags=["Battles"])
