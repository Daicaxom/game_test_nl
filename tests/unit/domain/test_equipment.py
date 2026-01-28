"""
Tests for Equipment System Entities
Following TDD approach - tests written first
"""
import pytest
from uuid import uuid4
from app.domain.entities.equipment import Equipment, EquipmentType, Rarity


class TestEquipmentCreation:
    """Test Equipment entity creation"""
    
    def test_create_weapon_equipment(self):
        """Should create weapon equipment"""
        equipment = Equipment(
            id=str(uuid4()),
            name="Thanh Long Đao",
            equipment_type=EquipmentType.WEAPON,
            rarity=Rarity.LEGENDARY,
            base_hp=0,
            base_atk=100,
            base_def=0,
            base_spd=10,
            base_crit=15,
            base_dex=5
        )
        
        assert equipment.name == "Thanh Long Đao"
        assert equipment.equipment_type == EquipmentType.WEAPON
        assert equipment.rarity == Rarity.LEGENDARY
        assert equipment.base_atk == 100
    
    def test_create_armor_equipment(self):
        """Should create armor equipment"""
        equipment = Equipment(
            id=str(uuid4()),
            name="Thanh Long Giáp",
            equipment_type=EquipmentType.ARMOR,
            rarity=Rarity.EPIC,
            base_hp=200,
            base_atk=0,
            base_def=80,
            base_spd=0,
            base_crit=0,
            base_dex=10
        )
        
        assert equipment.name == "Thanh Long Giáp"
        assert equipment.equipment_type == EquipmentType.ARMOR
        assert equipment.rarity == Rarity.EPIC
    
    def test_equipment_starts_at_level_1(self):
        """Equipment should start at level 1"""
        equipment = Equipment(
            id=str(uuid4()),
            name="Test Weapon",
            equipment_type=EquipmentType.WEAPON,
            rarity=Rarity.COMMON,
            base_hp=0,
            base_atk=10,
            base_def=0,
            base_spd=0,
            base_crit=0,
            base_dex=0
        )
        
        assert equipment.level == 1


class TestEquipmentTypes:
    """Test different equipment types"""
    
    def test_weapon_type(self):
        """Weapon equipment type"""
        equipment = Equipment(
            id=str(uuid4()),
            name="Sword",
            equipment_type=EquipmentType.WEAPON,
            rarity=Rarity.COMMON,
            base_hp=0,
            base_atk=10,
            base_def=0,
            base_spd=0,
            base_crit=0,
            base_dex=0
        )
        assert equipment.equipment_type == EquipmentType.WEAPON
    
    def test_armor_type(self):
        """Armor equipment type"""
        equipment = Equipment(
            id=str(uuid4()),
            name="Plate",
            equipment_type=EquipmentType.ARMOR,
            rarity=Rarity.COMMON,
            base_hp=50,
            base_atk=0,
            base_def=20,
            base_spd=0,
            base_crit=0,
            base_dex=0
        )
        assert equipment.equipment_type == EquipmentType.ARMOR
    
    def test_accessory_type(self):
        """Accessory equipment type"""
        equipment = Equipment(
            id=str(uuid4()),
            name="Ring",
            equipment_type=EquipmentType.ACCESSORY,
            rarity=Rarity.RARE,
            base_hp=0,
            base_atk=5,
            base_def=5,
            base_spd=10,
            base_crit=5,
            base_dex=5
        )
        assert equipment.equipment_type == EquipmentType.ACCESSORY
    
    def test_relic_type(self):
        """Relic equipment type"""
        equipment = Equipment(
            id=str(uuid4()),
            name="Ancient Relic",
            equipment_type=EquipmentType.RELIC,
            rarity=Rarity.MYTHIC,
            base_hp=100,
            base_atk=50,
            base_def=50,
            base_spd=20,
            base_crit=10,
            base_dex=10
        )
        assert equipment.equipment_type == EquipmentType.RELIC


class TestEquipmentRarity:
    """Test equipment rarity levels"""
    
    def test_common_rarity(self):
        """Common rarity"""
        equipment = Equipment(
            id=str(uuid4()),
            name="Common Sword",
            equipment_type=EquipmentType.WEAPON,
            rarity=Rarity.COMMON,
            base_hp=0,
            base_atk=10,
            base_def=0,
            base_spd=0,
            base_crit=0,
            base_dex=0
        )
        assert equipment.rarity == Rarity.COMMON
        assert equipment.get_max_level() == 10
    
    def test_rare_rarity(self):
        """Rare rarity"""
        equipment = Equipment(
            id=str(uuid4()),
            name="Rare Sword",
            equipment_type=EquipmentType.WEAPON,
            rarity=Rarity.RARE,
            base_hp=0,
            base_atk=20,
            base_def=0,
            base_spd=0,
            base_crit=0,
            base_dex=0
        )
        assert equipment.rarity == Rarity.RARE
        assert equipment.get_max_level() == 15
    
    def test_epic_rarity(self):
        """Epic rarity"""
        equipment = Equipment(
            id=str(uuid4()),
            name="Epic Sword",
            equipment_type=EquipmentType.WEAPON,
            rarity=Rarity.EPIC,
            base_hp=0,
            base_atk=30,
            base_def=0,
            base_spd=5,
            base_crit=5,
            base_dex=0
        )
        assert equipment.rarity == Rarity.EPIC
        assert equipment.get_max_level() == 20
    
    def test_legendary_rarity(self):
        """Legendary rarity"""
        equipment = Equipment(
            id=str(uuid4()),
            name="Legendary Sword",
            equipment_type=EquipmentType.WEAPON,
            rarity=Rarity.LEGENDARY,
            base_hp=0,
            base_atk=50,
            base_def=0,
            base_spd=10,
            base_crit=10,
            base_dex=5
        )
        assert equipment.rarity == Rarity.LEGENDARY
        assert equipment.get_max_level() == 25
    
    def test_mythic_rarity(self):
        """Mythic rarity"""
        equipment = Equipment(
            id=str(uuid4()),
            name="Mythic Sword",
            equipment_type=EquipmentType.WEAPON,
            rarity=Rarity.MYTHIC,
            base_hp=0,
            base_atk=100,
            base_def=0,
            base_spd=20,
            base_crit=20,
            base_dex=10
        )
        assert equipment.rarity == Rarity.MYTHIC
        assert equipment.get_max_level() == 30


class TestEquipmentStats:
    """Test equipment stat calculations"""
    
    def test_get_total_stats_base(self):
        """Get total stats at base level"""
        equipment = Equipment(
            id=str(uuid4()),
            name="Test Weapon",
            equipment_type=EquipmentType.WEAPON,
            rarity=Rarity.RARE,
            base_hp=0,
            base_atk=50,
            base_def=0,
            base_spd=10,
            base_crit=5,
            base_dex=5
        )
        
        stats = equipment.get_total_stats()
        
        assert stats.atk == 50
        assert stats.spd == 10
        assert stats.crit == 5
        assert stats.dex == 5
    
    def test_get_total_stats_with_bonus(self):
        """Get total stats including bonus stats"""
        equipment = Equipment(
            id=str(uuid4()),
            name="Test Weapon",
            equipment_type=EquipmentType.WEAPON,
            rarity=Rarity.RARE,
            base_hp=0,
            base_atk=50,
            base_def=0,
            base_spd=10,
            base_crit=5,
            base_dex=5,
            bonus_hp=0,
            bonus_atk=10,
            bonus_def=0,
            bonus_spd=5,
            bonus_crit=2,
            bonus_dex=0
        )
        
        stats = equipment.get_total_stats()
        
        assert stats.atk == 60  # 50 + 10
        assert stats.spd == 15  # 10 + 5
        assert stats.crit == 7  # 5 + 2


class TestEquipmentEnhancement:
    """Test equipment enhancement mechanics"""
    
    def test_can_enhance_when_below_max_level(self):
        """Can enhance when level is below max"""
        equipment = Equipment(
            id=str(uuid4()),
            name="Test Weapon",
            equipment_type=EquipmentType.WEAPON,
            rarity=Rarity.COMMON,
            base_hp=0,
            base_atk=10,
            base_def=0,
            base_spd=0,
            base_crit=0,
            base_dex=0
        )
        
        assert equipment.can_enhance() is True
    
    def test_cannot_enhance_at_max_level(self):
        """Cannot enhance when at max level"""
        equipment = Equipment(
            id=str(uuid4()),
            name="Test Weapon",
            equipment_type=EquipmentType.WEAPON,
            rarity=Rarity.COMMON,
            base_hp=0,
            base_atk=10,
            base_def=0,
            base_spd=0,
            base_crit=0,
            base_dex=0
        )
        equipment.level = 10  # Max for common
        
        assert equipment.can_enhance() is False
    
    def test_enhance_increases_level(self):
        """Enhancement should increase level"""
        equipment = Equipment(
            id=str(uuid4()),
            name="Test Weapon",
            equipment_type=EquipmentType.WEAPON,
            rarity=Rarity.COMMON,
            base_hp=0,
            base_atk=10,
            base_def=0,
            base_spd=0,
            base_crit=0,
            base_dex=0
        )
        
        result = equipment.enhance()
        
        assert equipment.level == 2
        assert result.success is True


class TestEquipmentSet:
    """Test equipment set mechanics"""
    
    def test_equipment_can_have_set_id(self):
        """Equipment can belong to a set"""
        equipment = Equipment(
            id=str(uuid4()),
            name="Thanh Long Đao",
            equipment_type=EquipmentType.WEAPON,
            rarity=Rarity.LEGENDARY,
            base_hp=0,
            base_atk=100,
            base_def=0,
            base_spd=10,
            base_crit=15,
            base_dex=5,
            set_id="thanh_long_set"
        )
        
        assert equipment.set_id == "thanh_long_set"
    
    def test_equipment_can_have_no_set(self):
        """Equipment can have no set"""
        equipment = Equipment(
            id=str(uuid4()),
            name="Basic Sword",
            equipment_type=EquipmentType.WEAPON,
            rarity=Rarity.COMMON,
            base_hp=0,
            base_atk=10,
            base_def=0,
            base_spd=0,
            base_crit=0,
            base_dex=0
        )
        
        assert equipment.set_id is None
