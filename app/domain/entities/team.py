"""
Team Entity - Team composition and formation management
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any, Tuple, Set
from collections import Counter

from app.domain.entities.hero import Hero
from app.domain.value_objects.element import Element
from app.domain.value_objects.grid_position import GridPosition


@dataclass
class TeamSlot:
    """
    Represents a slot in the team with hero and position.
    
    Attributes:
        hero: The hero in this slot
        position: Grid position in formation
    """
    hero: Hero
    position: GridPosition


@dataclass
class FormationBonus:
    """
    Represents a bonus granted by a formation.
    
    Attributes:
        stat: The stat to modify (e.g., "atk", "def_", "all")
        value: The bonus value
        bonus_type: "flat" or "percent"
    """
    stat: str
    value: float
    bonus_type: str = "percent"  # "flat" or "percent"


@dataclass
class Formation:
    """
    Battle formation with requirements and bonuses.
    
    Attributes:
        id: Unique identifier
        name: Display name
        description: Formation description
        required_elements: Number of unique elements required
        required_heroes: Specific hero template IDs required
        positions: Optimal positions for formation
        bonuses: List of stat bonuses when formation is active
    """
    
    id: str
    name: str
    description: str = ""
    required_elements: int = 0
    required_heroes: List[str] = field(default_factory=list)
    positions: List[Tuple[int, int]] = field(default_factory=list)
    bonuses: List[FormationBonus] = field(default_factory=list)
    min_members: int = 1
    
    def check_requirements(self, team: "Team") -> bool:
        """
        Check if a team meets the formation requirements.
        
        Args:
            team: Team to check
            
        Returns:
            True if requirements are met
        """
        # Check minimum members
        if len(team.members) < self.min_members:
            return False
        
        # Check element diversity requirement
        if self.required_elements > 0:
            elements = {slot.hero.element for slot in team.members}
            if len(elements) < self.required_elements:
                return False
        
        # Check specific hero requirements
        if self.required_heroes:
            hero_templates = {slot.hero.template_id for slot in team.members}
            if not all(h in hero_templates for h in self.required_heroes):
                return False
        
        return True
    
    def get_bonus_value(self, stat: str) -> float:
        """
        Get total bonus value for a specific stat.
        
        Args:
            stat: Stat name to get bonus for
            
        Returns:
            Total bonus value (as multiplier for percent, flat value otherwise)
        """
        total = 0
        for bonus in self.bonuses:
            if bonus.stat == stat or bonus.stat == "all":
                total += bonus.value
        return total


@dataclass
class Team:
    """
    Team entity managing hero composition and formation.
    
    Attributes:
        id: Unique team identifier
        player_id: Owner player ID
        name: Team name
        slot_number: Team slot (1-10)
        members: List of team slots with heroes
        formation: Active formation (if any)
        max_members: Maximum team size (default 5)
        is_default: Whether this is the default team
    """
    
    id: str
    player_id: str
    name: str
    slot_number: int
    
    members: List[TeamSlot] = field(default_factory=list)
    formation: Optional[Formation] = None
    max_members: int = 5
    is_default: bool = False
    
    def add_member(self, hero: Hero, position: GridPosition) -> bool:
        """
        Add a hero to the team.
        
        Args:
            hero: Hero to add
            position: Grid position for the hero
            
        Returns:
            True if added successfully, False otherwise
        """
        # Check max members
        if len(self.members) >= self.max_members:
            return False
        
        # Check if hero already in team
        if any(slot.hero.id == hero.id for slot in self.members):
            return False
        
        # Check if position is occupied
        if any(slot.position == position for slot in self.members):
            return False
        
        self.members.append(TeamSlot(hero=hero, position=position))
        return True
    
    def remove_member(self, hero_id: str) -> bool:
        """
        Remove a hero from the team.
        
        Args:
            hero_id: ID of hero to remove
            
        Returns:
            True if removed successfully, False if not found
        """
        for i, slot in enumerate(self.members):
            if slot.hero.id == hero_id:
                self.members.pop(i)
                return True
        return False
    
    def move_member(self, hero_id: str, new_position: GridPosition) -> bool:
        """
        Move a hero to a new position.
        
        Args:
            hero_id: ID of hero to move
            new_position: New grid position
            
        Returns:
            True if moved successfully
        """
        # Check if new position is occupied
        for slot in self.members:
            if slot.position == new_position and slot.hero.id != hero_id:
                return False
        
        # Find and move the hero
        for slot in self.members:
            if slot.hero.id == hero_id:
                slot.position = new_position
                return True
        
        return False
    
    def get_member_at_position(self, position: GridPosition) -> Optional[Hero]:
        """
        Get the hero at a specific position.
        
        Args:
            position: Grid position to check
            
        Returns:
            Hero at position or None
        """
        for slot in self.members:
            if slot.position == position:
                return slot.hero
        return None
    
    def set_formation(self, formation: Optional[Formation]) -> None:
        """
        Set the team's active formation.
        
        Args:
            formation: Formation to set, or None to clear
        """
        self.formation = formation
    
    def is_formation_active(self) -> bool:
        """
        Check if the current formation requirements are met.
        
        Returns:
            True if formation is active and requirements met
        """
        if not self.formation:
            return False
        return self.formation.check_requirements(self)
    
    def get_total_power(self, include_formation: bool = True) -> int:
        """
        Calculate total team power.
        
        Args:
            include_formation: Whether to include formation bonuses
            
        Returns:
            Total power rating
        """
        base_power = sum(slot.hero.get_total_power() for slot in self.members)
        
        if include_formation and self.is_formation_active():
            # Apply formation bonus
            all_bonus = self.formation.get_bonus_value("all")
            base_power = int(base_power * (1 + all_bonus / 100))
        
        # Add synergy bonuses
        synergy_bonus = self.calculate_element_synergy()
        
        return base_power + synergy_bonus
    
    def calculate_element_synergy(self) -> int:
        """
        Calculate synergy bonus from adjacent same-element heroes.
        
        Returns:
            Synergy bonus value
        """
        bonus = 0
        
        for i, slot1 in enumerate(self.members):
            for slot2 in self.members[i+1:]:
                if slot1.hero.element == slot2.hero.element:
                    if slot1.position.is_adjacent(slot2.position):
                        # Same element adjacent bonus
                        bonus += 50
        
        return bonus
    
    def get_element_distribution(self) -> Dict[Element, int]:
        """
        Get the distribution of elements in the team.
        
        Returns:
            Dictionary mapping elements to count
        """
        elements = [slot.hero.element for slot in self.members]
        return dict(Counter(elements))
    
    def get_heroes(self) -> List[Hero]:
        """
        Get all heroes in the team.
        
        Returns:
            List of heroes
        """
        return [slot.hero for slot in self.members]
    
    def get_hero_positions(self) -> Dict[str, GridPosition]:
        """
        Get mapping of hero IDs to positions.
        
        Returns:
            Dictionary mapping hero ID to grid position
        """
        return {slot.hero.id: slot.position for slot in self.members}
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert team to dictionary for serialization.
        
        Returns:
            Dictionary representation
        """
        return {
            "id": self.id,
            "name": self.name,
            "slot_number": self.slot_number,
            "members": [
                {
                    "hero_id": slot.hero.id,
                    "hero_name": slot.hero.name,
                    "position": {"x": slot.position.x, "y": slot.position.y}
                }
                for slot in self.members
            ],
            "formation_id": self.formation.id if self.formation else None,
            "total_power": self.get_total_power(),
            "is_default": self.is_default
        }
