"""
Player Service - Business logic for player operations
"""
from typing import Optional, Dict, Any
from uuid import UUID

from app.core.exceptions import (
    PlayerNotFoundException,
    InsufficientGoldException,
    InsufficientGemsException,
    InsufficientStaminaException
)


class PlayerService:
    """
    Service for player-related operations.
    
    Handles:
    - Profile management
    - Resource management
    - Statistics
    - Inventory
    """
    
    def __init__(self, player_repository=None, hero_repository=None, equipment_repository=None):
        """
        Initialize the player service.
        
        Args:
            player_repository: Optional PlayerRepository
            hero_repository: Optional HeroRepository
            equipment_repository: Optional EquipmentRepository
        """
        self.player_repository = player_repository
        self.hero_repository = hero_repository
        self.equipment_repository = equipment_repository
    
    async def get_player(self, player_id: str) -> dict:
        """
        Get player information.
        
        Args:
            player_id: The player ID
            
        Returns:
            Dictionary with player data
            
        Raises:
            PlayerNotFoundException: If player not found
        """
        if self.player_repository:
            player = await self.player_repository.get(player_id)
            if not player:
                raise PlayerNotFoundException(player_id)
            
            return {
                "id": str(player.id),
                "username": player.username,
                "email": player.email,
                "display_name": player.display_name,
                "level": player.level,
                "exp": player.exp,
                "gold": player.gold,
                "gems": player.gems,
                "stamina": player.stamina,
                "max_stamina": player.max_stamina,
                "vip_level": player.vip_level,
                "created_at": player.created_at,
                "last_login": player.last_login
            }
        
        # Return mock data
        return {
            "id": player_id,
            "username": "test_user",
            "email": "test@example.com",
            "display_name": "Test User",
            "level": 1,
            "exp": 0,
            "gold": 1000,
            "gems": 100,
            "stamina": 100,
            "max_stamina": 100,
            "vip_level": 0,
            "created_at": None,
            "last_login": None
        }
    
    async def update_profile(
        self,
        player_id: str,
        display_name: Optional[str] = None
    ) -> dict:
        """
        Update player profile.
        
        Args:
            player_id: The player ID
            display_name: New display name
            
        Returns:
            Updated player data
        """
        update_data = {}
        if display_name is not None:
            update_data["display_name"] = display_name
        
        if self.player_repository and update_data:
            player = await self.player_repository.update(player_id, update_data)
            if not player:
                raise PlayerNotFoundException(player_id)
            return await self.get_player(player_id)
        
        return await self.get_player(player_id)
    
    async def get_resources(self, player_id: str) -> dict:
        """
        Get player's resources.
        
        Args:
            player_id: The player ID
            
        Returns:
            Dictionary with resource amounts
        """
        player_data = await self.get_player(player_id)
        return {
            "gold": player_data["gold"],
            "gems": player_data["gems"],
            "stamina": player_data["stamina"],
            "max_stamina": player_data["max_stamina"]
        }
    
    async def spend_resources(
        self,
        player_id: str,
        gold: int = 0,
        gems: int = 0,
        stamina: int = 0
    ) -> dict:
        """
        Spend player resources.
        
        Args:
            player_id: The player ID
            gold: Gold to spend
            gems: Gems to spend
            stamina: Stamina to spend
            
        Returns:
            Updated resource amounts
            
        Raises:
            InsufficientGoldException: If not enough gold
            InsufficientGemsException: If not enough gems
            InsufficientStaminaException: If not enough stamina
        """
        player_data = await self.get_player(player_id)
        
        # Validate resources
        if gold > 0 and player_data["gold"] < gold:
            raise InsufficientGoldException(
                required=gold,
                available=player_data["gold"]
            )
        
        if gems > 0 and player_data["gems"] < gems:
            raise InsufficientGemsException(
                required=gems,
                available=player_data["gems"]
            )
        
        if stamina > 0 and player_data["stamina"] < stamina:
            raise InsufficientStaminaException(
                required=stamina,
                available=player_data["stamina"]
            )
        
        if self.player_repository:
            await self.player_repository.update_resources(
                player_id,
                gold_delta=-gold,
                gems_delta=-gems,
                stamina_delta=-stamina
            )
        
        return await self.get_resources(player_id)
    
    async def add_resources(
        self,
        player_id: str,
        gold: int = 0,
        gems: int = 0,
        stamina: int = 0
    ) -> dict:
        """
        Add resources to player.
        
        Args:
            player_id: The player ID
            gold: Gold to add
            gems: Gems to add
            stamina: Stamina to add
            
        Returns:
            Updated resource amounts
        """
        if self.player_repository:
            await self.player_repository.update_resources(
                player_id,
                gold_delta=gold,
                gems_delta=gems,
                stamina_delta=stamina
            )
        
        return await self.get_resources(player_id)
    
    async def add_experience(
        self,
        player_id: str,
        exp_amount: int
    ) -> dict:
        """
        Add experience to player.
        
        Args:
            player_id: The player ID
            exp_amount: Experience to add
            
        Returns:
            Dictionary with level up info
        """
        player_data = await self.get_player(player_id)
        old_level = player_data["level"]
        
        if self.player_repository:
            await self.player_repository.add_experience(player_id, exp_amount)
        
        updated_data = await self.get_player(player_id)
        
        return {
            "old_level": old_level,
            "new_level": updated_data["level"],
            "leveled_up": updated_data["level"] > old_level,
            "current_exp": updated_data["exp"]
        }
    
    async def get_stats(self, player_id: str) -> dict:
        """
        Get player statistics.
        
        Args:
            player_id: The player ID
            
        Returns:
            Dictionary with player stats
        """
        player_data = await self.get_player(player_id)
        
        hero_count = 0
        total_power = 0
        
        if self.hero_repository:
            hero_count = await self.hero_repository.count_by_player(player_id)
            # Calculate total power would require loading all heroes
        
        return {
            "player_id": player_id,
            "level": player_data["level"],
            "total_heroes": hero_count,
            "total_power": total_power,
            "story_progress": "Chapter 1",
            "battles_won": 0,
            "battles_lost": 0
        }
    
    async def get_inventory(self, player_id: str) -> dict:
        """
        Get player inventory summary.
        
        Args:
            player_id: The player ID
            
        Returns:
            Dictionary with inventory counts
        """
        hero_count = 0
        equipment_count = 0
        
        if self.hero_repository:
            hero_count = await self.hero_repository.count_by_player(player_id)
        
        if self.equipment_repository:
            equipment_count = await self.equipment_repository.count_by_player(player_id)
        
        return {
            "player_id": player_id,
            "hero_count": hero_count,
            "equipment_count": equipment_count,
            "mount_count": 0,
            "material_count": 0
        }
