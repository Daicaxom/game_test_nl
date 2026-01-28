"""
Mount Entity - Chiến mã và Linh thú
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any

from app.domain.value_objects.element import Element
from app.domain.value_objects.hexagon_stats import HexagonStats


class MountType(Enum):
    """Types of mounts"""
    HORSE = "horse"
    DRAGON = "dragon"
    MYTHICAL = "mythical"


@dataclass
class EvolutionStage:
    """
    Evolution stage for dragons.
    
    Attributes:
        stage: Stage number (0, 1, 2, ...)
        name: Stage name (e.g., "Hỏa Long Ấu Thể")
        level_req: Level requirement for this stage
        stat_bonus: Additional stats at this stage
    """
    stage: int
    name: str
    level_req: int
    stat_bonus: Dict[str, int] = field(default_factory=dict)


@dataclass
class Mount:
    """
    Mount entity - Chiến mã.
    
    Attributes:
        id: Unique identifier
        name: Mount name
        mount_type: Type (horse, dragon, mythical)
        rarity: Rarity level (1-5)
        level: Current level
        exp: Experience points
        bond_level: Bond with rider (1-10)
        bond_points: Points toward next bond level
        team_bonus: Team-wide stat bonuses
    """
    
    id: str
    name: str
    mount_type: MountType = MountType.HORSE
    rarity: int = 3
    
    level: int = 1
    exp: int = 0
    bond_level: int = 1
    bond_points: int = 0
    
    # Base stats
    base_hp: int = 0
    base_atk: int = 0
    base_def: int = 0
    base_spd: int = 0
    base_crit: int = 0
    base_dex: int = 0
    
    # Team bonus
    team_bonus: Dict[str, int] = field(default_factory=dict)
    
    # Equipment slots for mount
    equipment_slots: List[str] = field(default_factory=list)
    
    # Metadata
    template_id: str = ""
    description: str = ""
    
    # Level scaling factor
    _level_scale: float = 0.1  # 10% per level
    _bond_scale: float = 0.05  # 5% per bond level
    
    def get_stats(self) -> HexagonStats:
        """
        Get mount stats including level and bond bonuses.
        
        Returns:
            HexagonStats with all modifiers applied
        """
        level_multiplier = 1 + (self.level - 1) * self._level_scale
        bond_multiplier = 1 + (self.bond_level - 1) * self._bond_scale
        total_multiplier = level_multiplier * bond_multiplier
        
        return HexagonStats(
            hp=int(self.base_hp * total_multiplier),
            atk=int(self.base_atk * total_multiplier),
            def_=int(self.base_def * total_multiplier),
            spd=int(self.base_spd * total_multiplier),
            crit=int(self.base_crit * total_multiplier),
            dex=int(self.base_dex * total_multiplier)
        )
    
    def get_team_bonus(self) -> Dict[str, int]:
        """
        Get team-wide bonus stats including level scaling.
        
        Returns:
            Dictionary of stat bonuses
        """
        level_multiplier = 1 + (self.level - 1) * 0.05  # 5% per level
        
        return {
            stat: int(value * level_multiplier)
            for stat, value in self.team_bonus.items()
        }
    
    def add_bond_points(self, points: int) -> bool:
        """
        Add bond points and potentially increase bond level.
        
        Args:
            points: Points to add
            
        Returns:
            True if bond level increased
        """
        self.bond_points += points
        leveled_up = False
        
        # Points needed per level increases
        required = self.bond_level * 500
        
        while self.bond_points >= required and self.bond_level < 10:
            self.bond_points -= required
            self.bond_level += 1
            leveled_up = True
            required = self.bond_level * 500
        
        # Cap at level 10
        if self.bond_level >= 10:
            self.bond_level = 10
            self.bond_points = 0
        
        return leveled_up
    
    def gain_exp(self, amount: int) -> bool:
        """
        Gain experience points and potentially level up.
        
        Args:
            amount: EXP to gain
            
        Returns:
            True if leveled up
        """
        self.exp += amount
        leveled_up = False
        
        required = self._get_required_exp()
        
        while self.exp >= required:
            self.exp -= required
            self.level += 1
            leveled_up = True
            required = self._get_required_exp()
        
        return leveled_up
    
    def _get_required_exp(self) -> int:
        """Get EXP required for next level"""
        return 100 + (self.level * 50)
    
    def get_power_rating(self) -> int:
        """
        Calculate mount power rating.
        
        Returns:
            Power rating
        """
        stats = self.get_stats()
        base_power = stats.get_total_power()
        
        # Rarity multiplier
        rarity_multiplier = 1 + (self.rarity - 1) * 0.3
        
        return int(base_power * rarity_multiplier)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "mount_type": self.mount_type.value,
            "rarity": self.rarity,
            "level": self.level,
            "bond_level": self.bond_level,
            "stats": self.get_stats().to_dict(),
            "team_bonus": self.get_team_bonus(),
            "power": self.get_power_rating()
        }


@dataclass
class DragonCompanion(Mount):
    """
    Dragon companion - Special mount with element and evolution.
    
    Extends Mount with:
    - Element affinity
    - Evolution system
    - Element-based team buffs
    """
    
    element: Element = Element.HOA
    evolution_stage: int = 0
    awakening_level: int = 0
    evolution_stages: List[EvolutionStage] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        """Set mount type to dragon"""
        object.__setattr__(self, 'mount_type', MountType.DRAGON)
    
    def get_element_buff(self) -> Dict[str, float]:
        """
        Get element-based buff for team.
        
        Returns:
            Dictionary of element buffs
        """
        element_name = self.element.value.lower()
        base_buff = 0.1 + (self.awakening_level * 0.05)
        
        return {
            f"{element_name}_damage": base_buff,
            f"{element_name}_resistance": base_buff + 0.05
        }
    
    def get_stats(self) -> HexagonStats:
        """
        Get dragon stats including evolution bonuses.
        
        Returns:
            HexagonStats with all modifiers
        """
        base_stats = super().get_stats()
        
        # Add evolution stage bonuses
        current_stage = self.get_current_evolution_stage()
        if current_stage and current_stage.stat_bonus:
            return HexagonStats(
                hp=base_stats.hp + current_stage.stat_bonus.get("hp", 0),
                atk=base_stats.atk + current_stage.stat_bonus.get("atk", 0),
                def_=base_stats.def_ + current_stage.stat_bonus.get("def_", 0),
                spd=base_stats.spd + current_stage.stat_bonus.get("spd", 0),
                crit=base_stats.crit + current_stage.stat_bonus.get("crit", 0),
                dex=base_stats.dex + current_stage.stat_bonus.get("dex", 0)
            )
        
        return base_stats
    
    def get_current_evolution_stage(self) -> Optional[EvolutionStage]:
        """Get current evolution stage object"""
        for stage in self.evolution_stages:
            if stage.stage == self.evolution_stage:
                return stage
        return None
    
    def get_next_evolution_stage(self) -> Optional[EvolutionStage]:
        """Get next evolution stage object"""
        for stage in self.evolution_stages:
            if stage.stage == self.evolution_stage + 1:
                return stage
        return None
    
    def can_evolve(self) -> bool:
        """
        Check if dragon can evolve.
        
        Returns:
            True if evolution is possible
        """
        next_stage = self.get_next_evolution_stage()
        if not next_stage:
            return False
        
        return self.level >= next_stage.level_req
    
    def evolve(self) -> bool:
        """
        Evolve the dragon to next stage.
        
        Returns:
            True if evolution successful
        """
        if not self.can_evolve():
            return False
        
        self.evolution_stage += 1
        return True
    
    def get_team_bonus(self) -> Dict[str, Any]:
        """
        Get team bonus including element buff.
        
        Returns:
            Combined team and element bonuses
        """
        base_bonus = super().get_team_bonus()
        element_buff = self.get_element_buff()
        
        return {**base_bonus, **element_buff}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        base_dict = super().to_dict()
        base_dict.update({
            "element": self.element.value,
            "evolution_stage": self.evolution_stage,
            "awakening_level": self.awakening_level,
            "element_buff": self.get_element_buff()
        })
        return base_dict
