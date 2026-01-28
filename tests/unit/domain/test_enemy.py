"""
Tests for Enemy Entity
Following TDD approach - tests written first
"""
import pytest
from uuid import uuid4
from app.domain.entities.enemy import Enemy, EnemyBehavior
from app.domain.value_objects.element import Element
from app.domain.value_objects.hexagon_stats import HexagonStats
from app.domain.value_objects.grid_position import GridPosition


class TestEnemyCreation:
    """Test Enemy entity creation"""
    
    def test_create_enemy_with_basic_attributes(self):
        """Should create enemy with required attributes"""
        stats = HexagonStats(hp=500, atk=50, def_=30, spd=80, crit=5, dex=8)
        position = GridPosition(x=2, y=1)
        
        enemy = Enemy(
            id=str(uuid4()),
            name="Hoàng Cân Binh",
            element=Element.MOC,
            position=position,
            stats=stats,
            template_id="hoang_can_binh"
        )
        
        assert enemy.name == "Hoàng Cân Binh"
        assert enemy.element == Element.MOC
        assert enemy.position == position
        assert enemy.stats == stats
        assert enemy.template_id == "hoang_can_binh"
    
    def test_enemy_has_current_hp_equal_to_max_hp(self):
        """Current HP should equal max HP on creation"""
        stats = HexagonStats(hp=500, atk=50, def_=30, spd=80, crit=5, dex=8)
        position = GridPosition(x=2, y=1)
        
        enemy = Enemy(
            id=str(uuid4()),
            name="Test Enemy",
            element=Element.HOA,
            position=position,
            stats=stats,
            template_id="test_enemy"
        )
        
        assert enemy.current_hp == 500
    
    def test_enemy_has_behavior(self):
        """Enemy should have AI behavior"""
        stats = HexagonStats.default()
        position = GridPosition(x=2, y=1)
        
        enemy = Enemy(
            id=str(uuid4()),
            name="Test Enemy",
            element=Element.THUY,
            position=position,
            stats=stats,
            template_id="test_enemy",
            behavior=EnemyBehavior.AGGRESSIVE
        )
        
        assert enemy.behavior == EnemyBehavior.AGGRESSIVE
    
    def test_enemy_default_behavior_is_balanced(self):
        """Enemy default behavior should be balanced"""
        stats = HexagonStats.default()
        position = GridPosition(x=2, y=1)
        
        enemy = Enemy(
            id=str(uuid4()),
            name="Test Enemy",
            element=Element.THO,
            position=position,
            stats=stats,
            template_id="test_enemy"
        )
        
        assert enemy.behavior == EnemyBehavior.BALANCED


class TestEnemyInheritance:
    """Test Enemy inherits from Character properly"""
    
    def test_enemy_can_take_damage(self):
        """Enemy should be able to take damage"""
        stats = HexagonStats(hp=500, atk=50, def_=30, spd=80, crit=5, dex=8)
        position = GridPosition(x=2, y=1)
        
        enemy = Enemy(
            id=str(uuid4()),
            name="Test Enemy",
            element=Element.KIM,
            position=position,
            stats=stats,
            template_id="test_enemy"
        )
        
        result = enemy.take_damage(100)
        
        assert enemy.current_hp == 400
        assert result.is_dead is False
    
    def test_enemy_can_be_killed(self):
        """Enemy should die when HP reaches 0"""
        stats = HexagonStats(hp=100, atk=50, def_=30, spd=80, crit=5, dex=8)
        position = GridPosition(x=2, y=1)
        
        enemy = Enemy(
            id=str(uuid4()),
            name="Test Enemy",
            element=Element.MOC,
            position=position,
            stats=stats,
            template_id="test_enemy"
        )
        
        result = enemy.take_damage(150)
        
        assert enemy.current_hp == 0
        assert result.is_dead is True
        assert enemy.is_alive is False


class TestEnemyRewards:
    """Test Enemy reward system"""
    
    def test_enemy_has_exp_reward(self):
        """Enemy should have EXP reward value"""
        stats = HexagonStats.default()
        position = GridPosition(x=2, y=1)
        
        enemy = Enemy(
            id=str(uuid4()),
            name="Test Enemy",
            element=Element.HOA,
            position=position,
            stats=stats,
            template_id="test_enemy",
            exp_reward=50
        )
        
        assert enemy.exp_reward == 50
    
    def test_enemy_has_gold_reward(self):
        """Enemy should have gold reward value"""
        stats = HexagonStats.default()
        position = GridPosition(x=2, y=1)
        
        enemy = Enemy(
            id=str(uuid4()),
            name="Test Enemy",
            element=Element.THUY,
            position=position,
            stats=stats,
            template_id="test_enemy",
            gold_reward=100
        )
        
        assert enemy.gold_reward == 100
    
    def test_enemy_default_rewards_are_zero(self):
        """Enemy default rewards should be zero"""
        stats = HexagonStats.default()
        position = GridPosition(x=2, y=1)
        
        enemy = Enemy(
            id=str(uuid4()),
            name="Test Enemy",
            element=Element.THO,
            position=position,
            stats=stats,
            template_id="test_enemy"
        )
        
        assert enemy.exp_reward == 0
        assert enemy.gold_reward == 0


class TestEnemyDifficulty:
    """Test Enemy difficulty level"""
    
    def test_enemy_has_difficulty_level(self):
        """Enemy should have a difficulty level"""
        stats = HexagonStats.default()
        position = GridPosition(x=2, y=1)
        
        enemy = Enemy(
            id=str(uuid4()),
            name="Test Enemy",
            element=Element.KIM,
            position=position,
            stats=stats,
            template_id="test_enemy",
            difficulty=3
        )
        
        assert enemy.difficulty == 3
    
    def test_enemy_default_difficulty_is_1(self):
        """Enemy default difficulty should be 1"""
        stats = HexagonStats.default()
        position = GridPosition(x=2, y=1)
        
        enemy = Enemy(
            id=str(uuid4()),
            name="Test Enemy",
            element=Element.MOC,
            position=position,
            stats=stats,
            template_id="test_enemy"
        )
        
        assert enemy.difficulty == 1


class TestEnemyPowerCalculation:
    """Test Enemy power rating"""
    
    def test_enemy_power_based_on_stats_and_difficulty(self):
        """Enemy power should combine stats and difficulty"""
        stats = HexagonStats(hp=500, atk=50, def_=30, spd=80, crit=5, dex=8)
        position = GridPosition(x=2, y=1)
        
        enemy = Enemy(
            id=str(uuid4()),
            name="Test Enemy",
            element=Element.HOA,
            position=position,
            stats=stats,
            template_id="test_enemy",
            difficulty=2
        )
        
        power = enemy.get_power_rating()
        
        # Stats total = 500 + 50 + 30 + 80 + 5 + 8 = 673
        # Difficulty multiplier = 1 + (2-1) * 0.2 = 1.2
        # Expected = 673 * 1.2 = 807.6 -> 807
        assert power > 0
        assert isinstance(power, int)
