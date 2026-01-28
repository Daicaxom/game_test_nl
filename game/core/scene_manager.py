"""
Scene Manager
Manages scene transitions and lifecycle
"""
from typing import Dict, Type, Optional, List
import pygame
from game.scenes.base_scene import BaseScene


class SceneManager:
    """Manages game scenes and transitions"""
    
    def __init__(self, engine):
        """
        Initialize scene manager
        
        Args:
            engine: Reference to the game engine
        """
        self.engine = engine
        self.scenes: Dict[str, Type[BaseScene]] = {}
        self.current_scene: Optional[BaseScene] = None
        self.scene_stack: List[BaseScene] = []
    
    def register_scene(self, name: str, scene_class: Type[BaseScene]):
        """
        Register a scene class
        
        Args:
            name: Scene identifier
            scene_class: Scene class to register
        """
        self.scenes[name] = scene_class
    
    def change_scene(self, name: str, **kwargs):
        """
        Change to a new scene
        
        Args:
            name: Name of the scene to change to
            **kwargs: Additional arguments to pass to scene constructor
        
        Raises:
            ValueError: If scene is not registered
        """
        if self.current_scene:
            self.current_scene.on_exit()
        
        scene_class = self.scenes.get(name)
        if not scene_class:
            raise ValueError(f"Scene '{name}' not registered")
        
        self.current_scene = scene_class(self.engine, **kwargs)
        self.current_scene.on_enter()
    
    def push_scene(self, name: str, **kwargs):
        """
        Push a new scene on top (for modals/overlays)
        
        Args:
            name: Name of the scene to push
            **kwargs: Additional arguments to pass to scene constructor
        """
        if self.current_scene:
            self.scene_stack.append(self.current_scene)
            self.current_scene.on_pause()
        
        self.change_scene(name, **kwargs)
    
    def pop_scene(self):
        """Return to previous scene"""
        if self.current_scene:
            self.current_scene.on_exit()
        
        if self.scene_stack:
            self.current_scene = self.scene_stack.pop()
            self.current_scene.on_resume()
    
    def update(self, dt: float):
        """
        Update current scene
        
        Args:
            dt: Delta time in seconds
        """
        if self.current_scene:
            self.current_scene.update(dt)
    
    def render(self, screen: pygame.Surface):
        """
        Render current scene
        
        Args:
            screen: Pygame surface to render to
        """
        if self.current_scene:
            self.current_scene.render(screen)
