"""
Tests for HealthBar UI component
Following TDD approach
"""
import pytest
import pygame
from game.ui.components.health_bar import HealthBar


# Initialize pygame for testing
pygame.init()
pygame.display.set_mode((100, 100), pygame.HIDDEN)


class TestHealthBarCreation:
    """Test HealthBar component creation"""
    
    def test_create_health_bar_with_default_values(self):
        """Should create health bar with default values"""
        bar = HealthBar(position=(10, 20))
        
        assert bar.rect.x == 10
        assert bar.rect.y == 20
        assert bar.current == 100
        assert bar.maximum == 100
    
    def test_create_health_bar_with_custom_values(self):
        """Should create health bar with custom current and max values"""
        bar = HealthBar(position=(0, 0), current=75, maximum=150)
        
        assert bar.current == 75
        assert bar.maximum == 150
    
    def test_create_health_bar_with_custom_size(self):
        """Should create health bar with custom width and height"""
        bar = HealthBar(position=(0, 0), width=200, height=20)
        
        assert bar.rect.width == 200
        assert bar.rect.height == 20
    
    def test_health_bar_percentage_calculation(self):
        """Should calculate correct health percentage"""
        bar = HealthBar(position=(0, 0), current=50, maximum=100)
        
        assert bar.percentage == 0.5
    
    def test_health_bar_percentage_with_zero_max(self):
        """Should handle zero maximum gracefully"""
        bar = HealthBar(position=(0, 0), current=0, maximum=0)
        
        assert bar.percentage == 0


class TestHealthBarBehavior:
    """Test HealthBar component behavior"""
    
    def test_health_bar_updates_displayed_value(self):
        """Health bar should animate value changes"""
        bar = HealthBar(position=(0, 0), current=100, maximum=100)
        bar.displayed_value = 100
        
        # Change current health
        bar.current = 50
        
        # Update should animate towards new value
        bar.update(0.1)
        
        # Displayed value should be moving towards current
        assert bar.displayed_value != 100
        assert bar.displayed_value > 50
    
    def test_health_bar_animation_speed(self):
        """Health bar should have configurable animation speed"""
        bar = HealthBar(position=(0, 0), current=100, maximum=100)
        bar.animation_speed = 100  # 100 HP per second
        
        assert bar.animation_speed == 100


class TestHealthBarRendering:
    """Test HealthBar component rendering"""
    
    def test_health_bar_renders_without_error(self):
        """Health bar should render to a surface without error"""
        bar = HealthBar(position=(10, 10), current=80, maximum=100)
        screen = pygame.Surface((200, 200))
        
        # Should not raise exception
        bar.render(screen)
