"""
Tests for BaseScene abstract class
Following TDD approach
"""
import pytest
import pygame
from abc import ABC
from game.scenes.base_scene import BaseScene


# Initialize pygame for testing
pygame.init()


class ConcreteScene(BaseScene):
    """Concrete implementation of BaseScene for testing"""
    
    def __init__(self, engine):
        super().__init__(engine)
        self.entered = False
        self.exited = False
        self.paused = False
        self.resumed = False
    
    def on_enter(self):
        self.entered = True
    
    def on_exit(self):
        self.exited = True
    
    def on_pause(self):
        self.paused = True
    
    def on_resume(self):
        self.resumed = True
    
    def update(self, dt: float):
        pass
    
    def render(self, screen: pygame.Surface):
        pass
    
    def handle_event(self, event: pygame.event.Event):
        pass


class TestBaseSceneCreation:
    """Test BaseScene creation"""
    
    def test_create_base_scene_with_engine(self):
        """Should create scene with engine reference"""
        mock_engine = type('MockEngine', (), {})()
        scene = ConcreteScene(mock_engine)
        
        assert scene.engine == mock_engine
    
    def test_base_scene_is_abstract(self):
        """BaseScene should be abstract and not directly instantiable"""
        assert issubclass(BaseScene, ABC)


class TestBaseSceneLifecycle:
    """Test BaseScene lifecycle methods"""
    
    def test_on_enter_called(self):
        """on_enter should be called when scene becomes active"""
        mock_engine = type('MockEngine', (), {})()
        scene = ConcreteScene(mock_engine)
        
        scene.on_enter()
        
        assert scene.entered is True
    
    def test_on_exit_called(self):
        """on_exit should be called when scene is deactivated"""
        mock_engine = type('MockEngine', (), {})()
        scene = ConcreteScene(mock_engine)
        
        scene.on_exit()
        
        assert scene.exited is True
    
    def test_on_pause_called(self):
        """on_pause should be called when scene is pushed to stack"""
        mock_engine = type('MockEngine', (), {})()
        scene = ConcreteScene(mock_engine)
        
        scene.on_pause()
        
        assert scene.paused is True
    
    def test_on_resume_called(self):
        """on_resume should be called when scene is popped back from stack"""
        mock_engine = type('MockEngine', (), {})()
        scene = ConcreteScene(mock_engine)
        
        scene.on_resume()
        
        assert scene.resumed is True


class TestBaseSceneAbstractMethods:
    """Test that abstract methods must be implemented"""
    
    def test_update_method_exists(self):
        """Scene should implement update method"""
        mock_engine = type('MockEngine', (), {})()
        scene = ConcreteScene(mock_engine)
        
        # Should not raise exception
        scene.update(0.016)
    
    def test_render_method_exists(self):
        """Scene should implement render method"""
        mock_engine = type('MockEngine', (), {})()
        scene = ConcreteScene(mock_engine)
        screen = pygame.Surface((100, 100))
        
        # Should not raise exception
        scene.render(screen)
    
    def test_handle_event_method_exists(self):
        """Scene should implement handle_event method"""
        mock_engine = type('MockEngine', (), {})()
        scene = ConcreteScene(mock_engine)
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_SPACE})
        
        # Should not raise exception
        scene.handle_event(event)
