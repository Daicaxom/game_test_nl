"""
Hero SQLAlchemy Models
"""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, DECIMAL, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.config.database import Base


class HeroTemplate(Base):
    """Hero template (static data) model"""
    
    __tablename__ = "hero_templates"
    
    # Primary key
    id = Column(String(50), primary_key=True)
    
    # Basic info
    name = Column(String(100), nullable=False)
    title = Column(String(200))
    element = Column(String(10), nullable=False)  # KIM, MOC, THUY, HOA, THO
    base_rarity = Column(Integer, nullable=False)  # 1-6
    hero_class = Column(String(50), nullable=False)  # TANK, DPS, MAGE, SUPPORT, etc.
    
    # Base stats at level 1
    base_hp = Column(Integer, nullable=False)
    base_atk = Column(Integer, nullable=False)
    base_def = Column(Integer, nullable=False)
    base_spd = Column(Integer, nullable=False)
    base_crit = Column(Integer, nullable=False)
    base_dex = Column(Integer, nullable=False)
    
    # Growth rates per level
    growth_hp = Column(DECIMAL(5, 2), nullable=False)
    growth_atk = Column(DECIMAL(5, 2), nullable=False)
    growth_def = Column(DECIMAL(5, 2), nullable=False)
    growth_spd = Column(DECIMAL(5, 2), nullable=False)
    growth_crit = Column(DECIMAL(5, 2), nullable=False)
    growth_dex = Column(DECIMAL(5, 2), nullable=False)
    
    # Metadata
    description = Column(Text)
    lore = Column(Text)
    icon_url = Column(String(500))
    model_url = Column(String(500))
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    heroes = relationship("Hero", back_populates="template")
    
    def __repr__(self) -> str:
        return f"<HeroTemplate {self.name}>"


class Hero(Base):
    """Player's hero instance model"""
    
    __tablename__ = "heroes"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Foreign keys
    player_id = Column(UUID(as_uuid=True), ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    template_id = Column(String(50), ForeignKey("hero_templates.id"), nullable=False, index=True)
    
    # Progression
    level = Column(Integer, default=1)
    exp = Column(Integer, default=0)
    stars = Column(Integer, default=1)  # 1-6
    ascension_level = Column(Integer, default=0)  # 0-6
    awakening_level = Column(Integer, default=0)  # 0-6
    
    # Current calculated stats
    current_hp = Column(Integer, nullable=False)
    current_atk = Column(Integer, nullable=False)
    current_def = Column(Integer, nullable=False)
    current_spd = Column(Integer, nullable=False)
    current_crit = Column(Integer, nullable=False)
    current_dex = Column(Integer, nullable=False)
    
    # Equipment slots
    weapon_id = Column(UUID(as_uuid=True), ForeignKey("equipment.id"))
    armor_id = Column(UUID(as_uuid=True), ForeignKey("equipment.id"))
    accessory_id = Column(UUID(as_uuid=True), ForeignKey("equipment.id"))
    relic_id = Column(UUID(as_uuid=True), ForeignKey("equipment.id"))
    
    # Mount
    mount_id = Column(UUID(as_uuid=True))  # ForeignKey to mounts table
    
    # Metadata
    is_locked = Column(Boolean, default=False)
    is_favorite = Column(Boolean, default=False)
    
    # Timestamps
    acquired_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    player = relationship("Player", back_populates="heroes")
    template = relationship("HeroTemplate", back_populates="heroes")
    skills = relationship("HeroSkill", back_populates="hero", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Hero {self.template_id} (Player: {self.player_id})>"


class HeroSkill(Base):
    """Hero's learned skills model"""
    
    __tablename__ = "hero_skills"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Foreign keys
    hero_id = Column(UUID(as_uuid=True), ForeignKey("heroes.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(String(50), ForeignKey("skill_templates.id"), nullable=False)
    
    # Progression
    level = Column(Integer, default=1)  # 1-10
    is_unlocked = Column(Boolean, default=True)
    enhanced_branch = Column(String(20))  # power, efficiency, utility
    enhanced_level = Column(Integer, default=0)
    
    # Relationships
    hero = relationship("Hero", back_populates="skills")
    
    def __repr__(self) -> str:
        return f"<HeroSkill {self.skill_id} (Hero: {self.hero_id})>"
