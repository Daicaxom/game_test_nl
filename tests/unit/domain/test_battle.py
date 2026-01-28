"""
Tests for Battle Entity and Turn Manager
Following TDD approach
"""
import pytest
from uuid import uuid4
from app.domain.entities.battle import Battle, BattleState, BattleResult, TurnOrder
from app.domain.entities.character import Character
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
        template_id="test_enemy"
    )


class TestBattleCreation:
    """Test Battle entity creation"""
    
    def test_create_battle_with_teams(self):
        """Should create battle with player and enemy teams"""
        player_team = [create_test_hero()]
        enemy_team = [create_test_enemy()]
        
        battle = Battle(
            id=str(uuid4()),
            player_id=str(uuid4()),
            stage_id="stage_1_1",
            player_team=player_team,
            enemy_team=enemy_team
        )
        
        assert len(battle.player_team) == 1
        assert len(battle.enemy_team) == 1
    
    def test_battle_starts_in_progress_state(self):
        """Battle should start with IN_PROGRESS state"""
        battle = Battle(
            id=str(uuid4()),
            player_id=str(uuid4()),
            stage_id="stage_1_1",
            player_team=[create_test_hero()],
            enemy_team=[create_test_enemy()]
        )
        
        assert battle.state == BattleState.IN_PROGRESS
    
    def test_battle_starts_at_turn_1(self):
        """Battle should start at turn 1"""
        battle = Battle(
            id=str(uuid4()),
            player_id=str(uuid4()),
            stage_id="stage_1_1",
            player_team=[create_test_hero()],
            enemy_team=[create_test_enemy()]
        )
        
        assert battle.turn_number == 1


class TestTurnOrder:
    """Test Turn Order calculation"""
    
    def test_calculate_turn_order_by_speed(self):
        """Characters should be ordered by SPD (highest first)"""
        fast_hero = create_test_hero("Fast Hero", spd=150)
        slow_hero = create_test_hero("Slow Hero", spd=90)
        enemy = create_test_enemy("Enemy", spd=100)
        
        battle = Battle(
            id=str(uuid4()),
            player_id=str(uuid4()),
            stage_id="stage_1_1",
            player_team=[fast_hero, slow_hero],
            enemy_team=[enemy]
        )
        
        turn_order = battle.calculate_turn_order()
        
        assert turn_order[0].id == fast_hero.id  # SPD 150
        assert turn_order[1].id == enemy.id       # SPD 100
        assert turn_order[2].id == slow_hero.id   # SPD 90
    
    def test_turn_order_excludes_dead_characters(self):
        """Dead characters should not be in turn order"""
        hero = create_test_hero(spd=150)
        dead_hero = create_test_hero(spd=200)
        dead_hero.take_damage(10000)  # Kill the hero
        enemy = create_test_enemy(spd=100)
        
        battle = Battle(
            id=str(uuid4()),
            player_id=str(uuid4()),
            stage_id="stage_1_1",
            player_team=[hero, dead_hero],
            enemy_team=[enemy]
        )
        
        turn_order = battle.calculate_turn_order()
        
        assert len(turn_order) == 2
        assert dead_hero.id not in [c.id for c in turn_order]


class TestCurrentActor:
    """Test Current Actor management"""
    
    def test_get_current_actor(self):
        """Should return the character whose turn it is"""
        fast_hero = create_test_hero("Fast", spd=150)
        slow_enemy = create_test_enemy("Slow", spd=80)
        
        battle = Battle(
            id=str(uuid4()),
            player_id=str(uuid4()),
            stage_id="stage_1_1",
            player_team=[fast_hero],
            enemy_team=[slow_enemy]
        )
        
        battle.calculate_turn_order()
        current = battle.get_current_actor()
        
        assert current.id == fast_hero.id
    
    def test_is_player_turn(self):
        """Should correctly identify player's turn"""
        fast_hero = create_test_hero("Fast", spd=150)
        slow_enemy = create_test_enemy("Slow", spd=80)
        
        battle = Battle(
            id=str(uuid4()),
            player_id=str(uuid4()),
            stage_id="stage_1_1",
            player_team=[fast_hero],
            enemy_team=[slow_enemy]
        )
        
        battle.calculate_turn_order()
        
        assert battle.is_player_turn() is True
    
    def test_advance_to_next_turn(self):
        """Should advance to the next character's turn"""
        fast_hero = create_test_hero("Fast", spd=150)
        slow_enemy = create_test_enemy("Slow", spd=80)
        
        battle = Battle(
            id=str(uuid4()),
            player_id=str(uuid4()),
            stage_id="stage_1_1",
            player_team=[fast_hero],
            enemy_team=[slow_enemy]
        )
        
        battle.calculate_turn_order()
        battle.next_turn()
        
        assert battle.get_current_actor().id == slow_enemy.id


class TestBattleState:
    """Test Battle state management"""
    
    def test_check_victory_when_all_enemies_dead(self):
        """Should return victory when all enemies are dead"""
        hero = create_test_hero()
        enemy = create_test_enemy()
        enemy.take_damage(10000)  # Kill enemy
        
        battle = Battle(
            id=str(uuid4()),
            player_id=str(uuid4()),
            stage_id="stage_1_1",
            player_team=[hero],
            enemy_team=[enemy]
        )
        
        result = battle.check_battle_end()
        
        assert result == BattleResult.VICTORY
    
    def test_check_defeat_when_all_heroes_dead(self):
        """Should return defeat when all heroes are dead"""
        hero = create_test_hero()
        hero.take_damage(10000)  # Kill hero
        enemy = create_test_enemy()
        
        battle = Battle(
            id=str(uuid4()),
            player_id=str(uuid4()),
            stage_id="stage_1_1",
            player_team=[hero],
            enemy_team=[enemy]
        )
        
        result = battle.check_battle_end()
        
        assert result == BattleResult.DEFEAT
    
    def test_battle_continues_when_both_sides_alive(self):
        """Should return None when battle continues"""
        hero = create_test_hero()
        enemy = create_test_enemy()
        
        battle = Battle(
            id=str(uuid4()),
            player_id=str(uuid4()),
            stage_id="stage_1_1",
            player_team=[hero],
            enemy_team=[enemy]
        )
        
        result = battle.check_battle_end()
        
        assert result is None
    
    def test_is_ended_after_victory(self):
        """Battle should be ended after victory"""
        hero = create_test_hero()
        enemy = create_test_enemy()
        enemy.take_damage(10000)
        
        battle = Battle(
            id=str(uuid4()),
            player_id=str(uuid4()),
            stage_id="stage_1_1",
            player_team=[hero],
            enemy_team=[enemy]
        )
        
        battle.end_battle(BattleResult.VICTORY)
        
        assert battle.is_ended() is True
        assert battle.state == BattleState.VICTORY


class TestManaGeneration:
    """Test mana generation each turn"""
    
    def test_mana_generated_at_turn_start(self):
        """Characters should gain mana at turn start"""
        hero = create_test_hero()
        hero.current_mana = 0
        enemy = create_test_enemy()
        
        battle = Battle(
            id=str(uuid4()),
            player_id=str(uuid4()),
            stage_id="stage_1_1",
            player_team=[hero],
            enemy_team=[enemy]
        )
        
        battle.process_turn_start()
        
        assert hero.current_mana > 0
    
    def test_default_mana_generation_is_20(self):
        """Default mana generation should be 20 per turn"""
        hero = create_test_hero()
        hero.current_mana = 0
        enemy = create_test_enemy()
        
        battle = Battle(
            id=str(uuid4()),
            player_id=str(uuid4()),
            stage_id="stage_1_1",
            player_team=[hero],
            enemy_team=[enemy],
            mana_per_turn=20
        )
        
        battle.process_turn_start()
        
        assert hero.current_mana == 20


class TestRoundManagement:
    """Test round and turn management"""
    
    def test_round_increments_after_all_characters_act(self):
        """Turn number should increment after all characters act"""
        hero = create_test_hero()
        enemy = create_test_enemy()
        
        battle = Battle(
            id=str(uuid4()),
            player_id=str(uuid4()),
            stage_id="stage_1_1",
            player_team=[hero],
            enemy_team=[enemy]
        )
        
        battle.calculate_turn_order()
        
        # Both characters act
        battle.next_turn()  # Hero -> Enemy
        battle.next_turn()  # Enemy -> Hero (new round)
        
        assert battle.turn_number == 2


class TestBattleStateEnum:
    """Test BattleState enum"""
    
    def test_all_states_exist(self):
        """All battle states should exist"""
        assert BattleState.PREPARING is not None
        assert BattleState.IN_PROGRESS is not None
        assert BattleState.VICTORY is not None
        assert BattleState.DEFEAT is not None
        assert BattleState.RETREAT is not None


class TestTurnOrderClass:
    """Test TurnOrder utility class"""
    
    def test_turn_order_sorts_by_speed(self):
        """TurnOrder should sort characters by speed"""
        hero1 = create_test_hero("Fast", spd=150)
        hero2 = create_test_hero("Slow", spd=80)
        enemy = create_test_enemy("Mid", spd=100)
        
        characters = [hero2, enemy, hero1]
        turn_order = TurnOrder(characters)
        
        sorted_order = turn_order.get_order()
        
        assert sorted_order[0].stats.spd == 150
        assert sorted_order[1].stats.spd == 100
        assert sorted_order[2].stats.spd == 80
    
    def test_turn_order_current_index_starts_at_0(self):
        """TurnOrder current index should start at 0"""
        characters = [create_test_hero()]
        turn_order = TurnOrder(characters)
        
        assert turn_order.current_index == 0
    
    def test_turn_order_advance(self):
        """TurnOrder should advance to next character"""
        hero = create_test_hero(spd=150)
        enemy = create_test_enemy(spd=100)
        
        turn_order = TurnOrder([hero, enemy])
        turn_order.advance()
        
        assert turn_order.current_index == 1
    
    def test_turn_order_wraps_around(self):
        """TurnOrder should wrap around after last character"""
        hero = create_test_hero(spd=150)
        enemy = create_test_enemy(spd=100)
        
        turn_order = TurnOrder([hero, enemy])
        
        turn_order.advance()  # Index 1
        is_new_round = turn_order.advance()  # Index 0 (wrap)
        
        assert turn_order.current_index == 0
        assert is_new_round is True
