"""
Hero Service - Business logic for hero operations
"""
from typing import Optional, Dict, Any, List
from uuid import uuid4

from app.core.exceptions import (
    HeroNotFoundException,
    HeroAlreadyMaxLevelException,
    EquipmentNotFoundException,
    ValidationException
)


class HeroService:
    """
    Service for hero-related operations.
    
    Handles:
    - Hero management
    - Level up
    - Ascension
    - Awakening
    - Equipment management
    - Skill upgrades
    """
    
    def __init__(
        self,
        hero_repository=None,
        equipment_repository=None,
        player_service=None
    ):
        """
        Initialize the hero service.
        
        Args:
            hero_repository: Optional HeroRepository
            equipment_repository: Optional EquipmentRepository
            player_service: Optional PlayerService for resource management
        """
        self.hero_repository = hero_repository
        self.equipment_repository = equipment_repository
        self.player_service = player_service
    
    async def get_heroes(
        self,
        player_id: str,
        page: int = 1,
        per_page: int = 20,
        element: Optional[str] = None,
        rarity: Optional[int] = None
    ) -> dict:
        """
        Get player's heroes with filtering and pagination.
        
        Args:
            player_id: The player ID
            page: Page number
            per_page: Items per page
            element: Optional element filter
            rarity: Optional rarity filter
            
        Returns:
            Dictionary with heroes list and pagination info
        """
        skip = (page - 1) * per_page
        filters = {}
        if element:
            filters["element"] = element
        if rarity:
            filters["rarity"] = rarity
        
        heroes = []
        total = 0
        
        if self.hero_repository:
            heroes = await self.hero_repository.get_by_player(
                player_id,
                skip=skip,
                limit=per_page,
                filters=filters
            )
            total = await self.hero_repository.count_by_player(player_id, filters)
        else:
            # Mock data
            heroes = [self._mock_hero()]
            total = 1
        
        return {
            "heroes": [self._hero_to_brief(h) for h in heroes] if self.hero_repository else heroes,
            "total": total,
            "page": page,
            "per_page": per_page
        }
    
    async def get_hero(
        self,
        hero_id: str,
        player_id: str
    ) -> dict:
        """
        Get specific hero details.
        
        Args:
            hero_id: The hero ID
            player_id: The player ID for ownership verification
            
        Returns:
            Dictionary with hero data
            
        Raises:
            HeroNotFoundException: If hero not found
        """
        if self.hero_repository:
            hero = await self.hero_repository.get_hero_for_player(hero_id, player_id)
            if not hero:
                raise HeroNotFoundException(hero_id)
            return self._hero_to_response(hero)
        
        # Mock data
        return self._mock_hero()
    
    async def level_up(
        self,
        hero_id: str,
        player_id: str,
        exp_items: List[Dict[str, Any]]
    ) -> dict:
        """
        Level up a hero using experience items.
        
        Args:
            hero_id: The hero ID
            player_id: The player ID
            exp_items: List of exp items to consume
            
        Returns:
            Dictionary with level up result
        """
        hero_data = await self.get_hero(hero_id, player_id)
        old_level = hero_data.get("level", 1)
        
        # Calculate total EXP from items
        total_exp = 0
        for item in exp_items:
            # Each exp book gives 100 EXP per quantity
            total_exp += item.get("quantity", 0) * 100
        
        # Simple level up calculation
        new_level = old_level
        remaining_exp = hero_data.get("exp", 0) + total_exp
        
        # Level up formula: 100 + level * 50 EXP per level
        while remaining_exp >= 100 + new_level * 50:
            remaining_exp -= 100 + new_level * 50
            new_level += 1
        
        # Update stats based on new level
        new_stats = self._calculate_stats(hero_data, new_level)
        
        if self.hero_repository:
            await self.hero_repository.update_level(hero_id, new_level, remaining_exp)
            await self.hero_repository.update_stats(
                hero_id,
                hp=new_stats["hp"],
                atk=new_stats["atk"],
                def_=new_stats["def_"],
                spd=new_stats["spd"],
                crit=new_stats["crit"],
                dex=new_stats["dex"]
            )
        
        return {
            "hero_id": hero_id,
            "old_level": old_level,
            "new_level": new_level,
            "leveled_up": new_level > old_level,
            "stats": new_stats
        }
    
    async def ascend(
        self,
        hero_id: str,
        player_id: str
    ) -> dict:
        """
        Ascend a hero to unlock higher level cap.
        
        Args:
            hero_id: The hero ID
            player_id: The player ID
            
        Returns:
            Dictionary with ascension result
        """
        hero_data = await self.get_hero(hero_id, player_id)
        old_ascension = hero_data.get("ascension_level", 0)
        
        if old_ascension >= 6:
            raise ValidationException("Hero is already at max ascension level")
        
        new_ascension = old_ascension + 1
        new_level_cap = 20 + new_ascension * 10
        
        # Unlock passive based on ascension level
        unlocked_passive = None
        if new_ascension == 1:
            unlocked_passive = "Nội tại cấp 1"
        elif new_ascension == 2:
            unlocked_passive = "Nội tại cấp 2"
        
        if self.hero_repository:
            await self.hero_repository.update(hero_id, {"ascension_level": new_ascension})
        
        return {
            "hero_id": hero_id,
            "old_ascension_level": old_ascension,
            "new_ascension_level": new_ascension,
            "new_level_cap": new_level_cap,
            "unlocked_passive": unlocked_passive
        }
    
    async def awaken(
        self,
        hero_id: str,
        player_id: str
    ) -> dict:
        """
        Awaken a hero for stat boost and abilities.
        
        Args:
            hero_id: The hero ID
            player_id: The player ID
            
        Returns:
            Dictionary with awakening result
        """
        hero_data = await self.get_hero(hero_id, player_id)
        old_awakening = hero_data.get("awakening_level", 0)
        
        if old_awakening >= 6:
            raise ValidationException("Hero is already at max awakening level")
        
        new_awakening = old_awakening + 1
        stat_boost = new_awakening * 10  # 10% per level
        
        # Unlock ability based on awakening level
        unlocked_ability = None
        if new_awakening == 1:
            unlocked_ability = "new_skill_variant"
        elif new_awakening == 3:
            unlocked_ability = "transformation"
        
        if self.hero_repository:
            await self.hero_repository.update(hero_id, {"awakening_level": new_awakening})
        
        return {
            "hero_id": hero_id,
            "old_awakening_level": old_awakening,
            "new_awakening_level": new_awakening,
            "stat_boost_percent": stat_boost,
            "unlocked_ability": unlocked_ability
        }
    
    async def equip_item(
        self,
        hero_id: str,
        player_id: str,
        equipment_id: str,
        slot: str
    ) -> dict:
        """
        Equip an item to a hero.
        
        Args:
            hero_id: The hero ID
            player_id: The player ID
            equipment_id: The equipment ID
            slot: Equipment slot (weapon, armor, accessory, relic)
            
        Returns:
            Dictionary with equip result
        """
        hero_data = await self.get_hero(hero_id, player_id)
        
        # Get current equipment in slot
        slot_key = f"{slot}_id"
        current_equipment_id = hero_data.get("equipment", {}).get(slot_key)
        
        if self.equipment_repository:
            # Verify equipment belongs to player
            equipment = await self.equipment_repository.get_equipment_for_player(
                equipment_id, player_id
            )
            if not equipment:
                raise EquipmentNotFoundException(equipment_id)
        
        if self.hero_repository:
            await self.hero_repository.update_equipment(hero_id, slot, equipment_id)
        
        # Recalculate stats
        new_stats = self._calculate_stats(hero_data, hero_data.get("level", 1))
        
        return {
            "hero_id": hero_id,
            "slot": slot,
            "equipped_id": equipment_id,
            "unequipped_id": current_equipment_id,
            "new_stats": new_stats
        }
    
    async def unequip_item(
        self,
        hero_id: str,
        player_id: str,
        slot: str
    ) -> dict:
        """
        Remove equipment from a hero slot.
        
        Args:
            hero_id: The hero ID
            player_id: The player ID
            slot: Equipment slot
            
        Returns:
            Dictionary with unequip result
        """
        hero_data = await self.get_hero(hero_id, player_id)
        
        slot_key = f"{slot}_id"
        current_equipment_id = hero_data.get("equipment", {}).get(slot_key)
        
        if self.hero_repository:
            await self.hero_repository.update_equipment(hero_id, slot, None)
        
        return {
            "hero_id": hero_id,
            "slot": slot,
            "unequipped_id": current_equipment_id
        }
    
    def _calculate_stats(self, hero_data: dict, level: int) -> dict:
        """Calculate hero stats based on level."""
        # Base stats with level scaling
        base_hp = 1000 + (level - 1) * 50
        base_atk = 100 + (level - 1) * 5
        base_def = 50 + (level - 1) * 3
        base_spd = 100
        base_crit = 10 + (level - 1)
        base_dex = 10 + (level - 1)
        
        return {
            "hp": base_hp,
            "atk": base_atk,
            "def_": base_def,
            "spd": base_spd,
            "crit": base_crit,
            "dex": base_dex
        }
    
    def _mock_hero(self) -> dict:
        """Return mock hero data."""
        return {
            "id": "sample-hero-uuid",
            "template_id": "quan_vu",
            "name": "Quan Vũ",
            "element": "KIM",
            "rarity": 5,
            "level": 1,
            "exp": 0,
            "stars": 1,
            "ascension_level": 0,
            "awakening_level": 0,
            "stats": {"hp": 1000, "atk": 120, "def_": 80, "spd": 95, "crit": 15, "dex": 10},
            "power": 1320,
            "equipment": {
                "weapon_id": None,
                "armor_id": None,
                "accessory_id": None,
                "relic_id": None
            },
            "skills": [],
            "is_locked": False,
            "is_favorite": False
        }
    
    def _hero_to_brief(self, hero) -> dict:
        """Convert hero model to brief response."""
        return {
            "id": str(hero.id),
            "template_id": hero.template_id,
            "name": hero.template.name if hero.template else hero.template_id,
            "element": hero.template.element if hero.template else "KIM",
            "rarity": hero.stars,
            "level": hero.level,
            "stars": hero.stars,
            "power": self._calculate_power(hero)
        }
    
    def _hero_to_response(self, hero) -> dict:
        """Convert hero model to full response."""
        return {
            "id": str(hero.id),
            "template_id": hero.template_id,
            "name": hero.template.name if hero.template else hero.template_id,
            "element": hero.template.element if hero.template else "KIM",
            "rarity": hero.stars,
            "level": hero.level,
            "exp": hero.exp,
            "stars": hero.stars,
            "ascension_level": hero.ascension_level,
            "awakening_level": hero.awakening_level,
            "stats": {
                "hp": hero.current_hp,
                "atk": hero.current_atk,
                "def_": hero.current_def,
                "spd": hero.current_spd,
                "crit": hero.current_crit,
                "dex": hero.current_dex
            },
            "power": self._calculate_power(hero),
            "equipment": {
                "weapon_id": str(hero.weapon_id) if hero.weapon_id else None,
                "armor_id": str(hero.armor_id) if hero.armor_id else None,
                "accessory_id": str(hero.accessory_id) if hero.accessory_id else None,
                "relic_id": str(hero.relic_id) if hero.relic_id else None
            },
            "skills": [],
            "is_locked": hero.is_locked,
            "is_favorite": hero.is_favorite
        }
    
    def _calculate_power(self, hero) -> int:
        """Calculate hero power rating."""
        base_power = (
            hero.current_hp +
            hero.current_atk * 5 +
            hero.current_def * 3 +
            hero.current_spd * 2 +
            hero.current_crit * 10 +
            hero.current_dex * 2
        )
        return base_power
