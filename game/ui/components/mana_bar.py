"""
ManaBar UI Component
"""
import pygame
from typing import Tuple


class ManaBar:
    """Mana bar display component with smooth animations"""
    
    def __init__(
        self,
        position: Tuple[int, int],
        width: int = 100,
        height: int = 10,
        current: int = 0,
        maximum: int = 100,
        bg_color: Tuple[int, int, int] = (50, 50, 50),
        fill_color: Tuple[int, int, int] = (0, 150, 255),
        border_color: Tuple[int, int, int] = (255, 255, 255)
    ):
        """
        Initialize mana bar component
        
        Args:
            position: (x, y) position of the mana bar
            width: Width of the mana bar
            height: Height of the mana bar
            current: Current mana value
            maximum: Maximum mana value
            bg_color: Background color
            fill_color: Fill color for mana
            border_color: Border color
        """
        self.rect = pygame.Rect(position[0], position[1], width, height)
        self.current = current
        self.maximum = maximum
        self.bg_color = bg_color
        self.fill_color = fill_color
        self.border_color = border_color
        
        # Animation
        self.displayed_value = current
        self.animation_speed = 50  # Mana per second
        
        # Pre-create font to avoid creating on every render
        self.font = pygame.font.Font(None, 12)
    
    @property
    def percentage(self) -> float:
        """
        Calculate current mana percentage
        
        Returns:
            Mana percentage (0.0 to 1.0)
        """
        return self.current / self.maximum if self.maximum > 0 else 0
    
    def update(self, dt: float):
        """
        Update mana bar animation
        
        Args:
            dt: Delta time in seconds
        """
        # Animate mana change
        if self.displayed_value != self.current:
            diff = self.current - self.displayed_value
            change = min(abs(diff), self.animation_speed * dt)
            self.displayed_value += change if diff > 0 else -change
    
    def render(self, screen: pygame.Surface):
        """
        Render mana bar to screen
        
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
        
        pygame.draw.rect(screen, self.fill_color, fill_rect)
        
        # Border
        pygame.draw.rect(screen, self.border_color, self.rect, 1)
        
        # Text (optional)
        text = f"{int(self.displayed_value)}/{self.maximum}"
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
