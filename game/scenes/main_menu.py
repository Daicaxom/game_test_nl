"""
Main Menu Scene
The initial scene shown when the game starts
"""
import pygame
from game.scenes.base_scene import BaseScene
from game.ui.components.button import Button
from game.utils.colors import Colors
from game.utils.settings import Settings


class MainMenuScene(BaseScene):
    """Main menu scene with start game, settings, and quit options"""
    
    def __init__(self, engine):
        """
        Initialize main menu scene
        
        Args:
            engine: Reference to the game engine
        """
        super().__init__(engine)
        self.settings = Settings()
        self.buttons = []
        self.title_font = None
        
    def on_enter(self):
        """Called when scene becomes active"""
        # Initialize title font
        self.title_font = pygame.font.Font(None, 72)
        
        # Create menu buttons
        screen_center_x = self.settings.SCREEN_WIDTH // 2
        start_y = 300
        button_spacing = 70
        
        # Start Game button
        self.buttons.append(
            Button(
                position=(screen_center_x - 100, start_y),
                size=(200, 50),
                text="Start Game",
                on_click=self._on_start_game
            )
        )
        
        # Settings button
        self.buttons.append(
            Button(
                position=(screen_center_x - 100, start_y + button_spacing),
                size=(200, 50),
                text="Settings",
                on_click=self._on_settings
            )
        )
        
        # Demo button
        self.buttons.append(
            Button(
                position=(screen_center_x - 100, start_y + button_spacing * 2),
                size=(200, 50),
                text="UI Demo",
                on_click=self._on_demo
            )
        )
        
        # Quit button
        self.buttons.append(
            Button(
                position=(screen_center_x - 100, start_y + button_spacing * 3),
                size=(200, 50),
                text="Quit",
                on_click=self._on_quit
            )
        )
    
    def on_exit(self):
        """Called when scene is deactivated"""
        self.buttons.clear()
    
    def on_pause(self):
        """Called when scene is paused"""
        pass
    
    def on_resume(self):
        """Called when scene is resumed"""
        pass
    
    def update(self, dt: float):
        """
        Update menu logic
        
        Args:
            dt: Delta time in seconds
        """
        for button in self.buttons:
            button.update(dt)
    
    def render(self, screen: pygame.Surface):
        """
        Render menu to screen
        
        Args:
            screen: Pygame surface to render to
        """
        # Background
        screen.fill(Colors.BACKGROUND)
        
        # Title
        title_text = "Ngọa Long Tam Quốc"
        title_surface = self.title_font.render(title_text, True, Colors.TEXT)
        title_rect = title_surface.get_rect(
            center=(self.settings.SCREEN_WIDTH // 2, 150)
        )
        screen.blit(title_surface, title_rect)
        
        # Buttons
        for button in self.buttons:
            button.render(screen)
    
    def handle_event(self, event: pygame.event.Event):
        """
        Handle pygame events
        
        Args:
            event: Pygame event
        """
        for button in self.buttons:
            button.handle_event(event)
    
    def _on_start_game(self):
        """Handle start game button click"""
        self.engine.change_scene("battle")
    
    def _on_settings(self):
        """Handle settings button click"""
        # TODO: Push settings scene
        pass
    
    def _on_demo(self):
        """Handle demo button click"""
        self.engine.change_scene("demo")
    
    def _on_quit(self):
        """Handle quit button click"""
        if hasattr(self.engine, 'quit'):
            self.engine.quit()
