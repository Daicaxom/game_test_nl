"""
Tests for SkillFactory - Predefined skills and skill factory
Following TDD approach - tests written first
"""
import pytest

from app.domain.factories.skill_factory import SkillFactory, SkillTemplate
from app.domain.entities.skill import SkillType, TargetType
from app.domain.value_objects.element import Element


class TestSkillTemplateCreation:
    """Test SkillTemplate data class"""
    
    def test_create_skill_template(self):
        """Should create a skill template with all attributes"""
        template = SkillTemplate(
            template_id="long_tran_hao",
            name="Long Trần Hào",
            description="Múa đao tung hoành, gây sát thương diện rộng",
            mana_cost=100,
            cooldown=3,
            skill_type=SkillType.DAMAGE,
            target_type=TargetType.ALL_ENEMIES,
            damage_multiplier=1.5,
            element=Element.KIM
        )
        
        assert template.template_id == "long_tran_hao"
        assert template.name == "Long Trần Hào"
        assert template.mana_cost == 100
    
    def test_template_has_skill_type(self):
        """Template should have skill type"""
        template = SkillTemplate(
            template_id="test_skill",
            name="Test Skill",
            description="Test",
            mana_cost=50,
            cooldown=2,
            skill_type=SkillType.HEAL,
            target_type=TargetType.ALL_ALLIES
        )
        
        assert template.skill_type == SkillType.HEAL


class TestSkillFactory:
    """Test SkillFactory class"""
    
    def test_factory_has_predefined_skills(self):
        """Factory should have predefined skill templates"""
        factory = SkillFactory()
        
        templates = factory.get_all_templates()
        
        assert len(templates) > 0
    
    def test_factory_has_basic_attack(self):
        """Factory should have basic attack skill"""
        factory = SkillFactory()
        
        template = factory.get_template("basic_attack")
        
        assert template is not None
        assert template.name == "Đánh Thường"
        assert template.mana_cost == 0
        assert template.skill_type == SkillType.DAMAGE
    
    def test_factory_has_long_tran_hao(self):
        """Factory should have Long Trần Hào skill"""
        factory = SkillFactory()
        
        template = factory.get_template("long_tran_hao")
        
        assert template is not None
        assert "Long" in template.name
        assert template.skill_type == SkillType.DAMAGE
    
    def test_factory_has_thien_khi_heal(self):
        """Factory should have Thiên Khí healing skill"""
        factory = SkillFactory()
        
        template = factory.get_template("thien_khi")
        
        assert template is not None
        assert template.skill_type == SkillType.HEAL


class TestSkillCreationFromTemplate:
    """Test creating Skill instances from templates"""
    
    def test_create_skill_from_template(self):
        """Should create a Skill instance from template"""
        factory = SkillFactory()
        
        skill = factory.create_skill("basic_attack")
        
        assert skill is not None
        assert skill.name == "Đánh Thường"
    
    def test_created_skill_has_correct_type(self):
        """Created skill should have correct skill type"""
        factory = SkillFactory()
        
        skill = factory.create_skill("basic_attack")
        
        # Basic attack is a damage skill
        assert skill.skill_type == SkillType.DAMAGE
    
    def test_created_skill_starts_with_no_cooldown(self):
        """Created skill should start with 0 current cooldown"""
        factory = SkillFactory()
        
        skill = factory.create_skill("long_tran_hao")
        
        assert skill.current_cooldown == 0
    
    def test_created_skill_has_unique_id(self):
        """Each created skill should have unique ID"""
        factory = SkillFactory()
        
        skill1 = factory.create_skill("basic_attack")
        skill2 = factory.create_skill("basic_attack")
        
        assert skill1.id != skill2.id
    
    def test_create_skill_with_invalid_template_raises_error(self):
        """Should raise error when template doesn't exist"""
        factory = SkillFactory()
        
        with pytest.raises(ValueError, match="Skill template not found"):
            factory.create_skill("non_existent")


class TestDamageSkills:
    """Test damage skill templates"""
    
    def test_aoe_damage_skill_exists(self):
        """Should have AOE damage skill"""
        factory = SkillFactory()
        
        templates = factory.get_skills_by_type(SkillType.DAMAGE)
        aoe_skills = [t for t in templates if t.target_type == TargetType.ALL_ENEMIES]
        
        assert len(aoe_skills) >= 1
    
    def test_single_target_damage_skill_exists(self):
        """Should have single target damage skill"""
        factory = SkillFactory()
        
        templates = factory.get_skills_by_type(SkillType.DAMAGE)
        single_target = [t for t in templates if t.target_type == TargetType.SINGLE_ENEMY]
        
        assert len(single_target) >= 1
    
    def test_damage_skills_have_multiplier(self):
        """Damage skills should have damage multiplier"""
        factory = SkillFactory()
        
        skill = factory.create_skill("long_tran_hao")
        
        assert skill.damage_multiplier >= 1.0


class TestHealSkills:
    """Test heal skill templates"""
    
    def test_heal_skill_exists(self):
        """Should have healing skill"""
        factory = SkillFactory()
        
        templates = factory.get_skills_by_type(SkillType.HEAL)
        
        assert len(templates) >= 1
    
    def test_heal_skill_targets_allies(self):
        """Heal skills should target allies"""
        factory = SkillFactory()
        
        template = factory.get_template("thien_khi")
        
        assert template.target_type in [
            TargetType.SELF, 
            TargetType.SINGLE_ALLY, 
            TargetType.ALL_ALLIES
        ]
    
    def test_heal_skill_has_heal_multiplier(self):
        """Heal skills should have heal multiplier"""
        factory = SkillFactory()
        
        skill = factory.create_skill("thien_khi")
        
        assert skill.heal_multiplier > 0


class TestBuffDebuffSkills:
    """Test buff and debuff skill templates"""
    
    def test_buff_skill_exists(self):
        """Should have buff skill"""
        factory = SkillFactory()
        
        templates = factory.get_skills_by_type(SkillType.BUFF)
        
        assert len(templates) >= 1
    
    def test_debuff_skill_exists(self):
        """Should have debuff skill"""
        factory = SkillFactory()
        
        templates = factory.get_skills_by_type(SkillType.DEBUFF)
        
        assert len(templates) >= 1


class TestSkillCosts:
    """Test skill mana costs"""
    
    def test_basic_attack_costs_no_mana(self):
        """Basic attack should cost 0 mana"""
        factory = SkillFactory()
        
        template = factory.get_template("basic_attack")
        
        assert template.mana_cost == 0
    
    def test_powerful_skills_cost_mana(self):
        """Powerful skills should cost mana"""
        factory = SkillFactory()
        
        template = factory.get_template("long_tran_hao")
        
        assert template.mana_cost >= 50
    
    def test_heal_skills_cost_mana(self):
        """Heal skills should cost mana"""
        factory = SkillFactory()
        
        template = factory.get_template("thien_khi")
        
        assert template.mana_cost >= 40


class TestSkillsByElement:
    """Test getting skills by element"""
    
    def test_get_skills_by_element(self):
        """Should be able to get skills by element"""
        factory = SkillFactory()
        
        kim_skills = factory.get_skills_by_element(Element.KIM)
        
        assert all(s.element == Element.KIM for s in kim_skills if s.element)
    
    def test_some_skills_have_no_element(self):
        """Some skills should have no element (neutral)"""
        factory = SkillFactory()
        
        templates = factory.get_all_templates()
        neutral_skills = [t for t in templates if t.element is None]
        
        assert len(neutral_skills) >= 1  # At least basic attack should be neutral
