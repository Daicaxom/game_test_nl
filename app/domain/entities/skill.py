"""
Skill Entity - Base class for all skills
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, Any


class SkillType(Enum):
    """Types of skills"""
    DAMAGE = "damage"
    HEAL = "heal"
    BUFF = "buff"
    DEBUFF = "debuff"
    PASSIVE = "passive"
    ULTIMATE = "ultimate"


class TargetType(Enum):
    """Target types for skills"""
    SELF = "self"
    SINGLE_ALLY = "single_ally"
    SINGLE_ENEMY = "single_enemy"
    ALL_ALLIES = "all_allies"
    ALL_ENEMIES = "all_enemies"
    AOE = "aoe"  # Area of effect around a position


@dataclass
class Skill:
    """
    Base class for all skills.
    
    Attributes:
        id: Unique identifier
        name: Skill name
        description: Skill description
        mana_cost: Mana required to use
        cooldown: Number of turns before can use again
        current_cooldown: Current cooldown counter
        level: Skill level (1-10)
        max_level: Maximum skill level
    """
    
    id: str
    name: str
    description: str
    mana_cost: int
    cooldown: int
    current_cooldown: int = 0
    level: int = 1
    max_level: int = 10
    
    def is_ready(self) -> bool:
        """Check if skill is ready to use (not on cooldown)"""
        return self.current_cooldown == 0
    
    def trigger_cooldown(self) -> None:
        """Set skill on cooldown after use"""
        self.current_cooldown = self.cooldown
    
    def reduce_cooldown(self, amount: int = 1) -> None:
        """Reduce cooldown by amount (called at turn end)"""
        self.current_cooldown = max(0, self.current_cooldown - amount)
    
    def reset_cooldown(self) -> None:
        """Reset cooldown to 0"""
        self.current_cooldown = 0


@dataclass
class ActiveSkill(Skill):
    """
    Active skills that can be used in combat.
    
    Additional Attributes:
        skill_type: Type of skill (damage, heal, buff, debuff)
        target_type: Who can be targeted
        element: Optional element type for elemental damage
        damage_multiplier: Damage scaling (for damage skills)
        heal_multiplier: Heal scaling (for heal skills)
        buff_stats: Stats to buff (for buff skills)
        debuff_effects: Effects to apply (for debuff skills)
        aoe_range: Range for AOE skills
        duration: Effect duration in turns
    """
    
    skill_type: SkillType = SkillType.DAMAGE
    target_type: TargetType = TargetType.SINGLE_ENEMY
    element: Optional[Any] = None  # Element type from value_objects
    damage_multiplier: float = 1.0
    heal_multiplier: float = 0.0
    buff_stats: Dict[str, int] = field(default_factory=dict)
    debuff_effects: Dict[str, int] = field(default_factory=dict)
    aoe_range: int = 0
    duration: int = 0  # Effect duration in turns
    
    def get_effective_multiplier(self, level_bonus: float = 0.0) -> float:
        """Get effective damage/heal multiplier including level bonus"""
        if self.skill_type == SkillType.DAMAGE:
            return self.damage_multiplier + (self.level - 1) * 0.05 + level_bonus
        elif self.skill_type == SkillType.HEAL:
            return self.heal_multiplier + (self.level - 1) * 0.03 + level_bonus
        return 1.0


@dataclass
class PassiveSkill(Skill):
    """
    Passive skills that provide constant effects.
    
    Additional Attributes:
        trigger_condition: When the passive activates
        passive_effect: Effect when triggered
        stat_bonuses: Permanent stat bonuses
    """
    
    trigger_condition: str = "always"  # always, on_attack, on_hit, etc.
    passive_effect: Dict[str, Any] = field(default_factory=dict)
    stat_bonuses: Dict[str, int] = field(default_factory=dict)
    
    def __post_init__(self) -> None:
        """Override mana_cost and cooldown for passives"""
        self.mana_cost = 0
        self.cooldown = 0


@dataclass
class UltimateSkill(ActiveSkill):
    """
    Ultimate skills with special animations and effects.
    
    Additional Attributes:
        ultimate_gauge_cost: Ultimate gauge required (usually 100%)
        animation_id: Special animation identifier
    """
    
    ultimate_gauge_cost: int = 100
    animation_id: str = ""
    
    def __post_init__(self) -> None:
        """Set skill type to ultimate"""
        self.skill_type = SkillType.ULTIMATE
