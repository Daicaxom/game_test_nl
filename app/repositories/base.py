"""
Base Repository - Abstract base class for repositories
"""
from typing import Generic, TypeVar, Type, List, Optional, Any, Dict
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from app.config.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Base repository implementing common CRUD operations.
    
    Generic type parameter:
        ModelType: The SQLAlchemy model type
    """
    
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        """
        Initialize the repository.
        
        Args:
            model: The SQLAlchemy model class
            db: The async database session
        """
        self.model = model
        self.db = db
    
    async def create(self, obj_in: Dict[str, Any]) -> ModelType:
        """
        Create a new record.
        
        Args:
            obj_in: Dictionary of attributes for the new record
            
        Returns:
            The created model instance
        """
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj
    
    async def get(self, id: Any) -> Optional[ModelType]:
        """
        Get a record by ID.
        
        Args:
            id: The primary key value
            
        Returns:
            The model instance or None if not found
        """
        query = select(self.model).where(self.model.id == id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_field(self, field: str, value: Any) -> Optional[ModelType]:
        """
        Get a record by a specific field.
        
        Args:
            field: The field name to filter by
            value: The value to match
            
        Returns:
            The model instance or None if not found
        """
        column = getattr(self.model, field)
        query = select(self.model).where(column == value)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_multi(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ModelType]:
        """
        Get multiple records with pagination and optional filters.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            filters: Optional dictionary of filters
            
        Returns:
            List of model instances
        """
        query = select(self.model)
        
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field) and value is not None:
                    column = getattr(self.model, field)
                    query = query.where(column == value)
        
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Count records with optional filters.
        
        Args:
            filters: Optional dictionary of filters
            
        Returns:
            Number of matching records
        """
        from sqlalchemy import func
        query = select(func.count()).select_from(self.model)
        
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field) and value is not None:
                    column = getattr(self.model, field)
                    query = query.where(column == value)
        
        result = await self.db.execute(query)
        return result.scalar_one()
    
    async def update(
        self,
        id: Any,
        obj_in: Dict[str, Any]
    ) -> Optional[ModelType]:
        """
        Update a record.
        
        Args:
            id: The primary key value
            obj_in: Dictionary of attributes to update
            
        Returns:
            The updated model instance or None if not found
        """
        db_obj = await self.get(id)
        if not db_obj:
            return None
        
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj
    
    async def delete(self, id: Any) -> bool:
        """
        Delete a record.
        
        Args:
            id: The primary key value
            
        Returns:
            True if deleted, False if not found
        """
        db_obj = await self.get(id)
        if not db_obj:
            return False
        
        await self.db.delete(db_obj)
        await self.db.flush()
        return True
    
    async def exists(self, id: Any) -> bool:
        """
        Check if a record exists.
        
        Args:
            id: The primary key value
            
        Returns:
            True if exists, False otherwise
        """
        from sqlalchemy import exists as sql_exists
        query = select(sql_exists().where(self.model.id == id))
        result = await self.db.execute(query)
        return result.scalar()
