"""
Equipment Repository - Data access for Equipment model
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.repositories.base import BaseRepository
from app.models.equipment import Equipment, EquipmentTemplate, EquipmentSet


class EquipmentRepository(BaseRepository[Equipment]):
    """Repository for Equipment model operations"""
    
    def __init__(self, db: AsyncSession):
        """
        Initialize the equipment repository.
        
        Args:
            db: The async database session
        """
        super().__init__(Equipment, db)
    
    async def get_by_player(
        self,
        player_id: UUID,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Equipment]:
        """
        Get all equipment belonging to a player.
        
        Args:
            player_id: The player ID
            skip: Number of records to skip
            limit: Maximum number of records
            filters: Optional filters
            
        Returns:
            List of equipment
        """
        query = select(Equipment).where(Equipment.player_id == player_id)
        
        if filters:
            if filters.get("equipment_type"):
                query = query.join(EquipmentTemplate).where(
                    EquipmentTemplate.equipment_type == filters["equipment_type"]
                )
            # Note: is_equipped filter requires checking Hero equipment slots
            # For now, we skip this filter as it requires a separate query approach
        
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def count_by_player(
        self,
        player_id: UUID,
        filters: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Count equipment belonging to a player.
        
        Args:
            player_id: The player ID
            filters: Optional filters
            
        Returns:
            Number of matching equipment
        """
        from sqlalchemy import func
        query = select(func.count()).select_from(Equipment).where(
            Equipment.player_id == player_id
        )
        result = await self.db.execute(query)
        return result.scalar_one()
    
    async def get_equipment_for_player(
        self,
        equipment_id: UUID,
        player_id: UUID
    ) -> Optional[Equipment]:
        """
        Get equipment that belongs to a specific player.
        
        Args:
            equipment_id: The equipment ID
            player_id: The player ID
            
        Returns:
            Equipment if found and belongs to player, None otherwise
        """
        query = select(Equipment).where(
            and_(
                Equipment.id == equipment_id,
                Equipment.player_id == player_id
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def update_level(
        self,
        equipment_id: UUID,
        new_level: int,
        bonus_stats: Dict[str, int]
    ) -> Optional[Equipment]:
        """
        Update equipment level and bonus stats after enhancement.
        
        Args:
            equipment_id: The equipment ID
            new_level: New enhancement level
            bonus_stats: Dictionary of bonus stat values
            
        Returns:
            Updated equipment or None if not found
        """
        update_data = {"level": new_level}
        
        if "hp" in bonus_stats:
            update_data["bonus_hp"] = bonus_stats["hp"]
        if "atk" in bonus_stats:
            update_data["bonus_atk"] = bonus_stats["atk"]
        if "def_" in bonus_stats:
            update_data["bonus_def"] = bonus_stats["def_"]
        if "spd" in bonus_stats:
            update_data["bonus_spd"] = bonus_stats["spd"]
        if "crit" in bonus_stats:
            update_data["bonus_crit"] = bonus_stats["crit"]
        if "dex" in bonus_stats:
            update_data["bonus_dex"] = bonus_stats["dex"]
        
        return await self.update(equipment_id, update_data)
    
    async def get_unequipped(
        self,
        player_id: UUID,
        equipment_type: Optional[str] = None
    ) -> List[Equipment]:
        """
        Get unequipped equipment for a player.
        
        Args:
            player_id: The player ID
            equipment_type: Optional equipment type filter
            
        Returns:
            List of unequipped equipment
        """
        # Get equipment IDs that are equipped to heroes
        from app.models.hero import Hero
        
        equipped_ids_query = select(Hero.weapon_id).where(Hero.player_id == player_id)
        equipped_ids_query = equipped_ids_query.union_all(
            select(Hero.armor_id).where(Hero.player_id == player_id)
        ).union_all(
            select(Hero.accessory_id).where(Hero.player_id == player_id)
        ).union_all(
            select(Hero.relic_id).where(Hero.player_id == player_id)
        )
        
        query = select(Equipment).where(
            and_(
                Equipment.player_id == player_id,
                ~Equipment.id.in_(equipped_ids_query)
            )
        )
        
        if equipment_type:
            query = query.join(EquipmentTemplate).where(
                EquipmentTemplate.equipment_type == equipment_type
            )
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def delete_multiple(
        self,
        equipment_ids: List[UUID],
        player_id: UUID
    ) -> int:
        """
        Delete multiple equipment items.
        
        Args:
            equipment_ids: List of equipment IDs to delete
            player_id: The player ID (for ownership verification)
            
        Returns:
            Number of deleted items
        """
        from sqlalchemy import delete as sql_delete
        
        query = sql_delete(Equipment).where(
            and_(
                Equipment.id.in_(equipment_ids),
                Equipment.player_id == player_id
            )
        )
        result = await self.db.execute(query)
        await self.db.flush()
        return result.rowcount


class EquipmentTemplateRepository(BaseRepository[EquipmentTemplate]):
    """Repository for EquipmentTemplate model operations"""
    
    def __init__(self, db: AsyncSession):
        """
        Initialize the equipment template repository.
        
        Args:
            db: The async database session
        """
        super().__init__(EquipmentTemplate, db)
    
    async def get_by_type(self, equipment_type: str) -> List[EquipmentTemplate]:
        """
        Get all equipment templates by type.
        
        Args:
            equipment_type: The equipment type to filter by
            
        Returns:
            List of equipment templates
        """
        query = select(EquipmentTemplate).where(
            EquipmentTemplate.equipment_type == equipment_type
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_by_set(self, set_id: str) -> List[EquipmentTemplate]:
        """
        Get all equipment templates in a set.
        
        Args:
            set_id: The equipment set ID
            
        Returns:
            List of equipment templates
        """
        query = select(EquipmentTemplate).where(
            EquipmentTemplate.set_id == set_id
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())


class EquipmentSetRepository(BaseRepository[EquipmentSet]):
    """Repository for EquipmentSet model operations"""
    
    def __init__(self, db: AsyncSession):
        """
        Initialize the equipment set repository.
        
        Args:
            db: The async database session
        """
        super().__init__(EquipmentSet, db)
    
    async def get_all(self) -> List[EquipmentSet]:
        """
        Get all equipment sets.
        
        Returns:
            List of all equipment sets
        """
        query = select(EquipmentSet)
        result = await self.db.execute(query)
        return list(result.scalars().all())
