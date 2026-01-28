"""
Tests for Mount Entity
Following TDD approach
"""
import pytest
from uuid import uuid4
from app.domain.entities.mount import Mount, MountType, DragonCompanion, EvolutionStage
from app.domain.value_objects.element import Element
from app.domain.value_objects.hexagon_stats import HexagonStats


class TestMountCreation:
    """Test Mount entity creation"""
    
    def test_create_horse_mount(self):
        """Should create a horse type mount"""
        mount = Mount(
            id=str(uuid4()),
            name="Xích Thố",
            mount_type=MountType.HORSE,
            rarity=5
        )
        
        assert mount.name == "Xích Thố"
        assert mount.mount_type == MountType.HORSE
        assert mount.rarity == 5
    
    def test_mount_starts_at_level_1(self):
        """Mount should start at level 1"""
        mount = Mount(
            id=str(uuid4()),
            name="Test Mount",
            mount_type=MountType.HORSE,
            rarity=3
        )
        
        assert mount.level == 1
    
    def test_mount_starts_with_bond_level_1(self):
        """Mount should start with bond level 1"""
        mount = Mount(
            id=str(uuid4()),
            name="Test Mount",
            mount_type=MountType.HORSE,
            rarity=3
        )
        
        assert mount.bond_level == 1


class TestMountTypes:
    """Test Mount type enumeration"""
    
    def test_all_mount_types_exist(self):
        """All mount types should exist"""
        assert MountType.HORSE is not None
        assert MountType.DRAGON is not None
        assert MountType.MYTHICAL is not None


class TestMountStats:
    """Test Mount stat bonuses"""
    
    def test_mount_provides_stats(self):
        """Mount should provide stat bonuses"""
        mount = Mount(
            id=str(uuid4()),
            name="Xích Thố",
            mount_type=MountType.HORSE,
            rarity=5,
            base_spd=30,
            base_dex=15
        )
        
        stats = mount.get_stats()
        
        assert stats.spd == 30
        assert stats.dex == 15
    
    def test_mount_stats_scale_with_level(self):
        """Mount stats should increase with level"""
        mount = Mount(
            id=str(uuid4()),
            name="Test Mount",
            mount_type=MountType.HORSE,
            rarity=3,
            base_spd=10,
            level=1
        )
        
        level_1_stats = mount.get_stats()
        
        mount.level = 10
        level_10_stats = mount.get_stats()
        
        assert level_10_stats.spd > level_1_stats.spd


class TestMountBond:
    """Test Mount bond system"""
    
    def test_increase_bond_level(self):
        """Bond level should increase with bonding"""
        mount = Mount(
            id=str(uuid4()),
            name="Test Mount",
            mount_type=MountType.HORSE,
            rarity=3
        )
        
        mount.add_bond_points(1000)
        
        assert mount.bond_level >= 1
    
    def test_bond_level_affects_stats(self):
        """Higher bond level should give better stats"""
        mount = Mount(
            id=str(uuid4()),
            name="Test Mount",
            mount_type=MountType.HORSE,
            rarity=3,
            base_spd=10
        )
        
        low_bond_stats = mount.get_stats()
        
        mount.bond_level = 10
        high_bond_stats = mount.get_stats()
        
        assert high_bond_stats.spd > low_bond_stats.spd
    
    def test_bond_level_max_is_10(self):
        """Bond level should max at 10"""
        mount = Mount(
            id=str(uuid4()),
            name="Test Mount",
            mount_type=MountType.HORSE,
            rarity=3,
            bond_level=10
        )
        
        mount.add_bond_points(10000)
        
        assert mount.bond_level <= 10


class TestMountTeamBonus:
    """Test Mount team bonuses"""
    
    def test_mount_provides_team_bonus(self):
        """Mount should provide team-wide bonuses"""
        mount = Mount(
            id=str(uuid4()),
            name="Xích Thố",
            mount_type=MountType.HORSE,
            rarity=5,
            team_bonus={"spd": 10}
        )
        
        bonus = mount.get_team_bonus()
        
        assert bonus["spd"] == 10
    
    def test_team_bonus_scales_with_level(self):
        """Team bonus should scale with mount level"""
        mount = Mount(
            id=str(uuid4()),
            name="Test Mount",
            mount_type=MountType.HORSE,
            rarity=3,
            team_bonus={"spd": 5}
        )
        
        level_1_bonus = mount.get_team_bonus()
        
        mount.level = 20
        level_20_bonus = mount.get_team_bonus()
        
        assert level_20_bonus["spd"] > level_1_bonus["spd"]


class TestDragonCompanion:
    """Test Dragon Companion special mount"""
    
    def test_create_dragon_companion(self):
        """Should create a dragon companion"""
        dragon = DragonCompanion(
            id=str(uuid4()),
            name="Hỏa Long",
            element=Element.HOA,
            rarity=5
        )
        
        assert dragon.name == "Hỏa Long"
        assert dragon.element == Element.HOA
        assert dragon.mount_type == MountType.DRAGON
    
    def test_dragon_has_element(self):
        """Dragon should have an element"""
        dragon = DragonCompanion(
            id=str(uuid4()),
            name="Thanh Long",
            element=Element.MOC,
            rarity=5
        )
        
        assert dragon.element == Element.MOC
    
    def test_dragon_provides_element_buff(self):
        """Dragon should provide element-based buffs"""
        dragon = DragonCompanion(
            id=str(uuid4()),
            name="Hỏa Long",
            element=Element.HOA,
            rarity=5
        )
        
        buff = dragon.get_element_buff()
        
        assert "hoa_damage" in buff or Element.HOA.value.lower() in str(buff).lower()


class TestDragonEvolution:
    """Test Dragon evolution system"""
    
    def test_dragon_starts_at_stage_0(self):
        """Dragon should start at evolution stage 0"""
        dragon = DragonCompanion(
            id=str(uuid4()),
            name="Test Dragon",
            element=Element.THUY,
            rarity=5
        )
        
        assert dragon.evolution_stage == 0
    
    def test_dragon_can_evolve(self):
        """Dragon should be able to evolve"""
        dragon = DragonCompanion(
            id=str(uuid4()),
            name="Hỏa Long",
            element=Element.HOA,
            rarity=5,
            evolution_stages=[
                EvolutionStage(stage=0, name="Hỏa Long Ấu Thể", level_req=1),
                EvolutionStage(stage=1, name="Hỏa Long Trưởng Thành", level_req=30)
            ]
        )
        
        dragon.level = 30
        result = dragon.evolve()
        
        assert result is True
        assert dragon.evolution_stage == 1
    
    def test_evolution_increases_stats(self):
        """Evolution should increase dragon stats"""
        dragon = DragonCompanion(
            id=str(uuid4()),
            name="Test Dragon",
            element=Element.KIM,
            rarity=5,
            base_atk=20,
            evolution_stages=[
                EvolutionStage(stage=0, name="Stage 1", level_req=1),
                EvolutionStage(stage=1, name="Stage 2", level_req=30, stat_bonus={"atk": 50})
            ]
        )
        
        pre_evolution = dragon.get_stats()
        dragon.level = 30
        dragon.evolve()
        post_evolution = dragon.get_stats()
        
        assert post_evolution.atk > pre_evolution.atk
    
    def test_cannot_evolve_below_level_requirement(self):
        """Dragon cannot evolve if level requirement not met"""
        dragon = DragonCompanion(
            id=str(uuid4()),
            name="Test Dragon",
            element=Element.THO,
            rarity=5,
            level=10,
            evolution_stages=[
                EvolutionStage(stage=0, name="Stage 1", level_req=1),
                EvolutionStage(stage=1, name="Stage 2", level_req=30)
            ]
        )
        
        result = dragon.evolve()
        
        assert result is False
        assert dragon.evolution_stage == 0


class TestMountPower:
    """Test Mount power calculation"""
    
    def test_mount_has_power_rating(self):
        """Mount should have a power rating"""
        mount = Mount(
            id=str(uuid4()),
            name="Test Mount",
            mount_type=MountType.HORSE,
            rarity=3,
            base_hp=100,
            base_atk=20,
            base_spd=30
        )
        
        power = mount.get_power_rating()
        
        assert power > 0
    
    def test_rarity_affects_power(self):
        """Higher rarity should mean higher power"""
        low_rarity = Mount(
            id=str(uuid4()),
            name="Common Mount",
            mount_type=MountType.HORSE,
            rarity=1,
            base_spd=10
        )
        
        high_rarity = Mount(
            id=str(uuid4()),
            name="Legendary Mount",
            mount_type=MountType.HORSE,
            rarity=5,
            base_spd=10
        )
        
        assert high_rarity.get_power_rating() > low_rarity.get_power_rating()
