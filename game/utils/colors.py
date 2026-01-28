"""
Color constants for the game UI
"""


class Colors:
    """Color definitions for UI elements and game states"""
    
    # UI Colors
    PRIMARY = (70, 130, 180)
    SECONDARY = (100, 160, 210)
    BACKGROUND = (20, 20, 40)
    TEXT = (255, 255, 255)
    TEXT_SECONDARY = (200, 200, 200)
    
    # Element Colors (Five Elements)
    ELEMENT_KIM = (255, 215, 0)      # Gold - Metal
    ELEMENT_MOC = (34, 139, 34)      # Forest Green - Wood
    ELEMENT_THUY = (30, 144, 255)    # Dodger Blue - Water
    ELEMENT_HOA = (255, 69, 0)       # Red Orange - Fire
    ELEMENT_THO = (139, 69, 19)      # Saddle Brown - Earth
    
    # Rarity Colors
    RARITY_1 = (150, 150, 150)       # Gray - Common
    RARITY_2 = (100, 200, 100)       # Green - Uncommon
    RARITY_3 = (100, 150, 255)       # Blue - Rare
    RARITY_4 = (200, 100, 255)       # Purple - Epic
    RARITY_5 = (255, 200, 50)        # Gold - Legendary
    RARITY_6 = (255, 100, 100)       # Red - Mythic
    
    # Status Colors
    HEALTH_HIGH = (0, 200, 0)
    HEALTH_MEDIUM = (255, 200, 0)
    HEALTH_LOW = (200, 0, 0)
    MANA = (0, 150, 255)
