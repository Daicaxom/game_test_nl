"""
Player SQLAlchemy Model
"""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Integer, BigInteger, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.config.database import Base


class Player(Base):
    """Player database model"""
    
    __tablename__ = "players"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Authentication
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Profile
    display_name = Column(String(100))
    
    # Progression
    level = Column(Integer, default=1)
    exp = Column(BigInteger, default=0)
    
    # Resources
    gold = Column(BigInteger, default=0)
    gems = Column(Integer, default=0)
    stamina = Column(Integer, default=100)
    max_stamina = Column(Integer, default=100)
    stamina_updated_at = Column(DateTime, default=datetime.utcnow)
    
    # VIP
    vip_level = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Relationships
    heroes = relationship("Hero", back_populates="player", cascade="all, delete-orphan")
    equipment = relationship("Equipment", back_populates="player", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Player {self.username}>"
