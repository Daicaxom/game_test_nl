"""
Tests for HexagonChart UI component
Following TDD approach
"""
import pytest
import pygame
from game.ui.components.hexagon_chart import HexagonChart


# Initialize pygame for testing
pygame.init()
pygame.display.set_mode((100, 100), pygame.HIDDEN)


class TestHexagonChartCreation:
    """Test HexagonChart component creation"""
    
    def test_create_hexagon_chart_with_stats(self):
        """Should create hexagon chart with stat values"""
        stats = {
            'HP': 100,
            'ATK': 80,
            'DEF': 70,
            'SPD': 90,
            'CRIT': 60,
            'DEX': 75
        }
        chart = HexagonChart(position=(50, 50), stats=stats)
        
        assert chart.stats == stats
        assert chart.center_x == 50
        assert chart.center_y == 50
    
    def test_create_hexagon_chart_with_custom_radius(self):
        """Should create hexagon chart with custom radius"""
        stats = {'HP': 100, 'ATK': 80, 'DEF': 70, 'SPD': 90, 'CRIT': 60, 'DEX': 75}
        chart = HexagonChart(position=(50, 50), stats=stats, radius=80)
        
        assert chart.radius == 80
    
    def test_hexagon_chart_normalizes_stats(self):
        """Should normalize stats to 0-1 range"""
        stats = {'HP': 100, 'ATK': 50, 'DEF': 0, 'SPD': 200, 'CRIT': 25, 'DEX': 150}
        chart = HexagonChart(position=(50, 50), stats=stats, max_value=200)
        
        normalized = chart.get_normalized_stats()
        
        assert normalized['HP'] == 0.5  # 100/200
        assert normalized['SPD'] == 1.0  # 200/200
        assert normalized['DEF'] == 0.0  # 0/200


class TestHexagonChartCalculations:
    """Test HexagonChart calculations"""
    
    def test_calculate_hexagon_vertices(self):
        """Should calculate 6 vertices for hexagon"""
        stats = {'HP': 100, 'ATK': 100, 'DEF': 100, 'SPD': 100, 'CRIT': 100, 'DEX': 100}
        chart = HexagonChart(position=(100, 100), stats=stats, radius=50)
        
        vertices = chart.calculate_vertices()
        
        assert len(vertices) == 6
        # All vertices should be tuples of (x, y)
        for vertex in vertices:
            assert isinstance(vertex, tuple)
            assert len(vertex) == 2


class TestHexagonChartRendering:
    """Test HexagonChart component rendering"""
    
    def test_hexagon_chart_renders_without_error(self):
        """Hexagon chart should render to a surface without error"""
        stats = {'HP': 100, 'ATK': 80, 'DEF': 70, 'SPD': 90, 'CRIT': 60, 'DEX': 75}
        chart = HexagonChart(position=(100, 100), stats=stats)
        screen = pygame.Surface((300, 300))
        
        # Should not raise exception
        chart.render(screen)
