"""
Tests for Settings module
"""
from game.utils.settings import Settings


class TestSettings:
    """Test game settings"""
    
    def test_display_settings_defined(self):
        """Display settings should have proper values"""
        assert Settings.SCREEN_WIDTH > 0
        assert Settings.SCREEN_HEIGHT > 0
        assert Settings.FPS > 0
        assert isinstance(Settings.FULLSCREEN, bool)
    
    def test_api_settings_defined(self):
        """API settings should be defined"""
        assert isinstance(Settings.API_BASE_URL, str)
        assert 'http' in Settings.API_BASE_URL
    
    def test_game_settings_defined(self):
        """Game-specific settings should be defined"""
        assert Settings.MAX_TEAM_SIZE == 5
        assert Settings.GRID_SIZE == 3
    
    def test_ui_settings_defined(self):
        """UI settings should be defined"""
        assert isinstance(Settings.FONT_PATH, str)
        assert Settings.DEFAULT_FONT_SIZE > 0
    
    def test_audio_settings_defined(self):
        """Audio settings should be in valid range"""
        assert 0.0 <= Settings.DEFAULT_BGM_VOLUME <= 1.0
        assert 0.0 <= Settings.DEFAULT_SFX_VOLUME <= 1.0
