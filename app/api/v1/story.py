"""
Story API Endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter()


# Request/Response schemas
class StageResponse(BaseModel):
    """Stage response"""
    id: str
    stage_number: int
    name: str
    difficulty: int
    recommended_power: int
    stamina_cost: int
    waves: int
    is_boss_stage: bool
    is_unlocked: bool = True
    stars: int = 0
    cleared: bool = False


class ChapterBriefResponse(BaseModel):
    """Brief chapter response for listings"""
    id: str
    chapter_number: int
    title: str
    description: str
    is_mythical: bool
    is_unlocked: bool
    stage_count: int
    stages_cleared: int


class ChapterResponse(ChapterBriefResponse):
    """Full chapter response with stages"""
    stages: List[StageResponse]


class StageDetailResponse(StageResponse):
    """Detailed stage response"""
    chapter_id: str
    chapter_title: str
    first_clear_rewards: dict
    repeat_rewards: dict


class StartStageRequest(BaseModel):
    """Start stage request"""
    team_id: str


class StartStageResponse(BaseModel):
    """Start stage response"""
    stage_id: str
    team_id: str
    stamina_spent: int
    message: str


class StoryProgressResponse(BaseModel):
    """Story progress response"""
    player_id: str
    chapters_cleared: int
    total_chapters: int
    stages_cleared: int
    total_stages: int
    stars_earned: int
    max_stars: int
    current_chapter: str


# Endpoints
@router.get("/chapters", response_model=List[ChapterBriefResponse])
async def get_chapters():
    """
    Get all story chapters with progress.
    """
    # TODO: Implement with service layer
    return [
        {
            "id": "chapter_1",
            "chapter_number": 1,
            "title": "Khởi Nghĩa Hoàng Cân",
            "description": "Loạn Hoàng Cân nổi dậy, thiên hạ đại loạn",
            "is_mythical": False,
            "is_unlocked": True,
            "stage_count": 10,
            "stages_cleared": 3
        },
        {
            "id": "chapter_2",
            "chapter_number": 2,
            "title": "Đổng Trác Loạn Kinh",
            "description": "Đổng Trác kiểm soát triều đình",
            "is_mythical": False,
            "is_unlocked": False,
            "stage_count": 10,
            "stages_cleared": 0
        }
    ]


@router.get("/chapters/{chapter_id}", response_model=ChapterResponse)
async def get_chapter(chapter_id: str):
    """
    Get chapter details with stages.
    
    - **chapter_id**: Chapter ID
    """
    # TODO: Implement with service layer
    return {
        "id": chapter_id,
        "chapter_number": 1,
        "title": "Khởi Nghĩa Hoàng Cân",
        "description": "Loạn Hoàng Cân nổi dậy, thiên hạ đại loạn",
        "is_mythical": False,
        "is_unlocked": True,
        "stage_count": 3,
        "stages_cleared": 1,
        "stages": [
            {
                "id": "stage_1_1",
                "stage_number": 1,
                "name": "Hoàng Cân Chi Loạn",
                "difficulty": 1,
                "recommended_power": 1000,
                "stamina_cost": 10,
                "waves": 3,
                "is_boss_stage": False,
                "is_unlocked": True,
                "stars": 3,
                "cleared": True
            },
            {
                "id": "stage_1_2",
                "stage_number": 2,
                "name": "Tiêu Diệt Phản Quân",
                "difficulty": 2,
                "recommended_power": 1500,
                "stamina_cost": 10,
                "waves": 3,
                "is_boss_stage": False,
                "is_unlocked": True,
                "stars": 0,
                "cleared": False
            },
            {
                "id": "stage_1_3",
                "stage_number": 3,
                "name": "Đối Đầu Trương Giác",
                "difficulty": 3,
                "recommended_power": 2000,
                "stamina_cost": 15,
                "waves": 1,
                "is_boss_stage": True,
                "is_unlocked": False,
                "stars": 0,
                "cleared": False
            }
        ]
    }


@router.get("/stages/{stage_id}", response_model=StageDetailResponse)
async def get_stage(stage_id: str):
    """
    Get detailed stage information.
    
    - **stage_id**: Stage ID
    """
    # TODO: Implement with service layer
    return {
        "id": stage_id,
        "stage_number": 1,
        "name": "Hoàng Cân Chi Loạn",
        "difficulty": 1,
        "recommended_power": 1000,
        "stamina_cost": 10,
        "waves": 3,
        "is_boss_stage": False,
        "is_unlocked": True,
        "stars": 3,
        "cleared": True,
        "chapter_id": "chapter_1",
        "chapter_title": "Khởi Nghĩa Hoàng Cân",
        "first_clear_rewards": {
            "gold": 500,
            "gems": 10,
            "exp": 100
        },
        "repeat_rewards": {
            "gold": 100,
            "exp": 50
        }
    }


@router.post("/stages/{stage_id}/start", response_model=StartStageResponse)
async def start_stage(stage_id: str, request: StartStageRequest):
    """
    Start a stage battle.
    
    - **stage_id**: Stage ID
    - **team_id**: Team ID to use
    """
    # TODO: Implement with service layer
    return {
        "stage_id": stage_id,
        "team_id": request.team_id,
        "stamina_spent": 10,
        "message": "Stage started successfully"
    }


@router.get("/progress", response_model=StoryProgressResponse)
async def get_story_progress():
    """
    Get player's story progress.
    """
    # TODO: Implement with service layer
    return {
        "player_id": "current-player-uuid",
        "chapters_cleared": 0,
        "total_chapters": 7,
        "stages_cleared": 1,
        "total_stages": 70,
        "stars_earned": 3,
        "max_stars": 210,
        "current_chapter": "chapter_1"
    }
