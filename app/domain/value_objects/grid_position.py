"""
GridPosition Value Object
Represents a position on the 3x3 battle grid.
"""
from dataclasses import dataclass
from typing import List, ClassVar


@dataclass(frozen=True)
class GridPosition:
    """
    Immutable value object representing a position on the 3x3 battle grid.
    
    Coordinates:
        x: Column (0-2, left to right)
        y: Row (0-2, top to bottom)
    
    Grid Layout:
        (0,0) (1,0) (2,0)
        (0,1) (1,1) (2,1)
        (0,2) (1,2) (2,2)
    """
    
    x: int
    y: int
    
    GRID_SIZE: ClassVar[int] = 3
    
    def __post_init__(self) -> None:
        """Validate coordinates after initialization"""
        if not (0 <= self.x < self.GRID_SIZE):
            raise ValueError(f"x coordinate must be 0-{self.GRID_SIZE - 1}, got {self.x}")
        if not (0 <= self.y < self.GRID_SIZE):
            raise ValueError(f"y coordinate must be 0-{self.GRID_SIZE - 1}, got {self.y}")
    
    def is_valid(self) -> bool:
        """Check if position is within the grid bounds"""
        return 0 <= self.x < self.GRID_SIZE and 0 <= self.y < self.GRID_SIZE
    
    def distance_to(self, other: "GridPosition") -> int:
        """
        Calculate Manhattan distance to another position.
        
        Args:
            other: Target position
            
        Returns:
            Manhattan distance (|x1-x2| + |y1-y2|)
        """
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def is_adjacent(self, other: "GridPosition") -> bool:
        """
        Check if another position is adjacent (including diagonals).
        
        Args:
            other: Position to check
            
        Returns:
            True if positions are adjacent (not same), False otherwise
        """
        if self == other:
            return False
        
        dx = abs(self.x - other.x)
        dy = abs(self.y - other.y)
        
        return dx <= 1 and dy <= 1
    
    def get_neighbors(self) -> List["GridPosition"]:
        """
        Get all valid adjacent positions (including diagonals).
        
        Returns:
            List of valid adjacent GridPositions
        """
        neighbors: List[GridPosition] = []
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue  # Skip self
                    
                new_x = self.x + dx
                new_y = self.y + dy
                
                if 0 <= new_x < self.GRID_SIZE and 0 <= new_y < self.GRID_SIZE:
                    neighbors.append(GridPosition(new_x, new_y))
        
        return neighbors
    
    @classmethod
    @property
    def ALL_POSITIONS(cls) -> List["GridPosition"]:
        """
        Get all 9 positions on the 3x3 grid.
        
        Returns:
            List of all valid GridPositions
        """
        return [
            GridPosition(x, y)
            for x in range(cls.GRID_SIZE)
            for y in range(cls.GRID_SIZE)
        ]
