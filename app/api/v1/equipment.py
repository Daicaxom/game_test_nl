"""
Equipment API Endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter()


# Request/Response schemas
class EquipmentStatsResponse(BaseModel):
    """Equipment stats"""
    hp: int = 0
    atk: int = 0
    def_: int = Field(default=0, alias="def")
    spd: int = 0
    crit: int = 0
    dex: int = 0
    
    class Config:
        populate_by_name = True


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


class EquipmentResponse(EquipmentBriefResponse):
    """Full equipment response"""
    base_stats: EquipmentStatsResponse
    bonus_stats: EquipmentStatsResponse
    total_stats: EquipmentStatsResponse
    substats: List[dict] = Field(default_factory=list)
    set_id: Optional[str] = None
    unique_effect: Optional[dict] = None
    is_locked: bool


class EquipmentListResponse(BaseModel):
    """Equipment list response"""
    equipment: List[EquipmentBriefResponse]
    total: int
    page: int
    per_page: int


class EnhanceRequest(BaseModel):
    """Enhancement request"""
    materials: List[dict] = Field(default_factory=list)


class EnhanceResponse(BaseModel):
    """Enhancement response"""
    equipment_id: str
    old_level: int
    new_level: int
    success: bool
    stats_gained: Optional[EquipmentStatsResponse] = None
    gold_spent: int


class FuseRequest(BaseModel):
    """Fusion request"""
    equipment_ids: List[str] = Field(min_length=2)


class FuseResponse(BaseModel):
    """Fusion response"""
    result_equipment: EquipmentBriefResponse
    consumed_equipment: List[str]


class EquipmentSetResponse(BaseModel):
    """Equipment set response"""
    id: str
    name: str
    description: Optional[str]
    two_piece_bonus: Optional[dict] = None
    three_piece_bonus: Optional[dict] = None
    four_piece_bonus: Optional[dict] = None
    pieces: List[str] = Field(default_factory=list)


# Endpoints
@router.get("", response_model=EquipmentListResponse)
async def get_equipment_list(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    equipment_type: Optional[str] = None,
    rarity: Optional[str] = None
):
    """
    Get player's equipment with filtering and pagination.
    
    - **page**: Page number
    - **per_page**: Items per page
    - **equipment_type**: Filter by type (weapon, armor, accessory, relic)
    - **rarity**: Filter by rarity (common, rare, epic, legendary, mythic)
    """
    # TODO: Implement with service layer
    return {
        "equipment": [
            {
                "id": "sample-equipment-uuid",
                "template_id": "iron_sword",
                "name": "Thanh Long Đao",
                "equipment_type": "weapon",
                "rarity": "legendary",
                "level": 1,
                "power": 120,
                "equipped_by": None
            }
        ],
        "total": 1,
        "page": page,
        "per_page": per_page
    }


@router.get("/sets", response_model=List[EquipmentSetResponse])
async def get_equipment_sets():
    """
    Get all equipment sets.
    """
    # TODO: Implement with service layer
    return [
        {
            "id": "thanh_long",
            "name": "Thanh Long Yểm Nguyệt",
            "description": "Set trang bị của Quan Vũ",
            "two_piece_bonus": {"atk": 15, "crit": 10},
            "three_piece_bonus": {"unique_effect": "Giảm 20% sát thương"},
            "four_piece_bonus": None,
            "pieces": ["thanh_long_dao", "thanh_long_giap", "thanh_long_phu"]
        }
    ]


@router.get("/{equipment_id}", response_model=EquipmentResponse)
async def get_equipment(equipment_id: str):
    """
    Get specific equipment details.
    
    - **equipment_id**: Equipment ID
    """
    # TODO: Implement with service layer
    return {
        "id": equipment_id,
        "template_id": "iron_sword",
        "name": "Thanh Long Đao",
        "equipment_type": "weapon",
        "rarity": "legendary",
        "level": 1,
        "power": 120,
        "equipped_by": None,
        "base_stats": {"hp": 0, "atk": 50, "def_": 0, "spd": 10, "crit": 5, "dex": 5},
        "bonus_stats": {"hp": 0, "atk": 0, "def_": 0, "spd": 0, "crit": 0, "dex": 0},
        "total_stats": {"hp": 0, "atk": 50, "def_": 0, "spd": 10, "crit": 5, "dex": 5},
        "substats": [],
        "set_id": "thanh_long",
        "unique_effect": None,
        "is_locked": False
    }


@router.post("/{equipment_id}/enhance", response_model=EnhanceResponse)
async def enhance_equipment(equipment_id: str, request: EnhanceRequest):
    """
    Enhance equipment to increase its level.
    
    - **equipment_id**: Equipment ID
    - **materials**: Enhancement materials
    """
    # TODO: Implement with service layer
    return {
        "equipment_id": equipment_id,
        "old_level": 1,
        "new_level": 2,
        "success": True,
        "stats_gained": {"hp": 0, "atk": 5, "def_": 0, "spd": 1, "crit": 0, "dex": 0},
        "gold_spent": 100
    }


@router.post("/fuse", response_model=FuseResponse)
async def fuse_equipment(request: FuseRequest):
    """
    Fuse multiple equipment into one.
    
    - **equipment_ids**: List of equipment IDs to fuse
    """
    # TODO: Implement with service layer
    return {
        "result_equipment": {
            "id": "fused-equipment-uuid",
            "template_id": "upgraded_sword",
            "name": "Thanh Long Đao +",
            "equipment_type": "weapon",
            "rarity": "legendary",
            "level": 1,
            "power": 150,
            "equipped_by": None
        },
        "consumed_equipment": request.equipment_ids
    }
