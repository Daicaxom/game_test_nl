"""
Story and Stage SQLAlchemy Models
"""
from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, Text, BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.config.database import Base


class Chapter(Base):
    """Story chapter model"""
    
    __tablename__ = "chapters"
    
    # Primary key
    id = Column(String(50), primary_key=True)
    
    # Basic info
    chapter_number = Column(Integer, unique=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Chapter type
    is_mythical = Column(Boolean, default=False)  # Chapter 7 flag
    
    # Requirements
    unlock_requirements = Column(JSONB)  # {"level": 80, "heroes_5star": 5}
    
    # Relationships
    stages = relationship("Stage", back_populates="chapter", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Chapter {self.chapter_number}: {self.title}>"


class Stage(Base):
    """Battle stage model"""
    
    __tablename__ = "stages"
    
    # Primary key
    id = Column(String(50), primary_key=True)
    
    # Foreign keys
    chapter_id = Column(String(50), ForeignKey("chapters.id"), nullable=False, index=True)
    
    # Basic info
    stage_number = Column(Integer, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Difficulty
    difficulty = Column(Integer, nullable=False)  # 1-10
    recommended_power = Column(Integer)
    stamina_cost = Column(Integer, default=10)
    
    # Battle config
    waves = Column(Integer, default=1)
    is_boss_stage = Column(Boolean, default=False)
    
    # Rewards
    first_clear_rewards = Column(JSONB)  # {"gold": 1000, "items": [...]}
    repeat_rewards = Column(JSONB)
    star_conditions = Column(JSONB)  # [{"type": "no_death", "stars": 1}, ...]
    
    # Relationships
    chapter = relationship("Chapter", back_populates="stages")
    
    def __repr__(self) -> str:
        return f"<Stage {self.stage_number}: {self.name}>"


class Boss(Base):
    """Boss enemy model"""
    
    __tablename__ = "bosses"
    
    # Primary key
    id = Column(String(50), primary_key=True)
    
    # Foreign keys
    stage_id = Column(String(50), ForeignKey("stages.id"), index=True)
    
    # Basic info
    name = Column(String(100), nullable=False)
    title = Column(String(200))
    element = Column(String(10), nullable=False)
    
    # Mythical tier (for Chapter 7)
    mythical_tier = Column(String(20))  # TU_LINH, THIEN_VUONG, THUONG_CO, HON_DON
    
    # Stats
    hp = Column(BigInteger, nullable=False)
    atk = Column(Integer, nullable=False)
    defense = Column(Integer, nullable=False)  # 'def' is reserved
    spd = Column(Integer, nullable=False)
    crit = Column(Integer, nullable=False)
    dex = Column(Integer, nullable=False)
    
    # Skills and mechanics
    skills = Column(JSONB, nullable=False)  # {"skills": ["skill_id_1", ...]}
    special_mechanics = Column(JSONB)  # {"enrage_timer": 15, ...}
    
    # Metadata
    description = Column(Text)
    lore = Column(Text)
    
    def __repr__(self) -> str:
        return f"<Boss {self.name}>"
