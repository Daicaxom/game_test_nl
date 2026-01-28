"""
Battle Pydantic Schemas
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from app.schemas.common import PositionSchema


class CharacterStateResponse(BaseModel):
    """Character state in battle"""
    id: str
    name: str
    element: str
    position: PositionSchema
    current_hp: int
    max_hp: int
    current_mana: int
    max_mana: int
    is_alive: bool
    status_effects: List[str] = Field(default_factory=list)


class StartBattleRequest(BaseModel):
    """Start battle request schema"""
    stage_id: str
    team_id: str


class BattleStateResponse(BaseModel):
    """Battle state response schema"""
    battle_id: str
    turn_number: int
    current_actor_id: str
    is_player_turn: bool
    player_team: List[CharacterStateResponse]
    enemy_team: List[CharacterStateResponse]
    weather: Optional[str] = None


class ActionRequest(BaseModel):
    """Battle action request schema"""
    action_type: str = Field(pattern="^(attack|skill|move|defend|item)$")
    skill_id: Optional[str] = None
    target_ids: List[str] = Field(default_factory=list)
    destination: Optional[PositionSchema] = None
    item_id: Optional[str] = None


class DamageDealtInfo(BaseModel):
    """Damage dealt info"""
    target_id: str
    damage: int
    is_crit: bool
    element_multiplier: float = 1.0


class HealAmountInfo(BaseModel):
    """Heal amount info"""
    target_id: str
    heal_amount: int
    new_hp: int


class EffectAppliedInfo(BaseModel):
    """Effect applied info"""
    target_id: str
    effect_type: str
    duration: int


class ActionResultResponse(BaseModel):
    """Action result response schema"""
    action_type: str
    actor_id: str
    target_ids: List[str]
    damage_dealt: Optional[List[DamageDealtInfo]] = None
    heal_amount: Optional[List[HealAmountInfo]] = None
    effects_applied: Optional[List[EffectAppliedInfo]] = None
    skill_used: Optional[str] = None
    mana_consumed: int = 0
    turn_advanced: bool = False


class BattleDropInfo(BaseModel):
    """Battle drop info"""
    item_id: str
    item_name: str
    quantity: int


class BattleResultResponse(BaseModel):
    """Battle end result response schema"""
    battle_id: str
    victory: bool
    stars: int = Field(ge=0, le=3)
    exp_gained: int
    gold_gained: int
    drops: List[BattleDropInfo] = Field(default_factory=list)
    first_clear: bool


class BattleHistoryEntry(BaseModel):
    """Battle history entry"""
    battle_id: str
    stage_id: str
    stage_name: str
    victory: bool
    stars: int
    completed_at: str


class BattleHistoryResponse(BaseModel):
    """Battle history response"""
    battles: List[BattleHistoryEntry]
    total: int
    page: int
    per_page: int


class AIActionResponse(BaseModel):
    """AI action for display"""
    actor_id: str
    actor_name: str
    action_type: str
    target_ids: List[str]
    skill_used: Optional[str] = None
    results: ActionResultResponse


class BattleLogEntry(BaseModel):
    """Battle log entry"""
    turn: int
    actor_id: str
    action_type: str
    targets: List[str]
    result: Dict[str, Any]


class FullBattleLogResponse(BaseModel):
    """Full battle log response"""
    battle_id: str
    logs: List[BattleLogEntry]
    total_turns: int
