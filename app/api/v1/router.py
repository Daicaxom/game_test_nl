"""
API v1 Router - Aggregates all API endpoints
"""
from fastapi import APIRouter

from app.api.v1 import auth, heroes, battles, players, gacha, equipment, story, teams

api_router = APIRouter()

# Include routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(players.router, prefix="/players", tags=["Players"])
api_router.include_router(heroes.router, prefix="/heroes", tags=["Heroes"])
api_router.include_router(battles.router, prefix="/battles", tags=["Battles"])
api_router.include_router(gacha.router, prefix="/gacha", tags=["Gacha"])
api_router.include_router(equipment.router, prefix="/equipment", tags=["Equipment"])
api_router.include_router(story.router, prefix="/story", tags=["Story"])
api_router.include_router(teams.router, prefix="/teams", tags=["Teams"])
