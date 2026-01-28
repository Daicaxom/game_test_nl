"""
Tests for Element Value Object (Ngũ Hành)
Following TDD approach - tests written first
"""
import pytest
from app.domain.value_objects.element import Element


class TestElement:
    """Test suite for Element enum and relationships"""
    
    def test_element_values_exist(self):
        """All five elements should exist"""
        assert Element.KIM is not None
        assert Element.MOC is not None
        assert Element.THUY is not None
        assert Element.HOA is not None
        assert Element.THO is not None
    
    def test_element_value_names(self):
        """Element values should match Vietnamese names"""
        assert Element.KIM.value == "Kim"
        assert Element.MOC.value == "Mộc"
        assert Element.THUY.value == "Thủy"
        assert Element.HOA.value == "Hỏa"
        assert Element.THO.value == "Thổ"


class TestElementRelationships:
    """Test Ngũ Hành relationships - tương sinh tương khắc"""
    
    # Tương khắc (Strong against)
    def test_kim_strong_against_moc(self):
        """Kim khắc Mộc"""
        assert Element.KIM.get_strong_against() == Element.MOC
    
    def test_moc_strong_against_tho(self):
        """Mộc khắc Thổ"""
        assert Element.MOC.get_strong_against() == Element.THO
    
    def test_tho_strong_against_thuy(self):
        """Thổ khắc Thủy"""
        assert Element.THO.get_strong_against() == Element.THUY
    
    def test_thuy_strong_against_hoa(self):
        """Thủy khắc Hỏa"""
        assert Element.THUY.get_strong_against() == Element.HOA
    
    def test_hoa_strong_against_kim(self):
        """Hỏa khắc Kim"""
        assert Element.HOA.get_strong_against() == Element.KIM
    
    # Bị khắc (Weak against)
    def test_kim_weak_against_hoa(self):
        """Kim bị Hỏa khắc"""
        assert Element.KIM.get_weak_against() == Element.HOA
    
    def test_moc_weak_against_kim(self):
        """Mộc bị Kim khắc"""
        assert Element.MOC.get_weak_against() == Element.KIM
    
    def test_tho_weak_against_moc(self):
        """Thổ bị Mộc khắc"""
        assert Element.THO.get_weak_against() == Element.MOC
    
    def test_thuy_weak_against_tho(self):
        """Thủy bị Thổ khắc"""
        assert Element.THUY.get_weak_against() == Element.THO
    
    def test_hoa_weak_against_thuy(self):
        """Hỏa bị Thủy khắc"""
        assert Element.HOA.get_weak_against() == Element.THUY


class TestElementMultiplier:
    """Test damage multiplier calculations"""
    
    def test_strong_element_multiplier(self):
        """Attacking with advantage gives 1.5x damage"""
        multiplier = Element.KIM.calculate_multiplier(Element.MOC)
        assert multiplier == 1.5
    
    def test_weak_element_multiplier(self):
        """Attacking with disadvantage gives 0.7x damage"""
        multiplier = Element.KIM.calculate_multiplier(Element.HOA)
        assert multiplier == 0.7
    
    def test_neutral_element_multiplier(self):
        """Neutral matchup gives 1.0x damage"""
        multiplier = Element.KIM.calculate_multiplier(Element.THUY)
        assert multiplier == 1.0
    
    def test_same_element_multiplier(self):
        """Same element matchup gives 1.0x damage"""
        multiplier = Element.KIM.calculate_multiplier(Element.KIM)
        assert multiplier == 1.0
    
    def test_all_strong_matchups_give_bonus(self):
        """All strong matchups should give 1.5x"""
        matchups = [
            (Element.KIM, Element.MOC),
            (Element.MOC, Element.THO),
            (Element.THO, Element.THUY),
            (Element.THUY, Element.HOA),
            (Element.HOA, Element.KIM),
        ]
        for attacker, defender in matchups:
            assert attacker.calculate_multiplier(defender) == 1.5


class TestElementColors:
    """Test element color representations"""
    
    def test_kim_color_is_gold(self):
        """Kim (Metal) is gold colored"""
        assert Element.KIM.get_color() == "#FFD700"
    
    def test_moc_color_is_green(self):
        """Mộc (Wood) is green colored"""
        assert Element.MOC.get_color() == "#228B22"
    
    def test_thuy_color_is_blue(self):
        """Thủy (Water) is blue colored"""
        assert Element.THUY.get_color() == "#1E90FF"
    
    def test_hoa_color_is_red(self):
        """Hỏa (Fire) is red/orange colored"""
        assert Element.HOA.get_color() == "#FF4500"
    
    def test_tho_color_is_brown(self):
        """Thổ (Earth) is brown colored"""
        assert Element.THO.get_color() == "#8B4513"
