"""
Tests for SceneManager
Following TDD approach
"""
import pytest
import pygame
from game.core.scene_manager import SceneManager
from game.scenes.base_scene import BaseScene


# Initialize pygame for testing
pygame.init()


class TestScene1(BaseScene):
    """Test scene 1"""
    def __init__(self, engine): 
        super().__init__(engine)
        self.name = "TestScene1"
    def on_enter(self): pass
    def on_exit(self): pass
    def on_pause(self): pass
    def on_resume(self): pass
    def update(self, dt: float): pass
    def render(self, screen: pygame.Surface): pass
    def handle_event(self, event: pygame.event.Event): pass


class TestScene2(BaseScene):
    """Test scene 2"""
    def __init__(self, engine): 
        super().__init__(engine)
        self.name = "TestScene2"
    def on_enter(self): pass
    def on_exit(self): pass
    def on_pause(self): pass
    def on_resume(self): pass
    def update(self, dt: float): pass
    def render(self, screen: pygame.Surface): pass
    def handle_event(self, event: pygame.event.Event): pass


class TestSceneManagerCreation:
    """Test SceneManager creation"""
    
    def test_create_scene_manager_with_engine(self):
        """Should create scene manager with engine reference"""
        mock_engine = type('MockEngine', (), {})()
        manager = SceneManager(mock_engine)
        
        assert manager.engine == mock_engine
        assert manager.current_scene is None
        assert len(manager.scene_stack) == 0


class TestSceneRegistration:
    """Test scene registration"""
    
    def test_register_scene_class(self):
        """Should register a scene class by name"""
        mock_engine = type('MockEngine', (), {})()
        manager = SceneManager(mock_engine)
        
        manager.register_scene("test1", TestScene1)
        
        assert "test1" in manager.scenes
        assert manager.scenes["test1"] == TestScene1
    
    def test_register_multiple_scenes(self):
        """Should register multiple scene classes"""
        mock_engine = type('MockEngine', (), {})()
        manager = SceneManager(mock_engine)
        
        manager.register_scene("test1", TestScene1)
        manager.register_scene("test2", TestScene2)
        
        assert len(manager.scenes) == 2


class TestSceneChange:
    """Test scene changing"""
    
    def test_change_to_registered_scene(self):
        """Should change to a registered scene"""
        mock_engine = type('MockEngine', (), {})()
        manager = SceneManager(mock_engine)
        manager.register_scene("test1", TestScene1)
        
        manager.change_scene("test1")
        
        assert manager.current_scene is not None
        assert isinstance(manager.current_scene, TestScene1)
    
    def test_change_scene_raises_error_for_unregistered(self):
        """Should raise error when changing to unregistered scene"""
        mock_engine = type('MockEngine', (), {})()
        manager = SceneManager(mock_engine)
        
        with pytest.raises(ValueError):
            manager.change_scene("nonexistent")
    
    def test_change_scene_exits_previous_scene(self):
        """Should call on_exit on previous scene when changing"""
        mock_engine = type('MockEngine', (), {})()
        manager = SceneManager(mock_engine)
        manager.register_scene("test1", TestScene1)
        manager.register_scene("test2", TestScene2)
        
        # Change to first scene
        manager.change_scene("test1")
        first_scene = manager.current_scene
        
        # Mock the on_exit to track if called
        exit_called = False
        original_exit = first_scene.on_exit
        def mock_exit():
            nonlocal exit_called
            exit_called = True
            original_exit()
        first_scene.on_exit = mock_exit
        
        # Change to second scene
        manager.change_scene("test2")
        
        assert exit_called


class TestSceneStack:
    """Test scene stack for overlays"""
    
    def test_push_scene_adds_to_stack(self):
        """Should push current scene to stack"""
        mock_engine = type('MockEngine', (), {})()
        manager = SceneManager(mock_engine)
        manager.register_scene("test1", TestScene1)
        manager.register_scene("test2", TestScene2)
        
        manager.change_scene("test1")
        manager.push_scene("test2")
        
        assert len(manager.scene_stack) == 1
    
    def test_pop_scene_returns_to_previous(self):
        """Should pop scene and return to previous"""
        mock_engine = type('MockEngine', (), {})()
        manager = SceneManager(mock_engine)
        manager.register_scene("test1", TestScene1)
        manager.register_scene("test2", TestScene2)
        
        manager.change_scene("test1")
        first_scene = manager.current_scene
        manager.push_scene("test2")
        manager.pop_scene()
        
        assert manager.current_scene == first_scene


class TestSceneManagerUpdate:
    """Test scene manager update and render"""
    
    def test_update_calls_current_scene(self):
        """Should call update on current scene"""
        mock_engine = type('MockEngine', (), {})()
        manager = SceneManager(mock_engine)
        manager.register_scene("test1", TestScene1)
        manager.change_scene("test1")
        
        # Mock update to track if called
        update_called = False
        def mock_update(dt):
            nonlocal update_called
            update_called = True
        manager.current_scene.update = mock_update
        
        manager.update(0.016)
        
        assert update_called
    
    def test_render_calls_current_scene(self):
        """Should call render on current scene"""
        mock_engine = type('MockEngine', (), {})()
        manager = SceneManager(mock_engine)
        manager.register_scene("test1", TestScene1)
        manager.change_scene("test1")
        
        # Mock render to track if called
        render_called = False
        def mock_render(screen):
            nonlocal render_called
            render_called = True
        manager.current_scene.render = mock_render
        
        screen = pygame.Surface((100, 100))
        manager.render(screen)
        
        assert render_called
