"""
HexagonStats Value Object
Represents the six-dimensional stats (Lục Giác) for characters.
"""
from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class HexagonStats:
    """
    Immutable value object representing hexagonal stats.
    
    Attributes:
        hp: Hit Points
        atk: Attack power
        def_: Defense (using def_ to avoid Python keyword)
        spd: Speed
        crit: Critical rate (percentage)
        dex: Dexterity
    """
    
    hp: int
    atk: int
    def_: int
    spd: int
    crit: int
    dex: int
    
    @classmethod
    def default(cls) -> "HexagonStats":
        """Create stats with default values"""
        return cls(
            hp=100,
            atk=10,
            def_=5,
            spd=100,
            crit=5,
            dex=10
        )
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HexagonStats":
        """
        Create HexagonStats from dictionary.
        Uses uppercase keys for compatibility with game data format.
        Missing keys will use default values.
        """
        defaults = cls.default()
        return cls(
            hp=data.get("HP", defaults.hp),
            atk=data.get("ATK", defaults.atk),
            def_=data.get("DEF", defaults.def_),
            spd=data.get("SPD", defaults.spd),
            crit=data.get("CRIT", defaults.crit),
            dex=data.get("DEX", defaults.dex)
        )
    
    def get_total_power(self) -> int:
        """Calculate the sum of all stats (total power)"""
        return self.hp + self.atk + self.def_ + self.spd + self.crit + self.dex
    
    def add(self, other: "HexagonStats") -> "HexagonStats":
        """
        Add two stats together, returning a new HexagonStats instance.
        
        Args:
            other: Another HexagonStats to add
            
        Returns:
            New HexagonStats with summed values
        """
        return HexagonStats(
            hp=self.hp + other.hp,
            atk=self.atk + other.atk,
            def_=self.def_ + other.def_,
            spd=self.spd + other.spd,
            crit=self.crit + other.crit,
            dex=self.dex + other.dex
        )
    
    def multiply(self, factor: float) -> "HexagonStats":
        """
        Multiply all stats by a factor, returning a new HexagonStats instance.
        Results are truncated to integers.
        
        Args:
            factor: Multiplication factor
            
        Returns:
            New HexagonStats with multiplied values
        """
        return HexagonStats(
            hp=int(self.hp * factor),
            atk=int(self.atk * factor),
            def_=int(self.def_ * factor),
            spd=int(self.spd * factor),
            crit=int(self.crit * factor),
            dex=int(self.dex * factor)
        )
    
    def to_dict(self) -> Dict[str, int]:
        """
        Convert to dictionary with uppercase keys.
        Compatible with game data format.
        """
        return {
            "HP": self.hp,
            "ATK": self.atk,
            "DEF": self.def_,
            "SPD": self.spd,
            "CRIT": self.crit,
            "DEX": self.dex
        }
