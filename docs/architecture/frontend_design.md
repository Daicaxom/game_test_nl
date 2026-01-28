# Frontend Design - Ngọa Long Tam Quốc

## 1. Tổng Quan

### 1.1 Technology Stack

| Technology | Purpose |
|------------|---------|
| **PyGame** | Game rendering engine (Desktop) |
| **React** | Web UI (optional web version) |
| **TypeScript** | Type safety |
| **Redux Toolkit** | State management |
| **Socket.io** | Real-time communication |
| **Howler.js** | Audio management |

### 1.2 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       FRONTEND ARCHITECTURE                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                      PRESENTATION LAYER                               │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐     │  │
│  │  │   Battle    │ │  Character  │ │    Menu     │ │    Story    │     │  │
│  │  │   Screen    │ │   Screen    │ │   Screen    │ │   Screen    │     │  │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘     │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐     │  │
│  │  │   Gacha     │ │    Team     │ │  Equipment  │ │    Shop     │     │  │
│  │  │   Screen    │ │   Screen    │ │   Screen    │ │   Screen    │     │  │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘     │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                │                                            │
│  ┌─────────────────────────────▼─────────────────────────────────────────┐  │
│  │                      UI COMPONENTS                                    │  │
│  │  Button | Card | Modal | Grid | HealthBar | ManaBar | StatChart      │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                │                                            │
│  ┌─────────────────────────────▼─────────────────────────────────────────┐  │
│  │                      STATE MANAGEMENT                                 │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐     │  │
│  │  │   Player    │ │   Battle    │ │    Hero     │ │    UI       │     │  │
│  │  │   State     │ │   State     │ │   State     │ │   State     │     │  │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘     │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                │                                            │
│  ┌─────────────────────────────▼─────────────────────────────────────────┐  │
│  │                      SERVICES LAYER                                   │  │
│  │  API Client | WebSocket | Audio Manager | Asset Loader | Storage     │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. PyGame Project Structure

```
ngoa-long-frontend/
├── main.py                        # Entry point
├── game/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── engine.py              # Game engine
│   │   ├── scene_manager.py       # Scene management
│   │   ├── event_handler.py       # Input handling
│   │   └── audio_manager.py       # Sound/Music
│   ├── scenes/
│   │   ├── __init__.py
│   │   ├── base_scene.py          # Abstract scene
│   │   ├── main_menu.py           # Main menu
│   │   ├── battle_scene.py        # Battle screen
│   │   ├── character_scene.py     # Hero management
│   │   ├── team_scene.py          # Team building
│   │   ├── gacha_scene.py         # Gacha screen
│   │   ├── story_scene.py         # Story/Campaign
│   │   └── shop_scene.py          # Shop
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── components/
│   │   │   ├── __init__.py
│   │   │   ├── button.py
│   │   │   ├── card.py
│   │   │   ├── modal.py
│   │   │   ├── health_bar.py
│   │   │   ├── mana_bar.py
│   │   │   ├── hexagon_chart.py
│   │   │   └── grid.py
│   │   ├── layouts/
│   │   │   ├── __init__.py
│   │   │   └── battle_layout.py
│   │   └── animations/
│   │       ├── __init__.py
│   │       ├── sprite_animation.py
│   │       └── effect_animation.py
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── character_sprite.py
│   │   ├── skill_effect.py
│   │   └── particle.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── game_state.py          # Global state
│   │   └── api_client.py          # Backend API
│   └── utils/
│       ├── __init__.py
│       ├── constants.py
│       ├── colors.py
│       └── helpers.py
├── assets/
│   ├── images/
│   │   ├── characters/
│   │   ├── skills/
│   │   ├── equipment/
│   │   ├── ui/
│   │   └── backgrounds/
│   ├── sounds/
│   │   ├── bgm/
│   │   ├── sfx/
│   │   └── voice/
│   └── fonts/
├── config/
│   ├── settings.py
│   └── keybindings.py
├── requirements.txt
└── README.md
```

---

## 3. Core Components

### 3.1 Game Engine

```python
# game/core/engine.py

import pygame
from typing import Optional
from game.core.scene_manager import SceneManager
from game.core.event_handler import EventHandler
from game.core.audio_manager import AudioManager
from config.settings import Settings

class GameEngine:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Ngọa Long Tam Quốc")
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Core systems
        self.scene_manager = SceneManager(self)
        self.event_handler = EventHandler(self)
        self.audio_manager = AudioManager()
        
    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(self.settings.FPS) / 1000.0
            
            # Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                self.event_handler.handle(event)
            
            # Update current scene
            self.scene_manager.update(dt)
            
            # Render
            self.screen.fill((0, 0, 0))
            self.scene_manager.render(self.screen)
            pygame.display.flip()
        
        pygame.quit()
    
    def change_scene(self, scene_name: str, **kwargs):
        """Change to a different scene"""
        self.scene_manager.change_scene(scene_name, **kwargs)
    
    def quit(self):
        """Exit the game"""
        self.running = False
```

### 3.2 Scene Manager

```python
# game/core/scene_manager.py

from typing import Dict, Type, Optional
from game.scenes.base_scene import BaseScene

class SceneManager:
    def __init__(self, engine):
        self.engine = engine
        self.scenes: Dict[str, Type[BaseScene]] = {}
        self.current_scene: Optional[BaseScene] = None
        self.scene_stack = []
        
    def register_scene(self, name: str, scene_class: Type[BaseScene]):
        """Register a scene class"""
        self.scenes[name] = scene_class
    
    def change_scene(self, name: str, **kwargs):
        """Change to a new scene"""
        if self.current_scene:
            self.current_scene.on_exit()
        
        scene_class = self.scenes.get(name)
        if not scene_class:
            raise ValueError(f"Scene '{name}' not registered")
        
        self.current_scene = scene_class(self.engine, **kwargs)
        self.current_scene.on_enter()
    
    def push_scene(self, name: str, **kwargs):
        """Push a new scene on top (for modals/overlays)"""
        if self.current_scene:
            self.scene_stack.append(self.current_scene)
            self.current_scene.on_pause()
        
        self.change_scene(name, **kwargs)
    
    def pop_scene(self):
        """Return to previous scene"""
        if self.current_scene:
            self.current_scene.on_exit()
        
        if self.scene_stack:
            self.current_scene = self.scene_stack.pop()
            self.current_scene.on_resume()
    
    def update(self, dt: float):
        if self.current_scene:
            self.current_scene.update(dt)
    
    def render(self, screen):
        # Render stacked scenes first (for transparency effects)
        for scene in self.scene_stack:
            scene.render(screen)
        
        if self.current_scene:
            self.current_scene.render(screen)
```

### 3.3 Base Scene

```python
# game/scenes/base_scene.py

from abc import ABC, abstractmethod
import pygame
from typing import List
from game.ui.components import UIComponent

class BaseScene(ABC):
    def __init__(self, engine):
        self.engine = engine
        self.ui_components: List[UIComponent] = []
        self.is_active = False
    
    def on_enter(self):
        """Called when scene becomes active"""
        self.is_active = True
        self._setup()
    
    def on_exit(self):
        """Called when leaving scene"""
        self.is_active = False
        self._cleanup()
    
    def on_pause(self):
        """Called when scene is pushed to stack"""
        pass
    
    def on_resume(self):
        """Called when scene is popped back"""
        pass
    
    @abstractmethod
    def _setup(self):
        """Initialize scene resources"""
        pass
    
    @abstractmethod
    def _cleanup(self):
        """Clean up scene resources"""
        pass
    
    @abstractmethod
    def update(self, dt: float):
        """Update scene logic"""
        pass
    
    @abstractmethod
    def render(self, screen: pygame.Surface):
        """Render scene"""
        pass
    
    def handle_event(self, event: pygame.event.Event):
        """Handle input events"""
        for component in self.ui_components:
            if component.handle_event(event):
                return True
        return False
    
    def add_component(self, component: UIComponent):
        """Add UI component to scene"""
        self.ui_components.append(component)
    
    def remove_component(self, component: UIComponent):
        """Remove UI component from scene"""
        self.ui_components.remove(component)
```

---

## 4. Battle Scene Implementation

### 4.1 Battle Scene

```python
# game/scenes/battle_scene.py

import pygame
from game.scenes.base_scene import BaseScene
from game.ui.components import Button, HealthBar, ManaBar, SkillButton
from game.ui.layouts.battle_layout import BattleLayout
from game.entities.character_sprite import CharacterSprite
from game.data.api_client import APIClient

class BattleScene(BaseScene):
    def __init__(self, engine, battle_id: str, stage_data: dict):
        super().__init__(engine)
        self.battle_id = battle_id
        self.stage_data = stage_data
        self.api = APIClient()
        
        # Battle state
        self.battle_state = None
        self.current_actor = None
        self.selected_skill = None
        self.selected_targets = []
        self.is_player_turn = False
        
        # Visual elements
        self.layout = BattleLayout(engine.settings)
        self.player_sprites = []
        self.enemy_sprites = []
        self.skill_buttons = []
        self.animations_queue = []
        
    def _setup(self):
        # Load initial battle state
        self.battle_state = self.api.get_battle_state(self.battle_id)
        
        # Create character sprites
        self._create_sprites()
        
        # Setup UI
        self._setup_ui()
        
        # Start battle music
        self.engine.audio_manager.play_bgm("battle_theme")
    
    def _cleanup(self):
        self.engine.audio_manager.stop_bgm()
    
    def _create_sprites(self):
        # Player team sprites
        for i, hero in enumerate(self.battle_state['player_team']):
            pos = self.layout.get_player_position(i)
            sprite = CharacterSprite(hero, pos, is_player=True)
            self.player_sprites.append(sprite)
        
        # Enemy team sprites
        for i, enemy in enumerate(self.battle_state['enemy_team']):
            pos = self.layout.get_enemy_position(i)
            sprite = CharacterSprite(enemy, pos, is_player=False)
            self.enemy_sprites.append(sprite)
    
    def _setup_ui(self):
        # Turn indicator
        self.turn_indicator = self.layout.create_turn_indicator()
        
        # Skill buttons (shown during player turn)
        for i in range(4):
            btn = SkillButton(
                position=self.layout.get_skill_button_position(i),
                on_click=lambda skill_idx=i: self._on_skill_selected(skill_idx)
            )
            self.skill_buttons.append(btn)
            self.add_component(btn)
        
        # End turn button
        self.end_turn_btn = Button(
            position=self.layout.get_end_turn_position(),
            text="End Turn",
            on_click=self._on_end_turn
        )
        self.add_component(self.end_turn_btn)
        
        # Auto battle button
        self.auto_btn = Button(
            position=self.layout.get_auto_position(),
            text="Auto",
            on_click=self._toggle_auto
        )
        self.add_component(self.auto_btn)
    
    def update(self, dt: float):
        # Update animations
        self._update_animations(dt)
        
        # Update sprites
        for sprite in self.player_sprites + self.enemy_sprites:
            sprite.update(dt)
        
        # Check for turn change
        if self.battle_state:
            new_actor = self.battle_state.get('current_actor')
            if new_actor != self.current_actor:
                self._on_turn_change(new_actor)
        
        # Update UI components
        for component in self.ui_components:
            component.update(dt)
    
    def render(self, screen: pygame.Surface):
        # Background
        self._render_background(screen)
        
        # Grid
        self._render_grid(screen)
        
        # Characters
        for sprite in self.enemy_sprites:
            sprite.render(screen)
        for sprite in self.player_sprites:
            sprite.render(screen)
        
        # Health/Mana bars
        self._render_status_bars(screen)
        
        # Current animations
        self._render_animations(screen)
        
        # UI
        self._render_ui(screen)
        
        # Turn indicator
        self._render_turn_indicator(screen)
    
    def _render_grid(self, screen):
        """Render 3x3 battle grid"""
        grid_color = (100, 100, 100, 128)
        
        for x in range(3):
            for y in range(3):
                rect = self.layout.get_grid_cell_rect(x, y)
                pygame.draw.rect(screen, grid_color, rect, 2)
                
                # Highlight valid move/target cells
                if self.selected_skill and (x, y) in self._get_valid_targets():
                    pygame.draw.rect(screen, (255, 255, 0, 64), rect)
    
    def _render_status_bars(self, screen):
        """Render health and mana bars"""
        for sprite in self.player_sprites + self.enemy_sprites:
            char_data = sprite.character_data
            
            # Health bar
            hp_bar = HealthBar(
                position=(sprite.x - 30, sprite.y - 60),
                width=60,
                current=char_data['current_hp'],
                maximum=char_data['max_hp']
            )
            hp_bar.render(screen)
            
            # Mana bar (only for players)
            if sprite.is_player:
                mana_bar = ManaBar(
                    position=(sprite.x - 30, sprite.y - 50),
                    width=60,
                    current=char_data['current_mana'],
                    maximum=char_data['max_mana']
                )
                mana_bar.render(screen)
    
    def _on_skill_selected(self, skill_idx: int):
        """Handle skill button click"""
        if not self.is_player_turn:
            return
        
        actor_skills = self.current_actor.get('skills', [])
        if skill_idx >= len(actor_skills):
            return
        
        skill = actor_skills[skill_idx]
        
        # Check mana cost
        if self.current_actor['current_mana'] < skill['mana_cost']:
            self._show_message("Not enough mana!")
            return
        
        # Check cooldown
        if skill.get('current_cooldown', 0) > 0:
            self._show_message("Skill on cooldown!")
            return
        
        self.selected_skill = skill
        self._highlight_targets()
    
    def _on_target_selected(self, target):
        """Handle target selection"""
        if not self.selected_skill:
            return
        
        # Execute action via API
        result = self.api.execute_action(
            self.battle_id,
            action_type='skill',
            skill_id=self.selected_skill['id'],
            target_ids=[target['id']]
        )
        
        # Play skill animation
        self._play_skill_animation(self.selected_skill, [target])
        
        # Update state
        self.battle_state = result['battle_state']
        self._update_sprites_from_state()
        
        # Reset selection
        self.selected_skill = None
        
        # Check battle end
        if result.get('battle_ended'):
            self._on_battle_end(result)
    
    def _play_skill_animation(self, skill, targets):
        """Queue skill animation"""
        animation = SkillAnimation(
            skill_id=skill['id'],
            caster_sprite=self._get_actor_sprite(),
            target_sprites=[self._get_sprite_by_id(t['id']) for t in targets],
            on_complete=self._on_animation_complete
        )
        self.animations_queue.append(animation)
    
    def _on_battle_end(self, result):
        """Handle battle end"""
        self.engine.audio_manager.stop_bgm()
        
        if result['victory']:
            self.engine.audio_manager.play_sfx("victory")
            self.engine.scene_manager.push_scene(
                'battle_result',
                result=result,
                rewards=result.get('rewards', [])
            )
        else:
            self.engine.audio_manager.play_sfx("defeat")
            self.engine.scene_manager.push_scene(
                'battle_result',
                result=result,
                is_defeat=True
            )
```

---

## 5. UI Components

### 5.1 Button Component

```python
# game/ui/components/button.py

import pygame
from typing import Callable, Optional, Tuple

class Button:
    def __init__(
        self,
        position: Tuple[int, int],
        size: Tuple[int, int] = (120, 40),
        text: str = "",
        font_size: int = 18,
        color: Tuple[int, int, int] = (70, 130, 180),
        hover_color: Tuple[int, int, int] = (100, 160, 210),
        text_color: Tuple[int, int, int] = (255, 255, 255),
        on_click: Optional[Callable] = None,
        disabled: bool = False
    ):
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.on_click = on_click
        self.disabled = disabled
        
        self.is_hovered = False
        self.is_pressed = False
    
    def update(self, dt: float):
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos) and not self.disabled
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        if self.disabled:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                self.is_pressed = True
                return True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.is_pressed:
                self.is_pressed = False
                if self.is_hovered and self.on_click:
                    self.on_click()
                return True
        
        return False
    
    def render(self, screen: pygame.Surface):
        # Background
        color = self.hover_color if self.is_hovered else self.color
        if self.disabled:
            color = (128, 128, 128)
        
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=5)
        
        # Text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
```

### 5.2 Health Bar Component

```python
# game/ui/components/health_bar.py

import pygame
from typing import Tuple

class HealthBar:
    def __init__(
        self,
        position: Tuple[int, int],
        width: int = 100,
        height: int = 10,
        current: int = 100,
        maximum: int = 100,
        bg_color: Tuple[int, int, int] = (50, 50, 50),
        fill_color: Tuple[int, int, int] = (0, 200, 0),
        low_color: Tuple[int, int, int] = (200, 0, 0),
        border_color: Tuple[int, int, int] = (255, 255, 255)
    ):
        self.rect = pygame.Rect(position[0], position[1], width, height)
        self.current = current
        self.maximum = maximum
        self.bg_color = bg_color
        self.fill_color = fill_color
        self.low_color = low_color
        self.border_color = border_color
        
        # Animation
        self.displayed_value = current
        self.animation_speed = 50  # HP per second
    
    @property
    def percentage(self) -> float:
        return self.current / self.maximum if self.maximum > 0 else 0
    
    def update(self, dt: float):
        # Animate health change
        if self.displayed_value != self.current:
            diff = self.current - self.displayed_value
            change = min(abs(diff), self.animation_speed * dt)
            self.displayed_value += change if diff > 0 else -change
    
    def render(self, screen: pygame.Surface):
        # Background
        pygame.draw.rect(screen, self.bg_color, self.rect)
        
        # Fill
        fill_width = int(self.rect.width * (self.displayed_value / self.maximum))
        fill_rect = pygame.Rect(
            self.rect.x, self.rect.y,
            fill_width, self.rect.height
        )
        
        # Color based on health percentage
        color = self.low_color if self.percentage < 0.3 else self.fill_color
        pygame.draw.rect(screen, color, fill_rect)
        
        # Border
        pygame.draw.rect(screen, self.border_color, self.rect, 1)
        
        # Text (optional)
        font = pygame.font.Font(None, 12)
        text = f"{int(self.displayed_value)}/{self.maximum}"
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
```

### 5.3 Hexagon Stats Chart

```python
# game/ui/components/hexagon_chart.py

import pygame
import math
from typing import Dict, Tuple

class HexagonChart:
    """Biểu đồ lục giác cho stats"""
    
    def __init__(
        self,
        position: Tuple[int, int],
        radius: int = 80,
        stats: Dict[str, int] = None,
        max_stats: Dict[str, int] = None,
        colors: Dict[str, Tuple[int, int, int]] = None
    ):
        self.center = position
        self.radius = radius
        self.stats = stats or {
            'HP': 0, 'ATK': 0, 'DEF': 0,
            'SPD': 0, 'CRIT': 0, 'DEX': 0
        }
        self.max_stats = max_stats or {k: 100 for k in self.stats}
        self.colors = colors or {
            'fill': (100, 149, 237, 128),
            'outline': (65, 105, 225),
            'grid': (200, 200, 200),
            'text': (255, 255, 255)
        }
        
        # Pre-calculate angles for hexagon vertices
        self.angles = [i * (2 * math.pi / 6) - math.pi / 2 for i in range(6)]
        self.stat_names = ['HP', 'ATK', 'DEF', 'SPD', 'CRIT', 'DEX']
    
    def _get_point(self, angle: float, value: float) -> Tuple[int, int]:
        """Calculate point position based on angle and value"""
        normalized = value / 100  # Assuming max is 100
        x = self.center[0] + self.radius * normalized * math.cos(angle)
        y = self.center[1] + self.radius * normalized * math.sin(angle)
        return (int(x), int(y))
    
    def render(self, screen: pygame.Surface):
        # Draw background grid
        self._draw_grid(screen)
        
        # Draw stat polygon
        self._draw_stats(screen)
        
        # Draw labels
        self._draw_labels(screen)
    
    def _draw_grid(self, screen: pygame.Surface):
        """Draw hexagonal grid lines"""
        for level in [0.25, 0.5, 0.75, 1.0]:
            points = []
            for angle in self.angles:
                x = self.center[0] + self.radius * level * math.cos(angle)
                y = self.center[1] + self.radius * level * math.sin(angle)
                points.append((int(x), int(y)))
            pygame.draw.polygon(screen, self.colors['grid'], points, 1)
        
        # Draw axis lines
        for angle in self.angles:
            end_x = self.center[0] + self.radius * math.cos(angle)
            end_y = self.center[1] + self.radius * math.sin(angle)
            pygame.draw.line(
                screen, self.colors['grid'],
                self.center, (int(end_x), int(end_y)), 1
            )
    
    def _draw_stats(self, screen: pygame.Surface):
        """Draw filled stat polygon"""
        points = []
        for i, stat_name in enumerate(self.stat_names):
            value = self.stats.get(stat_name, 0)
            max_val = self.max_stats.get(stat_name, 100)
            normalized = min(value / max_val, 1.0) if max_val > 0 else 0
            points.append(self._get_point(self.angles[i], normalized * 100))
        
        # Fill
        if len(points) >= 3:
            # Create surface with alpha
            s = pygame.Surface((self.radius * 2 + 20, self.radius * 2 + 20), pygame.SRCALPHA)
            adjusted_points = [
                (p[0] - self.center[0] + self.radius + 10,
                 p[1] - self.center[1] + self.radius + 10)
                for p in points
            ]
            pygame.draw.polygon(s, self.colors['fill'], adjusted_points)
            screen.blit(s, (self.center[0] - self.radius - 10, self.center[1] - self.radius - 10))
        
        # Outline
        pygame.draw.polygon(screen, self.colors['outline'], points, 2)
        
        # Points
        for point in points:
            pygame.draw.circle(screen, self.colors['outline'], point, 4)
    
    def _draw_labels(self, screen: pygame.Surface):
        """Draw stat labels"""
        font = pygame.font.Font(None, 18)
        
        for i, stat_name in enumerate(self.stat_names):
            angle = self.angles[i]
            label_radius = self.radius + 25
            x = self.center[0] + label_radius * math.cos(angle)
            y = self.center[1] + label_radius * math.sin(angle)
            
            # Stat name
            text = font.render(stat_name, True, self.colors['text'])
            text_rect = text.get_rect(center=(int(x), int(y)))
            screen.blit(text, text_rect)
            
            # Stat value
            value = self.stats.get(stat_name, 0)
            value_text = font.render(str(value), True, self.colors['text'])
            value_rect = value_text.get_rect(center=(int(x), int(y) + 15))
            screen.blit(value_text, value_rect)
```

---

## 6. Character Sprite

```python
# game/entities/character_sprite.py

import pygame
from typing import Dict, Tuple, Optional
from game.ui.animations.sprite_animation import SpriteAnimation

class CharacterSprite:
    def __init__(
        self,
        character_data: Dict,
        position: Tuple[int, int],
        is_player: bool = True
    ):
        self.character_data = character_data
        self.x, self.y = position
        self.is_player = is_player
        
        # Load sprite sheet
        self.sprite_sheet = self._load_sprite_sheet(character_data['template_id'])
        
        # Animations
        self.animations = {
            'idle': SpriteAnimation(self.sprite_sheet, 'idle', fps=8),
            'attack': SpriteAnimation(self.sprite_sheet, 'attack', fps=12),
            'skill': SpriteAnimation(self.sprite_sheet, 'skill', fps=10),
            'hurt': SpriteAnimation(self.sprite_sheet, 'hurt', fps=10),
            'death': SpriteAnimation(self.sprite_sheet, 'death', fps=8, loop=False)
        }
        self.current_animation = 'idle'
        
        # State
        self.is_selected = False
        self.is_highlighted = False
        self.is_dead = False
        
        # Effects
        self.status_effects = []
        self.damage_numbers = []
    
    def _load_sprite_sheet(self, template_id: str) -> pygame.Surface:
        """Load character sprite sheet"""
        path = f"assets/images/characters/{template_id}.png"
        try:
            return pygame.image.load(path).convert_alpha()
        except pygame.error:
            # Return placeholder if not found
            surface = pygame.Surface((64, 64), pygame.SRCALPHA)
            pygame.draw.rect(surface, (100, 100, 100), (0, 0, 64, 64))
            return surface
    
    def update(self, dt: float):
        # Update animation
        self.animations[self.current_animation].update(dt)
        
        # Update damage numbers
        for dmg in self.damage_numbers[:]:
            dmg['y'] -= 50 * dt
            dmg['alpha'] -= 200 * dt
            if dmg['alpha'] <= 0:
                self.damage_numbers.remove(dmg)
    
    def render(self, screen: pygame.Surface):
        # Get current frame
        frame = self.animations[self.current_animation].get_current_frame()
        
        # Flip for enemies
        if not self.is_player:
            frame = pygame.transform.flip(frame, True, False)
        
        # Apply effects
        if self.is_selected:
            # Highlight outline
            pygame.draw.rect(
                screen, (255, 255, 0),
                (self.x - 2, self.y - 2, frame.get_width() + 4, frame.get_height() + 4),
                2
            )
        
        if self.is_highlighted:
            # Targeting highlight
            s = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            s.fill((255, 255, 0, 64))
            screen.blit(s, (self.x, self.y))
        
        # Draw sprite
        if self.is_dead:
            # Grayscale for dead characters
            frame = self._apply_grayscale(frame)
        
        screen.blit(frame, (self.x, self.y))
        
        # Draw damage numbers
        self._render_damage_numbers(screen)
        
        # Draw status effect icons
        self._render_status_effects(screen)
    
    def play_animation(self, name: str, on_complete: Optional[callable] = None):
        """Play a specific animation"""
        if name in self.animations:
            self.current_animation = name
            self.animations[name].reset()
            self.animations[name].on_complete = on_complete
    
    def show_damage(self, amount: int, is_crit: bool = False, is_heal: bool = False):
        """Show floating damage number"""
        color = (0, 255, 0) if is_heal else ((255, 255, 0) if is_crit else (255, 0, 0))
        size = 32 if is_crit else 24
        
        self.damage_numbers.append({
            'value': amount,
            'x': self.x + 32,
            'y': self.y - 20,
            'color': color,
            'size': size,
            'alpha': 255
        })
    
    def _render_damage_numbers(self, screen: pygame.Surface):
        """Render floating damage numbers"""
        for dmg in self.damage_numbers:
            font = pygame.font.Font(None, dmg['size'])
            text = font.render(str(dmg['value']), True, dmg['color'])
            text.set_alpha(int(dmg['alpha']))
            screen.blit(text, (dmg['x'], dmg['y']))
    
    def _render_status_effects(self, screen: pygame.Surface):
        """Render status effect icons"""
        icon_size = 16
        for i, effect in enumerate(self.status_effects):
            icon = self._get_effect_icon(effect['type'])
            x = self.x + i * (icon_size + 2)
            y = self.y - icon_size - 5
            screen.blit(icon, (x, y))
    
    def _apply_grayscale(self, surface: pygame.Surface) -> pygame.Surface:
        """Convert surface to grayscale"""
        arr = pygame.surfarray.array3d(surface)
        gray = arr.mean(axis=2)
        arr[:, :, 0] = gray
        arr[:, :, 1] = gray
        arr[:, :, 2] = gray
        return pygame.surfarray.make_surface(arr)
```

---

## 7. Gacha Scene

```python
# game/scenes/gacha_scene.py

import pygame
import random
from game.scenes.base_scene import BaseScene
from game.ui.components import Button, Card
from game.ui.animations.gacha_animation import GachaAnimation
from game.data.api_client import APIClient

class GachaScene(BaseScene):
    def __init__(self, engine):
        super().__init__(engine)
        self.api = APIClient()
        
        # UI State
        self.current_banner = None
        self.banners = []
        self.pull_results = []
        self.is_pulling = False
        
        # Animation
        self.gacha_animation = None
    
    def _setup(self):
        # Load banners
        self.banners = self.api.get_banners()
        if self.banners:
            self.current_banner = self.banners[0]
        
        # Setup UI
        self._setup_ui()
        
        # Play gacha BGM
        self.engine.audio_manager.play_bgm("gacha_theme")
    
    def _setup_ui(self):
        # Banner selector
        for i, banner in enumerate(self.banners):
            btn = Button(
                position=(50 + i * 200, 50),
                size=(180, 50),
                text=banner['name'],
                on_click=lambda b=banner: self._select_banner(b)
            )
            self.add_component(btn)
        
        # Pull buttons
        self.pull_1_btn = Button(
            position=(300, 500),
            size=(150, 60),
            text="Pull x1",
            on_click=lambda: self._do_pull(1)
        )
        self.add_component(self.pull_1_btn)
        
        self.pull_10_btn = Button(
            position=(500, 500),
            size=(150, 60),
            text="Pull x10",
            on_click=lambda: self._do_pull(10)
        )
        self.add_component(self.pull_10_btn)
        
        # Back button
        self.back_btn = Button(
            position=(50, 550),
            size=(100, 40),
            text="Back",
            on_click=self._go_back
        )
        self.add_component(self.back_btn)
    
    def _select_banner(self, banner):
        self.current_banner = banner
    
    def _do_pull(self, count: int):
        if self.is_pulling:
            return
        
        # Check gems
        player = self.api.get_player()
        cost = self.current_banner['cost'] * count
        
        if player['gems'] < cost:
            self._show_message("Not enough gems!")
            return
        
        self.is_pulling = True
        
        # Call API
        results = self.api.gacha_pull(
            self.current_banner['id'],
            count
        )
        
        self.pull_results = results
        
        # Start animation
        self.gacha_animation = GachaAnimation(
            results=results,
            on_complete=self._on_pull_complete
        )
        
        # Play gacha SFX
        self.engine.audio_manager.play_sfx("gacha_pull")
    
    def _on_pull_complete(self):
        self.is_pulling = False
        self.gacha_animation = None
        
        # Show results
        self.engine.scene_manager.push_scene(
            'gacha_results',
            results=self.pull_results
        )
    
    def update(self, dt: float):
        if self.gacha_animation:
            self.gacha_animation.update(dt)
        
        for component in self.ui_components:
            component.update(dt)
    
    def render(self, screen: pygame.Surface):
        # Background
        screen.fill((20, 20, 40))
        
        # Banner display
        self._render_banner(screen)
        
        # Pity counter
        self._render_pity(screen)
        
        # Animation
        if self.gacha_animation:
            self.gacha_animation.render(screen)
        
        # UI
        for component in self.ui_components:
            component.render(screen)
    
    def _render_banner(self, screen: pygame.Surface):
        if not self.current_banner:
            return
        
        # Banner image
        banner_img = pygame.image.load(
            f"assets/images/banners/{self.current_banner['id']}.png"
        ).convert_alpha()
        banner_img = pygame.transform.scale(banner_img, (600, 300))
        screen.blit(banner_img, (200, 100))
        
        # Featured heroes
        featured = self.current_banner.get('featured_heroes', [])
        for i, hero in enumerate(featured[:3]):
            hero_icon = self._load_hero_icon(hero['template_id'])
            screen.blit(hero_icon, (250 + i * 100, 420))
    
    def _render_pity(self, screen: pygame.Surface):
        pity = self.api.get_pity(self.current_banner['banner_type'])
        
        font = pygame.font.Font(None, 24)
        text = f"Pity: {pity['count']}/90"
        surface = font.render(text, True, (255, 255, 255))
        screen.blit(surface, (700, 100))
        
        if pity['guaranteed_featured']:
            guaranteed_text = "Next 5★ is guaranteed featured!"
            g_surface = font.render(guaranteed_text, True, (255, 215, 0))
            screen.blit(g_surface, (700, 130))
    
    def _go_back(self):
        self.engine.scene_manager.pop_scene()
```

---

## 8. API Client

```python
# game/data/api_client.py

import requests
from typing import Dict, List, Optional
from config.settings import Settings

class APIClient:
    def __init__(self):
        self.settings = Settings()
        self.base_url = self.settings.API_BASE_URL
        self.token = None
    
    def _headers(self) -> Dict:
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers
    
    def _get(self, endpoint: str, params: Dict = None) -> Dict:
        response = requests.get(
            f"{self.base_url}{endpoint}",
            params=params,
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()['data']
    
    def _post(self, endpoint: str, data: Dict = None) -> Dict:
        response = requests.post(
            f"{self.base_url}{endpoint}",
            json=data,
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()['data']
    
    # Auth
    def login(self, username: str, password: str) -> Dict:
        result = self._post('/auth/login', {
            'username': username,
            'password': password
        })
        self.token = result['access_token']
        return result
    
    def register(self, username: str, email: str, password: str) -> Dict:
        return self._post('/auth/register', {
            'username': username,
            'email': email,
            'password': password
        })
    
    # Player
    def get_player(self) -> Dict:
        return self._get('/players/me')
    
    # Heroes
    def get_heroes(self, filters: Dict = None) -> List[Dict]:
        return self._get('/heroes', filters)
    
    def get_hero(self, hero_id: str) -> Dict:
        return self._get(f'/heroes/{hero_id}')
    
    def level_up_hero(self, hero_id: str, exp_items: List[Dict]) -> Dict:
        return self._post(f'/heroes/{hero_id}/level-up', {
            'exp_items': exp_items
        })
    
    # Battle
    def start_battle(self, stage_id: str, team_id: str) -> Dict:
        return self._post('/battles/start', {
            'stage_id': stage_id,
            'team_id': team_id
        })
    
    def get_battle_state(self, battle_id: str) -> Dict:
        return self._get(f'/battles/{battle_id}/state')
    
    def execute_action(
        self,
        battle_id: str,
        action_type: str,
        skill_id: str = None,
        target_ids: List[str] = None
    ) -> Dict:
        return self._post(f'/battles/{battle_id}/action', {
            'action_type': action_type,
            'skill_id': skill_id,
            'target_ids': target_ids
        })
    
    # Gacha
    def get_banners(self) -> List[Dict]:
        return self._get('/gacha/banners')
    
    def gacha_pull(self, banner_id: str, count: int) -> List[Dict]:
        return self._post('/gacha/pull', {
            'banner_id': banner_id,
            'pull_count': count
        })
    
    def get_pity(self, banner_type: str) -> Dict:
        return self._get('/gacha/pity', {'banner_type': banner_type})
    
    # Story
    def get_chapters(self) -> List[Dict]:
        return self._get('/story/chapters')
    
    def get_stages(self, chapter_id: str) -> List[Dict]:
        return self._get(f'/story/chapters/{chapter_id}/stages')
    
    # Teams
    def get_teams(self) -> List[Dict]:
        return self._get('/teams')
    
    def save_team(self, team_data: Dict) -> Dict:
        if team_data.get('id'):
            return self._post(f"/teams/{team_data['id']}", team_data)
        return self._post('/teams', team_data)
```

---

## 9. Audio Manager

```python
# game/core/audio_manager.py

import pygame
from typing import Dict, Optional

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        
        self.bgm_volume = 0.7
        self.sfx_volume = 1.0
        self.voice_volume = 1.0
        
        self.current_bgm = None
        self.bgm_tracks: Dict[str, str] = {}
        self.sfx_cache: Dict[str, pygame.mixer.Sound] = {}
        
        # Load audio files
        self._load_audio()
    
    def _load_audio(self):
        """Load audio file paths"""
        self.bgm_tracks = {
            'main_menu': 'assets/sounds/bgm/main_menu.ogg',
            'battle_theme': 'assets/sounds/bgm/battle.ogg',
            'boss_battle': 'assets/sounds/bgm/boss.ogg',
            'gacha_theme': 'assets/sounds/bgm/gacha.ogg',
            'victory': 'assets/sounds/bgm/victory.ogg'
        }
        
        # Pre-load common SFX
        sfx_list = [
            'button_click', 'skill_use', 'hit', 'crit',
            'heal', 'buff', 'debuff', 'level_up',
            'gacha_pull', 'star_3', 'star_4', 'star_5'
        ]
        for sfx in sfx_list:
            try:
                path = f'assets/sounds/sfx/{sfx}.wav'
                self.sfx_cache[sfx] = pygame.mixer.Sound(path)
            except pygame.error:
                print(f"Warning: Could not load SFX {sfx}")
    
    def play_bgm(self, track_name: str, loop: bool = True):
        """Play background music"""
        if track_name not in self.bgm_tracks:
            return
        
        if self.current_bgm == track_name:
            return
        
        pygame.mixer.music.load(self.bgm_tracks[track_name])
        pygame.mixer.music.set_volume(self.bgm_volume)
        pygame.mixer.music.play(-1 if loop else 0)
        self.current_bgm = track_name
    
    def stop_bgm(self):
        """Stop background music"""
        pygame.mixer.music.stop()
        self.current_bgm = None
    
    def pause_bgm(self):
        """Pause background music"""
        pygame.mixer.music.pause()
    
    def resume_bgm(self):
        """Resume background music"""
        pygame.mixer.music.unpause()
    
    def play_sfx(self, sfx_name: str):
        """Play sound effect"""
        if sfx_name in self.sfx_cache:
            sound = self.sfx_cache[sfx_name]
            sound.set_volume(self.sfx_volume)
            sound.play()
    
    def set_bgm_volume(self, volume: float):
        """Set BGM volume (0.0 - 1.0)"""
        self.bgm_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.bgm_volume)
    
    def set_sfx_volume(self, volume: float):
        """Set SFX volume (0.0 - 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
```

---

## 10. Constants & Settings

```python
# config/settings.py

import os
from dataclasses import dataclass

@dataclass
class Settings:
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


# game/utils/colors.py

class Colors:
    # UI Colors
    PRIMARY = (70, 130, 180)
    SECONDARY = (100, 160, 210)
    BACKGROUND = (20, 20, 40)
    TEXT = (255, 255, 255)
    TEXT_SECONDARY = (200, 200, 200)
    
    # Element Colors
    ELEMENT_KIM = (255, 215, 0)      # Gold
    ELEMENT_MOC = (34, 139, 34)      # Forest Green
    ELEMENT_THUY = (30, 144, 255)    # Dodger Blue
    ELEMENT_HOA = (255, 69, 0)       # Red Orange
    ELEMENT_THO = (139, 69, 19)      # Saddle Brown
    
    # Rarity Colors
    RARITY_1 = (150, 150, 150)       # Gray
    RARITY_2 = (100, 200, 100)       # Green
    RARITY_3 = (100, 150, 255)       # Blue
    RARITY_4 = (200, 100, 255)       # Purple
    RARITY_5 = (255, 200, 50)        # Gold
    RARITY_6 = (255, 100, 100)       # Red (Mythic)
    
    # Status
    HEALTH_HIGH = (0, 200, 0)
    HEALTH_MEDIUM = (255, 200, 0)
    HEALTH_LOW = (200, 0, 0)
    MANA = (0, 150, 255)
```

---

## 11. Responsive Design

```python
# game/utils/responsive.py

class ResponsiveLayout:
    """Helper for responsive UI scaling"""
    
    def __init__(self, base_width: int = 1280, base_height: int = 720):
        self.base_width = base_width
        self.base_height = base_height
        self.current_width = base_width
        self.current_height = base_height
        self.scale_x = 1.0
        self.scale_y = 1.0
    
    def update(self, width: int, height: int):
        """Update current screen size"""
        self.current_width = width
        self.current_height = height
        self.scale_x = width / self.base_width
        self.scale_y = height / self.base_height
    
    def scale_position(self, x: int, y: int) -> tuple:
        """Scale position from base to current resolution"""
        return (int(x * self.scale_x), int(y * self.scale_y))
    
    def scale_size(self, width: int, height: int) -> tuple:
        """Scale size from base to current resolution"""
        return (int(width * self.scale_x), int(height * self.scale_y))
    
    def scale_rect(self, rect: tuple) -> tuple:
        """Scale rectangle (x, y, w, h)"""
        x, y, w, h = rect
        return (
            int(x * self.scale_x),
            int(y * self.scale_y),
            int(w * self.scale_x),
            int(h * self.scale_y)
        )
    
    def scale_font_size(self, size: int) -> int:
        """Scale font size based on average scale"""
        avg_scale = (self.scale_x + self.scale_y) / 2
        return max(8, int(size * avg_scale))
```

---

*Tài liệu này mô tả thiết kế Frontend cho game Ngọa Long Tam Quốc sử dụng PyGame. Xem thêm Backend Design và Database Design để biết cách tích hợp với server.*
