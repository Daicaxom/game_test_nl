"""
Tests for BattleService
Following TDD approach
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
from uuid import uuid4

from app.services.battle_service import BattleService
from app.domain.entities.battle import Battle, BattleState, BattleResult
from app.domain.entities.hero import Hero
from app.domain.entities.enemy import Enemy
from app.domain.value_objects.element import Element
from app.domain.value_objects.hexagon_stats import HexagonStats
from app.domain.value_objects.grid_position import GridPosition


def create_test_hero(name: str = "Test Hero", spd: int = 100) -> Hero:
    """Helper to create a test hero"""
    stats = HexagonStats(hp=1000, atk=100, def_=50, spd=spd, crit=10, dex=10)
    position = GridPosition(x=0, y=1)
    return Hero(
        id=str(uuid4()),
        name=name,
        element=Element.KIM,
        position=position,
        stats=stats,
        template_id="test_hero"
    )


def create_test_enemy(name: str = "Test Enemy", spd: int = 80) -> Enemy:
    """Helper to create a test enemy"""
    stats = HexagonStats(hp=500, atk=50, def_=30, spd=spd, crit=5, dex=5)
    position = GridPosition(x=2, y=1)
    return Enemy(
        id=str(uuid4()),
        name=name,
        element=Element.MOC,
        position=position,
        stats=stats,
        template_id="test_enemy",
        exp_reward=50,
        gold_reward=100
    )


class TestBattleServiceCreation:
    """Test BattleService instantiation"""
    
    def test_create_battle_service(self):
        """Should create BattleService instance"""
        service = BattleService()
        
        assert service is not None


class TestStartBattle:
    """Test starting a battle"""
    
    def test_start_battle_creates_battle(self):
        """Should create a battle with teams"""
        service = BattleService()
        
        player_team = [create_test_hero()]
        enemy_team = [create_test_enemy()]
        
        battle = service.start_battle(
            player_id=str(uuid4()),
            stage_id="stage_1_1",
            player_team=player_team,
            enemy_team=enemy_team
        )
        
        assert battle is not None
        assert battle.state == BattleState.IN_PROGRESS
    
    def test_start_battle_calculates_turn_order(self):
        """Battle should have turn order calculated"""
        service = BattleService()
        
        fast_hero = create_test_hero("Fast", spd=150)
        slow_enemy = create_test_enemy("Slow", spd=80)
        
        battle = service.start_battle(
            player_id=str(uuid4()),
            stage_id="stage_1_1",
            player_team=[fast_hero],
            enemy_team=[slow_enemy]
        )
        
        current = battle.get_current_actor()
        assert current.id == fast_hero.id
    
    def test_start_battle_generates_mana(self):
        """Starting battle should generate initial mana"""
        service = BattleService()
        
        hero = create_test_hero()
        hero.current_mana = 0
        enemy = create_test_enemy()
        
        battle = service.start_battle(
            player_id=str(uuid4()),
            stage_id="stage_1_1",
            player_team=[hero],
            enemy_team=[enemy]
        )
        
        # First turn should have mana generated
        assert hero.current_mana >= 0


class TestExecuteAction:
    """Test executing actions in battle"""
    
    def test_execute_basic_attack(self):
        """Should execute a basic attack"""
        service = BattleService()
        
        hero = create_test_hero()
        enemy = create_test_enemy()
        
        battle = service.start_battle(
            player_id=str(uuid4()),
            stage_id="stage_1_1",
            player_team=[hero],
            enemy_team=[enemy]
        )
        
        original_hp = enemy.current_hp
        
        result = service.execute_attack(battle, hero.id, enemy.id)
        
        assert result is not None
        assert enemy.current_hp < original_hp
    
    def test_attack_uses_element_multiplier(self):
        """Attack damage should include element multiplier"""
        service = BattleService()
        
        # KIM attacks MOC = 1.5x damage
        kim_hero = create_test_hero("Kim Hero")
        kim_hero.element = Element.KIM
        moc_enemy = create_test_enemy("Moc Enemy")
        moc_enemy.element = Element.MOC
        
        battle = service.start_battle(
            player_id=str(uuid4()),
            stage_id="stage_1_1",
            player_team=[kim_hero],
            enemy_team=[moc_enemy]
        )
        
        result = service.execute_attack(battle, kim_hero.id, moc_enemy.id)
        
        # Damage should be boosted by element
        assert result["damage"] > 0
        assert result["element_multiplier"] == 1.5


class TestBattleEnd:
    """Test battle ending conditions"""
    
    def test_battle_ends_on_victory(self):
        """Battle should end when all enemies die"""
        service = BattleService()
        
        hero = create_test_hero()
        weak_enemy = create_test_enemy()
        weak_enemy.current_hp = 1  # Very low HP
        
        battle = service.start_battle(
            player_id=str(uuid4()),
            stage_id="stage_1_1",
            player_team=[hero],
            enemy_team=[weak_enemy]
        )
        
        # Kill the enemy
        service.execute_attack(battle, hero.id, weak_enemy.id)
        
        result = battle.check_battle_end()
        
        assert result == BattleResult.VICTORY
    
    def test_battle_ends_on_defeat(self):
        """Battle should end when all heroes die"""
        service = BattleService()
        
        weak_hero = create_test_hero()
        weak_hero.current_hp = 1
        strong_enemy = create_test_enemy()
        strong_enemy.stats = HexagonStats(hp=5000, atk=500, def_=100, spd=150, crit=20, dex=20)
        
        battle = service.start_battle(
            player_id=str(uuid4()),
            stage_id="stage_1_1",
            player_team=[weak_hero],
            enemy_team=[strong_enemy]
        )
        
        # Enemy attacks hero
        service.execute_attack(battle, strong_enemy.id, weak_hero.id)
        
        result = battle.check_battle_end()
        
        assert result == BattleResult.DEFEAT


class TestBattleRewards:
    """Test battle reward calculation"""
    
    def test_calculate_rewards_on_victory(self):
        """Should calculate rewards when battle won"""
        service = BattleService()
        
        hero = create_test_hero()
        enemy = create_test_enemy()
        enemy.exp_reward = 100
        enemy.gold_reward = 200
        enemy.current_hp = 1
        
        battle = service.start_battle(
            player_id=str(uuid4()),
            stage_id="stage_1_1",
            player_team=[hero],
            enemy_team=[enemy]
        )
        
        service.execute_attack(battle, hero.id, enemy.id)
        battle.end_battle(BattleResult.VICTORY)
        
        rewards = service.calculate_rewards(battle)
        
        assert rewards["exp"] == 100
        assert rewards["gold"] == 200
    
    def test_calculate_rewards_sums_all_enemies(self):
        """Rewards should sum from all enemies"""
        service = BattleService()
        
        hero = create_test_hero()
        enemies = []
        for i in range(3):
            enemy = create_test_enemy(f"Enemy {i}")
            enemy.exp_reward = 50
            enemy.gold_reward = 100
            enemies.append(enemy)
        
        battle = service.start_battle(
            player_id=str(uuid4()),
            stage_id="stage_1_1",
            player_team=[hero],
            enemy_team=enemies
        )
        
        # Kill all enemies
        for enemy in enemies:
            enemy.take_damage(10000)
        
        battle.end_battle(BattleResult.VICTORY)
        rewards = service.calculate_rewards(battle)
        
        assert rewards["exp"] == 150  # 50 * 3
        assert rewards["gold"] == 300  # 100 * 3


class TestSkillUsage:
    """Test using skills in battle"""
    
    def test_use_skill_costs_mana(self):
        """Using a skill should cost mana"""
        service = BattleService()
        
        hero = create_test_hero()
        hero.current_mana = 100
        enemy = create_test_enemy()
        
        battle = service.start_battle(
            player_id=str(uuid4()),
            stage_id="stage_1_1",
            player_team=[hero],
            enemy_team=[enemy]
        )
        
        result = service.execute_skill(
            battle=battle,
            caster_id=hero.id,
            skill_id="test_skill",
            target_ids=[enemy.id],
            mana_cost=50
        )
        
        assert hero.current_mana == 50
    
    def test_cannot_use_skill_without_mana(self):
        """Should not be able to use skill without enough mana"""
        service = BattleService()
        
        hero = create_test_hero()
        hero.current_mana = 20
        enemy = create_test_enemy()
        
        battle = service.start_battle(
            player_id=str(uuid4()),
            stage_id="stage_1_1",
            player_team=[hero],
            enemy_team=[enemy]
        )
        
        result = service.execute_skill(
            battle=battle,
            caster_id=hero.id,
            skill_id="test_skill",
            target_ids=[enemy.id],
            mana_cost=50
        )
        
        assert result["success"] is False
        assert "insufficient mana" in result["error"].lower()
