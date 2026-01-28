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
from game.ui.components.card import Card
from game.ui.components.grid import Grid
from game.ui.components.modal import Modal
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
        self.cards = []
        self.grid = None
        self.modal = None
        
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
                position=(50, 650),
                size=(150, 40),
                text="Back to Menu",
                on_click=self._on_back
            )
        )
        
        # Show Modal button
        self.components.append(
            Button(
                position=(220, 650),
                size=(150, 40),
                text="Show Modal",
                on_click=self._show_modal
            )
        )
        
        # Create character cards
        self.cards = [
            Card(
                position=(750, 100),
                size=(100, 130),
                name="Lưu Bị",
                element="Mộc",
                rarity=5,
                stats={"HP": 100, "ATK": 70},
                on_click=lambda: print("Lưu Bị clicked")
            ),
            Card(
                position=(860, 100),
                size=(100, 130),
                name="Quan Vũ",
                element="Kim",
                rarity=5,
                stats={"HP": 100, "ATK": 90},
                on_click=lambda: print("Quan Vũ clicked")
            ),
            Card(
                position=(970, 100),
                size=(100, 130),
                name="Trương Phi",
                element="Hỏa",
                rarity=4,
                stats={"HP": 80, "ATK": 85},
                on_click=lambda: print("Trương Phi clicked")
            ),
        ]
        
        # Create battle grid demo
        self.grid = Grid(
            position=(750, 280),
            cell_size=60,
            spacing=5,
            on_cell_click=self._on_grid_cell_click
        )
        
        # Add some content to grid cells
        self.grid.set_cell_content(0, 1, {"name": "LB", "element": "Mộc"})
        self.grid.set_cell_content(1, 0, {"name": "QV", "element": "Kim"})
        self.grid.set_cell_content(1, 2, {"name": "TP", "element": "Hỏa"})
    
    def on_exit(self):
        """Called when scene is deactivated"""
        self.components.clear()
        self.health_bar = None
        self.mana_bar = None
        self.hexagon_chart = None
        self.cards = []
        self.grid = None
        self.modal = None
    
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
        
        # Update cards
        for card in self.cards:
            card.update(dt)
        
        # Update grid
        if self.grid:
            self.grid.update(dt)
        
        # Update modal
        if self.modal:
            self.modal.update(dt)
    
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
        
        # Cards section
        label = self.label_font.render("Character Cards:", True, Colors.TEXT_SECONDARY)
        screen.blit(label, (750, 70))
        
        for card in self.cards:
            card.render(screen)
        
        # Grid section
        label = self.label_font.render("Battle Grid (3x3):", True, Colors.TEXT_SECONDARY)
        screen.blit(label, (750, 250))
        
        if self.grid:
            self.grid.render(screen)
        
        # Grid instructions
        instr = self.label_font.render("Click cells to select", True, Colors.TEXT_SECONDARY)
        screen.blit(instr, (750, 490))
        
        # Render modal on top if visible
        if self.modal:
            self.modal.render(screen)
    
    def handle_event(self, event: pygame.event.Event):
        """
        Handle pygame events
        
        Args:
            event: Pygame event
        """
        # Modal handles events first if visible
        if self.modal and self.modal.visible:
            self.modal.handle_event(event)
            return
        
        for component in self.components:
            component.handle_event(event)
        
        for card in self.cards:
            card.handle_event(event)
        
        if self.grid:
            self.grid.handle_event(event)
    
    def _on_back(self):
        """Handle back button click"""
        self.engine.change_scene("main_menu")
    
    def _show_modal(self):
        """Show demo modal"""
        self.modal = Modal(
            position=(self.settings.SCREEN_WIDTH // 2 - 200, self.settings.SCREEN_HEIGHT // 2 - 150),
            size=(400, 300),
            title="Demo Modal",
            content="This is a demonstration of the Modal component. It supports:\n\n• Title and content text\n• Multiple buttons\n• Click outside to close\n• Press ESC to close",
            buttons=[
                {"text": "OK", "on_click": self._close_modal},
                {"text": "Cancel", "on_click": self._close_modal}
            ]
        )
    
    def _close_modal(self):
        """Close the modal"""
        if self.modal:
            self.modal.hide()
            self.modal = None
    
    def _on_grid_cell_click(self, row: int, col: int):
        """Handle grid cell click"""
        self.grid.select_cell(row, col)
        print(f"Grid cell clicked: ({row}, {col})")
