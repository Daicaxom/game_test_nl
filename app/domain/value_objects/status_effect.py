"""
StatusEffect Value Object
Represents buffs, debuffs, and other status effects in combat
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, Optional


class StatusEffectType(Enum):
    """Types of status effects"""
    BUFF = "buff"               # Positive stat modification
    DEBUFF = "debuff"           # Negative stat modification
    DOT = "dot"                 # Damage over time
    HOT = "hot"                 # Heal over time
    CROWD_CONTROL = "cc"        # Stun, freeze, etc.
    SHIELD = "shield"           # Damage absorption


@dataclass
class StatusEffect:
    """
    Status effect that can be applied to characters.
    
    Attributes:
        id: Unique identifier
        name: Display name
        effect_type: Type of effect (buff, debuff, etc.)
        duration: Remaining turns
        stat_modifiers: Dict of stat name to modifier (e.g., {"atk": 0.2} for 20% increase)
        damage_per_turn: Damage dealt per turn (for DOT)
        heal_per_turn: Healing per turn (for HOT)
        prevents_action: Whether this effect prevents actions (for CC)
        shield_amount: Damage absorption amount (for shields)
        is_stackable: Whether multiple instances can stack
        max_stacks: Maximum number of stacks
        current_stacks: Current number of stacks
    """
    
    id: str
    name: str
    effect_type: StatusEffectType
    duration: int
    
    # Stat modifiers
    stat_modifiers: Dict[str, float] = field(default_factory=dict)
    
    # DOT/HOT values
    damage_per_turn: int = 0
    heal_per_turn: int = 0
    
    # Crowd control
    prevents_action: bool = False
    
    # Shield
    shield_amount: int = 0
    
    # Stacking
    is_stackable: bool = False
    max_stacks: int = 1
    current_stacks: int = 1
    
    # Metadata
    source_id: Optional[str] = None  # ID of the character who applied this
    icon: Optional[str] = None
    description: Optional[str] = None
    
    def reduce_duration(self) -> None:
        """Reduce duration by 1 turn"""
        self.duration = max(0, self.duration - 1)
    
    def is_expired(self) -> bool:
        """Check if effect has expired (duration = 0)"""
        return self.duration <= 0
    
    def is_positive(self) -> bool:
        """Check if this is a positive effect for the target"""
        positive_types = {StatusEffectType.BUFF, StatusEffectType.HOT, StatusEffectType.SHIELD}
        return self.effect_type in positive_types
    
    def add_stack(self) -> bool:
        """
        Add a stack to this effect.
        
        Returns:
            True if stack was added, False if at max stacks
        """
        if not self.is_stackable:
            return False
        
        if self.current_stacks < self.max_stacks:
            self.current_stacks += 1
            return True
        
        return False
    
    def refresh(self, new_duration: int) -> None:
        """
        Refresh the effect with a new duration.
        
        Args:
            new_duration: New duration value
        """
        self.duration = new_duration
    
    def get_tick_damage(self) -> int:
        """
        Get DOT damage for this tick, accounting for stacks.
        
        Returns:
            Total damage for this tick
        """
        if self.effect_type != StatusEffectType.DOT:
            return 0
        return self.damage_per_turn * self.current_stacks
    
    def get_tick_heal(self) -> int:
        """
        Get HOT heal for this tick, accounting for stacks.
        
        Returns:
            Total heal for this tick
        """
        if self.effect_type != StatusEffectType.HOT:
            return 0
        return self.heal_per_turn * self.current_stacks
    
    def get_stat_modifier(self, stat_name: str) -> float:
        """
        Get the modifier for a specific stat, accounting for stacks.
        
        Args:
            stat_name: Name of the stat (e.g., "atk", "def_")
            
        Returns:
            Total modifier for the stat
        """
        base_modifier = self.stat_modifiers.get(stat_name, 0)
        return base_modifier * self.current_stacks if self.is_stackable else base_modifier
    
    def absorb_damage(self, damage: int) -> tuple[int, int]:
        """
        Absorb damage with shield (for shield effects).
        
        Args:
            damage: Incoming damage amount
            
        Returns:
            Tuple of (remaining_shield, damage_passed_through)
        """
        if self.effect_type != StatusEffectType.SHIELD:
            return 0, damage
        
        absorbed = min(self.shield_amount, damage)
        self.shield_amount -= absorbed
        remaining_damage = damage - absorbed
        
        return self.shield_amount, remaining_damage
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "effect_type": self.effect_type.value,
            "duration": self.duration,
            "current_stacks": self.current_stacks,
            "prevents_action": self.prevents_action,
            "is_positive": self.is_positive()
        }
