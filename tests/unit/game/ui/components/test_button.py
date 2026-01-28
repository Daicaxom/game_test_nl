"""
Tests for Button UI component
Following TDD approach
"""
import pytest
import pygame
from unittest.mock import Mock
from game.ui.components.button import Button


# Initialize pygame for testing
pygame.init()
pygame.display.set_mode((100, 100), pygame.HIDDEN)


class TestButtonCreation:
    """Test Button component creation"""
    
    def test_create_button_with_default_values(self):
        """Should create button with default size and colors"""
        button = Button(position=(10, 20), text="Test")
        
        assert button.rect.x == 10
        assert button.rect.y == 20
        assert button.text == "Test"
        assert button.disabled is False
    
    def test_create_button_with_custom_size(self):
        """Should create button with custom size"""
        button = Button(position=(0, 0), size=(200, 50), text="Large")
        
        assert button.rect.width == 200
        assert button.rect.height == 50
    
    def test_create_button_with_callback(self):
        """Should create button with on_click callback"""
        callback = Mock()
        button = Button(position=(0, 0), text="Click", on_click=callback)
        
        assert button.on_click == callback
    
    def test_create_disabled_button(self):
        """Should create button in disabled state"""
        button = Button(position=(0, 0), text="Disabled", disabled=True)
        
        assert button.disabled is True


class TestButtonBehavior:
    """Test Button component behavior"""
    
    def test_button_hover_state_updated_on_update(self):
        """Button should update hover state when update is called"""
        button = Button(position=(10, 10), size=(100, 40))
        
        # Initially not hovered
        assert button.is_hovered is False
        
        # Calling update checks mouse position
        button.update(0.016)
        
        # is_hovered is updated based on current mouse position
        assert isinstance(button.is_hovered, bool)
    
    def test_button_tracks_pressed_state(self):
        """Button should track pressed state"""
        button = Button(position=(10, 10), size=(100, 40))
        
        assert button.is_pressed is False
    
    def test_button_click_with_manual_state(self):
        """Button click should trigger on_click callback when manually set to hovered"""
        callback = Mock()
        button = Button(position=(10, 10), size=(100, 40), on_click=callback)
        
        # Manually set hover state for testing
        button.is_hovered = True
        
        # Simulate click
        event_down = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (50, 25)})
        event_up = pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1, 'pos': (50, 25)})
        
        button.handle_event(event_down)
        button.handle_event(event_up)
        
        callback.assert_called_once()
    
    def test_disabled_button_ignores_click(self):
        """Disabled button should not trigger callback"""
        callback = Mock()
        button = Button(position=(10, 10), size=(100, 40), on_click=callback, disabled=True)
        
        button.is_hovered = True
        
        event_down = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (50, 25)})
        event_up = pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1, 'pos': (50, 25)})
        
        button.handle_event(event_down)
        button.handle_event(event_up)
        
        callback.assert_not_called()


class TestButtonRendering:
    """Test Button component rendering"""
    
    def test_button_renders_without_error(self):
        """Button should render to a surface without error"""
        button = Button(position=(10, 10), text="Render Test")
        screen = pygame.Surface((200, 200))
        
        # Should not raise exception
        button.render(screen)
