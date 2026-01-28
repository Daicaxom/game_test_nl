"""
Tests for Character and Hero Entities
Following TDD approach - tests written first
"""
import pytest
from uuid import uuid4
from app.domain.entities.character import Character
from app.domain.entities.hero import Hero
from app.domain.value_objects.element import Element
from app.domain.value_objects.hexagon_stats import HexagonStats
from app.domain.value_objects.grid_position import GridPosition


class TestCharacterCreation:
    """Test Character entity creation"""
    
    def test_create_character_with_basic_attributes(self):
        """Should create character with required attributes"""
        stats = HexagonStats(hp=1000, atk=100, def_=80, spd=95, crit=15, dex=20)
        position = GridPosition(x=1, y=1)
        
        character = Character(
            id=str(uuid4()),
            name="Quan Vũ",
            element=Element.KIM,
            position=position,
            stats=stats
        )
        
        assert character.name == "Quan Vũ"
        assert character.element == Element.KIM
        assert character.position == position
        assert character.stats == stats
    
    def test_character_has_current_hp_equal_to_max_hp(self):
        """Current HP should equal max HP on creation"""
        stats = HexagonStats(hp=1000, atk=100, def_=80, spd=95, crit=15, dex=20)
        position = GridPosition(x=1, y=1)
        
        character = Character(
            id=str(uuid4()),
            name="Test",
            element=Element.KIM,
            position=position,
            stats=stats
        )
        
        assert character.current_hp == 1000
    
    def test_character_starts_with_zero_mana(self):
        """Character should start with 0 mana"""
        stats = HexagonStats.default()
        position = GridPosition(x=0, y=0)
        
        character = Character(
            id=str(uuid4()),
            name="Test",
            element=Element.MOC,
            position=position,
            stats=stats
        )
        
        assert character.current_mana == 0
    
    def test_character_max_mana_is_100(self):
        """Character max mana should be 100"""
        stats = HexagonStats.default()
        position = GridPosition(x=0, y=0)
        
        character = Character(
            id=str(uuid4()),
            name="Test",
            element=Element.MOC,
            position=position,
            stats=stats
        )
        
        assert character.max_mana == 100


class TestCharacterDamage:
    """Test Character damage mechanics"""
    
    def test_take_damage_reduces_hp(self):
        """Taking damage should reduce current HP"""
        stats = HexagonStats(hp=1000, atk=100, def_=80, spd=95, crit=15, dex=20)
        position = GridPosition(x=1, y=1)
        character = Character(
            id=str(uuid4()),
            name="Test",
            element=Element.KIM,
            position=position,
            stats=stats
        )
        
        result = character.take_damage(200)
        
        assert character.current_hp == 800
        assert result.is_dead is False
    
    def test_take_lethal_damage_returns_dead(self):
        """Taking lethal damage should return is_dead=True"""
        stats = HexagonStats(hp=100, atk=100, def_=80, spd=95, crit=15, dex=20)
        position = GridPosition(x=1, y=1)
        character = Character(
            id=str(uuid4()),
            name="Test",
            element=Element.KIM,
            position=position,
            stats=stats
        )
        
        result = character.take_damage(200)
        
        assert character.current_hp == 0
        assert result.is_dead is True
    
    def test_hp_cannot_go_below_zero(self):
        """HP should not go below 0"""
        stats = HexagonStats(hp=100, atk=100, def_=80, spd=95, crit=15, dex=20)
        position = GridPosition(x=1, y=1)
        character = Character(
            id=str(uuid4()),
            name="Test",
            element=Element.KIM,
            position=position,
            stats=stats
        )
        
        character.take_damage(500)
        
        assert character.current_hp == 0


class TestCharacterHealing:
    """Test Character healing mechanics"""
    
    def test_heal_increases_hp(self):
        """Healing should increase current HP"""
        stats = HexagonStats(hp=1000, atk=100, def_=80, spd=95, crit=15, dex=20)
        position = GridPosition(x=1, y=1)
        character = Character(
            id=str(uuid4()),
            name="Test",
            element=Element.KIM,
            position=position,
            stats=stats
        )
        character.take_damage(500)  # HP = 500
        
        result = character.heal(200)
        
        assert character.current_hp == 700
        assert result.actual_heal == 200
    
    def test_heal_cannot_exceed_max_hp(self):
        """Healing should not exceed max HP"""
        stats = HexagonStats(hp=1000, atk=100, def_=80, spd=95, crit=15, dex=20)
        position = GridPosition(x=1, y=1)
        character = Character(
            id=str(uuid4()),
            name="Test",
            element=Element.KIM,
            position=position,
            stats=stats
        )
        character.take_damage(100)  # HP = 900
        
        result = character.heal(500)  # Try to heal 500, should only heal 100
        
        assert character.current_hp == 1000
        assert result.actual_heal == 100


class TestCharacterStatus:
    """Test Character status effect mechanics"""
    
    def test_can_act_when_no_status_effects(self):
        """Character can act when no disabling status effects"""
        stats = HexagonStats.default()
        position = GridPosition(x=0, y=0)
        character = Character(
            id=str(uuid4()),
            name="Test",
            element=Element.MOC,
            position=position,
            stats=stats
        )
        
        assert character.can_act() is True
    
    def test_is_alive_when_hp_above_zero(self):
        """Character is alive when HP > 0"""
        stats = HexagonStats(hp=1000, atk=100, def_=80, spd=95, crit=15, dex=20)
        position = GridPosition(x=1, y=1)
        character = Character(
            id=str(uuid4()),
            name="Test",
            element=Element.KIM,
            position=position,
            stats=stats
        )
        
        assert character.is_alive is True
    
    def test_is_not_alive_when_hp_zero(self):
        """Character is not alive when HP = 0"""
        stats = HexagonStats(hp=100, atk=100, def_=80, spd=95, crit=15, dex=20)
        position = GridPosition(x=1, y=1)
        character = Character(
            id=str(uuid4()),
            name="Test",
            element=Element.KIM,
            position=position,
            stats=stats
        )
        character.take_damage(100)
        
        assert character.is_alive is False


class TestCharacterMana:
    """Test Character mana mechanics"""
    
    def test_gain_mana(self):
        """Character can gain mana"""
        stats = HexagonStats.default()
        position = GridPosition(x=0, y=0)
        character = Character(
            id=str(uuid4()),
            name="Test",
            element=Element.MOC,
            position=position,
            stats=stats
        )
        
        character.gain_mana(20)
        
        assert character.current_mana == 20
    
    def test_mana_cannot_exceed_max(self):
        """Mana cannot exceed max mana"""
        stats = HexagonStats.default()
        position = GridPosition(x=0, y=0)
        character = Character(
            id=str(uuid4()),
            name="Test",
            element=Element.MOC,
            position=position,
            stats=stats
        )
        
        character.gain_mana(150)
        
        assert character.current_mana == 100
    
    def test_use_mana(self):
        """Character can use mana"""
        stats = HexagonStats.default()
        position = GridPosition(x=0, y=0)
        character = Character(
            id=str(uuid4()),
            name="Test",
            element=Element.MOC,
            position=position,
            stats=stats
        )
        character.gain_mana(50)
        
        character.use_mana(30)
        
        assert character.current_mana == 20
    
    def test_cannot_use_more_mana_than_available(self):
        """Should raise error when using more mana than available"""
        stats = HexagonStats.default()
        position = GridPosition(x=0, y=0)
        character = Character(
            id=str(uuid4()),
            name="Test",
            element=Element.MOC,
            position=position,
            stats=stats
        )
        character.gain_mana(20)
        
        with pytest.raises(ValueError, match="Insufficient mana"):
            character.use_mana(50)


class TestHeroCreation:
    """Test Hero entity creation"""
    
    def test_create_hero_with_basic_attributes(self):
        """Should create hero with required attributes"""
        stats = HexagonStats(hp=1000, atk=100, def_=80, spd=95, crit=15, dex=20)
        position = GridPosition(x=1, y=1)
        
        hero = Hero(
            id=str(uuid4()),
            name="Quan Vũ",
            element=Element.KIM,
            position=position,
            stats=stats,
            template_id="quan_vu",
            rarity=5
        )
        
        assert hero.name == "Quan Vũ"
        assert hero.element == Element.KIM
        assert hero.template_id == "quan_vu"
        assert hero.rarity == 5
    
    def test_hero_starts_at_level_1(self):
        """Hero should start at level 1"""
        stats = HexagonStats.default()
        position = GridPosition(x=0, y=0)
        
        hero = Hero(
            id=str(uuid4()),
            name="Test Hero",
            element=Element.MOC,
            position=position,
            stats=stats,
            template_id="test",
            rarity=3
        )
        
        assert hero.level == 1
    
    def test_hero_starts_with_zero_exp(self):
        """Hero should start with 0 EXP"""
        stats = HexagonStats.default()
        position = GridPosition(x=0, y=0)
        
        hero = Hero(
            id=str(uuid4()),
            name="Test Hero",
            element=Element.MOC,
            position=position,
            stats=stats,
            template_id="test",
            rarity=3
        )
        
        assert hero.exp == 0
    
    def test_hero_starts_with_1_star(self):
        """Hero should start with 1 star"""
        stats = HexagonStats.default()
        position = GridPosition(x=0, y=0)
        
        hero = Hero(
            id=str(uuid4()),
            name="Test Hero",
            element=Element.MOC,
            position=position,
            stats=stats,
            template_id="test",
            rarity=3
        )
        
        assert hero.stars == 1
    
    def test_hero_starts_with_zero_ascension(self):
        """Hero should start with 0 ascension level"""
        stats = HexagonStats.default()
        position = GridPosition(x=0, y=0)
        
        hero = Hero(
            id=str(uuid4()),
            name="Test Hero",
            element=Element.MOC,
            position=position,
            stats=stats,
            template_id="test",
            rarity=3
        )
        
        assert hero.ascension_level == 0
    
    def test_hero_starts_with_zero_awakening(self):
        """Hero should start with 0 awakening level"""
        stats = HexagonStats.default()
        position = GridPosition(x=0, y=0)
        
        hero = Hero(
            id=str(uuid4()),
            name="Test Hero",
            element=Element.MOC,
            position=position,
            stats=stats,
            template_id="test",
            rarity=3
        )
        
        assert hero.awakening_level == 0


class TestHeroExperience:
    """Test Hero experience mechanics"""
    
    def test_gain_exp(self):
        """Hero can gain EXP"""
        stats = HexagonStats.default()
        position = GridPosition(x=0, y=0)
        
        hero = Hero(
            id=str(uuid4()),
            name="Test Hero",
            element=Element.MOC,
            position=position,
            stats=stats,
            template_id="test",
            rarity=3
        )
        
        result = hero.gain_exp(50)
        
        assert hero.exp == 50
        assert result.leveled_up is False
    
    def test_level_up_when_enough_exp(self):
        """Hero should level up when gaining enough EXP"""
        stats = HexagonStats.default()
        position = GridPosition(x=0, y=0)
        
        hero = Hero(
            id=str(uuid4()),
            name="Test Hero",
            element=Element.MOC,
            position=position,
            stats=stats,
            template_id="test",
            rarity=3
        )
        
        # Assuming 100 EXP needed for level 2
        result = hero.gain_exp(150)
        
        assert hero.level >= 2
        assert result.leveled_up is True


class TestHeroEquipment:
    """Test Hero equipment mechanics"""
    
    def test_hero_has_equipment_slots(self):
        """Hero should have 4 equipment slots"""
        stats = HexagonStats.default()
        position = GridPosition(x=0, y=0)
        
        hero = Hero(
            id=str(uuid4()),
            name="Test Hero",
            element=Element.MOC,
            position=position,
            stats=stats,
            template_id="test",
            rarity=3
        )
        
        assert hasattr(hero, 'weapon_id')
        assert hasattr(hero, 'armor_id')
        assert hasattr(hero, 'accessory_id')
        assert hasattr(hero, 'relic_id')
    
    def test_hero_equipment_slots_start_empty(self):
        """Hero equipment slots should start empty (None)"""
        stats = HexagonStats.default()
        position = GridPosition(x=0, y=0)
        
        hero = Hero(
            id=str(uuid4()),
            name="Test Hero",
            element=Element.MOC,
            position=position,
            stats=stats,
            template_id="test",
            rarity=3
        )
        
        assert hero.weapon_id is None
        assert hero.armor_id is None
        assert hero.accessory_id is None
        assert hero.relic_id is None
