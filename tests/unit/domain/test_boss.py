"""
Tests for Boss Entity
Following TDD approach - tests written first
"""
import pytest
from uuid import uuid4
from app.domain.entities.boss import Boss, BossPhase, MythicalTier
from app.domain.entities.enemy import EnemyBehavior
from app.domain.value_objects.element import Element
from app.domain.value_objects.hexagon_stats import HexagonStats
from app.domain.value_objects.grid_position import GridPosition


class TestBossCreation:
    """Test Boss entity creation"""
    
    def test_create_boss_with_basic_attributes(self):
        """Should create boss with required attributes"""
        stats = HexagonStats(hp=10000, atk=200, def_=150, spd=120, crit=15, dex=20)
        position = GridPosition(x=2, y=1)
        
        boss = Boss(
            id=str(uuid4()),
            name="Đổng Trác",
            title="Nghịch Thần",
            element=Element.HOA,
            position=position,
            stats=stats,
            template_id="dong_trac"
        )
        
        assert boss.name == "Đổng Trác"
        assert boss.title == "Nghịch Thần"
        assert boss.element == Element.HOA
        assert boss.template_id == "dong_trac"
    
    def test_boss_has_title(self):
        """Boss should have a title"""
        stats = HexagonStats.default()
        position = GridPosition(x=2, y=1)
        
        boss = Boss(
            id=str(uuid4()),
            name="Lã Bố",
            title="Chiến Thần",
            element=Element.KIM,
            position=position,
            stats=stats,
            template_id="la_bo"
        )
        
        assert boss.title == "Chiến Thần"
    
    def test_boss_inherits_from_enemy(self):
        """Boss should inherit from Enemy"""
        stats = HexagonStats(hp=5000, atk=150, def_=100, spd=100, crit=10, dex=15)
        position = GridPosition(x=2, y=1)
        
        boss = Boss(
            id=str(uuid4()),
            name="Test Boss",
            title="Test Title",
            element=Element.MOC,
            position=position,
            stats=stats,
            template_id="test_boss",
            exp_reward=500,
            gold_reward=1000
        )
        
        # Should have enemy attributes
        assert boss.exp_reward == 500
        assert boss.gold_reward == 1000
        assert boss.behavior is not None


class TestBossPhases:
    """Test Boss phase system"""
    
    def test_boss_has_phases(self):
        """Boss should have multiple phases"""
        stats = HexagonStats(hp=10000, atk=200, def_=150, spd=120, crit=15, dex=20)
        position = GridPosition(x=2, y=1)
        
        phases = [
            BossPhase(
                phase_number=1,
                hp_threshold=1.0,
                name="Phase 1",
                stat_modifiers={}
            ),
            BossPhase(
                phase_number=2,
                hp_threshold=0.5,
                name="Enraged",
                stat_modifiers={"atk": 1.5, "spd": 1.2}
            )
        ]
        
        boss = Boss(
            id=str(uuid4()),
            name="Test Boss",
            title="Multi-Phase",
            element=Element.THUY,
            position=position,
            stats=stats,
            template_id="test_boss",
            phases=phases
        )
        
        assert len(boss.phases) == 2
        assert boss.phases[0].name == "Phase 1"
        assert boss.phases[1].name == "Enraged"
    
    def test_boss_current_phase_starts_at_1(self):
        """Boss should start at phase 1"""
        stats = HexagonStats.default()
        position = GridPosition(x=2, y=1)
        
        boss = Boss(
            id=str(uuid4()),
            name="Test Boss",
            title="Test",
            element=Element.THO,
            position=position,
            stats=stats,
            template_id="test_boss"
        )
        
        assert boss.current_phase == 1
    
    def test_boss_transitions_to_next_phase(self):
        """Boss should transition phase when HP threshold reached"""
        stats = HexagonStats(hp=1000, atk=100, def_=50, spd=100, crit=10, dex=10)
        position = GridPosition(x=2, y=1)
        
        phases = [
            BossPhase(phase_number=1, hp_threshold=1.0, name="Normal"),
            BossPhase(phase_number=2, hp_threshold=0.5, name="Enraged")
        ]
        
        boss = Boss(
            id=str(uuid4()),
            name="Test Boss",
            title="Test",
            element=Element.KIM,
            position=position,
            stats=stats,
            template_id="test_boss",
            phases=phases
        )
        
        # Take damage to below 50%
        boss.take_damage(600)  # HP goes to 400 (40%)
        boss.check_phase_transition()
        
        assert boss.current_phase == 2
    
    def test_boss_phase_modifies_stats(self):
        """Phase transition should modify boss stats"""
        stats = HexagonStats(hp=1000, atk=100, def_=50, spd=100, crit=10, dex=10)
        position = GridPosition(x=2, y=1)
        
        phases = [
            BossPhase(phase_number=1, hp_threshold=1.0, name="Normal"),
            BossPhase(
                phase_number=2, 
                hp_threshold=0.5, 
                name="Enraged",
                stat_modifiers={"atk": 1.5}
            )
        ]
        
        boss = Boss(
            id=str(uuid4()),
            name="Test Boss",
            title="Test",
            element=Element.MOC,
            position=position,
            stats=stats,
            template_id="test_boss",
            phases=phases
        )
        
        original_atk = boss.get_effective_atk()
        
        boss.take_damage(600)
        boss.check_phase_transition()
        
        new_atk = boss.get_effective_atk()
        assert new_atk > original_atk


class TestMythicalBoss:
    """Test Mythical Boss tier system"""
    
    def test_boss_can_have_mythical_tier(self):
        """Boss can have a mythical tier"""
        stats = HexagonStats(hp=50000, atk=2000, def_=1500, spd=150, crit=15, dex=20)
        position = GridPosition(x=1, y=1)
        
        boss = Boss(
            id=str(uuid4()),
            name="Thanh Long",
            title="Đông Phương Thần Thú",
            element=Element.MOC,
            position=position,
            stats=stats,
            template_id="thanh_long",
            mythical_tier=MythicalTier.TU_LINH
        )
        
        assert boss.mythical_tier == MythicalTier.TU_LINH
    
    def test_mythical_tier_affects_power_rating(self):
        """Mythical tier should increase power rating"""
        stats = HexagonStats(hp=10000, atk=500, def_=300, spd=150, crit=15, dex=20)
        position = GridPosition(x=1, y=1)
        
        normal_boss = Boss(
            id=str(uuid4()),
            name="Normal Boss",
            title="Normal",
            element=Element.HOA,
            position=position,
            stats=stats,
            template_id="normal"
        )
        
        mythical_boss = Boss(
            id=str(uuid4()),
            name="Mythical Boss",
            title="Mythical",
            element=Element.HOA,
            position=position,
            stats=stats,
            template_id="mythical",
            mythical_tier=MythicalTier.TU_LINH
        )
        
        assert mythical_boss.get_power_rating() > normal_boss.get_power_rating()
    
    def test_all_mythical_tiers_exist(self):
        """All mythical tiers should exist"""
        assert MythicalTier.TU_LINH is not None
        assert MythicalTier.THIEN_VUONG is not None
        assert MythicalTier.THUONG_CO is not None
        assert MythicalTier.HON_DON is not None


class TestBossSpecialMechanics:
    """Test Boss special mechanics"""
    
    def test_boss_has_special_skills(self):
        """Boss should have special skills"""
        stats = HexagonStats.default()
        position = GridPosition(x=2, y=1)
        
        boss = Boss(
            id=str(uuid4()),
            name="Test Boss",
            title="Test",
            element=Element.THUY,
            position=position,
            stats=stats,
            template_id="test_boss",
            skills=["boss_skill_1", "boss_ultimate"]
        )
        
        assert "boss_skill_1" in boss.skills
        assert "boss_ultimate" in boss.skills
    
    def test_boss_is_immune_to_instant_death(self):
        """Boss should be immune to instant death effects"""
        stats = HexagonStats(hp=50000, atk=2000, def_=1500, spd=150, crit=15, dex=20)
        position = GridPosition(x=1, y=1)
        
        boss = Boss(
            id=str(uuid4()),
            name="Test Boss",
            title="Test",
            element=Element.THO,
            position=position,
            stats=stats,
            template_id="test_boss"
        )
        
        assert boss.is_immune_to("instant_death")
    
    def test_boss_can_have_special_mechanics(self):
        """Boss can have special battle mechanics"""
        stats = HexagonStats.default()
        position = GridPosition(x=2, y=1)
        
        special_mechanics = {
            "shield_phase": {"hp_threshold": 0.75, "duration": 2},
            "summon_adds": {"hp_threshold": 0.5, "adds_count": 3}
        }
        
        boss = Boss(
            id=str(uuid4()),
            name="Test Boss",
            title="Test",
            element=Element.KIM,
            position=position,
            stats=stats,
            template_id="test_boss",
            special_mechanics=special_mechanics
        )
        
        assert "shield_phase" in boss.special_mechanics
        assert "summon_adds" in boss.special_mechanics
