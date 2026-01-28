"""
Character Entity - Base class for all characters
"""
from dataclasses import dataclass, field
from typing import List, Optional
from app.domain.value_objects.element import Element
from app.domain.value_objects.hexagon_stats import HexagonStats
from app.domain.value_objects.grid_position import GridPosition


@dataclass
class DamageResult:
    """Result of taking damage"""
    damage_taken: int
    is_dead: bool


@dataclass
class HealResult:
    """Result of healing"""
    actual_heal: int


@dataclass
class Character:
    """
    Base class for all characters (heroes, enemies, bosses).
    
    Attributes:
        id: Unique identifier
        name: Character name
        element: Ngũ Hành element
        position: Grid position (3x3)
        stats: Hexagon stats
        current_hp: Current hit points
        current_mana: Current mana points
        max_mana: Maximum mana points
        skills: List of skill IDs
        status_effects: List of active status effects
    """
    
    id: str
    name: str
    element: Element
    position: GridPosition
    stats: HexagonStats
    current_hp: int = field(init=False)
    current_mana: int = field(default=0)
    max_mana: int = field(default=100)
    skills: List[str] = field(default_factory=list)
    status_effects: List[str] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        """Initialize current HP to max HP from stats"""
        self.current_hp = self.stats.hp
    
    def take_damage(self, damage: int) -> DamageResult:
        """
        Take damage and reduce current HP.
        
        Args:
            damage: Amount of damage to take
            
        Returns:
            DamageResult with damage taken and death status
        """
        actual_damage = min(damage, self.current_hp)
        self.current_hp = max(0, self.current_hp - damage)
        
        return DamageResult(
            damage_taken=actual_damage,
            is_dead=self.current_hp <= 0
        )
    
    def heal(self, amount: int) -> HealResult:
        """
        Heal and increase current HP.
        
        Args:
            amount: Amount to heal
            
        Returns:
            HealResult with actual heal amount
        """
        max_hp = self.stats.hp
        actual_heal = min(amount, max_hp - self.current_hp)
        self.current_hp = min(max_hp, self.current_hp + amount)
        
        return HealResult(actual_heal=actual_heal)
    
    def gain_mana(self, amount: int) -> None:
        """
        Gain mana points.
        
        Args:
            amount: Amount of mana to gain
        """
        self.current_mana = min(self.max_mana, self.current_mana + amount)
    
    def use_mana(self, amount: int) -> None:
        """
        Use mana points.
        
        Args:
            amount: Amount of mana to use
            
        Raises:
            ValueError: If insufficient mana
        """
        if amount > self.current_mana:
            raise ValueError(f"Insufficient mana: have {self.current_mana}, need {amount}")
        self.current_mana -= amount
    
    def can_act(self) -> bool:
        """
        Check if character can perform actions.
        
        Returns:
            True if no disabling status effects
        """
        disabling_effects = {"stun", "freeze", "sleep"}
        return not any(effect in disabling_effects for effect in self.status_effects)
    
    @property
    def is_alive(self) -> bool:
        """Check if character is alive (HP > 0)"""
        return self.current_hp > 0
    
    def get_effective_stats(self) -> HexagonStats:
        """
        Calculate effective stats including buffs/debuffs.
        
        Returns:
            HexagonStats with all modifiers applied
        """
        # For now, just return base stats
        # TODO: Apply equipment and status effect modifiers
        return self.stats
