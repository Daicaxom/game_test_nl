"""
HealthBar UI Component
"""
import pygame
from typing import Tuple


class HealthBar:
    """Health bar display component with smooth animations"""
    
    def __init__(
        self,
        position: Tuple[int, int],
        width: int = 100,
        height: int = 10,
        current: int = 100,
        maximum: int = 100,
        bg_color: Tuple[int, int, int] = (50, 50, 50),
        fill_color: Tuple[int, int, int] = (0, 200, 0),
        low_color: Tuple[int, int, int] = (200, 0, 0),
        border_color: Tuple[int, int, int] = (255, 255, 255)
    ):
        """
        Initialize health bar component
        
        Args:
            position: (x, y) position of the health bar
            width: Width of the health bar
            height: Height of the health bar
            current: Current health value
            maximum: Maximum health value
            bg_color: Background color
            fill_color: Fill color for healthy state
            low_color: Fill color for low health
            border_color: Border color
        """
        self.rect = pygame.Rect(position[0], position[1], width, height)
        self.current = current
        self.maximum = maximum
        self.bg_color = bg_color
        self.fill_color = fill_color
        self.low_color = low_color
        self.border_color = border_color
        
        # Animation
        self.displayed_value = current
        self.animation_speed = 50  # HP per second
        
        # Pre-create font to avoid creating on every render
        self.font = pygame.font.Font(None, 12)
    
    @property
    def percentage(self) -> float:
        """
        Calculate current health percentage
        
        Returns:
            Health percentage (0.0 to 1.0)
        """
        return self.current / self.maximum if self.maximum > 0 else 0
    
    def update(self, dt: float):
        """
        Update health bar animation
        
        Args:
            dt: Delta time in seconds
        """
        # Animate health change
        if self.displayed_value != self.current:
            diff = self.current - self.displayed_value
            change = min(abs(diff), self.animation_speed * dt)
            self.displayed_value += change if diff > 0 else -change
    
    def render(self, screen: pygame.Surface):
        """
        Render health bar to screen
        
        Args:
            screen: Pygame surface to render to
        """
        # Background
        pygame.draw.rect(screen, self.bg_color, self.rect)
        
        # Fill - use percentage property to avoid division by zero
        fill_width = int(self.rect.width * self.percentage)
        fill_rect = pygame.Rect(
            self.rect.x, self.rect.y,
            fill_width, self.rect.height
        )
        
        # Color based on health percentage
        color = self.low_color if self.percentage < 0.3 else self.fill_color
        pygame.draw.rect(screen, color, fill_rect)
        
        # Border
        pygame.draw.rect(screen, self.border_color, self.rect, 1)
        
        # Text (optional)
        text = f"{int(self.displayed_value)}/{self.maximum}"
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
