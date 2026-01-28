"""
Hero Repository - Data access for Hero model
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.repositories.base import BaseRepository
from app.models.hero import Hero, HeroTemplate, HeroSkill


class HeroRepository(BaseRepository[Hero]):
    """Repository for Hero model operations"""
    
    def __init__(self, db: AsyncSession):
        """
        Initialize the hero repository.
        
        Args:
            db: The async database session
        """
        super().__init__(Hero, db)
    
    async def get_by_player(
        self,
        player_id: UUID,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Hero]:
        """
        Get all heroes belonging to a player.
        
        Args:
            player_id: The player ID
            skip: Number of records to skip
            limit: Maximum number of records
            filters: Optional filters (element, rarity, etc.)
            
        Returns:
            List of heroes
        """
        query = (
            select(Hero)
            .where(Hero.player_id == player_id)
            .options(selectinload(Hero.template))
            .options(selectinload(Hero.skills))
        )
        
        if filters:
            if filters.get("element"):
                query = query.join(HeroTemplate).where(
                    HeroTemplate.element == filters["element"]
                )
            if filters.get("rarity"):
                query = query.where(Hero.stars >= filters["rarity"])
        
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def count_by_player(
        self,
        player_id: UUID,
        filters: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Count heroes belonging to a player.
        
        Args:
            player_id: The player ID
            filters: Optional filters
            
        Returns:
            Number of matching heroes
        """
        from sqlalchemy import func
        query = select(func.count()).select_from(Hero).where(Hero.player_id == player_id)
        
        if filters:
            if filters.get("element"):
                query = query.join(HeroTemplate).where(
                    HeroTemplate.element == filters["element"]
                )
        
        result = await self.db.execute(query)
        return result.scalar_one()
    
    async def get_with_template(self, hero_id: UUID) -> Optional[Hero]:
        """
        Get a hero with its template loaded.
        
        Args:
            hero_id: The hero ID
            
        Returns:
            Hero with template or None
        """
        query = (
            select(Hero)
            .where(Hero.id == hero_id)
            .options(selectinload(Hero.template))
            .options(selectinload(Hero.skills))
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_hero_for_player(
        self,
        hero_id: UUID,
        player_id: UUID
    ) -> Optional[Hero]:
        """
        Get a hero that belongs to a specific player.
        
        Args:
            hero_id: The hero ID
            player_id: The player ID
            
        Returns:
            Hero if found and belongs to player, None otherwise
        """
        query = (
            select(Hero)
            .where(and_(Hero.id == hero_id, Hero.player_id == player_id))
            .options(selectinload(Hero.template))
            .options(selectinload(Hero.skills))
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def update_stats(
        self,
        hero_id: UUID,
        hp: int,
        atk: int,
        def_: int,
        spd: int,
        crit: int,
        dex: int
    ) -> Optional[Hero]:
        """
        Update hero's current stats.
        
        Args:
            hero_id: The hero ID
            hp, atk, def_, spd, crit, dex: New stat values
            
        Returns:
            Updated hero or None if not found
        """
        return await self.update(hero_id, {
            "current_hp": hp,
            "current_atk": atk,
            "current_def": def_,
            "current_spd": spd,
            "current_crit": crit,
            "current_dex": dex
        })
    
    async def update_level(
        self,
        hero_id: UUID,
        level: int,
        exp: int
    ) -> Optional[Hero]:
        """
        Update hero's level and experience.
        
        Args:
            hero_id: The hero ID
            level: New level
            exp: New experience points
            
        Returns:
            Updated hero or None if not found
        """
        return await self.update(hero_id, {
            "level": level,
            "exp": exp
        })
    
    async def update_equipment(
        self,
        hero_id: UUID,
        slot: str,
        equipment_id: Optional[UUID]
    ) -> Optional[Hero]:
        """
        Update hero's equipment in a slot.
        
        Args:
            hero_id: The hero ID
            slot: Equipment slot (weapon, armor, accessory, relic)
            equipment_id: Equipment ID or None to unequip
            
        Returns:
            Updated hero or None if not found
        """
        slot_mapping = {
            "weapon": "weapon_id",
            "armor": "armor_id",
            "accessory": "accessory_id",
            "relic": "relic_id"
        }
        
        if slot not in slot_mapping:
            return None
        
        return await self.update(hero_id, {slot_mapping[slot]: equipment_id})
    
    async def get_team_heroes(
        self,
        hero_ids: List[UUID]
    ) -> List[Hero]:
        """
        Get multiple heroes by IDs (for team loading).
        
        Args:
            hero_ids: List of hero IDs
            
        Returns:
            List of heroes
        """
        query = (
            select(Hero)
            .where(Hero.id.in_(hero_ids))
            .options(selectinload(Hero.template))
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())


class HeroTemplateRepository(BaseRepository[HeroTemplate]):
    """Repository for HeroTemplate model operations"""
    
    def __init__(self, db: AsyncSession):
        """
        Initialize the hero template repository.
        
        Args:
            db: The async database session
        """
        super().__init__(HeroTemplate, db)
    
    async def get_by_element(self, element: str) -> List[HeroTemplate]:
        """
        Get all hero templates by element.
        
        Args:
            element: The element to filter by
            
        Returns:
            List of hero templates
        """
        query = select(HeroTemplate).where(HeroTemplate.element == element)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_by_rarity(self, rarity: int) -> List[HeroTemplate]:
        """
        Get all hero templates by rarity.
        
        Args:
            rarity: The rarity to filter by
            
        Returns:
            List of hero templates
        """
        query = select(HeroTemplate).where(HeroTemplate.base_rarity == rarity)
        result = await self.db.execute(query)
        return list(result.scalars().all())
