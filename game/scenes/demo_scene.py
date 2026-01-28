"""
Demo Scene
Showcases all implemented UI components
"""
import pygame
from game.scenes.base_scene import BaseScene
from game.ui.components.button import Button
from game.ui.components.health_bar import HealthBar
from game.ui.components.mana_bar import ManaBar
from game.ui.components.hexagon_chart import HexagonChart
from game.utils.colors import Colors
from game.utils.settings import Settings


class DemoScene(BaseScene):
    """Demo scene showing all UI components"""
    
    def __init__(self, engine):
        """
        Initialize demo scene
        
        Args:
            engine: Reference to the game engine
        """
        super().__init__(engine)
        self.settings = Settings()
        self.components = []
        self.health_bar = None
        self.mana_bar = None
        self.time_elapsed = 0
        
    def on_enter(self):
        """Called when scene becomes active"""
        # Initialize fonts
        self.title_font = pygame.font.Font(None, 48)
        self.label_font = pygame.font.Font(None, 24)
        
        # Create demo buttons
        self.components.append(
            Button(
                position=(50, 100),
                size=(150, 40),
                text="Normal Button",
                on_click=lambda: print("Normal clicked")
            )
        )
        
        self.components.append(
            Button(
                position=(220, 100),
                size=(150, 40),
                text="Disabled",
                disabled=True
            )
        )
        
        # Health and mana bars
        self.health_bar = HealthBar(
            position=(50, 180),
            width=200,
            height=20,
            current=80,
            maximum=100
        )
        
        self.mana_bar = ManaBar(
            position=(50, 220),
            width=200,
            height=20,
            current=50,
            maximum=100
        )
        
        # Hexagon chart showing character stats
        self.hexagon_chart = HexagonChart(
            position=(550, 250),
            stats={
                'HP': 100,
                'ATK': 85,
                'DEF': 70,
                'SPD': 95,
                'CRIT': 60,
                'DEX': 80
            },
            radius=80
        )
        
        # Back button
        self.components.append(
            Button(
                position=(50, 600),
                size=(150, 40),
                text="Back to Menu",
                on_click=self._on_back
            )
        )
    
    def on_exit(self):
        """Called when scene is deactivated"""
        self.components.clear()
        self.health_bar = None
        self.mana_bar = None
        self.hexagon_chart = None
    
    def on_pause(self):
        """Called when scene is paused"""
        pass
    
    def on_resume(self):
        """Called when scene is resumed"""
        pass
    
    def update(self, dt: float):
        """
        Update demo scene
        
        Args:
            dt: Delta time in seconds
        """
        self.time_elapsed += dt
        
        # Update all components
        for component in self.components:
            component.update(dt)
        
        if self.health_bar:
            self.health_bar.update(dt)
        
        if self.mana_bar:
            self.mana_bar.update(dt)
            
        # Animate mana bar filling up
        if self.time_elapsed > 1.0:
            self.mana_bar.current = min(self.mana_bar.current + dt * 10, 100)
    
    def render(self, screen: pygame.Surface):
        """
        Render demo scene
        
        Args:
            screen: Pygame surface to render to
        """
        # Background
        screen.fill(Colors.BACKGROUND)
        
        # Title
        title_surface = self.title_font.render("UI Components Demo", True, Colors.TEXT)
        screen.blit(title_surface, (50, 30))
        
        # Section labels
        # Buttons section
        label = self.label_font.render("Buttons:", True, Colors.TEXT_SECONDARY)
        screen.blit(label, (50, 70))
        
        # Bars section
        label = self.label_font.render("Health & Mana Bars:", True, Colors.TEXT_SECONDARY)
        screen.blit(label, (50, 150))
        
        # Hexagon section
        label = self.label_font.render("Character Stats (Hexagon Chart):", True, Colors.TEXT_SECONDARY)
        screen.blit(label, (400, 70))
        
        # Render all components
        for component in self.components:
            component.render(screen)
        
        if self.health_bar:
            self.health_bar.render(screen)
        
        if self.mana_bar:
            self.mana_bar.render(screen)
        
        if self.hexagon_chart:
            self.hexagon_chart.render(screen)
        
        # Display element colors
        label = self.label_font.render("Element Colors:", True, Colors.TEXT_SECONDARY)
        screen.blit(label, (50, 300))
        
        elements = [
            ("Kim (Metal)", Colors.ELEMENT_KIM),
            ("Mộc (Wood)", Colors.ELEMENT_MOC),
            ("Thủy (Water)", Colors.ELEMENT_THUY),
            ("Hỏa (Fire)", Colors.ELEMENT_HOA),
            ("Thổ (Earth)", Colors.ELEMENT_THO),
        ]
        
        y_offset = 330
        for name, color in elements:
            # Color box
            pygame.draw.rect(screen, color, (50, y_offset, 30, 30))
            pygame.draw.rect(screen, Colors.TEXT, (50, y_offset, 30, 30), 1)
            # Label
            text = self.label_font.render(name, True, Colors.TEXT)
            screen.blit(text, (90, y_offset + 5))
            y_offset += 40
    
    def handle_event(self, event: pygame.event.Event):
        """
        Handle pygame events
        
        Args:
            event: Pygame event
        """
        for component in self.components:
            component.handle_event(event)
    
    def _on_back(self):
        """Handle back button click"""
        self.engine.change_scene("main_menu")
