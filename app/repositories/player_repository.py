"""
Player Repository - Data access for Player model
"""
from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.repositories.base import BaseRepository
from app.models.player import Player


class PlayerRepository(BaseRepository[Player]):
    """Repository for Player model operations"""
    
    def __init__(self, db: AsyncSession):
        """
        Initialize the player repository.
        
        Args:
            db: The async database session
        """
        super().__init__(Player, db)
    
    async def get_by_username(self, username: str) -> Optional[Player]:
        """
        Get a player by username.
        
        Args:
            username: The username to search for
            
        Returns:
            Player instance or None if not found
        """
        return await self.get_by_field("username", username)
    
    async def get_by_email(self, email: str) -> Optional[Player]:
        """
        Get a player by email.
        
        Args:
            email: The email to search for
            
        Returns:
            Player instance or None if not found
        """
        return await self.get_by_field("email", email)
    
    async def username_exists(self, username: str) -> bool:
        """
        Check if a username already exists.
        
        Args:
            username: The username to check
            
        Returns:
            True if exists, False otherwise
        """
        player = await self.get_by_username(username)
        return player is not None
    
    async def email_exists(self, email: str) -> bool:
        """
        Check if an email already exists.
        
        Args:
            email: The email to check
            
        Returns:
            True if exists, False otherwise
        """
        player = await self.get_by_email(email)
        return player is not None
    
    async def get_with_heroes(self, player_id: UUID) -> Optional[Player]:
        """
        Get a player with their heroes loaded.
        
        Args:
            player_id: The player ID
            
        Returns:
            Player with heroes or None if not found
        """
        from sqlalchemy.orm import selectinload
        
        query = (
            select(Player)
            .where(Player.id == player_id)
            .options(selectinload(Player.heroes))
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def update_resources(
        self,
        player_id: UUID,
        gold_delta: int = 0,
        gems_delta: int = 0,
        stamina_delta: int = 0
    ) -> Optional[Player]:
        """
        Update player resources.
        
        Args:
            player_id: The player ID
            gold_delta: Amount to add/subtract from gold
            gems_delta: Amount to add/subtract from gems
            stamina_delta: Amount to add/subtract from stamina
            
        Returns:
            Updated player or None if not found
        """
        player = await self.get(player_id)
        if not player:
            return None
        
        player.gold = max(0, player.gold + gold_delta)
        player.gems = max(0, player.gems + gems_delta)
        player.stamina = min(
            player.max_stamina,
            max(0, player.stamina + stamina_delta)
        )
        
        await self.db.flush()
        await self.db.refresh(player)
        return player
    
    async def add_experience(
        self,
        player_id: UUID,
        exp_amount: int
    ) -> Optional[Player]:
        """
        Add experience to a player and handle level up.
        
        Args:
            player_id: The player ID
            exp_amount: Amount of experience to add
            
        Returns:
            Updated player or None if not found
        """
        player = await self.get(player_id)
        if not player:
            return None
        
        player.exp += exp_amount
        
        # Simple level up formula
        while player.exp >= player.level * 100:
            player.exp -= player.level * 100
            player.level += 1
        
        await self.db.flush()
        await self.db.refresh(player)
        return player
    
    async def update_last_login(self, player_id: UUID) -> Optional[Player]:
        """
        Update the last login timestamp.
        
        Args:
            player_id: The player ID
            
        Returns:
            Updated player or None if not found
        """
        from datetime import datetime
        
        return await self.update(player_id, {"last_login": datetime.utcnow()})
    
    async def get_leaderboard(
        self,
        limit: int = 100,
        order_by: str = "level"
    ) -> List[Player]:
        """
        Get players sorted by a field for leaderboard.
        
        Args:
            limit: Maximum number of players to return
            order_by: Field to order by (level, gold, etc.)
            
        Returns:
            List of players sorted by the specified field
        """
        from sqlalchemy import desc
        
        column = getattr(Player, order_by, Player.level)
        query = select(Player).order_by(desc(column)).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())
