"""
Equipment Pydantic Schemas
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from app.schemas.common import StatsBase, ItemQuantity


class EquipmentStatsResponse(StatsBase):
    """Equipment stats response"""
    pass


class SubstatSchema(BaseModel):
    """Equipment substat schema"""
    stat: str
    value: int


class EquipmentBase(BaseModel):
    """Base equipment schema"""
    template_id: str
    name: str
    equipment_type: str  # weapon, armor, accessory, relic
    rarity: str  # common, rare, epic, legendary, mythic


class EquipmentResponse(EquipmentBase):
    """Equipment response schema"""
    id: str
    level: int
    base_stats: EquipmentStatsResponse
    bonus_stats: EquipmentStatsResponse
    total_stats: EquipmentStatsResponse
    substats: List[SubstatSchema] = Field(default_factory=list)
    set_id: Optional[str] = None
    unique_effect: Optional[Dict[str, Any]] = None
    equipped_by: Optional[str] = None
    is_locked: bool
    power: int
    
    class Config:
        from_attributes = True


class EquipmentBriefResponse(BaseModel):
    """Brief equipment response for listings"""
    id: str
    template_id: str
    name: str
    equipment_type: str
    rarity: str
    level: int
    power: int
    equipped_by: Optional[str] = None


class EquipmentListResponse(BaseModel):
    """Equipment list response"""
    equipment: List[EquipmentBriefResponse]
    total: int
    page: int
    per_page: int


class EnhanceRequest(BaseModel):
    """Enhance equipment request"""
    materials: List[ItemQuantity] = Field(default_factory=list)
    gold_cost: int = Field(default=0, ge=0)


class EnhanceResponse(BaseModel):
    """Enhance equipment response"""
    equipment_id: str
    old_level: int
    new_level: int
    success: bool
    stats_gained: Optional[EquipmentStatsResponse] = None
    gold_spent: int


class FuseRequest(BaseModel):
    """Fuse equipment request"""
    equipment_ids: List[str] = Field(min_length=2)


class FuseResponse(BaseModel):
    """Fuse equipment response"""
    result_equipment: EquipmentBriefResponse
    consumed_equipment: List[str]


class EquipmentFilterParams(BaseModel):
    """Equipment filter parameters"""
    equipment_type: Optional[str] = None
    rarity: Optional[str] = None
    min_level: Optional[int] = Field(default=None, ge=1)
    set_id: Optional[str] = None
    is_equipped: Optional[bool] = None


class EquipmentSetResponse(BaseModel):
    """Equipment set response"""
    id: str
    name: str
    description: Optional[str]
    two_piece_bonus: Optional[Dict[str, int]] = None
    three_piece_bonus: Optional[Dict[str, int]] = None
    four_piece_bonus: Optional[Dict[str, int]] = None
    pieces: List[str] = Field(default_factory=list)
