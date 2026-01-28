"""
Skill SQLAlchemy Models
"""
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB

from app.config.database import Base


class SkillTemplate(Base):
    """Skill template (static data) model"""
    
    __tablename__ = "skill_templates"
    
    # Primary key
    id = Column(String(50), primary_key=True)
    
    # Basic info
    name = Column(String(100), nullable=False)
    description = Column(Text)
    
    # Skill type
    skill_type = Column(String(20), nullable=False)  # ACTIVE, PASSIVE, ULTIMATE
    element = Column(String(10))  # Optional element
    
    # Resource cost
    mana_cost = Column(Integer, nullable=False, default=0)
    cooldown = Column(Integer, default=0)
    
    # Targeting
    target_type = Column(String(20), nullable=False)  # SELF, SINGLE_ALLY, SINGLE_ENEMY, etc.
    
    # Effects (JSONB for flexibility)
    damage_multiplier = Column(Integer)  # Stored as percentage (150 = 1.5x)
    heal_multiplier = Column(Integer)  # Stored as percentage
    buff_stats = Column(JSONB)  # {"ATK": 20, "DEF": 10}
    debuff_effects = Column(JSONB)  # {"DEF": -15}
    special_effects = Column(JSONB)  # Custom effects
    
    # Visual
    animation_id = Column(String(50))
    icon_url = Column(String(500))
    
    def __repr__(self) -> str:
        return f"<SkillTemplate {self.name}>"
