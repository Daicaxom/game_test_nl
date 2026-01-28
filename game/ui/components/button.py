"""
Button UI Component
"""
import pygame
from typing import Callable, Optional, Tuple


class Button:
    """Interactive button component"""
    
    def __init__(
        self,
        position: Tuple[int, int],
        size: Tuple[int, int] = (120, 40),
        text: str = "",
        font_size: int = 18,
        color: Tuple[int, int, int] = (70, 130, 180),
        hover_color: Tuple[int, int, int] = (100, 160, 210),
        text_color: Tuple[int, int, int] = (255, 255, 255),
        on_click: Optional[Callable] = None,
        disabled: bool = False
    ):
        """
        Initialize button component
        
        Args:
            position: (x, y) position of the button
            size: (width, height) of the button
            text: Button text
            font_size: Font size for the text
            color: Normal button color
            hover_color: Color when hovered
            text_color: Text color
            on_click: Callback function when clicked
            disabled: Whether button is disabled
        """
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.on_click = on_click
        self.disabled = disabled
        
        self.is_hovered = False
        self.is_pressed = False
    
    def update(self, dt: float):
        """
        Update button state
        
        Args:
            dt: Delta time in seconds
        """
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos) and not self.disabled
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame events
        
        Args:
            event: Pygame event
            
        Returns:
            True if event was handled
        """
        if self.disabled:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                self.is_pressed = True
                return True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.is_pressed:
                self.is_pressed = False
                if self.is_hovered and self.on_click:
                    self.on_click()
                return True
        
        return False
    
    def render(self, screen: pygame.Surface):
        """
        Render button to screen
        
        Args:
            screen: Pygame surface to render to
        """
        # Background
        color = self.hover_color if self.is_hovered else self.color
        if self.disabled:
            color = (128, 128, 128)
        
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=5)
        
        # Text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
