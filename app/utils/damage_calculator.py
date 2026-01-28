"""
Damage Calculator Utility
Implements game damage formula as per design doc
"""
import random
from typing import List, Dict, Any
from app.domain.value_objects.element import Element
from app.domain.value_objects.hexagon_stats import HexagonStats


class DamageCalculator:
    """
    Calculator for battle damage, healing, and turn order.
    
    Damage Formula:
        damage = (ATK * skill_multiplier - DEF * 0.5) * element_multiplier * crit_multiplier
    """
    
    DEF_REDUCTION_FACTOR = 0.5
    MIN_DAMAGE = 1
    
    def calculate_damage(
        self,
        attacker_stats: HexagonStats,
        defender_stats: HexagonStats,
        skill_multiplier: float = 1.0,
        attacker_element: Element = Element.KIM,
        defender_element: Element = Element.KIM,
        is_crit: bool = False
    ) -> int:
        """
        Calculate damage dealt.
        
        Args:
            attacker_stats: Attacker's stats
            defender_stats: Defender's stats
            skill_multiplier: Skill damage multiplier
            attacker_element: Attacker's element
            defender_element: Defender's element
            is_crit: Whether this is a critical hit
            
        Returns:
            Final damage amount (minimum 1)
        """
        # Base damage calculation
        base_damage = (
            attacker_stats.atk * skill_multiplier 
            - defender_stats.def_ * self.DEF_REDUCTION_FACTOR
        )
        
        # Element multiplier
        element_multiplier = attacker_element.calculate_multiplier(defender_element)
        
        # Apply element multiplier
        damage = base_damage * element_multiplier
        
        # Critical hit multiplier
        if is_crit:
            crit_multiplier = 1 + (attacker_stats.crit / 100)
            damage *= crit_multiplier
        
        # Ensure minimum damage
        return max(self.MIN_DAMAGE, int(damage))
    
    def calculate_heal(
        self,
        target_max_hp: int,
        heal_multiplier: float = 0.3
    ) -> int:
        """
        Calculate heal amount based on target's max HP.
        
        Args:
            target_max_hp: Target's maximum HP
            heal_multiplier: Percentage of max HP to heal
            
        Returns:
            Heal amount
        """
        return int(target_max_hp * heal_multiplier)
    
    def calculate_heal_from_atk(
        self,
        caster_atk: int,
        heal_multiplier: float = 1.0
    ) -> int:
        """
        Calculate heal amount based on caster's ATK.
        
        Args:
            caster_atk: Caster's ATK stat
            heal_multiplier: Multiplier for ATK-based healing
            
        Returns:
            Heal amount
        """
        return int(caster_atk * heal_multiplier)
    
    def calculate_turn_order(
        self,
        characters: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Calculate turn order based on SPD stat.
        Higher SPD goes first.
        
        Args:
            characters: List of character dicts with 'id' and 'spd' keys
            
        Returns:
            Sorted list (highest SPD first)
        """
        return sorted(
            characters,
            key=lambda c: c.get("spd", 0),
            reverse=True
        )
    
    def get_crit_chance(self, crit_stat: int) -> float:
        """
        Get critical hit chance based on CRIT stat.
        
        Args:
            crit_stat: Character's CRIT stat
            
        Returns:
            Probability of critical hit (0.0 to 1.0)
        """
        # Base chance is CRIT/100, capped at 100%
        chance = min(1.0, crit_stat / 100)
        return max(0.0, chance)
    
    def roll_crit(self, crit_stat: int) -> bool:
        """
        Roll for critical hit.
        
        Args:
            crit_stat: Character's CRIT stat
            
        Returns:
            True if critical hit, False otherwise
        """
        chance = self.get_crit_chance(crit_stat)
        return random.random() < chance
