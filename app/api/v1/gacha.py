"""
Gacha API Endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter()


# Request/Response schemas
class BannerResponse(BaseModel):
    """Gacha banner response"""
    id: str
    name: str
    rates: dict  # {"3": 80, "4": 18, "5": 2}
    cost_single: int
    cost_multi: int
    featured: Optional[str] = None


class BannerDetailResponse(BannerResponse):
    """Detailed banner response"""
    pity_counter: int
    featured_rate_up: Optional[int] = None


class PullRequest(BaseModel):
    """Pull request"""
    banner_id: str
    pull_count: int = Field(default=1, ge=1, le=10)


class PullResult(BaseModel):
    """Single pull result"""
    hero_id: str
    rarity: int
    is_new: bool
    is_featured: bool


class PullResponse(BaseModel):
    """Pull response"""
    banner_id: str
    pull_count: int
    gems_spent: int
    results: List[PullResult]
    pity_counter: int


class PityResponse(BaseModel):
    """Pity counter response"""
    player_id: str
    banner_id: str
    current_pity: int
    pity_threshold: int
    pulls_until_guaranteed: int


class GachaHistoryEntry(BaseModel):
    """Gacha history entry"""
    banner_id: str
    hero_id: str
    rarity: int
    timestamp: str


class GachaHistoryResponse(BaseModel):
    """Gacha history response"""
    history: List[GachaHistoryEntry]
    total: int
    page: int
    per_page: int


# Endpoints
@router.get("/banners", response_model=List[BannerResponse])
async def get_banners():
    """
    Get all available gacha banners.
    """
    # TODO: Implement with service layer
    return [
        {
            "id": "standard",
            "name": "Banner Tiêu Chuẩn",
            "rates": {"3": 80, "4": 18, "5": 2},
            "cost_single": 160,
            "cost_multi": 1440,
            "featured": None
        },
        {
            "id": "limited_quan_vu",
            "name": "Banner Quan Vũ",
            "rates": {"3": 75, "4": 20, "5": 5},
            "cost_single": 160,
            "cost_multi": 1440,
            "featured": "quan_vu"
        }
    ]


@router.get("/banners/{banner_id}", response_model=BannerDetailResponse)
async def get_banner(banner_id: str):
    """
    Get detailed banner information.
    
    - **banner_id**: The banner ID
    """
    # TODO: Implement with service layer
    return {
        "id": banner_id,
        "name": "Banner Tiêu Chuẩn",
        "rates": {"3": 80, "4": 18, "5": 2},
        "cost_single": 160,
        "cost_multi": 1440,
        "featured": None,
        "pity_counter": 90,
        "featured_rate_up": None
    }


@router.post("/pull", response_model=PullResponse)
async def pull_gacha(request: PullRequest):
    """
    Perform gacha pulls.
    
    - **banner_id**: ID of the banner to pull from
    - **pull_count**: Number of pulls (1 or 10)
    """
    # TODO: Implement with service layer
    results = []
    for i in range(request.pull_count):
        results.append({
            "hero_id": "quan_binh" if i < 8 else ("xu_chu" if i < 9 else "quan_vu"),
            "rarity": 3 if i < 8 else (4 if i < 9 else 5),
            "is_new": True,
            "is_featured": i == 9
        })
    
    return {
        "banner_id": request.banner_id,
        "pull_count": request.pull_count,
        "gems_spent": 160 if request.pull_count == 1 else 1440,
        "results": results,
        "pity_counter": 5
    }


@router.get("/pity", response_model=PityResponse)
async def get_pity(banner_id: str = Query(...)):
    """
    Get current pity counter for a banner.
    
    - **banner_id**: The banner ID
    """
    # TODO: Implement with service layer
    return {
        "player_id": "current-player-uuid",
        "banner_id": banner_id,
        "current_pity": 5,
        "pity_threshold": 90,
        "pulls_until_guaranteed": 85
    }


@router.get("/history", response_model=GachaHistoryResponse)
async def get_gacha_history(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100)
):
    """
    Get gacha pull history.
    
    - **page**: Page number
    - **per_page**: Items per page
    """
    # TODO: Implement with service layer
    return {
        "history": [
            {
                "banner_id": "standard",
                "hero_id": "quan_vu",
                "rarity": 5,
                "timestamp": "2024-01-15T10:30:00Z"
            }
        ],
        "total": 1,
        "page": page,
        "per_page": per_page
    }
