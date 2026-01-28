"""
Enemy Entity - Non-player controlled combat units
"""
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any
from app.domain.entities.character import Character
from app.domain.value_objects.element import Element
from app.domain.value_objects.hexagon_stats import HexagonStats
from app.domain.value_objects.grid_position import GridPosition


class EnemyBehavior(Enum):
    """AI behavior patterns for enemies"""
    AGGRESSIVE = "aggressive"   # Prioritizes attacking
    DEFENSIVE = "defensive"     # Prioritizes defense/healing
    BALANCED = "balanced"       # Mixed approach
    SUPPORT = "support"         # Focuses on buffing allies
    BERSERKER = "berserker"     # More aggressive at low HP


@dataclass
class Enemy(Character):
    """
    Enemy entity - AI-controlled combat unit.
    
    Extends Character with:
    - AI behavior patterns
    - Rewards (EXP, gold, drops)
    - Difficulty level
    """
    
    template_id: str = ""
    behavior: EnemyBehavior = EnemyBehavior.BALANCED
    difficulty: int = 1  # 1-10 difficulty rating
    
    # Rewards
    exp_reward: int = 0
    gold_reward: int = 0
    drop_table: List[Dict[str, Any]] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        """Initialize enemy-specific attributes"""
        super().__post_init__()
    
    def get_power_rating(self) -> int:
        """
        Calculate enemy power rating based on stats and difficulty.
        
        Returns:
            Power rating as integer
        """
        base_power = self.stats.get_total_power()
        difficulty_multiplier = 1 + (self.difficulty - 1) * 0.2
        return int(base_power * difficulty_multiplier)
    
    def select_action(self, battle_state: Any) -> "EnemyAction":
        """
        Select an action based on AI behavior and battle state.
        
        Args:
            battle_state: Current state of the battle
            
        Returns:
            EnemyAction describing what the enemy will do
        """
        # Default implementation - will be enhanced by AI service
        return EnemyAction(
            action_type="attack",
            target_selection="lowest_hp"
        )
    
    def should_use_skill(self) -> bool:
        """
        Determine if enemy should use a skill this turn.
        
        Returns:
            True if should use skill, False for basic attack
        """
        if not self.skills or self.current_mana < 50:
            return False
        
        # Behavior-based skill usage probability
        skill_chance = {
            EnemyBehavior.AGGRESSIVE: 0.6,
            EnemyBehavior.DEFENSIVE: 0.4,
            EnemyBehavior.BALANCED: 0.5,
            EnemyBehavior.SUPPORT: 0.7,
            EnemyBehavior.BERSERKER: 0.3
        }
        
        return random.random() < skill_chance.get(self.behavior, 0.5)


@dataclass
class EnemyAction:
    """Represents an action chosen by an enemy AI"""
    action_type: str  # "attack", "skill", "move"
    target_selection: str = "lowest_hp"  # targeting strategy
    skill_id: Optional[str] = None
    destination: Optional[GridPosition] = None
