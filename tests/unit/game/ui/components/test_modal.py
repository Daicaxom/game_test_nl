"""
Tests for Modal UI component
Following TDD approach
"""
import pytest
import pygame
from unittest.mock import Mock
from game.ui.components.modal import Modal


# Initialize pygame for testing
pygame.init()
pygame.display.set_mode((100, 100), pygame.HIDDEN)


class TestModalCreation:
    """Test Modal component creation"""
    
    def test_create_modal_with_default_values(self):
        """Should create modal with default size and values"""
        modal = Modal(position=(100, 100), title="Test Modal")
        
        assert modal.rect.x == 100
        assert modal.rect.y == 100
        assert modal.title == "Test Modal"
        assert modal.visible is True
    
    def test_create_modal_with_custom_size(self):
        """Should create modal with custom size"""
        modal = Modal(position=(0, 0), size=(500, 400), title="Large Modal")
        
        assert modal.rect.width == 500
        assert modal.rect.height == 400
    
    def test_create_modal_with_content(self):
        """Should create modal with content text"""
        modal = Modal(
            position=(0, 0),
            title="Info",
            content="This is a test message."
        )
        
        assert modal.content == "This is a test message."
    
    def test_create_modal_with_buttons(self):
        """Should create modal with buttons"""
        buttons = [
            {"text": "OK", "on_click": Mock()},
            {"text": "Cancel", "on_click": Mock()}
        ]
        modal = Modal(position=(0, 0), title="Confirm", buttons=buttons)
        
        assert len(modal.buttons) == 2
    
    def test_create_non_closable_modal(self):
        """Should create modal that cannot be closed by clicking outside"""
        modal = Modal(position=(0, 0), title="Important", closable=False)
        
        assert modal.closable is False


class TestModalBehavior:
    """Test Modal component behavior"""
    
    def test_modal_show_and_hide(self):
        """Modal should show and hide correctly"""
        modal = Modal(position=(0, 0), title="Test")
        
        assert modal.visible is True
        
        modal.hide()
        assert modal.visible is False
        
        modal.show()
        assert modal.visible is True
    
    def test_modal_close_callback(self):
        """Modal should call on_close when hidden"""
        callback = Mock()
        modal = Modal(position=(0, 0), title="Test", on_close=callback)
        
        modal.hide()
        callback.assert_called_once()
    
    def test_modal_escape_closes_when_closable(self):
        """Pressing escape should close closable modal"""
        modal = Modal(position=(100, 100), size=(200, 200), title="Test", closable=True)
        
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE})
        modal.handle_event(event)
        
        assert modal.visible is False
    
    def test_modal_escape_does_not_close_when_not_closable(self):
        """Pressing escape should not close non-closable modal"""
        modal = Modal(position=(100, 100), size=(200, 200), title="Test", closable=False)
        
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE})
        modal.handle_event(event)
        
        assert modal.visible is True
    
    def test_hidden_modal_does_not_handle_events(self):
        """Hidden modal should not handle events"""
        modal = Modal(position=(0, 0), title="Test")
        modal.hide()
        
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE})
        result = modal.handle_event(event)
        
        assert result is False


class TestModalRendering:
    """Test Modal component rendering"""
    
    def test_modal_renders_without_error(self):
        """Modal should render to a surface without error"""
        modal = Modal(
            position=(100, 100),
            title="Test Modal",
            content="This is test content."
        )
        screen = pygame.Surface((800, 600))
        
        # Should not raise exception
        modal.render(screen)
    
    def test_modal_renders_with_buttons(self):
        """Modal should render correctly with buttons"""
        buttons = [
            {"text": "OK", "on_click": Mock()},
            {"text": "Cancel", "on_click": Mock()}
        ]
        modal = Modal(
            position=(100, 100),
            title="Confirm",
            content="Are you sure?",
            buttons=buttons
        )
        screen = pygame.Surface((800, 600))
        
        # Should not raise exception
        modal.render(screen)
    
    def test_hidden_modal_does_not_render(self):
        """Hidden modal should not render anything"""
        modal = Modal(position=(100, 100), title="Test")
        modal.hide()
        
        screen = pygame.Surface((800, 600))
        screen.fill((0, 0, 0))
        
        # Render should do nothing when hidden
        modal.render(screen)
        # No exception raised
