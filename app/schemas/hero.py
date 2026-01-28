"""
Hero Pydantic Schemas
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from app.schemas.common import StatsBase, ItemQuantity


class HeroStatsResponse(StatsBase):
    """Hero stats response schema"""
    pass


class HeroSkillResponse(BaseModel):
    """Hero skill response schema"""
    skill_id: str
    name: str
    level: int
    is_unlocked: bool
    mana_cost: int
    cooldown: int


class HeroEquipmentSlots(BaseModel):
    """Hero equipment slots schema"""
    weapon_id: Optional[str] = None
    armor_id: Optional[str] = None
    accessory_id: Optional[str] = None
    relic_id: Optional[str] = None


class HeroBase(BaseModel):
    """Base hero schema"""
    template_id: str
    name: str
    element: str
    rarity: int = Field(ge=1, le=6)


class HeroResponse(HeroBase):
    """Hero response schema"""
    id: str
    level: int
    exp: int
    stars: int = Field(ge=1, le=6)
    ascension_level: int = Field(ge=0, le=6)
    awakening_level: int = Field(ge=0, le=6)
    stats: HeroStatsResponse
    power: int
    equipment: HeroEquipmentSlots
    skills: List[HeroSkillResponse] = Field(default_factory=list)
    is_locked: bool
    is_favorite: bool
    
    class Config:
        from_attributes = True


class HeroBriefResponse(BaseModel):
    """Brief hero response for listings"""
    id: str
    template_id: str
    name: str
    element: str
    rarity: int
    level: int
    stars: int
    power: int


class HeroListResponse(BaseModel):
    """Hero list response schema"""
    heroes: List[HeroBriefResponse]
    total: int
    page: int
    per_page: int


class LevelUpRequest(BaseModel):
    """Level up request schema"""
    exp_items: List[ItemQuantity] = Field(min_length=1)


class LevelUpResponse(BaseModel):
    """Level up response schema"""
    hero_id: str
    old_level: int
    new_level: int
    leveled_up: bool
    stats: HeroStatsResponse


class AscendRequest(BaseModel):
    """Ascend hero request schema"""
    materials: List[ItemQuantity] = Field(default_factory=list)


class AscendResponse(BaseModel):
    """Ascend hero response schema"""
    hero_id: str
    old_ascension_level: int
    new_ascension_level: int
    new_level_cap: int
    unlocked_passive: Optional[str] = None


class AwakenRequest(BaseModel):
    """Awaken hero request schema"""
    materials: List[ItemQuantity] = Field(default_factory=list)


class AwakenResponse(BaseModel):
    """Awaken hero response schema"""
    hero_id: str
    old_awakening_level: int
    new_awakening_level: int
    stat_boost_percent: int
    unlocked_ability: Optional[str] = None


class EquipRequest(BaseModel):
    """Equip equipment request schema"""
    equipment_id: str
    slot: str = Field(pattern="^(weapon|armor|accessory|relic)$")


class EquipResponse(BaseModel):
    """Equip response schema"""
    hero_id: str
    slot: str
    equipped_id: str
    unequipped_id: Optional[str] = None
    new_stats: HeroStatsResponse


class UnequipResponse(BaseModel):
    """Unequip response schema"""
    hero_id: str
    slot: str
    unequipped_id: str


class SkillUpgradeRequest(BaseModel):
    """Skill upgrade request schema"""
    materials: List[ItemQuantity] = Field(default_factory=list)


class SkillUpgradeResponse(BaseModel):
    """Skill upgrade response schema"""
    hero_id: str
    skill_id: str
    old_level: int
    new_level: int
    new_effect: Optional[Dict[str, Any]] = None


class HeroFilterParams(BaseModel):
    """Hero filter parameters"""
    element: Optional[str] = None
    rarity: Optional[int] = Field(default=None, ge=1, le=6)
    min_level: Optional[int] = Field(default=None, ge=1)
    max_level: Optional[int] = Field(default=None, ge=1)
    stars: Optional[int] = Field(default=None, ge=1, le=6)
