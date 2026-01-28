"""
Tests for Card UI component
Following TDD approach
"""
import pytest
import pygame
from unittest.mock import Mock
from game.ui.components.card import Card


# Initialize pygame for testing
pygame.init()
pygame.display.set_mode((100, 100), pygame.HIDDEN)


class TestCardCreation:
    """Test Card component creation"""
    
    def test_create_card_with_default_values(self):
        """Should create card with default size and values"""
        card = Card(position=(10, 20), name="Test Hero")
        
        assert card.rect.x == 10
        assert card.rect.y == 20
        assert card.name == "Test Hero"
        assert card.rarity == 1
    
    def test_create_card_with_custom_size(self):
        """Should create card with custom size"""
        card = Card(position=(0, 0), size=(150, 200), name="Large Card")
        
        assert card.rect.width == 150
        assert card.rect.height == 200
    
    def test_create_card_with_element(self):
        """Should create card with element type"""
        card = Card(position=(0, 0), name="Fire Hero", element="Hỏa")
        
        assert card.element == "Hỏa"
    
    def test_create_card_with_rarity(self):
        """Should create card with rarity level"""
        card = Card(position=(0, 0), name="Legendary", rarity=5)
        
        assert card.rarity == 5
    
    def test_create_card_with_stats(self):
        """Should create card with stats"""
        stats = {"HP": 100, "ATK": 50, "DEF": 30}
        card = Card(position=(0, 0), name="Hero", stats=stats)
        
        assert card.stats == stats
    
    def test_create_card_with_callback(self):
        """Should create card with on_click callback"""
        callback = Mock()
        card = Card(position=(0, 0), name="Clickable", on_click=callback)
        
        assert card.on_click == callback


class TestCardBehavior:
    """Test Card component behavior"""
    
    def test_card_hover_state_updated_on_update(self):
        """Card should update hover state when update is called"""
        card = Card(position=(10, 10), size=(100, 100))
        
        assert card.is_hovered is False
        card.update(0.016)
        assert isinstance(card.is_hovered, bool)
    
    def test_card_click_with_manual_state(self):
        """Card click should trigger on_click callback"""
        callback = Mock()
        card = Card(position=(10, 10), size=(100, 100), on_click=callback)
        
        card.is_hovered = True
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (50, 50)})
        card.handle_event(event)
        
        callback.assert_called_once()
    
    def test_card_selection_state(self):
        """Card should track selection state"""
        card = Card(position=(0, 0), name="Hero", selected=True)
        
        assert card.selected is True


class TestCardRendering:
    """Test Card component rendering"""
    
    def test_card_renders_without_error(self):
        """Card should render to a surface without error"""
        card = Card(
            position=(10, 10),
            name="Test Hero",
            element="Kim",
            rarity=3,
            stats={"HP": 100, "ATK": 50}
        )
        screen = pygame.Surface((200, 300))
        
        # Should not raise exception
        card.render(screen)
    
    def test_card_renders_with_all_elements(self):
        """Card should render correctly for all element types"""
        elements = ["Kim", "Mộc", "Thủy", "Hỏa", "Thổ"]
        screen = pygame.Surface((200, 300))
        
        for element in elements:
            card = Card(position=(10, 10), name="Hero", element=element)
            card.render(screen)  # Should not raise
    
    def test_card_renders_all_rarities(self):
        """Card should render correctly for all rarity levels"""
        screen = pygame.Surface((200, 300))
        
        for rarity in range(1, 7):
            card = Card(position=(10, 10), name="Hero", rarity=rarity)
            card.render(screen)  # Should not raise
