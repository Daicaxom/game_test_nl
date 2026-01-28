"""
Battle Entity - Core battle mechanics and state management
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any, Union
from uuid import uuid4

from app.domain.entities.character import Character
from app.domain.entities.hero import Hero
from app.domain.entities.enemy import Enemy


class BattleState(Enum):
    """Battle state enumeration"""
    PREPARING = "preparing"
    IN_PROGRESS = "in_progress"
    VICTORY = "victory"
    DEFEAT = "defeat"
    RETREAT = "retreat"


class BattleResult(Enum):
    """Battle result enumeration"""
    VICTORY = "victory"
    DEFEAT = "defeat"
    RETREAT = "retreat"


@dataclass
class TurnOrder:
    """
    Manages turn order in battle based on character speed.
    
    Attributes:
        characters: List of characters in the battle
        current_index: Index of current actor
    """
    
    characters: List[Character] = field(default_factory=list)
    current_index: int = 0
    _sorted_order: List[Character] = field(default_factory=list, init=False)
    
    def __post_init__(self) -> None:
        """Initialize and sort turn order"""
        self._recalculate_order()
    
    def _recalculate_order(self) -> None:
        """Recalculate turn order based on speed"""
        alive_characters = [c for c in self.characters if c.is_alive]
        self._sorted_order = sorted(
            alive_characters,
            key=lambda c: c.stats.spd,
            reverse=True
        )
    
    def get_order(self) -> List[Character]:
        """Get the sorted turn order"""
        return self._sorted_order
    
    def get_current(self) -> Optional[Character]:
        """Get the current actor"""
        if not self._sorted_order or self.current_index >= len(self._sorted_order):
            return None
        return self._sorted_order[self.current_index]
    
    def advance(self) -> bool:
        """
        Advance to the next character.
        
        Returns:
            True if a new round has started (wrapped around)
        """
        self.current_index += 1
        
        if self.current_index >= len(self._sorted_order):
            self.current_index = 0
            self._recalculate_order()  # Recalculate for new round
            return True
        
        return False
    
    def remove_character(self, character_id: str) -> None:
        """Remove a character from turn order (when they die)"""
        self._sorted_order = [c for c in self._sorted_order if c.id != character_id]
        if self.current_index >= len(self._sorted_order):
            self.current_index = 0


@dataclass
class Battle:
    """
    Battle entity managing combat state and flow.
    
    Attributes:
        id: Unique battle identifier
        player_id: ID of the player
        stage_id: ID of the stage being fought
        player_team: List of player heroes
        enemy_team: List of enemies
        state: Current battle state
        turn_number: Current round number
        mana_per_turn: Mana regenerated per turn
        weather: Current weather condition (if any)
    """
    
    id: str
    player_id: str
    stage_id: str
    player_team: List[Hero]
    enemy_team: List[Enemy]
    
    state: BattleState = BattleState.IN_PROGRESS
    turn_number: int = 1
    mana_per_turn: int = 20
    
    weather: Optional[str] = None
    
    # Internal state
    _turn_order: Optional[TurnOrder] = field(default=None, init=False)
    _action_log: List[Dict[str, Any]] = field(default_factory=list, init=False)
    
    def calculate_turn_order(self) -> List[Character]:
        """
        Calculate and set turn order for the battle.
        
        Returns:
            List of characters in turn order
        """
        all_characters: List[Character] = list(self.player_team) + list(self.enemy_team)
        self._turn_order = TurnOrder(all_characters)
        return self._turn_order.get_order()
    
    def get_current_actor(self) -> Optional[Character]:
        """
        Get the character whose turn it currently is.
        
        Returns:
            Current acting character or None
        """
        if not self._turn_order:
            self.calculate_turn_order()
        return self._turn_order.get_current()
    
    def is_player_turn(self) -> bool:
        """
        Check if it's currently a player character's turn.
        
        Returns:
            True if player's turn, False if enemy's turn
        """
        current = self.get_current_actor()
        if not current:
            return False
        
        return any(h.id == current.id for h in self.player_team)
    
    def next_turn(self) -> None:
        """Advance to the next character's turn"""
        if not self._turn_order:
            self.calculate_turn_order()
        
        is_new_round = self._turn_order.advance()
        
        if is_new_round:
            self.turn_number += 1
            self._process_new_round()
    
    def _process_new_round(self) -> None:
        """Process effects at the start of a new round"""
        # Process status effects, regeneration, etc.
        for character in self.player_team + self.enemy_team:
            if character.is_alive:
                # Reduce skill cooldowns
                for skill_id in character.skills:
                    pass  # Would reduce cooldown if skill objects were attached
    
    def process_turn_start(self) -> None:
        """Process effects at the start of each turn"""
        # Generate mana for current actor
        current = self.get_current_actor()
        if current:
            current.gain_mana(self.mana_per_turn)
        
        # Process DOT/HOT effects
        # This will be expanded with status effect system
    
    def check_battle_end(self) -> Optional[BattleResult]:
        """
        Check if the battle has ended.
        
        Returns:
            BattleResult if battle ended, None if continues
        """
        player_alive = any(h.is_alive for h in self.player_team)
        enemy_alive = any(e.is_alive for e in self.enemy_team)
        
        if not enemy_alive:
            return BattleResult.VICTORY
        elif not player_alive:
            return BattleResult.DEFEAT
        
        return None
    
    def end_battle(self, result: BattleResult) -> None:
        """
        End the battle with a result.
        
        Args:
            result: The battle result
        """
        state_mapping = {
            BattleResult.VICTORY: BattleState.VICTORY,
            BattleResult.DEFEAT: BattleState.DEFEAT,
            BattleResult.RETREAT: BattleState.RETREAT
        }
        
        self.state = state_mapping.get(result, BattleState.DEFEAT)
    
    def is_ended(self) -> bool:
        """Check if the battle has ended"""
        return self.state in {BattleState.VICTORY, BattleState.DEFEAT, BattleState.RETREAT}
    
    def get_living_heroes(self) -> List[Hero]:
        """Get all living heroes"""
        return [h for h in self.player_team if h.is_alive]
    
    def get_living_enemies(self) -> List[Enemy]:
        """Get all living enemies"""
        return [e for e in self.enemy_team if e.is_alive]
    
    def get_character_by_id(self, character_id: str) -> Optional[Character]:
        """
        Find a character by ID from either team.
        
        Args:
            character_id: ID to search for
            
        Returns:
            Character if found, None otherwise
        """
        for character in self.player_team + self.enemy_team:
            if character.id == character_id:
                return character
        return None
    
    def log_action(self, action: Dict[str, Any]) -> None:
        """
        Log an action for battle history.
        
        Args:
            action: Action data to log
        """
        self._action_log.append({
            "turn": self.turn_number,
            "actor": self.get_current_actor().id if self.get_current_actor() else None,
            **action
        })
    
    def get_battle_state_snapshot(self) -> Dict[str, Any]:
        """
        Get a snapshot of the current battle state.
        
        Returns:
            Dictionary with current battle state
        """
        return {
            "battle_id": self.id,
            "turn_number": self.turn_number,
            "state": self.state.value,
            "current_actor_id": self.get_current_actor().id if self.get_current_actor() else None,
            "is_player_turn": self.is_player_turn(),
            "player_team": [
                {
                    "id": h.id,
                    "name": h.name,
                    "current_hp": h.current_hp,
                    "max_hp": h.stats.hp,
                    "current_mana": h.current_mana,
                    "is_alive": h.is_alive
                }
                for h in self.player_team
            ],
            "enemy_team": [
                {
                    "id": e.id,
                    "name": e.name,
                    "current_hp": e.current_hp,
                    "max_hp": e.stats.hp,
                    "current_mana": e.current_mana,
                    "is_alive": e.is_alive
                }
                for e in self.enemy_team
            ],
            "weather": self.weather
        }
