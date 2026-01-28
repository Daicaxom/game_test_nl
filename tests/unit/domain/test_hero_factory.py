"""
Tests for HeroFactory - Creating predefined heroes from templates
Following TDD approach - tests written first
"""
import pytest
from uuid import uuid4

from app.domain.factories.hero_factory import HeroFactory, HeroTemplate
from app.domain.value_objects.element import Element
from app.domain.value_objects.grid_position import GridPosition


class TestHeroTemplateCreation:
    """Test HeroTemplate data class"""
    
    def test_create_hero_template(self):
        """Should create a hero template with all attributes"""
        template = HeroTemplate(
            template_id="quan_vu",
            name="Quan Vũ",
            element=Element.KIM,
            base_hp=1200,
            base_atk=120,
            base_def=80,
            base_spd=95,
            base_crit=15,
            base_dex=20,
            rarity=5,
            description="Võ Thánh, sử dụng Thanh Long Yểm Nguyệt Đao"
        )
        
        assert template.template_id == "quan_vu"
        assert template.name == "Quan Vũ"
        assert template.element == Element.KIM
    
    def test_template_has_base_stats(self):
        """Template should have all base stats"""
        template = HeroTemplate(
            template_id="test",
            name="Test Hero",
            element=Element.MOC,
            base_hp=1000,
            base_atk=100,
            base_def=50,
            base_spd=100,
            base_crit=10,
            base_dex=15,
            rarity=3
        )
        
        assert template.base_hp == 1000
        assert template.base_atk == 100
        assert template.base_def == 50
        assert template.base_spd == 100
        assert template.base_crit == 10
        assert template.base_dex == 15


class TestHeroFactory:
    """Test HeroFactory class"""
    
    def test_factory_has_predefined_templates(self):
        """Factory should have predefined hero templates"""
        factory = HeroFactory()
        
        templates = factory.get_all_templates()
        
        assert len(templates) > 0
    
    def test_factory_has_quan_vu(self):
        """Factory should have Quan Vũ template"""
        factory = HeroFactory()
        
        template = factory.get_template("quan_vu")
        
        assert template is not None
        assert template.name == "Quan Vũ"
        assert template.element == Element.KIM
    
    def test_factory_has_truong_phi(self):
        """Factory should have Trương Phi template"""
        factory = HeroFactory()
        
        template = factory.get_template("truong_phi")
        
        assert template is not None
        assert template.name == "Trương Phi"
        assert template.element == Element.HOA
    
    def test_factory_has_luu_bi(self):
        """Factory should have Lưu Bị template"""
        factory = HeroFactory()
        
        template = factory.get_template("luu_bi")
        
        assert template is not None
        assert template.name == "Lưu Bị"
        assert template.element == Element.MOC
    
    def test_factory_has_gia_cat_luong(self):
        """Factory should have Gia Cát Lượng template"""
        factory = HeroFactory()
        
        template = factory.get_template("gia_cat_luong")
        
        assert template is not None
        assert template.name == "Gia Cát Lượng"
        assert template.element == Element.THUY
    
    def test_factory_has_trieu_van(self):
        """Factory should have Triệu Vân template"""
        factory = HeroFactory()
        
        template = factory.get_template("trieu_van")
        
        assert template is not None
        assert template.name == "Triệu Vân"
        assert template.element == Element.THO


class TestHeroCreationFromTemplate:
    """Test creating Hero instances from templates"""
    
    def test_create_hero_from_template(self):
        """Should create a Hero instance from template"""
        factory = HeroFactory()
        
        hero = factory.create_hero("quan_vu", GridPosition(x=1, y=1))
        
        assert hero is not None
        assert hero.name == "Quan Vũ"
        assert hero.element == Element.KIM
        assert hero.template_id == "quan_vu"
    
    def test_created_hero_has_base_stats(self):
        """Created hero should have base stats from template"""
        factory = HeroFactory()
        
        hero = factory.create_hero("quan_vu", GridPosition(x=1, y=1))
        
        # Quan Vũ is a Kim element high ATK hero
        assert hero.stats.atk >= 100
        assert hero.stats.hp >= 1000
    
    def test_created_hero_starts_at_level_1(self):
        """Created hero should start at level 1"""
        factory = HeroFactory()
        
        hero = factory.create_hero("quan_vu", GridPosition(x=1, y=1))
        
        assert hero.level == 1
    
    def test_created_hero_has_unique_id(self):
        """Each created hero should have unique ID"""
        factory = HeroFactory()
        
        hero1 = factory.create_hero("quan_vu", GridPosition(x=0, y=0))
        hero2 = factory.create_hero("quan_vu", GridPosition(x=1, y=1))
        
        assert hero1.id != hero2.id
    
    def test_created_hero_at_specified_position(self):
        """Created hero should be at specified position"""
        factory = HeroFactory()
        position = GridPosition(x=2, y=1)
        
        hero = factory.create_hero("luu_bi", position)
        
        assert hero.position == position
    
    def test_create_hero_with_invalid_template_raises_error(self):
        """Should raise error when template doesn't exist"""
        factory = HeroFactory()
        
        with pytest.raises(ValueError, match="Template not found"):
            factory.create_hero("non_existent", GridPosition(x=0, y=0))


class TestElementStatDistribution:
    """Test that element types have appropriate stat distributions"""
    
    def test_kim_heroes_have_high_atk(self):
        """Kim (Metal) heroes should have high ATK"""
        factory = HeroFactory()
        
        # Quan Vũ is Kim
        quan_vu = factory.get_template("quan_vu")
        
        # ATK should be notably high for Kim heroes
        assert quan_vu.base_atk >= 110
    
    def test_moc_heroes_have_high_hp(self):
        """Mộc (Wood) heroes should have high HP"""
        factory = HeroFactory()
        
        # Lưu Bị is Mộc
        luu_bi = factory.get_template("luu_bi")
        
        # HP should be notably high for Mộc heroes
        assert luu_bi.base_hp >= 1200
    
    def test_thuy_heroes_have_high_spd(self):
        """Thủy (Water) heroes should have high SPD"""
        factory = HeroFactory()
        
        # Gia Cát Lượng is Thủy
        gia_cat_luong = factory.get_template("gia_cat_luong")
        
        # SPD should be notably high for Thủy heroes
        assert gia_cat_luong.base_spd >= 110
    
    def test_hoa_heroes_have_high_crit(self):
        """Hỏa (Fire) heroes should have high CRIT"""
        factory = HeroFactory()
        
        # Trương Phi is Hỏa
        truong_phi = factory.get_template("truong_phi")
        
        # CRIT should be notably high for Hỏa heroes
        assert truong_phi.base_crit >= 20
    
    def test_tho_heroes_have_high_def(self):
        """Thổ (Earth) heroes should have high DEF"""
        factory = HeroFactory()
        
        # Triệu Vân is Thổ
        trieu_van = factory.get_template("trieu_van")
        
        # DEF should be notably high for Thổ heroes
        assert trieu_van.base_def >= 90


class TestHeroRarity:
    """Test hero rarity system"""
    
    def test_template_has_rarity(self):
        """Template should have rarity (1-6)"""
        factory = HeroFactory()
        
        template = factory.get_template("quan_vu")
        
        assert 1 <= template.rarity <= 6
    
    def test_5_star_heroes_exist(self):
        """Factory should have 5-star heroes"""
        factory = HeroFactory()
        
        five_star_heroes = [
            t for t in factory.get_all_templates() 
            if t.rarity == 5
        ]
        
        assert len(five_star_heroes) >= 3
    
    def test_created_hero_inherits_rarity(self):
        """Created hero should inherit rarity from template"""
        factory = HeroFactory()
        
        hero = factory.create_hero("quan_vu", GridPosition(x=0, y=0))
        
        template = factory.get_template("quan_vu")
        assert hero.rarity == template.rarity
