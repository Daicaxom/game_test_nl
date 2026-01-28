"""
Tests for Grid UI component
Following TDD approach
"""
import pytest
import pygame
from unittest.mock import Mock
from game.ui.components.grid import Grid, GridCell


# Initialize pygame for testing
pygame.init()
pygame.display.set_mode((100, 100), pygame.HIDDEN)


class TestGridCreation:
    """Test Grid component creation"""
    
    def test_create_grid_with_default_values(self):
        """Should create 3x3 grid with default values"""
        grid = Grid(position=(10, 20))
        
        assert grid.rows == 3
        assert grid.cols == 3
        assert len(grid.cells) == 3
        assert len(grid.cells[0]) == 3
    
    def test_create_grid_with_custom_size(self):
        """Should create grid with custom cell size"""
        grid = Grid(position=(0, 0), cell_size=100, spacing=10)
        
        assert grid.cell_size == 100
        assert grid.spacing == 10
    
    def test_create_grid_with_custom_dimensions(self):
        """Should create grid with custom rows and columns"""
        grid = Grid(position=(0, 0), rows=4, cols=5)
        
        assert grid.rows == 4
        assert grid.cols == 5
        assert len(grid.cells) == 4
        assert len(grid.cells[0]) == 5
    
    def test_grid_width_calculation(self):
        """Should calculate total grid width correctly"""
        grid = Grid(position=(0, 0), cell_size=80, spacing=5, cols=3)
        
        expected_width = 3 * 80 + 2 * 5  # 3 cells + 2 gaps
        assert grid.width == expected_width
    
    def test_grid_height_calculation(self):
        """Should calculate total grid height correctly"""
        grid = Grid(position=(0, 0), cell_size=80, spacing=5, rows=3)
        
        expected_height = 3 * 80 + 2 * 5  # 3 cells + 2 gaps
        assert grid.height == expected_height


class TestGridCellOperations:
    """Test Grid cell operations"""
    
    def test_get_cell_valid_position(self):
        """Should get cell at valid position"""
        grid = Grid(position=(0, 0))
        
        cell = grid.get_cell(1, 1)
        assert cell is not None
        assert cell.row == 1
        assert cell.col == 1
    
    def test_get_cell_invalid_position(self):
        """Should return None for invalid position"""
        grid = Grid(position=(0, 0))
        
        assert grid.get_cell(-1, 0) is None
        assert grid.get_cell(0, -1) is None
        assert grid.get_cell(3, 0) is None
        assert grid.get_cell(0, 3) is None
    
    def test_set_cell_content(self):
        """Should set content for a cell"""
        grid = Grid(position=(0, 0))
        content = {"name": "Hero", "element": "Hỏa"}
        
        grid.set_cell_content(1, 1, content)
        
        assert grid.get_cell_content(1, 1) == content
    
    def test_clear_cell(self):
        """Should clear content from a cell"""
        grid = Grid(position=(0, 0))
        grid.set_cell_content(1, 1, "Test")
        
        grid.clear_cell(1, 1)
        
        assert grid.get_cell_content(1, 1) is None
    
    def test_clear_all_cells(self):
        """Should clear all cells"""
        grid = Grid(position=(0, 0))
        grid.set_cell_content(0, 0, "A")
        grid.set_cell_content(1, 1, "B")
        grid.set_cell_content(2, 2, "C")
        
        grid.clear_all()
        
        for row in range(3):
            for col in range(3):
                assert grid.get_cell_content(row, col) is None


class TestGridSelection:
    """Test Grid selection functionality"""
    
    def test_select_cell(self):
        """Should select a cell"""
        grid = Grid(position=(0, 0))
        
        grid.select_cell(1, 1)
        
        assert grid.selected_cell == (1, 1)
        assert grid.get_cell(1, 1).is_selected is True
    
    def test_select_new_cell_deselects_previous(self):
        """Selecting new cell should deselect previous"""
        grid = Grid(position=(0, 0))
        
        grid.select_cell(0, 0)
        grid.select_cell(1, 1)
        
        assert grid.selected_cell == (1, 1)
        assert grid.get_cell(0, 0).is_selected is False
        assert grid.get_cell(1, 1).is_selected is True
    
    def test_deselect(self):
        """Should deselect current selection"""
        grid = Grid(position=(0, 0))
        grid.select_cell(1, 1)
        
        grid.deselect()
        
        assert grid.selected_cell is None
        assert grid.get_cell(1, 1).is_selected is False


class TestGridHighlighting:
    """Test Grid highlighting functionality"""
    
    def test_highlight_cells(self):
        """Should highlight specified cells"""
        grid = Grid(position=(0, 0))
        
        positions = [(0, 0), (0, 1), (1, 0)]
        grid.highlight_cells(positions)
        
        assert grid.get_cell(0, 0).is_highlighted is True
        assert grid.get_cell(0, 1).is_highlighted is True
        assert grid.get_cell(1, 0).is_highlighted is True
        assert grid.get_cell(1, 1).is_highlighted is False
    
    def test_highlight_cells_as_targets(self):
        """Should highlight cells as attack targets"""
        grid = Grid(position=(0, 0))
        
        grid.highlight_cells([(1, 1), (1, 2)], as_targets=True)
        
        assert grid.get_cell(1, 1).is_target is True
        assert grid.get_cell(1, 2).is_target is True
    
    def test_clear_highlights(self):
        """Should clear all highlights"""
        grid = Grid(position=(0, 0))
        grid.highlight_cells([(0, 0), (1, 1)])
        grid.highlight_cells([(2, 2)], as_targets=True)
        
        grid.clear_highlights()
        
        for row in range(3):
            for col in range(3):
                cell = grid.get_cell(row, col)
                assert cell.is_highlighted is False
                assert cell.is_target is False


class TestGridEvents:
    """Test Grid event handling"""
    
    def test_cell_click_callback(self):
        """Should call on_cell_click when cell is clicked"""
        callback = Mock()
        grid = Grid(position=(0, 0), cell_size=80, spacing=5, on_cell_click=callback)
        
        # Simulate click in first cell area
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (40, 40)})
        grid.handle_event(event)
        
        callback.assert_called_once_with(0, 0)


class TestGridRendering:
    """Test Grid component rendering"""
    
    def test_grid_renders_without_error(self):
        """Grid should render to a surface without error"""
        grid = Grid(position=(10, 10))
        screen = pygame.Surface((500, 500))
        
        # Should not raise exception
        grid.render(screen)
    
    def test_grid_renders_with_content(self):
        """Grid should render correctly with cell content"""
        grid = Grid(position=(10, 10))
        grid.set_cell_content(1, 1, {"name": "Hero", "element": "Hỏa"})
        
        screen = pygame.Surface((500, 500))
        grid.render(screen)  # Should not raise
    
    def test_grid_renders_with_selection(self):
        """Grid should render selected cell differently"""
        grid = Grid(position=(10, 10))
        grid.select_cell(1, 1)
        
        screen = pygame.Surface((500, 500))
        grid.render(screen)  # Should not raise
    
    def test_grid_renders_with_highlights(self):
        """Grid should render highlighted cells correctly"""
        grid = Grid(position=(10, 10))
        grid.highlight_cells([(0, 0), (1, 1)])
        grid.highlight_cells([(2, 2)], as_targets=True)
        
        screen = pygame.Surface((500, 500))
        grid.render(screen)  # Should not raise
