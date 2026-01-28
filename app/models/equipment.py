"""
Equipment SQLAlchemy Models
"""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.config.database import Base


class EquipmentSet(Base):
    """Equipment set (static data) model"""
    
    __tablename__ = "equipment_sets"
    
    # Primary key
    id = Column(String(50), primary_key=True)
    
    # Basic info
    name = Column(String(100), nullable=False)
    description = Column(Text)
    
    # Set bonuses (JSONB for flexibility)
    two_piece_bonus = Column(JSONB)  # {"ATK": 15, "CRIT": 10}
    three_piece_bonus = Column(JSONB)
    four_piece_bonus = Column(JSONB)
    
    def __repr__(self) -> str:
        return f"<EquipmentSet {self.name}>"


class EquipmentTemplate(Base):
    """Equipment template (static data) model"""
    
    __tablename__ = "equipment_templates"
    
    # Primary key
    id = Column(String(50), primary_key=True)
    
    # Basic info
    name = Column(String(100), nullable=False)
    equipment_type = Column(String(20), nullable=False)  # WEAPON, ARMOR, ACCESSORY, RELIC
    base_rarity = Column(Integer, nullable=False)
    
    # Set
    set_id = Column(String(50), ForeignKey("equipment_sets.id"))
    
    # Base stats
    base_hp = Column(Integer, default=0)
    base_atk = Column(Integer, default=0)
    base_def = Column(Integer, default=0)
    base_spd = Column(Integer, default=0)
    base_crit = Column(Integer, default=0)
    base_dex = Column(Integer, default=0)
    
    # Special effect
    unique_effect = Column(JSONB)  # {"effect_type": "...", "value": ...}
    
    # Requirements
    required_level = Column(Integer, default=1)
    required_element = Column(String(10))  # Optional element requirement
    
    # Metadata
    description = Column(Text)
    icon_url = Column(String(500))
    
    def __repr__(self) -> str:
        return f"<EquipmentTemplate {self.name}>"


class Equipment(Base):
    """Player's equipment instance model"""
    
    __tablename__ = "equipment"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Foreign keys
    player_id = Column(UUID(as_uuid=True), ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    template_id = Column(String(50), ForeignKey("equipment_templates.id"), nullable=False, index=True)
    
    # Enhancement
    level = Column(Integer, default=1)  # 1-30 depending on rarity
    
    # Bonus stats from enhancement
    bonus_hp = Column(Integer, default=0)
    bonus_atk = Column(Integer, default=0)
    bonus_def = Column(Integer, default=0)
    bonus_spd = Column(Integer, default=0)
    bonus_crit = Column(Integer, default=0)
    bonus_dex = Column(Integer, default=0)
    
    # Random substats (JSONB for flexibility)
    substats = Column(JSONB)  # [{"stat": "ATK", "value": 10}, ...]
    
    # Metadata
    is_locked = Column(Boolean, default=False)
    
    # Timestamps
    acquired_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    player = relationship("Player", back_populates="equipment")
    
    def __repr__(self) -> str:
        return f"<Equipment {self.template_id} (Player: {self.player_id})>"
