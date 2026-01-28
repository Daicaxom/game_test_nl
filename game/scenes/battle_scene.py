"""
Battle Scene
Turn-based combat scene with 3x3 grid layout
"""
import pygame
from typing import Dict, List, Optional
from game.scenes.base_scene import BaseScene
from game.ui.components.button import Button
from game.ui.components.grid import Grid
from game.ui.components.health_bar import HealthBar
from game.ui.components.mana_bar import ManaBar
from game.ui.components.card import Card
from game.ui.components.modal import Modal
from game.utils.colors import Colors
from game.utils.settings import Settings


class BattleScene(BaseScene):
    """Battle scene for turn-based combat with 3x3 grid"""
    
    def __init__(self, engine):
        """
        Initialize battle scene
        
        Args:
            engine: Reference to the game engine
        """
        super().__init__(engine)
        self.settings = Settings()
        
        # UI Components
        self.player_grid: Optional[Grid] = None
        self.enemy_grid: Optional[Grid] = None
        self.buttons: List[Button] = []
        self.health_bars: Dict[str, HealthBar] = {}
        self.mana_bars: Dict[str, ManaBar] = {}
        self.character_cards: List[Card] = []
        self.modal: Optional[Modal] = None
        
        # Game state
        self.turn = 1
        self.current_phase = "player"  # "player" or "enemy"
        self.selected_character = None
        self.selected_action = None
        
    def on_enter(self):
        """Called when scene becomes active"""
        # Initialize fonts
        self.title_font = pygame.font.Font(None, 36)
        self.label_font = pygame.font.Font(None, 24)
        self.info_font = pygame.font.Font(None, 20)
        
        # Create player grid (left side)
        self.player_grid = Grid(
            position=(50, 150),
            cell_size=70,
            spacing=5,
            on_cell_click=self._on_player_cell_click
        )
        
        # Create enemy grid (right side)
        self.enemy_grid = Grid(
            position=(self.settings.SCREEN_WIDTH - 50 - 225, 150),
            cell_size=70,
            spacing=5,
            on_cell_click=self._on_enemy_cell_click
        )
        
        # Place sample characters
        self._setup_characters()
        
        # Create action buttons
        button_y = 500
        button_spacing = 110
        
        self.buttons.append(Button(
            position=(50, button_y),
            size=(100, 40),
            text="Attack",
            on_click=lambda: self._select_action("attack")
        ))
        
        self.buttons.append(Button(
            position=(50 + button_spacing, button_y),
            size=(100, 40),
            text="Skill",
            on_click=lambda: self._select_action("skill")
        ))
        
        self.buttons.append(Button(
            position=(50 + button_spacing * 2, button_y),
            size=(100, 40),
            text="Defend",
            on_click=lambda: self._select_action("defend")
        ))
        
        self.buttons.append(Button(
            position=(50 + button_spacing * 3, button_y),
            size=(100, 40),
            text="End Turn",
            on_click=self._end_turn
        ))
        
        # Back button
        self.buttons.append(Button(
            position=(50, 650),
            size=(120, 35),
            text="Back to Menu",
            on_click=self._on_back
        ))
        
        # Create character cards display
        self._create_character_cards()
        
        # Create health and mana bars
        self._create_status_bars()
        
    def _setup_characters(self):
        """Setup initial character positions"""
        # Player team
        player_characters = [
            {"name": "Lưu Bị", "element": "Mộc", "hp": 100, "mana": 0},
            {"name": "Quan Vũ", "element": "Kim", "hp": 100, "mana": 30},
            {"name": "Trương Phi", "element": "Hỏa", "hp": 80, "mana": 50},
        ]
        
        # Place in player grid
        positions = [(0, 1), (1, 0), (1, 2)]
        for i, char in enumerate(player_characters):
            if i < len(positions):
                row, col = positions[i]
                self.player_grid.set_cell_content(row, col, char)
        
        # Enemy team
        enemy_characters = [
            {"name": "Tào Tháo", "element": "Thủy", "hp": 100, "mana": 40},
            {"name": "Lã Bố", "element": "Hỏa", "hp": 90, "mana": 60},
        ]
        
        # Place in enemy grid
        positions = [(1, 1), (0, 2)]
        for i, char in enumerate(enemy_characters):
            if i < len(positions):
                row, col = positions[i]
                self.enemy_grid.set_cell_content(row, col, char)
    
    def _create_character_cards(self):
        """Create character card displays"""
        self.character_cards = []
        
        # Create cards for player characters
        card_x = 50
        card_y = 560
        
        for i, char_info in enumerate([
            {"name": "Lưu Bị", "element": "Mộc", "rarity": 5, "stats": {"HP": 100, "ATK": 70}},
            {"name": "Quan Vũ", "element": "Kim", "rarity": 5, "stats": {"HP": 100, "ATK": 90}},
            {"name": "Trương Phi", "element": "Hỏa", "rarity": 4, "stats": {"HP": 80, "ATK": 85}},
        ]):
            card = Card(
                position=(card_x + i * 95, card_y),
                size=(90, 80),
                name=char_info["name"],
                element=char_info["element"],
                rarity=char_info["rarity"],
                stats=char_info["stats"],
                on_click=lambda n=char_info["name"]: self._on_card_click(n)
            )
            self.character_cards.append(card)
    
    def _create_status_bars(self):
        """Create health and mana bars for characters"""
        # Player team bars
        bar_x = 50
        bar_y = 420
        
        self.health_bars["player"] = HealthBar(
            position=(bar_x, bar_y),
            width=200,
            height=20,
            current=80,
            maximum=100
        )
        
        self.mana_bars["player"] = ManaBar(
            position=(bar_x, bar_y + 25),
            width=200,
            height=15,
            current=30,
            maximum=100
        )
        
        # Enemy team bars
        enemy_bar_x = self.settings.SCREEN_WIDTH - 250
        
        self.health_bars["enemy"] = HealthBar(
            position=(enemy_bar_x, bar_y),
            width=200,
            height=20,
            current=90,
            maximum=100
        )
        
        self.mana_bars["enemy"] = ManaBar(
            position=(enemy_bar_x, bar_y + 25),
            width=200,
            height=15,
            current=60,
            maximum=100
        )
    
    def on_exit(self):
        """Called when scene is deactivated"""
        self.buttons.clear()
        self.health_bars.clear()
        self.mana_bars.clear()
        self.character_cards.clear()
        self.player_grid = None
        self.enemy_grid = None
        self.modal = None
    
    def on_pause(self):
        """Called when scene is paused"""
        pass
    
    def on_resume(self):
        """Called when scene is resumed"""
        pass
    
    def update(self, dt: float):
        """
        Update battle scene
        
        Args:
            dt: Delta time in seconds
        """
        # Update grids
        if self.player_grid:
            self.player_grid.update(dt)
        if self.enemy_grid:
            self.enemy_grid.update(dt)
        
        # Update buttons
        for button in self.buttons:
            button.update(dt)
        
        # Update status bars
        for bar in self.health_bars.values():
            bar.update(dt)
        for bar in self.mana_bars.values():
            bar.update(dt)
        
        # Update character cards
        for card in self.character_cards:
            card.update(dt)
        
        # Update modal if visible
        if self.modal:
            self.modal.update(dt)
    
    def render(self, screen: pygame.Surface):
        """
        Render battle scene
        
        Args:
            screen: Pygame surface to render to
        """
        # Background
        screen.fill(Colors.BACKGROUND)
        
        # Title
        title_text = f"Battle - Turn {self.turn}"
        title_surface = self.title_font.render(title_text, True, Colors.TEXT)
        screen.blit(title_surface, (self.settings.SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 20))
        
        # Phase indicator
        phase_text = f"Phase: {self.current_phase.capitalize()}"
        phase_surface = self.label_font.render(phase_text, True, Colors.TEXT_SECONDARY)
        screen.blit(phase_surface, (self.settings.SCREEN_WIDTH // 2 - phase_surface.get_width() // 2, 55))
        
        # Grid labels
        player_label = self.label_font.render("Your Team", True, Colors.TEXT)
        screen.blit(player_label, (50, 120))
        
        enemy_label = self.label_font.render("Enemy Team", True, Colors.TEXT)
        screen.blit(enemy_label, (self.settings.SCREEN_WIDTH - 275, 120))
        
        # Render grids
        if self.player_grid:
            self.player_grid.render(screen)
        if self.enemy_grid:
            self.enemy_grid.render(screen)
        
        # Status bar labels
        player_hp_label = self.label_font.render("Player HP:", True, Colors.TEXT_SECONDARY)
        screen.blit(player_hp_label, (50, 395))
        
        enemy_hp_label = self.label_font.render("Enemy HP:", True, Colors.TEXT_SECONDARY)
        screen.blit(enemy_hp_label, (self.settings.SCREEN_WIDTH - 250, 395))
        
        # Render status bars
        for bar in self.health_bars.values():
            bar.render(screen)
        for bar in self.mana_bars.values():
            bar.render(screen)
        
        # Action label
        action_label = self.label_font.render("Actions:", True, Colors.TEXT_SECONDARY)
        screen.blit(action_label, (50, 475))
        
        # Render buttons
        for button in self.buttons:
            button.render(screen)
        
        # Selected action indicator
        if self.selected_action:
            action_text = f"Selected: {self.selected_action.capitalize()}"
            action_surface = self.info_font.render(action_text, True, Colors.PRIMARY)
            screen.blit(action_surface, (500, 515))
        
        # VS indicator
        vs_surface = self.title_font.render("VS", True, (200, 50, 50))
        vs_rect = vs_surface.get_rect(center=(self.settings.SCREEN_WIDTH // 2, 250))
        screen.blit(vs_surface, vs_rect)
        
        # Render character cards
        cards_label = self.label_font.render("Team:", True, Colors.TEXT_SECONDARY)
        screen.blit(cards_label, (50, 540))
        
        for card in self.character_cards:
            card.render(screen)
        
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
        
        # Handle grid events
        if self.player_grid:
            self.player_grid.handle_event(event)
        if self.enemy_grid:
            self.enemy_grid.handle_event(event)
        
        # Handle button events
        for button in self.buttons:
            button.handle_event(event)
        
        # Handle card events
        for card in self.character_cards:
            card.handle_event(event)
    
    def _on_player_cell_click(self, row: int, col: int):
        """Handle player grid cell click"""
        content = self.player_grid.get_cell_content(row, col)
        if content:
            self.player_grid.select_cell(row, col)
            self.selected_character = content
            # Clear enemy grid selection
            self.enemy_grid.deselect()
    
    def _on_enemy_cell_click(self, row: int, col: int):
        """Handle enemy grid cell click"""
        if self.selected_action == "attack" and self.selected_character:
            content = self.enemy_grid.get_cell_content(row, col)
            if content:
                self._perform_attack(content)
    
    def _on_card_click(self, name: str):
        """Handle character card click"""
        # Find and select the character in the grid
        for row in range(3):
            for col in range(3):
                content = self.player_grid.get_cell_content(row, col)
                if content and content.get("name") == name:
                    self.player_grid.select_cell(row, col)
                    self.selected_character = content
                    return
    
    def _select_action(self, action: str):
        """Select an action"""
        self.selected_action = action
        
        if action == "attack":
            # Highlight enemy positions as targets
            self.enemy_grid.clear_highlights()
            targets = []
            for row in range(3):
                for col in range(3):
                    if self.enemy_grid.get_cell_content(row, col):
                        targets.append((row, col))
            self.enemy_grid.highlight_cells(targets, as_targets=True)
        
        elif action == "skill":
            self._show_skill_modal()
        
        elif action == "defend":
            # Immediate defend action
            self._show_message("Defend", "Character is defending. Damage reduced by 50% this turn.")
    
    def _perform_attack(self, target: dict):
        """Perform attack on target"""
        damage = 20
        self.health_bars["enemy"].current = max(0, self.health_bars["enemy"].current - damage)
        
        self.enemy_grid.clear_highlights()
        self.selected_action = None
        
        self._show_message("Attack!", f"Dealt {damage} damage to {target.get('name', 'enemy')}!")
    
    def _show_skill_modal(self):
        """Show skill selection modal"""
        self.modal = Modal(
            position=(self.settings.SCREEN_WIDTH // 2 - 200, self.settings.SCREEN_HEIGHT // 2 - 150),
            size=(400, 300),
            title="Select Skill",
            content="Choose a skill to use:\n\n• Long Tran Hào (100 Mana) - AOE damage\n• Thiên Khí (80 Mana) - Heal allies\n• Basic Strike (Free) - Single target",
            buttons=[
                {"text": "Use", "on_click": self._use_skill},
                {"text": "Cancel", "on_click": self._close_modal}
            ]
        )
    
    def _show_message(self, title: str, content: str):
        """Show a message modal"""
        self.modal = Modal(
            position=(self.settings.SCREEN_WIDTH // 2 - 200, self.settings.SCREEN_HEIGHT // 2 - 100),
            size=(400, 200),
            title=title,
            content=content,
            buttons=[
                {"text": "OK", "on_click": self._close_modal}
            ]
        )
    
    def _use_skill(self):
        """Use selected skill"""
        self.mana_bars["player"].current = max(0, self.mana_bars["player"].current - 30)
        self._close_modal()
        self._show_message("Skill Used!", "Basic Strike dealt 30 damage!")
    
    def _close_modal(self):
        """Close the modal"""
        if self.modal:
            self.modal.hide()
            self.modal = None
    
    def _end_turn(self):
        """End current turn"""
        self.turn += 1
        self.current_phase = "enemy" if self.current_phase == "player" else "player"
        self.selected_action = None
        self.selected_character = None
        self.player_grid.deselect()
        self.enemy_grid.deselect()
        self.enemy_grid.clear_highlights()
        
        # Regenerate some mana each turn
        self.mana_bars["player"].current = min(100, self.mana_bars["player"].current + 10)
        self.mana_bars["enemy"].current = min(100, self.mana_bars["enemy"].current + 10)
    
    def _on_back(self):
        """Handle back button click"""
        self.engine.change_scene("main_menu")
