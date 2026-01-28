# Frontend Implementation - Ngọa Long Tam Quốc

This document describes the PyGame-based frontend implementation following the design specifications.

## Overview

Implementation of core frontend components for the turn-based strategy RPG game "Ngọa Long Tam Quốc" (Three Kingdoms) using PyGame, following Test-Driven Development (TDD) approach.

## Implemented Components

### 1. Core Infrastructure ✅
- **Settings Module** (`game/utils/settings.py`): Game configuration including display, API, game rules, UI, and audio settings
- **Colors Module** (`game/utils/colors.py`): Centralized color definitions for UI elements, element types (Five Elements), rarity levels, and status indicators

### 2. Core Engine ✅
- **GameEngine** (`game/core/engine.py`): Main game loop with scene management, event handling, and rendering
- **SceneManager** (`game/core/scene_manager.py`): Scene lifecycle management with support for scene stacking (for modals/overlays)
- **BaseScene** (`game/scenes/base_scene.py`): Abstract base class for all game scenes with lifecycle methods

### 3. UI Components ✅
All components follow TDD approach with comprehensive test coverage:

- **Button** (`game/ui/components/button.py`): Interactive button with hover states, click callbacks, and disabled state
- **HealthBar** (`game/ui/components/health_bar.py`): Animated health bar with color-coded states (high/medium/low)
- **ManaBar** (`game/ui/components/mana_bar.py`): Animated mana bar for skill resources
- **HexagonChart** (`game/ui/components/hexagon_chart.py`): Radar chart for character stats visualization (HP, ATK, DEF, SPD, CRIT, DEX)

### 4. Game Scenes ✅
- **MainMenuScene** (`game/scenes/main_menu.py`): Main menu with Start Game, Settings, UI Demo, and Quit options
- **DemoScene** (`game/scenes/demo_scene.py`): Showcase scene demonstrating all implemented UI components

## Test Coverage

**50 tests passing** across all modules:
- Settings & Colors: 9 tests
- BaseScene: 9 tests  
- SceneManager: 10 tests
- Button Component: 9 tests
- HealthBar Component: 8 tests
- HexagonChart Component: 5 tests

All tests written following TDD methodology (tests written before implementation).

## Running the Application

### Prerequisites
```bash
pip install pygame pytest pytest-mock
```

### Run the Game
```bash
python main.py
```

### Run Tests
```bash
pytest tests/unit/game/ -v
```

### Capture Screenshots
```bash
python capture_screenshots.py
```

## Screenshots

### Main Menu
![Main Menu](https://github.com/user-attachments/assets/afb4469d-2900-418c-8f1f-533ff78f3617)

The main menu features:
- Game title "Ngọa Long Tam Quốc"
- Interactive buttons with hover effects
- Clean, centered layout

### UI Components Demo
![UI Components Demo](https://github.com/user-attachments/assets/599944ad-2765-44b1-a674-104a8636b701)

The demo scene showcases:
- **Buttons**: Normal and disabled states with hover effects
- **Health & Mana Bars**: Animated bars with smooth transitions
- **Hexagon Chart**: Character stats visualization in radar chart format
- **Element Colors**: Five Elements (Wu Xing) color palette display
  - Kim (Metal) - Gold
  - Mộc (Wood) - Forest Green
  - Thủy (Water) - Dodger Blue
  - Hỏa (Fire) - Red Orange
  - Thổ (Earth) - Saddle Brown

## Architecture

The implementation follows a clean architecture pattern:

```
game/
├── core/              # Core engine and systems
│   ├── engine.py      # Main game engine
│   └── scene_manager.py
├── scenes/            # Game scenes
│   ├── base_scene.py
│   ├── main_menu.py
│   └── demo_scene.py
├── ui/                # UI components
│   └── components/
│       ├── button.py
│       ├── health_bar.py
│       ├── mana_bar.py
│       └── hexagon_chart.py
└── utils/             # Utilities
    ├── settings.py
    └── colors.py
```

## Next Steps (Not Implemented)

The following components from the design document are ready for future implementation:

### Core Systems
- EventHandler for advanced input handling
- AudioManager for background music and sound effects

### UI Components
- Card component for character/item cards
- Modal component for dialogs
- Grid component for battle grid (3x3)

### Game Scenes
- BattleScene for turn-based combat
- CharacterScene for hero management
- TeamScene for team building
- GachaScene for character summoning
- StoryScene for campaign/story mode
- ShopScene for purchases

### Support Modules
- APIClient for backend integration
- Sprite animation system
- Effect animations
- Responsive layout utilities

## Design Philosophy

1. **Test-Driven Development**: All components have comprehensive test coverage written before implementation
2. **Minimal Changes**: Focused implementation of core components as specified in the design document
3. **Modularity**: Each component is independent and reusable
4. **Clean Code**: Well-documented with clear separation of concerns
5. **Extensibility**: Easy to add new scenes and components following established patterns

## Notes

- The game runs in both windowed and headless (CI) environments
- Audio initialization gracefully handles missing audio devices
- All UI components support customization through constructor parameters
- Scene lifecycle properly managed with enter/exit/pause/resume hooks
