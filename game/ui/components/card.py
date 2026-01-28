"""
Card UI Component
Displays character or item cards with stats and rarity
"""
import pygame
from typing import Tuple, Optional, Dict, Callable


class Card:
    """Card component for displaying characters or items"""
    
    def __init__(
        self,
        position: Tuple[int, int],
        size: Tuple[int, int] = (120, 160),
        name: str = "",
        element: Optional[str] = None,
        rarity: int = 1,
        stats: Optional[Dict[str, int]] = None,
        image: Optional[pygame.Surface] = None,
        bg_color: Tuple[int, int, int] = (40, 40, 60),
        border_width: int = 2,
        on_click: Optional[Callable] = None,
        selected: bool = False
    ):
        """
        Initialize card component
        
        Args:
            position: (x, y) position of the card
            size: (width, height) of the card
            name: Character or item name
            element: Element type (Kim, Mộc, Thủy, Hỏa, Thổ)
            rarity: Rarity level 1-6
            stats: Optional dictionary of stats to display
            image: Optional character/item image
            bg_color: Background color
            border_width: Width of the border
            on_click: Callback when card is clicked
            selected: Whether card is currently selected
        """
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.name = name
        self.element = element
        self.rarity = rarity
        self.stats = stats or {}
        self.image = image
        self.bg_color = bg_color
        self.border_width = border_width
        self.on_click = on_click
        self.selected = selected
        
        self.is_hovered = False
        
        # Pre-create fonts
        self.name_font = pygame.font.Font(None, 18)
        self.stat_font = pygame.font.Font(None, 14)
        
        # Rarity colors
        self.rarity_colors = {
            1: (150, 150, 150),   # Gray - Common
            2: (100, 200, 100),   # Green - Uncommon
            3: (100, 150, 255),   # Blue - Rare
            4: (200, 100, 255),   # Purple - Epic
            5: (255, 200, 50),    # Gold - Legendary
            6: (255, 100, 100),   # Red - Mythic
        }
        
        # Element colors
        self.element_colors = {
            "Kim": (255, 215, 0),     # Gold - Metal
            "Mộc": (34, 139, 34),     # Forest Green - Wood
            "Thủy": (30, 144, 255),   # Dodger Blue - Water
            "Hỏa": (255, 69, 0),      # Red Orange - Fire
            "Thổ": (139, 69, 19),     # Saddle Brown - Earth
        }
    
    def update(self, dt: float):
        """
        Update card state
        
        Args:
            dt: Delta time in seconds
        """
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame events
        
        Args:
            event: Pygame event
            
        Returns:
            True if event was handled
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                if self.on_click:
                    self.on_click()
                return True
        return False
    
    def render(self, screen: pygame.Surface):
        """
        Render card to screen
        
        Args:
            screen: Pygame surface to render to
        """
        # Background with hover effect
        bg = self.bg_color
        if self.is_hovered:
            bg = tuple(min(c + 20, 255) for c in self.bg_color)
        
        pygame.draw.rect(screen, bg, self.rect, border_radius=8)
        
        # Border with rarity color
        border_color = self.rarity_colors.get(self.rarity, (150, 150, 150))
        if self.selected:
            border_color = (255, 255, 255)
        pygame.draw.rect(screen, border_color, self.rect, self.border_width, border_radius=8)
        
        # Image area (top portion)
        image_rect = pygame.Rect(
            self.rect.x + 5,
            self.rect.y + 5,
            self.rect.width - 10,
            self.rect.height // 2 - 5
        )
        
        if self.image:
            # Scale image to fit
            scaled_image = pygame.transform.scale(self.image, (image_rect.width, image_rect.height))
            screen.blit(scaled_image, image_rect)
        else:
            # Placeholder with element color
            placeholder_color = (60, 60, 80)
            if self.element and self.element in self.element_colors:
                placeholder_color = self.element_colors[self.element]
            pygame.draw.rect(screen, placeholder_color, image_rect, border_radius=4)
        
        # Element indicator (small colored dot)
        if self.element and self.element in self.element_colors:
            element_color = self.element_colors[self.element]
            pygame.draw.circle(
                screen,
                element_color,
                (self.rect.x + self.rect.width - 15, self.rect.y + 15),
                8
            )
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (self.rect.x + self.rect.width - 15, self.rect.y + 15),
                8,
                1
            )
        
        # Name
        name_y = self.rect.y + self.rect.height // 2 + 5
        name_surface = self.name_font.render(self.name, True, (255, 255, 255))
        name_rect = name_surface.get_rect(centerx=self.rect.centerx, y=name_y)
        screen.blit(name_surface, name_rect)
        
        # Rarity stars
        star_y = name_y + 20
        star_x = self.rect.centerx - (self.rarity * 10) // 2
        star_color = self.rarity_colors.get(self.rarity, (150, 150, 150))
        for i in range(self.rarity):
            self._draw_star(screen, star_x + i * 10, star_y, 4, star_color)
        
        # Stats (if provided)
        if self.stats:
            stats_y = star_y + 15
            stat_text = " | ".join(f"{k}:{v}" for k, v in list(self.stats.items())[:3])
            stat_surface = self.stat_font.render(stat_text, True, (200, 200, 200))
            stat_rect = stat_surface.get_rect(centerx=self.rect.centerx, y=stats_y)
            screen.blit(stat_surface, stat_rect)
    
    def _draw_star(self, screen: pygame.Surface, x: int, y: int, size: int, color: Tuple[int, int, int]):
        """Draw a simple star shape"""
        # Simple diamond shape as star
        points = [
            (x, y - size),      # top
            (x + size, y),      # right
            (x, y + size),      # bottom
            (x - size, y),      # left
        ]
        pygame.draw.polygon(screen, color, points)
