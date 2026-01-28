"""
Script to capture screenshots of the UI components
Runs in virtual display mode for CI/headless environments
"""
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'

import pygame
from game.core.engine import GameEngine

def capture_screenshots():
    """Capture screenshots of different scenes"""
    # Initialize pygame with dummy video driver
    pygame.init()
    
    # Create game engine
    engine = GameEngine()
    
    # Create screenshots directory
    os.makedirs('screenshots', exist_ok=True)
    
    # Capture main menu
    print("Capturing main menu...")
    engine.scene_manager.change_scene("main_menu")
    engine.scene_manager.update(0.016)
    engine.screen.fill((0, 0, 0))
    engine.scene_manager.render(engine.screen)
    pygame.image.save(engine.screen, 'screenshots/main_menu.png')
    print("Saved screenshots/main_menu.png")
    
    # Capture demo scene
    print("Capturing demo scene...")
    engine.scene_manager.change_scene("demo")
    engine.scene_manager.update(0.016)
    engine.screen.fill((0, 0, 0))
    engine.scene_manager.render(engine.screen)
    pygame.image.save(engine.screen, 'screenshots/demo_ui_components.png')
    print("Saved screenshots/demo_ui_components.png")
    
    pygame.quit()
    print("Screenshots captured successfully!")

if __name__ == "__main__":
    capture_screenshots()
