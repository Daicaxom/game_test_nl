"""
Grid UI Component
Battle grid (3x3) for turn-based combat positioning
"""
import pygame
from typing import Tuple, Optional, Callable, List, Any


class GridCell:
    """Individual cell in the battle grid"""
    
    def __init__(
        self,
        row: int,
        col: int,
        rect: pygame.Rect,
        bg_color: Tuple[int, int, int] = (50, 50, 70),
        highlight_color: Tuple[int, int, int] = (70, 130, 180),
        border_color: Tuple[int, int, int] = (100, 100, 120)
    ):
        """
        Initialize grid cell
        
        Args:
            row: Row index (0-2)
            col: Column index (0-2)
            rect: Cell rectangle
            bg_color: Background color
            highlight_color: Color when highlighted/selected
            border_color: Border color
        """
        self.row = row
        self.col = col
        self.rect = rect
        self.bg_color = bg_color
        self.highlight_color = highlight_color
        self.border_color = border_color
        
        self.content: Any = None  # Character or item in this cell
        self.is_hovered = False
        self.is_selected = False
        self.is_highlighted = False  # For showing valid moves
        self.is_target = False  # For showing attack targets


class Grid:
    """3x3 Battle grid component"""
    
    # Class-level element colors to avoid recreation
    ELEMENT_COLORS = {
        "Kim": (255, 215, 0),
        "Mộc": (34, 139, 34),
        "Thủy": (30, 144, 255),
        "Hỏa": (255, 69, 0),
        "Thổ": (139, 69, 19),
    }
    
    def __init__(
        self,
        position: Tuple[int, int],
        cell_size: int = 80,
        spacing: int = 5,
        rows: int = 3,
        cols: int = 3,
        bg_color: Tuple[int, int, int] = (50, 50, 70),
        highlight_color: Tuple[int, int, int] = (70, 130, 180),
        border_color: Tuple[int, int, int] = (100, 100, 120),
        on_cell_click: Optional[Callable[[int, int], None]] = None,
        on_cell_hover: Optional[Callable[[int, int], None]] = None
    ):
        """
        Initialize grid component
        
        Args:
            position: (x, y) top-left position of the grid
            cell_size: Size of each cell (square)
            spacing: Spacing between cells
            rows: Number of rows (default 3)
            cols: Number of columns (default 3)
            bg_color: Cell background color
            highlight_color: Color for highlighted cells
            border_color: Cell border color
            on_cell_click: Callback when a cell is clicked (row, col)
            on_cell_hover: Callback when mouse hovers over a cell (row, col)
        """
        self.position = position
        self.cell_size = cell_size
        self.spacing = spacing
        self.rows = rows
        self.cols = cols
        self.bg_color = bg_color
        self.highlight_color = highlight_color
        self.border_color = border_color
        self.on_cell_click = on_cell_click
        self.on_cell_hover = on_cell_hover
        
        self.cells: List[List[GridCell]] = []
        self.selected_cell: Optional[Tuple[int, int]] = None
        
        self._create_cells()
        
        # Pre-create font
        self.label_font = pygame.font.Font(None, 20)
    
    def _create_cells(self):
        """Create grid cells"""
        self.cells = []
        x_start, y_start = self.position
        
        for row in range(self.rows):
            row_cells = []
            for col in range(self.cols):
                x = x_start + col * (self.cell_size + self.spacing)
                y = y_start + row * (self.cell_size + self.spacing)
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                
                cell = GridCell(
                    row=row,
                    col=col,
                    rect=rect,
                    bg_color=self.bg_color,
                    highlight_color=self.highlight_color,
                    border_color=self.border_color
                )
                row_cells.append(cell)
            self.cells.append(row_cells)
    
    @property
    def width(self) -> int:
        """Total width of the grid"""
        return self.cols * self.cell_size + (self.cols - 1) * self.spacing
    
    @property
    def height(self) -> int:
        """Total height of the grid"""
        return self.rows * self.cell_size + (self.rows - 1) * self.spacing
    
    def get_cell(self, row: int, col: int) -> Optional[GridCell]:
        """
        Get cell at specified position
        
        Args:
            row: Row index
            col: Column index
            
        Returns:
            GridCell or None if invalid position
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.cells[row][col]
        return None
    
    def set_cell_content(self, row: int, col: int, content: Any):
        """
        Set content for a cell
        
        Args:
            row: Row index
            col: Column index
            content: Content to place in cell (character, item, etc.)
        """
        cell = self.get_cell(row, col)
        if cell:
            cell.content = content
    
    def get_cell_content(self, row: int, col: int) -> Any:
        """
        Get content from a cell
        
        Args:
            row: Row index
            col: Column index
            
        Returns:
            Cell content or None
        """
        cell = self.get_cell(row, col)
        return cell.content if cell else None
    
    def clear_cell(self, row: int, col: int):
        """
        Clear content from a cell
        
        Args:
            row: Row index
            col: Column index
        """
        cell = self.get_cell(row, col)
        if cell:
            cell.content = None
    
    def clear_all(self):
        """Clear all cells"""
        for row in self.cells:
            for cell in row:
                cell.content = None
    
    def select_cell(self, row: int, col: int):
        """
        Select a cell
        
        Args:
            row: Row index
            col: Column index
        """
        # Deselect previous
        if self.selected_cell:
            old_row, old_col = self.selected_cell
            self.cells[old_row][old_col].is_selected = False
        
        # Select new
        cell = self.get_cell(row, col)
        if cell:
            cell.is_selected = True
            self.selected_cell = (row, col)
    
    def deselect(self):
        """Deselect current selection"""
        if self.selected_cell:
            row, col = self.selected_cell
            self.cells[row][col].is_selected = False
            self.selected_cell = None
    
    def highlight_cells(self, positions: List[Tuple[int, int]], as_targets: bool = False):
        """
        Highlight specified cells
        
        Args:
            positions: List of (row, col) positions to highlight
            as_targets: If True, highlight as attack targets
        """
        for row, col in positions:
            cell = self.get_cell(row, col)
            if cell:
                if as_targets:
                    cell.is_target = True
                else:
                    cell.is_highlighted = True
    
    def clear_highlights(self):
        """Clear all cell highlights"""
        for row in self.cells:
            for cell in row:
                cell.is_highlighted = False
                cell.is_target = False
    
    def update(self, dt: float):
        """
        Update grid state
        
        Args:
            dt: Delta time in seconds
        """
        mouse_pos = pygame.mouse.get_pos()
        
        for row in self.cells:
            for cell in row:
                was_hovered = cell.is_hovered
                cell.is_hovered = cell.rect.collidepoint(mouse_pos)
                
                # Trigger hover callback on change
                if cell.is_hovered and not was_hovered and self.on_cell_hover:
                    self.on_cell_hover(cell.row, cell.col)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame events
        
        Args:
            event: Pygame event
            
        Returns:
            True if event was handled
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for row in self.cells:
                    for cell in row:
                        if cell.rect.collidepoint(mouse_pos):
                            if self.on_cell_click:
                                self.on_cell_click(cell.row, cell.col)
                            return True
        return False
    
    def render(self, screen: pygame.Surface):
        """
        Render grid to screen
        
        Args:
            screen: Pygame surface to render to
        """
        for row in self.cells:
            for cell in row:
                self._render_cell(screen, cell)
    
    def _render_cell(self, screen: pygame.Surface, cell: GridCell):
        """
        Render a single cell
        
        Args:
            screen: Pygame surface to render to
            cell: GridCell to render
        """
        # Determine cell color based on state
        if cell.is_selected:
            color = (100, 180, 220)  # Light blue for selected
        elif cell.is_target:
            color = (200, 80, 80)  # Red for targets
        elif cell.is_highlighted:
            color = (80, 180, 80)  # Green for valid moves
        elif cell.is_hovered:
            color = tuple(min(c + 30, 255) for c in cell.bg_color)
        else:
            color = cell.bg_color
        
        # Draw cell background
        pygame.draw.rect(screen, color, cell.rect, border_radius=5)
        
        # Draw border
        border_color = cell.border_color
        if cell.is_selected:
            border_color = (255, 255, 255)
        pygame.draw.rect(screen, border_color, cell.rect, 2, border_radius=5)
        
        # Draw content (if character, draw a simple representation)
        if cell.content:
            self._render_cell_content(screen, cell)
        
        # Draw position label (for debugging/demo)
        label = f"({cell.row},{cell.col})"
        label_surface = self.label_font.render(label, True, (150, 150, 150))
        label_rect = label_surface.get_rect(
            bottomright=(cell.rect.right - 5, cell.rect.bottom - 5)
        )
        screen.blit(label_surface, label_rect)
    
    def _render_cell_content(self, screen: pygame.Surface, cell: GridCell):
        """
        Render cell content (character or item)
        
        Args:
            screen: Pygame surface to render to
            cell: GridCell with content
        """
        content = cell.content
        
        # If content has a render method, use it
        if hasattr(content, 'render'):
            content.render(screen)
            return
        
        # Otherwise, render a simple placeholder
        if isinstance(content, dict):
            # Dictionary with character info
            name = content.get('name', '?')
            element = content.get('element', None)
            
            color = self.ELEMENT_COLORS.get(element, (200, 200, 200))
            
            # Draw character circle
            pygame.draw.circle(
                screen,
                color,
                cell.rect.center,
                self.cell_size // 3
            )
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                cell.rect.center,
                self.cell_size // 3,
                2
            )
            
            # Draw name
            name_surface = self.label_font.render(name[:4], True, (255, 255, 255))
            name_rect = name_surface.get_rect(center=cell.rect.center)
            screen.blit(name_surface, name_rect)
        elif isinstance(content, str):
            # Simple string label
            text_surface = self.label_font.render(content[:4], True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=cell.rect.center)
            screen.blit(text_surface, text_rect)
