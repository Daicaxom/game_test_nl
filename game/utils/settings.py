"""
Game settings and configuration
"""
import os


class Settings:
    """Game configuration settings"""
    
    # Display
    SCREEN_WIDTH: int = 1280
    SCREEN_HEIGHT: int = 720
    FPS: int = 60
    FULLSCREEN: bool = False
    
    # API
    API_BASE_URL: str = os.getenv('API_URL', 'http://localhost:8000/api/v1')
    
    # Game
    MAX_TEAM_SIZE: int = 5
    GRID_SIZE: int = 3
    
    # UI
    FONT_PATH: str = 'assets/fonts/NotoSansSC-Regular.ttf'
    DEFAULT_FONT_SIZE: int = 24
    
    # Audio
    DEFAULT_BGM_VOLUME: float = 0.7
    DEFAULT_SFX_VOLUME: float = 1.0
