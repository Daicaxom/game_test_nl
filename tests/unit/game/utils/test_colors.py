"""
Tests for Colors utility module
"""
from game.utils.colors import Colors


class TestColors:
    """Test color definitions"""
    
    def test_ui_colors_defined(self):
        """UI colors should be defined as RGB tuples"""
        assert isinstance(Colors.PRIMARY, tuple)
        assert len(Colors.PRIMARY) == 3
        assert all(0 <= c <= 255 for c in Colors.PRIMARY)
        
        assert isinstance(Colors.BACKGROUND, tuple)
        assert len(Colors.BACKGROUND) == 3
    
    def test_element_colors_defined(self):
        """All five element colors should be defined"""
        assert isinstance(Colors.ELEMENT_KIM, tuple)
        assert isinstance(Colors.ELEMENT_MOC, tuple)
        assert isinstance(Colors.ELEMENT_THUY, tuple)
        assert isinstance(Colors.ELEMENT_HOA, tuple)
        assert isinstance(Colors.ELEMENT_THO, tuple)
    
    def test_rarity_colors_defined(self):
        """All six rarity levels should have colors"""
        for i in range(1, 7):
            color = getattr(Colors, f'RARITY_{i}')
            assert isinstance(color, tuple)
            assert len(color) == 3
    
    def test_status_colors_defined(self):
        """Status colors for health and mana should be defined"""
        assert isinstance(Colors.HEALTH_HIGH, tuple)
        assert isinstance(Colors.HEALTH_MEDIUM, tuple)
        assert isinstance(Colors.HEALTH_LOW, tuple)
        assert isinstance(Colors.MANA, tuple)
