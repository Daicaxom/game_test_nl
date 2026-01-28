"""
Tests for Team and Formation Entities
Following TDD approach
"""
import pytest
from uuid import uuid4
from app.domain.entities.team import Team, TeamSlot, Formation, FormationBonus
from app.domain.entities.hero import Hero
from app.domain.value_objects.element import Element
from app.domain.value_objects.hexagon_stats import HexagonStats
from app.domain.value_objects.grid_position import GridPosition


def create_test_hero(name: str, element: Element = Element.KIM) -> Hero:
    """Helper to create a test hero"""
    stats = HexagonStats(hp=1000, atk=100, def_=50, spd=100, crit=10, dex=10)
    position = GridPosition(x=0, y=1)
    return Hero(
        id=str(uuid4()),
        name=name,
        element=element,
        position=position,
        stats=stats,
        template_id=name.lower().replace(" ", "_")
    )


class TestTeamCreation:
    """Test Team entity creation"""
    
    def test_create_team_with_name(self):
        """Should create team with a name"""
        team = Team(
            id=str(uuid4()),
            player_id=str(uuid4()),
            name="Main Team",
            slot_number=1
        )
        
        assert team.name == "Main Team"
        assert team.slot_number == 1
    
    def test_team_has_5_slots(self):
        """Team should have 5 slots maximum"""
        team = Team(
            id=str(uuid4()),
            player_id=str(uuid4()),
            name="Test Team",
            slot_number=1
        )
        
        assert team.max_members == 5
    
    def test_team_starts_empty(self):
        """Team should start with no members"""
        team = Team(
            id=str(uuid4()),
            player_id=str(uuid4()),
            name="Test Team",
            slot_number=1
        )
        
        assert len(team.members) == 0


class TestTeamMembers:
    """Test Team member management"""
    
    def test_add_hero_to_team(self):
        """Should add a hero to the team"""
        team = Team(
            id=str(uuid4()),
            player_id=str(uuid4()),
            name="Test Team",
            slot_number=1
        )
        hero = create_test_hero("Quan Vũ")
        
        result = team.add_member(hero, position=GridPosition(x=1, y=1))
        
        assert result is True
        assert len(team.members) == 1
        assert team.members[0].hero.name == "Quan Vũ"
    
    def test_cannot_add_more_than_5_members(self):
        """Should not allow more than 5 members"""
        team = Team(
            id=str(uuid4()),
            player_id=str(uuid4()),
            name="Test Team",
            slot_number=1
        )
        
        for i in range(5):
            hero = create_test_hero(f"Hero {i}")
            team.add_member(hero, position=GridPosition(x=i % 3, y=i // 3))
        
        extra_hero = create_test_hero("Extra Hero")
        result = team.add_member(extra_hero, position=GridPosition(x=0, y=0))
        
        assert result is False
        assert len(team.members) == 5
    
    def test_remove_hero_from_team(self):
        """Should remove a hero from the team"""
        team = Team(
            id=str(uuid4()),
            player_id=str(uuid4()),
            name="Test Team",
            slot_number=1
        )
        hero = create_test_hero("Quan Vũ")
        team.add_member(hero, position=GridPosition(x=1, y=1))
        
        result = team.remove_member(hero.id)
        
        assert result is True
        assert len(team.members) == 0
    
    def test_cannot_add_same_hero_twice(self):
        """Should not allow adding the same hero twice"""
        team = Team(
            id=str(uuid4()),
            player_id=str(uuid4()),
            name="Test Team",
            slot_number=1
        )
        hero = create_test_hero("Quan Vũ")
        
        team.add_member(hero, position=GridPosition(x=0, y=0))
        result = team.add_member(hero, position=GridPosition(x=1, y=1))
        
        assert result is False
        assert len(team.members) == 1


class TestTeamPositions:
    """Test Team position management"""
    
    def test_hero_position_stored(self):
        """Hero position should be stored in team"""
        team = Team(
            id=str(uuid4()),
            player_id=str(uuid4()),
            name="Test Team",
            slot_number=1
        )
        hero = create_test_hero("Quan Vũ")
        position = GridPosition(x=2, y=1)
        
        team.add_member(hero, position=position)
        
        assert team.members[0].position == position
    
    def test_cannot_place_two_heroes_same_position(self):
        """Two heroes cannot occupy the same position"""
        team = Team(
            id=str(uuid4()),
            player_id=str(uuid4()),
            name="Test Team",
            slot_number=1
        )
        hero1 = create_test_hero("Hero 1")
        hero2 = create_test_hero("Hero 2")
        position = GridPosition(x=1, y=1)
        
        team.add_member(hero1, position=position)
        result = team.add_member(hero2, position=position)
        
        assert result is False
    
    def test_move_hero_position(self):
        """Should be able to move hero to different position"""
        team = Team(
            id=str(uuid4()),
            player_id=str(uuid4()),
            name="Test Team",
            slot_number=1
        )
        hero = create_test_hero("Quan Vũ")
        team.add_member(hero, position=GridPosition(x=0, y=0))
        
        result = team.move_member(hero.id, GridPosition(x=2, y=2))
        
        assert result is True
        assert team.members[0].position == GridPosition(x=2, y=2)


class TestFormationCreation:
    """Test Formation entity creation"""
    
    def test_create_formation(self):
        """Should create a formation with requirements"""
        formation = Formation(
            id="ngu_hanh_tran",
            name="Ngũ Hành Trận",
            description="All five elements formation",
            required_elements=5,  # All different elements
            positions=[(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)]
        )
        
        assert formation.name == "Ngũ Hành Trận"
        assert formation.required_elements == 5
    
    def test_formation_has_bonuses(self):
        """Formation should have stat bonuses"""
        formation = Formation(
            id="test_formation",
            name="Test Formation",
            bonuses=[
                FormationBonus(stat="atk", value=15, bonus_type="percent"),
                FormationBonus(stat="def_", value=10, bonus_type="percent")
            ]
        )
        
        assert len(formation.bonuses) == 2


class TestFormationRequirements:
    """Test Formation requirement checking"""
    
    def test_check_formation_element_requirement(self):
        """Should check if team meets element requirements"""
        formation = Formation(
            id="ngu_hanh_tran",
            name="Ngũ Hành Trận",
            required_elements=5
        )
        
        team = Team(
            id=str(uuid4()),
            player_id=str(uuid4()),
            name="Test Team",
            slot_number=1
        )
        
        # Add heroes with all different elements
        elements = [Element.KIM, Element.MOC, Element.THUY, Element.HOA, Element.THO]
        for i, elem in enumerate(elements):
            hero = create_test_hero(f"Hero {i}", element=elem)
            team.add_member(hero, position=GridPosition(x=i % 3, y=i // 3))
        
        meets_requirements = formation.check_requirements(team)
        
        assert meets_requirements is True
    
    def test_formation_not_met_with_insufficient_elements(self):
        """Formation requirements not met with same elements"""
        formation = Formation(
            id="ngu_hanh_tran",
            name="Ngũ Hành Trận",
            required_elements=5
        )
        
        team = Team(
            id=str(uuid4()),
            player_id=str(uuid4()),
            name="Test Team",
            slot_number=1
        )
        
        # Add heroes with same element
        for i in range(5):
            hero = create_test_hero(f"Hero {i}", element=Element.KIM)
            team.add_member(hero, position=GridPosition(x=i % 3, y=i // 3))
        
        meets_requirements = formation.check_requirements(team)
        
        assert meets_requirements is False


class TestTeamPower:
    """Test Team power calculation"""
    
    def test_calculate_team_total_power(self):
        """Should calculate total team power"""
        team = Team(
            id=str(uuid4()),
            player_id=str(uuid4()),
            name="Test Team",
            slot_number=1
        )
        
        for i in range(3):
            hero = create_test_hero(f"Hero {i}")
            team.add_member(hero, position=GridPosition(x=i, y=0))
        
        total_power = team.get_total_power()
        
        assert total_power > 0
    
    def test_team_power_includes_formation_bonus(self):
        """Team power should include formation bonus when active"""
        team = Team(
            id=str(uuid4()),
            player_id=str(uuid4()),
            name="Test Team",
            slot_number=1
        )
        
        formation = Formation(
            id="bonus_formation",
            name="Bonus Formation",
            bonuses=[FormationBonus(stat="all", value=10, bonus_type="percent")]
        )
        team.set_formation(formation)
        
        for i in range(3):
            hero = create_test_hero(f"Hero {i}")
            team.add_member(hero, position=GridPosition(x=i, y=0))
        
        power_with_formation = team.get_total_power(include_formation=True)
        power_without = team.get_total_power(include_formation=False)
        
        assert power_with_formation > power_without


class TestTeamSynergy:
    """Test Team synergy mechanics"""
    
    def test_same_element_bonus(self):
        """Heroes of same element near each other get bonus"""
        team = Team(
            id=str(uuid4()),
            player_id=str(uuid4()),
            name="Test Team",
            slot_number=1
        )
        
        # Add two KIM element heroes adjacent
        hero1 = create_test_hero("Kim Hero 1", element=Element.KIM)
        hero2 = create_test_hero("Kim Hero 2", element=Element.KIM)
        
        team.add_member(hero1, position=GridPosition(x=0, y=0))
        team.add_member(hero2, position=GridPosition(x=1, y=0))
        
        synergy_bonus = team.calculate_element_synergy()
        
        assert synergy_bonus > 0
    
    def test_get_team_element_distribution(self):
        """Should return element distribution of team"""
        team = Team(
            id=str(uuid4()),
            player_id=str(uuid4()),
            name="Test Team",
            slot_number=1
        )
        
        team.add_member(create_test_hero("H1", Element.KIM), GridPosition(0, 0))
        team.add_member(create_test_hero("H2", Element.KIM), GridPosition(1, 0))
        team.add_member(create_test_hero("H3", Element.MOC), GridPosition(2, 0))
        
        distribution = team.get_element_distribution()
        
        assert distribution[Element.KIM] == 2
        assert distribution[Element.MOC] == 1
