"""
Heroes API Endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel

router = APIRouter()


# Request/Response schemas
class HeroStatsResponse(BaseModel):
    """Hero stats response schema"""
    hp: int
    atk: int
    def_: int
    spd: int
    crit: int
    dex: int
    
    class Config:
        populate_by_name = True


class HeroResponse(BaseModel):
    """Hero response schema"""
    id: str
    template_id: str
    name: str
    element: str
    rarity: int
    level: int
    exp: int
    stars: int
    ascension_level: int
    awakening_level: int
    stats: HeroStatsResponse
    power: int


class HeroListResponse(BaseModel):
    """Hero list response schema"""
    heroes: List[HeroResponse]
    total: int
    page: int
    per_page: int


class LevelUpRequest(BaseModel):
    """Level up request schema"""
    exp_items: List[dict]  # [{"item_id": "exp_book_1", "quantity": 5}]


class LevelUpResponse(BaseModel):
    """Level up response schema"""
    hero_id: str
    old_level: int
    new_level: int
    leveled_up: bool
    stats: HeroStatsResponse


class EquipRequest(BaseModel):
    """Equip equipment request schema"""
    equipment_id: str
    slot: str  # weapon, armor, accessory, relic


# Endpoints
@router.get("", response_model=HeroListResponse)
async def get_heroes(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    element: Optional[str] = None,
    rarity: Optional[int] = None
):
    """
    Get player's heroes with filtering and pagination.
    
    - **page**: Page number (default: 1)
    - **per_page**: Items per page (default: 20, max: 100)
    - **element**: Filter by element (KIM, MOC, THUY, HOA, THO)
    - **rarity**: Filter by rarity (1-6)
    """
    # TODO: Implement with service layer
    sample_hero = {
        "id": "sample-hero-uuid",
        "template_id": "quan_vu",
        "name": "Quan Vũ",
        "element": "KIM",
        "rarity": 5,
        "level": 1,
        "exp": 0,
        "stars": 1,
        "ascension_level": 0,
        "awakening_level": 0,
        "stats": {"hp": 1000, "atk": 120, "def_": 80, "spd": 95, "crit": 15, "dex": 10},
        "power": 1320
    }
    
    return {
        "heroes": [sample_hero],
        "total": 1,
        "page": page,
        "per_page": per_page
    }


@router.get("/{hero_id}", response_model=HeroResponse)
async def get_hero(hero_id: str):
    """Get specific hero details"""
    # TODO: Implement with service layer
    return {
        "id": hero_id,
        "template_id": "quan_vu",
        "name": "Quan Vũ",
        "element": "KIM",
        "rarity": 5,
        "level": 1,
        "exp": 0,
        "stars": 1,
        "ascension_level": 0,
        "awakening_level": 0,
        "stats": {"hp": 1000, "atk": 120, "def_": 80, "spd": 95, "crit": 15, "dex": 10},
        "power": 1320
    }


@router.post("/{hero_id}/level-up", response_model=LevelUpResponse)
async def level_up_hero(hero_id: str, request: LevelUpRequest):
    """
    Level up a hero using experience items.
    
    - **exp_items**: List of experience items to consume
    """
    # TODO: Implement with service layer
    return {
        "hero_id": hero_id,
        "old_level": 1,
        "new_level": 2,
        "leveled_up": True,
        "stats": {"hp": 1050, "atk": 125, "def_": 83, "spd": 98, "crit": 16, "dex": 11}
    }


@router.post("/{hero_id}/ascend")
async def ascend_hero(hero_id: str):
    """
    Ascend a hero to unlock higher level cap and passive skills.
    
    Requirements:
    - Hero must be at max level for current ascension
    - Required ascension materials
    """
    # TODO: Implement with service layer
    return {
        "hero_id": hero_id,
        "new_ascension_level": 1,
        "new_level_cap": 30,
        "unlocked_passive": "Thanh Long Hộ Thể"
    }


@router.post("/{hero_id}/awaken")
async def awaken_hero(hero_id: str):
    """
    Awaken a hero to unlock special abilities and stat boost.
    
    Requirements:
    - Hero must meet awakening requirements
    - Required awakening materials
    """
    # TODO: Implement with service layer
    return {
        "hero_id": hero_id,
        "new_awakening_level": 1,
        "stat_boost_percent": 10,
        "unlocked_ability": "new_skill_variant"
    }


@router.post("/{hero_id}/equip")
async def equip_item(hero_id: str, request: EquipRequest):
    """
    Equip an item to a hero.
    
    - **equipment_id**: ID of equipment to equip
    - **slot**: Equipment slot (weapon, armor, accessory, relic)
    """
    # TODO: Implement with service layer
    return {
        "hero_id": hero_id,
        "slot": request.slot,
        "equipped_id": request.equipment_id,
        "unequipped_id": None,
        "new_stats": {"hp": 1100, "atk": 170, "def_": 80, "spd": 100, "crit": 20, "dex": 15}
    }


@router.delete("/{hero_id}/equip/{slot}")
async def unequip_item(hero_id: str, slot: str):
    """
    Remove equipment from a hero slot.
    
    - **slot**: Equipment slot to unequip (weapon, armor, accessory, relic)
    """
    # TODO: Implement with service layer
    return {
        "hero_id": hero_id,
        "slot": slot,
        "unequipped_id": "removed-equipment-uuid"
    }
