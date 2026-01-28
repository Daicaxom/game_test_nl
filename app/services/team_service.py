"""
Team Service - Business logic for team management
"""
from typing import Optional, Dict, Any, List
from uuid import uuid4

from app.core.exceptions import (
    TeamNotFoundException,
    HeroNotFoundException,
    TeamFullException,
    ValidationException
)


class TeamService:
    """
    Service for team management operations.
    
    Handles:
    - Team creation and management
    - Formation management
    - Team composition
    """
    
    # In-memory storage (would be in database)
    _teams: Dict[str, Dict[str, Any]] = {}
    MAX_TEAMS_PER_PLAYER = 10
    MAX_MEMBERS_PER_TEAM = 5
    
    def __init__(self, hero_service=None):
        """
        Initialize the team service.
        
        Args:
            hero_service: Optional HeroService for hero validation
        """
        self.hero_service = hero_service
    
    async def get_teams(self, player_id: str) -> List[dict]:
        """
        Get all teams for a player.
        
        Args:
            player_id: The player ID
            
        Returns:
            List of team data
        """
        teams = [
            team for team_id, team in self._teams.items()
            if team["player_id"] == player_id
        ]
        
        if not teams:
            # Create default team
            default_team = await self.create_team(
                player_id,
                name="Default Team",
                is_default=True
            )
            teams = [default_team]
        
        return teams
    
    async def get_team(self, team_id: str, player_id: str) -> dict:
        """
        Get specific team details.
        
        Args:
            team_id: The team ID
            player_id: The player ID for ownership verification
            
        Returns:
            Team data
            
        Raises:
            TeamNotFoundException: If team not found
        """
        team = self._teams.get(team_id)
        if not team or team["player_id"] != player_id:
            raise TeamNotFoundException(team_id)
        
        return team
    
    async def create_team(
        self,
        player_id: str,
        name: str,
        is_default: bool = False
    ) -> dict:
        """
        Create a new team.
        
        Args:
            player_id: The player ID
            name: Team name
            is_default: Whether this is the default team
            
        Returns:
            Created team data
        """
        # Check team limit
        existing_teams = [
            t for t in self._teams.values()
            if t["player_id"] == player_id
        ]
        if len(existing_teams) >= self.MAX_TEAMS_PER_PLAYER:
            raise ValidationException(
                f"Maximum number of teams ({self.MAX_TEAMS_PER_PLAYER}) reached"
            )
        
        # If setting as default, unset other defaults
        if is_default:
            for team in existing_teams:
                team["is_default"] = False
        
        team_id = str(uuid4())
        slot_number = len(existing_teams) + 1
        
        team = {
            "id": team_id,
            "player_id": player_id,
            "name": name,
            "slot_number": slot_number,
            "members": [],
            "formation_id": None,
            "is_default": is_default,
            "total_power": 0
        }
        
        self._teams[team_id] = team
        return team
    
    async def update_team(
        self,
        team_id: str,
        player_id: str,
        name: Optional[str] = None,
        members: Optional[List[Dict[str, Any]]] = None
    ) -> dict:
        """
        Update a team.
        
        Args:
            team_id: The team ID
            player_id: The player ID
            name: New team name
            members: New team members list
            
        Returns:
            Updated team data
        """
        team = await self.get_team(team_id, player_id)
        
        if name is not None:
            team["name"] = name
        
        if members is not None:
            if len(members) > self.MAX_MEMBERS_PER_TEAM:
                raise TeamFullException(team_id, self.MAX_MEMBERS_PER_TEAM)
            
            # Validate hero positions
            positions = set()
            for member in members:
                pos = (member.get("position", {}).get("x", 0), 
                       member.get("position", {}).get("y", 0))
                if pos in positions:
                    raise ValidationException("Duplicate position in team")
                positions.add(pos)
            
            team["members"] = members
            team["total_power"] = self._calculate_team_power(members)
        
        return team
    
    async def delete_team(self, team_id: str, player_id: str) -> bool:
        """
        Delete a team.
        
        Args:
            team_id: The team ID
            player_id: The player ID
            
        Returns:
            True if deleted
        """
        team = await self.get_team(team_id, player_id)
        
        if team["is_default"]:
            raise ValidationException("Cannot delete default team")
        
        del self._teams[team_id]
        return True
    
    async def add_member(
        self,
        team_id: str,
        player_id: str,
        hero_id: str,
        position: Dict[str, int]
    ) -> dict:
        """
        Add a hero to a team.
        
        Args:
            team_id: The team ID
            player_id: The player ID
            hero_id: The hero ID to add
            position: Grid position {"x": int, "y": int}
            
        Returns:
            Updated team data
        """
        team = await self.get_team(team_id, player_id)
        
        if len(team["members"]) >= self.MAX_MEMBERS_PER_TEAM:
            raise TeamFullException(team_id, self.MAX_MEMBERS_PER_TEAM)
        
        # Check if hero already in team
        if any(m["hero_id"] == hero_id for m in team["members"]):
            raise ValidationException("Hero is already in team")
        
        # Check if position is occupied
        pos_tuple = (position["x"], position["y"])
        if any(
            (m["position"]["x"], m["position"]["y"]) == pos_tuple
            for m in team["members"]
        ):
            raise ValidationException("Position is already occupied")
        
        # Get hero data
        hero_data = None
        if self.hero_service:
            hero_data = await self.hero_service.get_hero(hero_id, player_id)
        else:
            hero_data = {
                "id": hero_id,
                "name": "Test Hero",
                "power": 1000
            }
        
        member = {
            "hero_id": hero_id,
            "hero_name": hero_data.get("name", "Unknown"),
            "position": position,
            "power": hero_data.get("power", 0)
        }
        
        team["members"].append(member)
        team["total_power"] = self._calculate_team_power(team["members"])
        
        return team
    
    async def remove_member(
        self,
        team_id: str,
        player_id: str,
        hero_id: str
    ) -> dict:
        """
        Remove a hero from a team.
        
        Args:
            team_id: The team ID
            player_id: The player ID
            hero_id: The hero ID to remove
            
        Returns:
            Updated team data
        """
        team = await self.get_team(team_id, player_id)
        
        team["members"] = [
            m for m in team["members"]
            if m["hero_id"] != hero_id
        ]
        team["total_power"] = self._calculate_team_power(team["members"])
        
        return team
    
    async def update_formation(
        self,
        team_id: str,
        player_id: str,
        formation_id: Optional[str] = None
    ) -> dict:
        """
        Update team's formation.
        
        Args:
            team_id: The team ID
            player_id: The player ID
            formation_id: Formation ID or None to clear
            
        Returns:
            Updated team data
        """
        team = await self.get_team(team_id, player_id)
        team["formation_id"] = formation_id
        
        return team
    
    async def get_formations(self) -> List[dict]:
        """
        Get all available formations.
        
        Returns:
            List of formation data
        """
        return [
            {
                "id": "ngu_hanh_tran",
                "name": "Ngũ Hành Trận",
                "description": "Requires 5 heroes with all different elements",
                "required_members": 5,
                "bonuses": [
                    {"stat": "all", "value": 5, "bonus_type": "percent"},
                    {"stat": "element_power", "value": 20, "bonus_type": "percent"}
                ]
            },
            {
                "id": "long_dang_ho_khieu",
                "name": "Long Đằng Hổ Khiếu",
                "description": "Offensive formation for 3 heroes",
                "required_members": 3,
                "bonuses": [
                    {"stat": "atk", "value": 15, "bonus_type": "percent"},
                    {"stat": "spd", "value": 10, "bonus_type": "percent"}
                ]
            }
        ]
    
    def _calculate_team_power(self, members: List[Dict[str, Any]]) -> int:
        """Calculate total team power."""
        return sum(m.get("power", 0) for m in members)
