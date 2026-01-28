"""
HexagonChart UI Component
Displays character stats in a hexagonal radar chart
"""
import pygame
import math
from typing import Dict, Tuple, List


class HexagonChart:
    """Hexagon chart for displaying character stats"""
    
    def __init__(
        self,
        position: Tuple[int, int],
        stats: Dict[str, float],
        radius: int = 60,
        max_value: float = 100,
        line_color: Tuple[int, int, int] = (100, 100, 100),
        fill_color: Tuple[int, int, int] = (70, 130, 180),
        fill_alpha: int = 128
    ):
        """
        Initialize hexagon chart component
        
        Args:
            position: (x, y) center position of the chart
            stats: Dictionary of stat names and values (expects 6 stats)
            radius: Radius of the hexagon
            max_value: Maximum value for normalization
            line_color: Color for hexagon outline
            fill_color: Color for stat fill
            fill_alpha: Alpha transparency for fill (0-255)
        """
        self.center_x, self.center_y = position
        self.stats = stats
        self.radius = radius
        self.max_value = max_value
        self.line_color = line_color
        self.fill_color = fill_color
        self.fill_alpha = fill_alpha
        
        # Stat order for consistent hexagon layout
        self.stat_order = ['HP', 'ATK', 'DEF', 'SPD', 'CRIT', 'DEX']
    
    def get_normalized_stats(self) -> Dict[str, float]:
        """
        Normalize stats to 0-1 range
        
        Returns:
            Dictionary of normalized stat values
        """
        normalized = {}
        for stat_name, value in self.stats.items():
            normalized[stat_name] = min(value / self.max_value, 1.0)
        return normalized
    
    def calculate_vertices(self, scale: float = 1.0) -> List[Tuple[float, float]]:
        """
        Calculate hexagon vertices
        
        Args:
            scale: Scale factor for the hexagon (0-1 for inner hexagons)
            
        Returns:
            List of (x, y) vertex coordinates
        """
        vertices = []
        for i in range(6):
            # Start from top and go clockwise
            angle = math.radians(90 - i * 60)
            x = self.center_x + self.radius * scale * math.cos(angle)
            y = self.center_y - self.radius * scale * math.sin(angle)
            vertices.append((x, y))
        return vertices
    
    def render(self, screen: pygame.Surface):
        """
        Render hexagon chart to screen
        
        Args:
            screen: Pygame surface to render to
        """
        # Draw background grid lines (multiple hexagons at different scales)
        for scale in [0.25, 0.5, 0.75, 1.0]:
            vertices = self.calculate_vertices(scale)
            pygame.draw.polygon(screen, self.line_color, vertices, 1)
        
        # Draw axes from center to vertices
        outer_vertices = self.calculate_vertices(1.0)
        for vertex in outer_vertices:
            pygame.draw.line(
                screen,
                self.line_color,
                (self.center_x, self.center_y),
                vertex,
                1
            )
        
        # Calculate stat vertices
        normalized = self.get_normalized_stats()
        stat_vertices = []
        for i, stat_name in enumerate(self.stat_order):
            value = normalized.get(stat_name, 0)
            angle = math.radians(90 - i * 60)
            x = self.center_x + self.radius * value * math.cos(angle)
            y = self.center_y - self.radius * value * math.sin(angle)
            stat_vertices.append((x, y))
        
        # Draw filled stat polygon with transparency
        if len(stat_vertices) >= 3:
            # Create a temporary surface for alpha blending
            temp_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            pygame.draw.polygon(temp_surface, (*self.fill_color, self.fill_alpha), stat_vertices)
            screen.blit(temp_surface, (0, 0))
        
        # Draw stat polygon outline
        if len(stat_vertices) >= 3:
            pygame.draw.polygon(screen, self.fill_color, stat_vertices, 2)
        
        # Draw stat labels
        font = pygame.font.Font(None, 16)
        for i, stat_name in enumerate(self.stat_order):
            angle = math.radians(90 - i * 60)
            label_distance = self.radius + 20
            x = self.center_x + label_distance * math.cos(angle)
            y = self.center_y - label_distance * math.sin(angle)
            
            text_surface = font.render(stat_name, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(x, y))
            screen.blit(text_surface, text_rect)
