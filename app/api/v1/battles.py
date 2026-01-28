"""
Battles API Endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

router = APIRouter()


# Request/Response schemas
class StartBattleRequest(BaseModel):
    """Start battle request schema"""
    stage_id: str
    team_id: str


class ActionRequest(BaseModel):
    """Battle action request schema"""
    action_type: str  # attack, skill, move
    skill_id: Optional[str] = None
    target_ids: List[str]
    destination: Optional[dict] = None  # {"x": 0, "y": 1} for move


class CharacterStateResponse(BaseModel):
    """Character state in battle"""
    id: str
    name: str
    element: str
    position: dict
    current_hp: int
    max_hp: int
    current_mana: int
    max_mana: int
    is_alive: bool
    status_effects: List[str]


class BattleStateResponse(BaseModel):
    """Battle state response schema"""
    battle_id: str
    turn_number: int
    current_actor_id: str
    is_player_turn: bool
    player_team: List[CharacterStateResponse]
    enemy_team: List[CharacterStateResponse]
    weather: Optional[str] = None


class ActionResultResponse(BaseModel):
    """Action result response schema"""
    action_type: str
    actor_id: str
    target_ids: List[str]
    damage_dealt: Optional[List[dict]] = None
    heal_amount: Optional[List[dict]] = None
    effects_applied: Optional[List[dict]] = None
    skill_used: Optional[str] = None


class BattleResultResponse(BaseModel):
    """Battle end result response schema"""
    battle_id: str
    victory: bool
    stars: int
    exp_gained: int
    gold_gained: int
    drops: List[dict]
    first_clear: bool


# Endpoints
@router.post("/start", response_model=BattleStateResponse)
async def start_battle(request: StartBattleRequest):
    """
    Start a new battle against a stage.
    
    - **stage_id**: ID of the stage to battle
    - **team_id**: ID of the player's team to use
    """
    # TODO: Implement with service layer
    return {
        "battle_id": "new-battle-uuid",
        "turn_number": 1,
        "current_actor_id": "hero-1-uuid",
        "is_player_turn": True,
        "player_team": [
            {
                "id": "hero-1-uuid",
                "name": "Quan Vũ",
                "element": "KIM",
                "position": {"x": 0, "y": 1},
                "current_hp": 1000,
                "max_hp": 1000,
                "current_mana": 0,
                "max_mana": 100,
                "is_alive": True,
                "status_effects": []
            }
        ],
        "enemy_team": [
            {
                "id": "enemy-1-uuid",
                "name": "Hoàng Cân Binh",
                "element": "MOC",
                "position": {"x": 2, "y": 1},
                "current_hp": 500,
                "max_hp": 500,
                "current_mana": 0,
                "max_mana": 50,
                "is_alive": True,
                "status_effects": []
            }
        ],
        "weather": None
    }


@router.post("/{battle_id}/action", response_model=ActionResultResponse)
async def execute_action(battle_id: str, request: ActionRequest):
    """
    Execute an action in battle.
    
    - **action_type**: Type of action (attack, skill, move)
    - **skill_id**: Skill ID if using a skill
    - **target_ids**: List of target character IDs
    - **destination**: Grid position if moving
    """
    # TODO: Implement with service layer
    return {
        "action_type": request.action_type,
        "actor_id": "hero-1-uuid",
        "target_ids": request.target_ids,
        "damage_dealt": [{"target_id": request.target_ids[0], "damage": 150, "is_crit": False}],
        "heal_amount": None,
        "effects_applied": None,
        "skill_used": request.skill_id
    }


@router.get("/{battle_id}/state", response_model=BattleStateResponse)
async def get_battle_state(battle_id: str):
    """Get current battle state"""
    # TODO: Implement with service layer
    return {
        "battle_id": battle_id,
        "turn_number": 3,
        "current_actor_id": "hero-1-uuid",
        "is_player_turn": True,
        "player_team": [
            {
                "id": "hero-1-uuid",
                "name": "Quan Vũ",
                "element": "KIM",
                "position": {"x": 1, "y": 1},
                "current_hp": 850,
                "max_hp": 1000,
                "current_mana": 30,
                "max_mana": 100,
                "is_alive": True,
                "status_effects": []
            }
        ],
        "enemy_team": [
            {
                "id": "enemy-1-uuid",
                "name": "Hoàng Cân Binh",
                "element": "MOC",
                "position": {"x": 2, "y": 1},
                "current_hp": 200,
                "max_hp": 500,
                "current_mana": 20,
                "max_mana": 50,
                "is_alive": True,
                "status_effects": []
            }
        ],
        "weather": None
    }


@router.post("/{battle_id}/end", response_model=BattleResultResponse)
async def end_battle(battle_id: str):
    """
    End battle and get rewards.
    Called automatically when all enemies are defeated or can be called to forfeit.
    """
    # TODO: Implement with service layer
    return {
        "battle_id": battle_id,
        "victory": True,
        "stars": 3,
        "exp_gained": 150,
        "gold_gained": 500,
        "drops": [
            {"item_id": "exp_book_1", "quantity": 2},
            {"item_id": "gold_chest", "quantity": 1}
        ],
        "first_clear": True
    }


@router.get("/history")
async def get_battle_history(
    page: int = 1,
    per_page: int = 20
):
    """Get player's battle history"""
    # TODO: Implement with service layer
    return {
        "battles": [
            {
                "battle_id": "past-battle-uuid",
                "stage_id": "stage_1_1",
                "stage_name": "Hoàng Cân Chi Loạn",
                "victory": True,
                "stars": 3,
                "completed_at": "2024-01-15T10:30:00Z"
            }
        ],
        "total": 1,
        "page": page,
        "per_page": per_page
    }
