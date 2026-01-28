"""
Hero Entity - Player-controlled character
"""
from dataclasses import dataclass, field
from typing import Optional, Dict
from app.domain.entities.character import Character
from app.domain.value_objects.element import Element
from app.domain.value_objects.hexagon_stats import HexagonStats
from app.domain.value_objects.grid_position import GridPosition


@dataclass
class LevelUpResult:
    """Result of gaining experience"""
    leveled_up: bool
    old_level: int
    new_level: int
    exp_remaining: int


@dataclass
class Hero(Character):
    """
    Hero entity - player-controlled character.
    
    Extends Character with progression systems:
    - Level and EXP
    - Stars (rarity upgrade)
    - Ascension
    - Awakening
    - Equipment
    - Mount
    """
    
    template_id: str = ""
    rarity: int = 1  # Base rarity 1-6
    level: int = 1
    exp: int = 0
    stars: int = 1  # Current star level
    ascension_level: int = 0  # 0-6
    awakening_level: int = 0  # 0-6
    
    # Equipment slots (None means empty)
    weapon_id: Optional[str] = None
    armor_id: Optional[str] = None
    accessory_id: Optional[str] = None
    relic_id: Optional[str] = None
    
    # Mount
    mount_id: Optional[str] = None
    
    # Growth rates for stat calculation
    growth_rates: Dict[str, float] = field(default_factory=dict)
    
    # Metadata
    is_locked: bool = False
    is_favorite: bool = False
    
    # EXP required for each level (can be customized)
    _exp_table: Dict[int, int] = field(default_factory=lambda: {
        1: 100, 2: 150, 3: 200, 4: 250, 5: 300,
        6: 400, 7: 500, 8: 600, 9: 700, 10: 800
    })
    
    def __post_init__(self) -> None:
        """Initialize hero-specific attributes"""
        super().__post_init__()
    
    def get_required_exp(self, level: int) -> int:
        """Get EXP required to reach next level from current level"""
        if level in self._exp_table:
            return self._exp_table[level]
        # Default formula for levels not in table
        return 100 + (level * 50)
    
    def gain_exp(self, amount: int) -> LevelUpResult:
        """
        Gain experience points and potentially level up.
        
        Args:
            amount: Amount of EXP to gain
            
        Returns:
            LevelUpResult with level up information
        """
        old_level = self.level
        self.exp += amount
        leveled_up = False
        
        # Check for level ups
        while self.exp >= self.get_required_exp(self.level):
            self.exp -= self.get_required_exp(self.level)
            self.level += 1
            leveled_up = True
            self._apply_level_up_stats()
        
        return LevelUpResult(
            leveled_up=leveled_up,
            old_level=old_level,
            new_level=self.level,
            exp_remaining=self.exp
        )
    
    def _apply_level_up_stats(self) -> None:
        """Apply stat increases from leveling up"""
        if not self.growth_rates:
            return
        
        # Apply growth rates to stats
        # This will be handled by a stat calculator service
        pass
    
    def get_max_level(self) -> int:
        """Get maximum level based on ascension level"""
        base_max = 20
        ascension_bonus = self.ascension_level * 10
        return base_max + ascension_bonus
    
    def can_ascend(self) -> bool:
        """Check if hero can be ascended"""
        if self.ascension_level >= 6:
            return False
        required_level = self.get_ascension_level_requirement()
        return self.level >= required_level
    
    def get_ascension_level_requirement(self) -> int:
        """Get level required for next ascension"""
        requirements = {0: 20, 1: 30, 2: 40, 3: 50, 4: 60, 5: 70}
        return requirements.get(self.ascension_level, 80)
    
    def get_total_power(self) -> int:
        """Calculate total power rating"""
        base_power = self.stats.get_total_power()
        level_multiplier = 1 + (self.level - 1) * 0.05
        star_multiplier = 1 + (self.stars - 1) * 0.2
        ascension_bonus = self.ascension_level * 100
        awakening_bonus = self.awakening_level * 150
        
        return int(base_power * level_multiplier * star_multiplier) + ascension_bonus + awakening_bonus
