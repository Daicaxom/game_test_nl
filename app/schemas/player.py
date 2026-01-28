"""
Player Pydantic Schemas
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class PlayerBase(BaseModel):
    """Base player schema"""
    username: str
    email: EmailStr
    display_name: Optional[str] = None


class PlayerCreate(PlayerBase):
    """Player creation schema"""
    password: str = Field(min_length=8)


class PlayerUpdate(BaseModel):
    """Player update schema"""
    display_name: Optional[str] = Field(default=None, max_length=100)


class PlayerResponse(BaseModel):
    """Player response schema"""
    id: str
    username: str
    email: str
    display_name: Optional[str]
    level: int
    exp: int
    gold: int
    gems: int
    stamina: int
    max_stamina: int
    vip_level: int
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True


class PlayerBriefResponse(BaseModel):
    """Brief player response for listings"""
    id: str
    username: str
    display_name: Optional[str]
    level: int


class PlayerStatsResponse(BaseModel):
    """Player stats summary"""
    player_id: str
    level: int
    total_heroes: int
    total_power: int
    story_progress: str
    battles_won: int
    battles_lost: int


class PlayerResourcesResponse(BaseModel):
    """Player resources"""
    gold: int
    gems: int
    stamina: int
    max_stamina: int


class UpdateResourcesRequest(BaseModel):
    """Request to add/spend resources"""
    gold: int = Field(default=0)
    gems: int = Field(default=0)
    stamina: int = Field(default=0)


class PlayerInventoryResponse(BaseModel):
    """Player inventory summary"""
    player_id: str
    hero_count: int
    equipment_count: int
    mount_count: int
    material_count: int
