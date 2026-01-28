"""
Game Engine
Main game loop and initialization
"""
import pygame
from game.core.scene_manager import SceneManager
from game.scenes.main_menu import MainMenuScene
from game.scenes.demo_scene import DemoScene
from game.scenes.battle_scene import BattleScene
from game.utils.settings import Settings


class GameEngine:
    """Main game engine class"""
    
    def __init__(self):
        """Initialize game engine"""
        pygame.init()
        
        # Try to initialize audio, but continue if it fails (e.g., in headless environments)
        try:
            pygame.mixer.init()
        except pygame.error:
            print("Warning: Could not initialize audio device. Continuing without audio.")
        
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Ngọa Long Tam Quốc")
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Core systems
        self.scene_manager = SceneManager(self)
        
        # Register scenes
        self.scene_manager.register_scene("main_menu", MainMenuScene)
        self.scene_manager.register_scene("demo", DemoScene)
        self.scene_manager.register_scene("battle", BattleScene)
        
    def run(self):
        """Main game loop"""
        # Start with main menu
        self.scene_manager.change_scene("main_menu")
        
        while self.running:
            dt = self.clock.tick(self.settings.FPS) / 1000.0
            
            # Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.scene_manager.current_scene.handle_event(event)
            
            # Update current scene
            self.scene_manager.update(dt)
            
            # Render
            self.screen.fill((0, 0, 0))
            self.scene_manager.render(self.screen)
            pygame.display.flip()
        
        pygame.quit()
    
    def change_scene(self, scene_name: str, **kwargs):
        """
        Change to a different scene
        
        Args:
            scene_name: Name of the scene to change to
            **kwargs: Additional arguments to pass to scene
        """
        self.scene_manager.change_scene(scene_name, **kwargs)
    
    def quit(self):
        """Exit the game"""
        self.running = False


def main():
    """Main entry point"""
    engine = GameEngine()
    engine.run()


if __name__ == "__main__":
    main()
