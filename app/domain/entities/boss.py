"""
Boss Entity - Powerful enemies with phases and special mechanics
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any, Set
from app.domain.entities.enemy import Enemy, EnemyBehavior
from app.domain.value_objects.element import Element
from app.domain.value_objects.hexagon_stats import HexagonStats
from app.domain.value_objects.grid_position import GridPosition


class MythicalTier(Enum):
    """Mythical boss tiers (Thiên Giới bosses)"""
    TU_LINH = "tu_linh"        # Tứ Linh (Four Spirits)
    THIEN_VUONG = "thien_vuong"  # Thiên Vương
    THUONG_CO = "thuong_co"    # Thượng Cổ (Ancient)
    HON_DON = "hon_don"        # Hỗn Độn (Chaos)


@dataclass
class BossPhase:
    """
    Represents a boss phase with HP threshold and modifiers.
    
    Attributes:
        phase_number: Phase index (1, 2, 3...)
        hp_threshold: HP percentage to trigger this phase (1.0 = 100%)
        name: Display name for the phase
        stat_modifiers: Multipliers for stats in this phase
        new_skills: Skills unlocked in this phase
        special_effects: Special effects active in this phase
    """
    phase_number: int
    hp_threshold: float  # 1.0 = 100%, 0.5 = 50%
    name: str = ""
    stat_modifiers: Dict[str, float] = field(default_factory=dict)
    new_skills: List[str] = field(default_factory=list)
    special_effects: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Boss(Enemy):
    """
    Boss entity - Powerful enemy with multiple phases.
    
    Extends Enemy with:
    - Title (e.g., "Võ Thánh", "Nghịch Thần")
    - Multiple phases with different behaviors
    - Mythical tier for Thiên Giới bosses
    - Immunities to certain effects
    - Special mechanics
    """
    
    title: str = ""
    phases: List[BossPhase] = field(default_factory=list)
    current_phase: int = 1
    mythical_tier: Optional[MythicalTier] = None
    special_mechanics: Dict[str, Any] = field(default_factory=dict)
    
    # Immunities
    _immunities: Set[str] = field(default_factory=lambda: {"instant_death", "charm"})
    
    def __post_init__(self) -> None:
        """Initialize boss-specific attributes"""
        super().__post_init__()
        
        # Bosses default to higher difficulty
        if self.difficulty == 1:
            self.difficulty = 5
        
        # Default behavior based on mythical tier
        if self.mythical_tier == MythicalTier.HON_DON:
            self.behavior = EnemyBehavior.BERSERKER
    
    def check_phase_transition(self) -> bool:
        """
        Check if boss should transition to next phase.
        
        Returns:
            True if phase transition occurred, False otherwise
        """
        if not self.phases:
            return False
        
        hp_percentage = self.current_hp / self.stats.hp
        
        # Find the appropriate phase for current HP
        for phase in sorted(self.phases, key=lambda p: p.hp_threshold, reverse=True):
            if hp_percentage <= phase.hp_threshold and phase.phase_number > self.current_phase:
                self._transition_to_phase(phase)
                return True
        
        return False
    
    def _transition_to_phase(self, new_phase: BossPhase) -> None:
        """
        Transition to a new phase.
        
        Args:
            new_phase: The phase to transition to
        """
        self.current_phase = new_phase.phase_number
        
        # Add new skills
        for skill_id in new_phase.new_skills:
            if skill_id not in self.skills:
                self.skills.append(skill_id)
    
    def get_current_phase(self) -> Optional[BossPhase]:
        """
        Get the current phase object.
        
        Returns:
            BossPhase or None if no phases defined
        """
        for phase in self.phases:
            if phase.phase_number == self.current_phase:
                return phase
        return None
    
    def get_effective_atk(self) -> int:
        """
        Get effective ATK including phase modifiers.
        
        Returns:
            Modified ATK value
        """
        base_atk = self.stats.atk
        current_phase = self.get_current_phase()
        
        if current_phase and "atk" in current_phase.stat_modifiers:
            return int(base_atk * current_phase.stat_modifiers["atk"])
        
        return base_atk
    
    def get_effective_spd(self) -> int:
        """
        Get effective SPD including phase modifiers.
        
        Returns:
            Modified SPD value
        """
        base_spd = self.stats.spd
        current_phase = self.get_current_phase()
        
        if current_phase and "spd" in current_phase.stat_modifiers:
            return int(base_spd * current_phase.stat_modifiers["spd"])
        
        return base_spd
    
    def get_power_rating(self) -> int:
        """
        Calculate boss power rating including mythical tier.
        
        Returns:
            Power rating as integer
        """
        base_power = super().get_power_rating()
        
        # Mythical tier multipliers
        tier_multipliers = {
            MythicalTier.TU_LINH: 2.0,
            MythicalTier.THIEN_VUONG: 3.0,
            MythicalTier.THUONG_CO: 4.0,
            MythicalTier.HON_DON: 5.0
        }
        
        if self.mythical_tier:
            return int(base_power * tier_multipliers.get(self.mythical_tier, 1.0))
        
        return base_power
    
    def is_immune_to(self, effect_type: str) -> bool:
        """
        Check if boss is immune to an effect type.
        
        Args:
            effect_type: The type of effect to check
            
        Returns:
            True if immune, False otherwise
        """
        return effect_type in self._immunities
    
    def add_immunity(self, effect_type: str) -> None:
        """
        Add an immunity to the boss.
        
        Args:
            effect_type: The effect type to become immune to
        """
        self._immunities.add(effect_type)
    
    def get_display_name(self) -> str:
        """
        Get full display name with title.
        
        Returns:
            Formatted display name
        """
        if self.title:
            return f"{self.name} - {self.title}"
        return self.name
