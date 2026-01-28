"""
Equipment Entity - Weapons, Armor, Accessories, Relics
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, Any

from app.domain.value_objects.hexagon_stats import HexagonStats


class EquipmentType(Enum):
    """Types of equipment"""
    WEAPON = "weapon"
    ARMOR = "armor"
    ACCESSORY = "accessory"
    RELIC = "relic"


class Rarity(Enum):
    """Equipment rarity levels"""
    COMMON = "common"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    MYTHIC = "mythic"


@dataclass
class EnhanceResult:
    """Result of enhancement attempt"""
    success: bool
    new_level: int
    stats_gained: Optional[HexagonStats] = None


@dataclass
class Equipment:
    """
    Equipment entity that can be equipped by heroes.
    
    Attributes:
        id: Unique identifier
        name: Equipment name
        equipment_type: Type (weapon, armor, accessory, relic)
        rarity: Rarity level
        level: Enhancement level
        base_*: Base stat values
        bonus_*: Bonus stats from enhancement
        set_id: Equipment set identifier (if part of a set)
        unique_effect: Special effect (for legendary+)
        required_level: Minimum hero level to equip
        required_element: Required element (if any)
    """
    
    id: str
    name: str
    equipment_type: EquipmentType
    rarity: Rarity
    
    # Base stats
    base_hp: int = 0
    base_atk: int = 0
    base_def: int = 0
    base_spd: int = 0
    base_crit: int = 0
    base_dex: int = 0
    
    # Bonus stats from enhancement
    bonus_hp: int = 0
    bonus_atk: int = 0
    bonus_def: int = 0
    bonus_spd: int = 0
    bonus_crit: int = 0
    bonus_dex: int = 0
    
    # Enhancement level
    level: int = 1
    
    # Set and effects
    set_id: Optional[str] = None
    unique_effect: Optional[Dict[str, Any]] = None
    
    # Requirements
    required_level: int = 1
    required_element: Optional[str] = None
    
    # Metadata
    is_locked: bool = False
    equipped_by: Optional[str] = None  # Hero ID if equipped
    
    # Max levels by rarity
    _max_levels: Dict[Rarity, int] = field(default_factory=lambda: {
        Rarity.COMMON: 10,
        Rarity.RARE: 15,
        Rarity.EPIC: 20,
        Rarity.LEGENDARY: 25,
        Rarity.MYTHIC: 30
    })
    
    def get_max_level(self) -> int:
        """Get maximum enhancement level based on rarity"""
        return self._max_levels.get(self.rarity, 10)
    
    def can_enhance(self) -> bool:
        """Check if equipment can be enhanced"""
        return self.level < self.get_max_level()
    
    def enhance(self) -> EnhanceResult:
        """
        Enhance equipment by 1 level.
        
        Returns:
            EnhanceResult with success status and new stats
        """
        if not self.can_enhance():
            return EnhanceResult(success=False, new_level=self.level)
        
        self.level += 1
        
        # Calculate stat gains (10% of base per level)
        stat_gain_multiplier = 0.1
        
        hp_gain = int(self.base_hp * stat_gain_multiplier)
        atk_gain = int(self.base_atk * stat_gain_multiplier)
        def_gain = int(self.base_def * stat_gain_multiplier)
        spd_gain = int(self.base_spd * stat_gain_multiplier)
        crit_gain = int(self.base_crit * stat_gain_multiplier)
        dex_gain = int(self.base_dex * stat_gain_multiplier)
        
        self.bonus_hp += hp_gain
        self.bonus_atk += atk_gain
        self.bonus_def += def_gain
        self.bonus_spd += spd_gain
        self.bonus_crit += crit_gain
        self.bonus_dex += dex_gain
        
        stats_gained = HexagonStats(
            hp=hp_gain,
            atk=atk_gain,
            def_=def_gain,
            spd=spd_gain,
            crit=crit_gain,
            dex=dex_gain
        )
        
        return EnhanceResult(
            success=True,
            new_level=self.level,
            stats_gained=stats_gained
        )
    
    def get_total_stats(self) -> HexagonStats:
        """
        Get total stats including base and bonus.
        
        Returns:
            HexagonStats with combined values
        """
        return HexagonStats(
            hp=self.base_hp + self.bonus_hp,
            atk=self.base_atk + self.bonus_atk,
            def_=self.base_def + self.bonus_def,
            spd=self.base_spd + self.bonus_spd,
            crit=self.base_crit + self.bonus_crit,
            dex=self.base_dex + self.bonus_dex
        )
    
    def get_power_rating(self) -> int:
        """Calculate equipment power rating"""
        stats = self.get_total_stats()
        base_power = stats.get_total_power()
        
        # Rarity multiplier
        rarity_multiplier = {
            Rarity.COMMON: 1.0,
            Rarity.RARE: 1.2,
            Rarity.EPIC: 1.5,
            Rarity.LEGENDARY: 2.0,
            Rarity.MYTHIC: 2.5
        }
        
        return int(base_power * rarity_multiplier.get(self.rarity, 1.0))
