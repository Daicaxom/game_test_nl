"""
Tests for GridPosition Value Object
Following TDD approach - tests written first
"""
import pytest
from app.domain.value_objects.grid_position import GridPosition


class TestGridPositionCreation:
    """Test GridPosition initialization"""
    
    def test_create_valid_position(self):
        """Should create position with valid coordinates"""
        pos = GridPosition(x=1, y=2)
        assert pos.x == 1
        assert pos.y == 2
    
    def test_create_corner_positions(self):
        """Should create all corner positions"""
        assert GridPosition(x=0, y=0)  # top-left
        assert GridPosition(x=0, y=2)  # bottom-left
        assert GridPosition(x=2, y=0)  # top-right
        assert GridPosition(x=2, y=2)  # bottom-right
    
    def test_create_center_position(self):
        """Should create center position"""
        pos = GridPosition(x=1, y=1)
        assert pos.x == 1
        assert pos.y == 1


class TestGridPositionValidation:
    """Test GridPosition validation"""
    
    def test_valid_position_in_range(self):
        """Positions 0-2 are valid for 3x3 grid"""
        pos = GridPosition(x=1, y=1)
        assert pos.is_valid() is True
    
    def test_invalid_negative_x(self):
        """Negative x coordinate is invalid"""
        with pytest.raises(ValueError):
            GridPosition(x=-1, y=0)
    
    def test_invalid_negative_y(self):
        """Negative y coordinate is invalid"""
        with pytest.raises(ValueError):
            GridPosition(x=0, y=-1)
    
    def test_invalid_x_out_of_range(self):
        """X coordinate >= 3 is invalid for 3x3 grid"""
        with pytest.raises(ValueError):
            GridPosition(x=3, y=0)
    
    def test_invalid_y_out_of_range(self):
        """Y coordinate >= 3 is invalid for 3x3 grid"""
        with pytest.raises(ValueError):
            GridPosition(x=0, y=3)


class TestGridPositionDistance:
    """Test distance calculations"""
    
    def test_distance_to_same_position(self):
        """Distance to self is 0"""
        pos = GridPosition(x=1, y=1)
        assert pos.distance_to(pos) == 0
    
    def test_distance_horizontal(self):
        """Horizontal distance"""
        pos1 = GridPosition(x=0, y=1)
        pos2 = GridPosition(x=2, y=1)
        assert pos1.distance_to(pos2) == 2
    
    def test_distance_vertical(self):
        """Vertical distance"""
        pos1 = GridPosition(x=1, y=0)
        pos2 = GridPosition(x=1, y=2)
        assert pos1.distance_to(pos2) == 2
    
    def test_distance_diagonal(self):
        """Diagonal distance (Manhattan distance)"""
        pos1 = GridPosition(x=0, y=0)
        pos2 = GridPosition(x=2, y=2)
        assert pos1.distance_to(pos2) == 4  # Manhattan distance
    
    def test_distance_is_symmetric(self):
        """Distance should be same regardless of direction"""
        pos1 = GridPosition(x=0, y=0)
        pos2 = GridPosition(x=2, y=1)
        assert pos1.distance_to(pos2) == pos2.distance_to(pos1)


class TestGridPositionAdjacency:
    """Test adjacency checks"""
    
    def test_horizontal_adjacent(self):
        """Horizontal neighbors are adjacent"""
        pos1 = GridPosition(x=1, y=1)
        pos2 = GridPosition(x=2, y=1)
        assert pos1.is_adjacent(pos2) is True
    
    def test_vertical_adjacent(self):
        """Vertical neighbors are adjacent"""
        pos1 = GridPosition(x=1, y=1)
        pos2 = GridPosition(x=1, y=2)
        assert pos1.is_adjacent(pos2) is True
    
    def test_diagonal_adjacent(self):
        """Diagonal positions are adjacent"""
        pos1 = GridPosition(x=1, y=1)
        pos2 = GridPosition(x=2, y=2)
        assert pos1.is_adjacent(pos2) is True
    
    def test_not_adjacent_far_position(self):
        """Positions more than 1 step away are not adjacent"""
        pos1 = GridPosition(x=0, y=0)
        pos2 = GridPosition(x=2, y=2)
        assert pos1.is_adjacent(pos2) is False
    
    def test_same_position_not_adjacent(self):
        """Same position is not considered adjacent"""
        pos = GridPosition(x=1, y=1)
        assert pos.is_adjacent(pos) is False


class TestGridPositionNeighbors:
    """Test neighbor retrieval"""
    
    def test_center_has_eight_neighbors(self):
        """Center position (1,1) has 8 neighbors"""
        pos = GridPosition(x=1, y=1)
        neighbors = pos.get_neighbors()
        assert len(neighbors) == 8
    
    def test_corner_has_three_neighbors(self):
        """Corner position has 3 neighbors"""
        pos = GridPosition(x=0, y=0)
        neighbors = pos.get_neighbors()
        assert len(neighbors) == 3
    
    def test_edge_has_five_neighbors(self):
        """Edge position (not corner) has 5 neighbors"""
        pos = GridPosition(x=1, y=0)
        neighbors = pos.get_neighbors()
        assert len(neighbors) == 5
    
    def test_neighbors_are_valid_positions(self):
        """All returned neighbors should be valid GridPositions"""
        pos = GridPosition(x=1, y=1)
        neighbors = pos.get_neighbors()
        for neighbor in neighbors:
            assert isinstance(neighbor, GridPosition)
            assert neighbor.is_valid()
    
    def test_self_not_in_neighbors(self):
        """Position itself should not be in neighbors list"""
        pos = GridPosition(x=1, y=1)
        neighbors = pos.get_neighbors()
        assert pos not in neighbors


class TestGridPositionAllPositions:
    """Test ALL_POSITIONS constant"""
    
    def test_all_positions_count(self):
        """Should have 9 positions for 3x3 grid"""
        assert len(GridPosition.ALL_POSITIONS) == 9
    
    def test_all_positions_are_valid(self):
        """All positions should be valid"""
        for pos in GridPosition.ALL_POSITIONS:
            assert pos.is_valid()
    
    def test_all_positions_unique(self):
        """All positions should be unique"""
        positions_set = set(GridPosition.ALL_POSITIONS)
        assert len(positions_set) == 9


class TestGridPositionEquality:
    """Test GridPosition equality"""
    
    def test_equal_positions(self):
        """Same coordinates should be equal"""
        pos1 = GridPosition(x=1, y=2)
        pos2 = GridPosition(x=1, y=2)
        assert pos1 == pos2
    
    def test_different_positions(self):
        """Different coordinates should not be equal"""
        pos1 = GridPosition(x=1, y=2)
        pos2 = GridPosition(x=2, y=1)
        assert pos1 != pos2
    
    def test_hash_for_equal_positions(self):
        """Equal positions should have same hash"""
        pos1 = GridPosition(x=1, y=2)
        pos2 = GridPosition(x=1, y=2)
        assert hash(pos1) == hash(pos2)
    
    def test_can_use_as_dict_key(self):
        """Should be usable as dictionary key"""
        pos1 = GridPosition(x=1, y=1)
        pos2 = GridPosition(x=1, y=1)
        data = {pos1: "value"}
        assert data[pos2] == "value"


class TestGridPositionImmutability:
    """Test that GridPosition is immutable"""
    
    def test_position_is_frozen(self):
        """Should not allow attribute modification"""
        pos = GridPosition(x=1, y=1)
        with pytest.raises((AttributeError, TypeError)):
            pos.x = 2
