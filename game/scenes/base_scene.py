"""
Base Scene abstract class
All game scenes inherit from this class
"""
from abc import ABC, abstractmethod
import pygame


class BaseScene(ABC):
    """Abstract base class for all game scenes"""
    
    def __init__(self, engine):
        """
        Initialize base scene
        
        Args:
            engine: Reference to the game engine
        """
        self.engine = engine
    
    @abstractmethod
    def on_enter(self):
        """Called when scene becomes active"""
        pass
    
    @abstractmethod
    def on_exit(self):
        """Called when scene is deactivated"""
        pass
    
    @abstractmethod
    def on_pause(self):
        """Called when scene is pushed to stack (overlayed by another scene)"""
        pass
    
    @abstractmethod
    def on_resume(self):
        """Called when scene is popped back from stack"""
        pass
    
    @abstractmethod
    def update(self, dt: float):
        """
        Update scene logic
        
        Args:
            dt: Delta time in seconds
        """
        pass
    
    @abstractmethod
    def render(self, screen: pygame.Surface):
        """
        Render scene to screen
        
        Args:
            screen: Pygame surface to render to
        """
        pass
    
    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        """
        Handle pygame events
        
        Args:
            event: Pygame event
        """
        pass
