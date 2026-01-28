"""
Tests for Skill System Entities
Following TDD approach - tests written first
"""
import pytest
from uuid import uuid4
from app.domain.entities.skill import Skill, ActiveSkill, SkillType, TargetType


class TestSkillCreation:
    """Test Skill entity creation"""
    
    def test_create_skill_with_basic_attributes(self):
        """Should create skill with required attributes"""
        skill = Skill(
            id=str(uuid4()),
            name="Long Tran Hào",
            description="Gây sát thương diện rộng",
            mana_cost=100,
            cooldown=3
        )
        
        assert skill.name == "Long Tran Hào"
        assert skill.mana_cost == 100
        assert skill.cooldown == 3
    
    def test_skill_starts_with_zero_current_cooldown(self):
        """Skill should start with 0 current cooldown"""
        skill = Skill(
            id=str(uuid4()),
            name="Test Skill",
            description="Test",
            mana_cost=50,
            cooldown=2
        )
        
        assert skill.current_cooldown == 0
    
    def test_skill_starts_at_level_1(self):
        """Skill should start at level 1"""
        skill = Skill(
            id=str(uuid4()),
            name="Test Skill",
            description="Test",
            mana_cost=50,
            cooldown=2
        )
        
        assert skill.level == 1


class TestSkillCooldown:
    """Test Skill cooldown mechanics"""
    
    def test_skill_ready_when_cooldown_zero(self):
        """Skill should be ready when cooldown is 0"""
        skill = Skill(
            id=str(uuid4()),
            name="Test Skill",
            description="Test",
            mana_cost=50,
            cooldown=2
        )
        
        assert skill.is_ready() is True
    
    def test_skill_not_ready_when_on_cooldown(self):
        """Skill should not be ready when on cooldown"""
        skill = Skill(
            id=str(uuid4()),
            name="Test Skill",
            description="Test",
            mana_cost=50,
            cooldown=2
        )
        skill.trigger_cooldown()
        
        assert skill.is_ready() is False
    
    def test_trigger_cooldown_sets_current_cooldown(self):
        """Triggering cooldown should set current cooldown to max"""
        skill = Skill(
            id=str(uuid4()),
            name="Test Skill",
            description="Test",
            mana_cost=50,
            cooldown=3
        )
        skill.trigger_cooldown()
        
        assert skill.current_cooldown == 3
    
    def test_reduce_cooldown(self):
        """Should reduce cooldown by 1"""
        skill = Skill(
            id=str(uuid4()),
            name="Test Skill",
            description="Test",
            mana_cost=50,
            cooldown=3
        )
        skill.trigger_cooldown()
        skill.reduce_cooldown()
        
        assert skill.current_cooldown == 2
    
    def test_reduce_cooldown_cannot_go_below_zero(self):
        """Cooldown should not go below 0"""
        skill = Skill(
            id=str(uuid4()),
            name="Test Skill",
            description="Test",
            mana_cost=50,
            cooldown=3
        )
        skill.reduce_cooldown()
        
        assert skill.current_cooldown == 0
    
    def test_reset_cooldown(self):
        """Should reset cooldown to 0"""
        skill = Skill(
            id=str(uuid4()),
            name="Test Skill",
            description="Test",
            mana_cost=50,
            cooldown=3
        )
        skill.trigger_cooldown()
        skill.reset_cooldown()
        
        assert skill.current_cooldown == 0


class TestActiveSkillCreation:
    """Test ActiveSkill entity creation"""
    
    def test_create_damage_skill(self):
        """Should create damage skill"""
        skill = ActiveSkill(
            id=str(uuid4()),
            name="Long Tran Hào",
            description="Gây sát thương diện rộng",
            mana_cost=100,
            cooldown=3,
            skill_type=SkillType.DAMAGE,
            target_type=TargetType.ALL_ENEMIES,
            damage_multiplier=1.5
        )
        
        assert skill.skill_type == SkillType.DAMAGE
        assert skill.target_type == TargetType.ALL_ENEMIES
        assert skill.damage_multiplier == 1.5
    
    def test_create_heal_skill(self):
        """Should create heal skill"""
        skill = ActiveSkill(
            id=str(uuid4()),
            name="Thiên Khí",
            description="Hồi phục HP đồng đội",
            mana_cost=80,
            cooldown=2,
            skill_type=SkillType.HEAL,
            target_type=TargetType.ALL_ALLIES,
            heal_multiplier=0.3
        )
        
        assert skill.skill_type == SkillType.HEAL
        assert skill.target_type == TargetType.ALL_ALLIES
        assert skill.heal_multiplier == 0.3
    
    def test_create_buff_skill(self):
        """Should create buff skill"""
        skill = ActiveSkill(
            id=str(uuid4()),
            name="Cường Hóa",
            description="Tăng sức tấn công",
            mana_cost=60,
            cooldown=4,
            skill_type=SkillType.BUFF,
            target_type=TargetType.SINGLE_ALLY,
            buff_stats={"ATK": 20}
        )
        
        assert skill.skill_type == SkillType.BUFF
        assert skill.buff_stats == {"ATK": 20}
    
    def test_create_debuff_skill(self):
        """Should create debuff skill"""
        skill = ActiveSkill(
            id=str(uuid4()),
            name="Hắc Ám",
            description="Giảm phòng thủ địch",
            mana_cost=70,
            cooldown=3,
            skill_type=SkillType.DEBUFF,
            target_type=TargetType.SINGLE_ENEMY,
            debuff_effects={"DEF": -15}
        )
        
        assert skill.skill_type == SkillType.DEBUFF
        assert skill.debuff_effects == {"DEF": -15}


class TestSkillTargetTypes:
    """Test skill target type validation"""
    
    def test_self_target(self):
        """Self target type"""
        skill = ActiveSkill(
            id=str(uuid4()),
            name="Self Buff",
            description="Buff self",
            mana_cost=30,
            cooldown=1,
            skill_type=SkillType.BUFF,
            target_type=TargetType.SELF
        )
        
        assert skill.target_type == TargetType.SELF
    
    def test_single_ally_target(self):
        """Single ally target type"""
        skill = ActiveSkill(
            id=str(uuid4()),
            name="Single Heal",
            description="Heal one ally",
            mana_cost=40,
            cooldown=1,
            skill_type=SkillType.HEAL,
            target_type=TargetType.SINGLE_ALLY
        )
        
        assert skill.target_type == TargetType.SINGLE_ALLY
    
    def test_single_enemy_target(self):
        """Single enemy target type"""
        skill = ActiveSkill(
            id=str(uuid4()),
            name="Single Strike",
            description="Attack one enemy",
            mana_cost=50,
            cooldown=0,
            skill_type=SkillType.DAMAGE,
            target_type=TargetType.SINGLE_ENEMY
        )
        
        assert skill.target_type == TargetType.SINGLE_ENEMY
    
    def test_aoe_target(self):
        """AOE target type (area around position)"""
        skill = ActiveSkill(
            id=str(uuid4()),
            name="Area Attack",
            description="Attack area",
            mana_cost=80,
            cooldown=3,
            skill_type=SkillType.DAMAGE,
            target_type=TargetType.AOE,
            aoe_range=1
        )
        
        assert skill.target_type == TargetType.AOE
        assert skill.aoe_range == 1


class TestSkillElement:
    """Test skill element attributes"""
    
    def test_skill_with_element(self):
        """Skill can have an element"""
        from app.domain.value_objects.element import Element
        
        skill = ActiveSkill(
            id=str(uuid4()),
            name="Fire Strike",
            description="Fire attack",
            mana_cost=60,
            cooldown=2,
            skill_type=SkillType.DAMAGE,
            target_type=TargetType.SINGLE_ENEMY,
            element=Element.HOA,
            damage_multiplier=1.2
        )
        
        assert skill.element == Element.HOA
    
    def test_skill_without_element(self):
        """Skill can have no element (physical)"""
        skill = ActiveSkill(
            id=str(uuid4()),
            name="Physical Strike",
            description="Physical attack",
            mana_cost=30,
            cooldown=0,
            skill_type=SkillType.DAMAGE,
            target_type=TargetType.SINGLE_ENEMY,
            damage_multiplier=1.0
        )
        
        assert skill.element is None
