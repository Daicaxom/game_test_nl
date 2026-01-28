"""
Modal UI Component
Dialog box for displaying information or confirmations
"""
import pygame
from typing import Tuple, Optional, Callable, List
from game.ui.components.button import Button


class Modal:
    """Modal dialog component for displaying information or confirmations"""
    
    def __init__(
        self,
        position: Tuple[int, int],
        size: Tuple[int, int] = (400, 300),
        title: str = "",
        content: str = "",
        buttons: Optional[List[dict]] = None,
        bg_color: Tuple[int, int, int] = (40, 40, 60),
        border_color: Tuple[int, int, int] = (70, 130, 180),
        overlay_alpha: int = 128,
        closable: bool = True,
        on_close: Optional[Callable] = None
    ):
        """
        Initialize modal component
        
        Args:
            position: (x, y) position of the modal (top-left corner)
            size: (width, height) of the modal
            title: Modal title text
            content: Modal content/message text
            buttons: List of button configs [{"text": "OK", "on_click": callable}, ...]
            bg_color: Background color
            border_color: Border color
            overlay_alpha: Alpha value for background overlay (0-255)
            closable: Whether modal can be closed by clicking outside
            on_close: Callback when modal is closed
        """
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.title = title
        self.content = content
        self.bg_color = bg_color
        self.border_color = border_color
        self.overlay_alpha = overlay_alpha
        self.closable = closable
        self.on_close = on_close
        
        self.visible = True
        self.buttons: List[Button] = []
        
        # Pre-create fonts
        self.title_font = pygame.font.Font(None, 32)
        self.content_font = pygame.font.Font(None, 22)
        
        # Cache wrapped content lines
        self._wrapped_lines: List[str] = []
        self._wrap_content()
        
        # Close button rect (for click detection)
        self._close_button_rect = pygame.Rect(
            self.rect.right - 30, self.rect.y + 8, 24, 24
        ) if self.closable else None
        
        # Create buttons
        self._create_buttons(buttons or [])
    
    def _create_buttons(self, button_configs: List[dict]):
        """
        Create button components from configs
        
        Args:
            button_configs: List of button configuration dictionaries
        """
        if not button_configs:
            return
        
        # Position buttons at bottom of modal
        button_width = 100
        button_height = 35
        button_spacing = 20
        total_width = len(button_configs) * button_width + (len(button_configs) - 1) * button_spacing
        start_x = self.rect.centerx - total_width // 2
        button_y = self.rect.bottom - button_height - 20
        
        for i, config in enumerate(button_configs):
            button = Button(
                position=(start_x + i * (button_width + button_spacing), button_y),
                size=(button_width, button_height),
                text=config.get("text", "Button"),
                on_click=config.get("on_click")
            )
            self.buttons.append(button)
    
    def _wrap_content(self):
        """Pre-calculate wrapped content lines"""
        if not self.content:
            self._wrapped_lines = []
            return
        
        max_width = self.rect.width - 40
        words = self.content.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            test_text = ' '.join(current_line)
            if self.content_font.size(test_text)[0] > max_width:
                if len(current_line) > 1:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(test_text)
                    current_line = []
        
        if current_line:
            lines.append(' '.join(current_line))
        
        self._wrapped_lines = lines
    
    def show(self):
        """Show the modal"""
        self.visible = True
    
    def hide(self):
        """Hide the modal"""
        self.visible = False
        if self.on_close:
            self.on_close()
    
    def update(self, dt: float):
        """
        Update modal state
        
        Args:
            dt: Delta time in seconds
        """
        if not self.visible:
            return
        
        for button in self.buttons:
            button.update(dt)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame events
        
        Args:
            event: Pygame event
            
        Returns:
            True if event was handled (consumed by modal)
        """
        if not self.visible:
            return False
        
        # Handle button events
        for button in self.buttons:
            if button.handle_event(event):
                return True
        
        # Handle clicking close button or outside to close
        if self.closable and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                # Check close button
                if self._close_button_rect and self._close_button_rect.collidepoint(mouse_pos):
                    self.hide()
                    return True
                # Check clicking outside
                if not self.rect.collidepoint(mouse_pos):
                    self.hide()
                    return True
        
        # Handle escape key to close
        if self.closable and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.hide()
                return True
        
        # Modal consumes all events when visible
        return True
    
    def render(self, screen: pygame.Surface):
        """
        Render modal to screen
        
        Args:
            screen: Pygame surface to render to
        """
        if not self.visible:
            return
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, self.overlay_alpha))
        screen.blit(overlay, (0, 0))
        
        # Draw modal background
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, self.border_color, self.rect, 2, border_radius=10)
        
        # Draw title bar
        title_bar_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, 40)
        pygame.draw.rect(screen, self.border_color, title_bar_rect, border_radius=10)
        # Fix the bottom corners of title bar
        bottom_rect = pygame.Rect(self.rect.x, self.rect.y + 30, self.rect.width, 10)
        pygame.draw.rect(screen, self.border_color, bottom_rect)
        
        # Draw title text
        if self.title:
            title_surface = self.title_font.render(self.title, True, (255, 255, 255))
            title_rect = title_surface.get_rect(centerx=self.rect.centerx, centery=self.rect.y + 20)
            screen.blit(title_surface, title_rect)
        
        # Draw close button (X) if closable
        if self.closable:
            close_x = self.rect.right - 25
            close_y = self.rect.y + 12
            close_color = (200, 200, 200)
            pygame.draw.line(screen, close_color, (close_x, close_y), (close_x + 16, close_y + 16), 2)
            pygame.draw.line(screen, close_color, (close_x + 16, close_y), (close_x, close_y + 16), 2)
        
        # Draw content text (using pre-wrapped lines)
        if self._wrapped_lines:
            content_y = self.rect.y + 60
            for i, line in enumerate(self._wrapped_lines):
                line_surface = self.content_font.render(line, True, (220, 220, 220))
                screen.blit(line_surface, (self.rect.x + 20, content_y + i * 25))
        
        # Draw buttons
        for button in self.buttons:
            button.render(screen)
