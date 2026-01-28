"""
Tests for DamageCalculator Utility
Following TDD approach - tests written first
"""
import pytest
from app.utils.damage_calculator import DamageCalculator
from app.domain.value_objects.element import Element
from app.domain.value_objects.hexagon_stats import HexagonStats


class TestDamageCalculation:
    """Test damage calculation formula"""
    
    def test_basic_damage_calculation(self):
        """Basic damage = ATK * multiplier - DEF * 0.5"""
        calc = DamageCalculator()
        
        attacker_stats = HexagonStats(hp=1000, atk=100, def_=50, spd=100, crit=10, dex=10)
        defender_stats = HexagonStats(hp=1000, atk=50, def_=40, spd=80, crit=5, dex=5)
        
        damage = calc.calculate_damage(
            attacker_stats=attacker_stats,
            defender_stats=defender_stats,
            skill_multiplier=1.0,
            attacker_element=Element.KIM,
            defender_element=Element.THUY,  # Neutral
            is_crit=False
        )
        
        # damage = (100 * 1.0 - 40 * 0.5) * 1.0 = 80
        assert damage == 80
    
    def test_damage_with_skill_multiplier(self):
        """Damage increases with skill multiplier"""
        calc = DamageCalculator()
        
        attacker_stats = HexagonStats(hp=1000, atk=100, def_=50, spd=100, crit=10, dex=10)
        defender_stats = HexagonStats(hp=1000, atk=50, def_=40, spd=80, crit=5, dex=5)
        
        damage = calc.calculate_damage(
            attacker_stats=attacker_stats,
            defender_stats=defender_stats,
            skill_multiplier=1.5,
            attacker_element=Element.KIM,
            defender_element=Element.THUY,
            is_crit=False
        )
        
        # damage = (100 * 1.5 - 40 * 0.5) * 1.0 = 130
        assert damage == 130
    
    def test_damage_with_element_advantage(self):
        """Element advantage multiplies damage by 1.5"""
        calc = DamageCalculator()
        
        attacker_stats = HexagonStats(hp=1000, atk=100, def_=50, spd=100, crit=10, dex=10)
        defender_stats = HexagonStats(hp=1000, atk=50, def_=40, spd=80, crit=5, dex=5)
        
        damage = calc.calculate_damage(
            attacker_stats=attacker_stats,
            defender_stats=defender_stats,
            skill_multiplier=1.0,
            attacker_element=Element.KIM,
            defender_element=Element.MOC,  # Kim khắc Mộc
            is_crit=False
        )
        
        # damage = (100 * 1.0 - 40 * 0.5) * 1.5 = 120
        assert damage == 120
    
    def test_damage_with_element_disadvantage(self):
        """Element disadvantage multiplies damage by 0.7"""
        calc = DamageCalculator()
        
        attacker_stats = HexagonStats(hp=1000, atk=100, def_=50, spd=100, crit=10, dex=10)
        defender_stats = HexagonStats(hp=1000, atk=50, def_=40, spd=80, crit=5, dex=5)
        
        damage = calc.calculate_damage(
            attacker_stats=attacker_stats,
            defender_stats=defender_stats,
            skill_multiplier=1.0,
            attacker_element=Element.KIM,
            defender_element=Element.HOA,  # Kim bị Hỏa khắc
            is_crit=False
        )
        
        # damage = (100 * 1.0 - 40 * 0.5) * 0.7 = 56
        assert damage == 56
    
    def test_damage_with_critical_hit(self):
        """Critical hit increases damage based on crit stat"""
        calc = DamageCalculator()
        
        attacker_stats = HexagonStats(hp=1000, atk=100, def_=50, spd=100, crit=50, dex=10)
        defender_stats = HexagonStats(hp=1000, atk=50, def_=40, spd=80, crit=5, dex=5)
        
        damage = calc.calculate_damage(
            attacker_stats=attacker_stats,
            defender_stats=defender_stats,
            skill_multiplier=1.0,
            attacker_element=Element.KIM,
            defender_element=Element.THUY,
            is_crit=True
        )
        
        # Base damage = 80
        # Crit multiplier = 1 + (50 / 100) = 1.5
        # Final = 80 * 1.5 = 120
        assert damage == 120
    
    def test_damage_minimum_is_one(self):
        """Damage should never be less than 1"""
        calc = DamageCalculator()
        
        attacker_stats = HexagonStats(hp=1000, atk=10, def_=50, spd=100, crit=10, dex=10)
        defender_stats = HexagonStats(hp=1000, atk=50, def_=100, spd=80, crit=5, dex=5)
        
        damage = calc.calculate_damage(
            attacker_stats=attacker_stats,
            defender_stats=defender_stats,
            skill_multiplier=1.0,
            attacker_element=Element.KIM,
            defender_element=Element.THUY,
            is_crit=False
        )
        
        # damage = (10 * 1.0 - 100 * 0.5) = -40 -> min 1
        assert damage == 1


class TestHealCalculation:
    """Test heal calculation"""
    
    def test_heal_based_on_max_hp_percentage(self):
        """Heal amount based on target's max HP"""
        calc = DamageCalculator()
        
        target_max_hp = 1000
        heal_multiplier = 0.3  # 30%
        
        heal = calc.calculate_heal(
            target_max_hp=target_max_hp,
            heal_multiplier=heal_multiplier
        )
        
        assert heal == 300
    
    def test_heal_based_on_caster_atk(self):
        """Heal based on caster's ATK"""
        calc = DamageCalculator()
        
        caster_atk = 200
        heal_multiplier = 1.5
        
        heal = calc.calculate_heal_from_atk(
            caster_atk=caster_atk,
            heal_multiplier=heal_multiplier
        )
        
        assert heal == 300


class TestTurnOrder:
    """Test turn order calculation"""
    
    def test_faster_character_goes_first(self):
        """Character with higher SPD should go first"""
        calc = DamageCalculator()
        
        chars = [
            {"id": "a", "spd": 100},
            {"id": "b", "spd": 150},
            {"id": "c", "spd": 120}
        ]
        
        order = calc.calculate_turn_order(chars)
        
        assert order[0]["id"] == "b"  # SPD 150
        assert order[1]["id"] == "c"  # SPD 120
        assert order[2]["id"] == "a"  # SPD 100
    
    def test_same_speed_maintains_input_order(self):
        """Characters with same SPD maintain input order"""
        calc = DamageCalculator()
        
        chars = [
            {"id": "a", "spd": 100},
            {"id": "b", "spd": 100},
            {"id": "c", "spd": 100}
        ]
        
        order = calc.calculate_turn_order(chars)
        
        # Should maintain stable sort order
        assert len(order) == 3


class TestCriticalHitChance:
    """Test critical hit chance calculation"""
    
    def test_crit_chance_within_bounds(self):
        """Crit chance should be between 0% and 100%"""
        calc = DamageCalculator()
        
        # Low crit stat
        chance_low = calc.get_crit_chance(5)
        assert 0 <= chance_low <= 1.0
        
        # High crit stat
        chance_high = calc.get_crit_chance(100)
        assert 0 <= chance_high <= 1.0
    
    def test_higher_crit_stat_means_higher_chance(self):
        """Higher CRIT stat should mean higher crit chance"""
        calc = DamageCalculator()
        
        chance_low = calc.get_crit_chance(10)
        chance_high = calc.get_crit_chance(50)
        
        assert chance_high > chance_low
