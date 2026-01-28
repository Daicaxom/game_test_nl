"""
Equipment Service - Business logic for equipment operations
"""
from typing import Optional, Dict, Any, List

from app.core.exceptions import (
    EquipmentNotFoundException,
    ValidationException,
    InsufficientGoldException
)


class EquipmentService:
    """
    Service for equipment-related operations.
    
    Handles:
    - Equipment management
    - Enhancement
    - Fusion
    """
    
    def __init__(
        self,
        equipment_repository=None,
        player_service=None
    ):
        """
        Initialize the equipment service.
        
        Args:
            equipment_repository: Optional EquipmentRepository
            player_service: Optional PlayerService for resource management
        """
        self.equipment_repository = equipment_repository
        self.player_service = player_service
    
    async def get_equipment_list(
        self,
        player_id: str,
        page: int = 1,
        per_page: int = 20,
        equipment_type: Optional[str] = None,
        rarity: Optional[str] = None
    ) -> dict:
        """
        Get player's equipment with filtering and pagination.
        
        Args:
            player_id: The player ID
            page: Page number
            per_page: Items per page
            equipment_type: Optional type filter
            rarity: Optional rarity filter
            
        Returns:
            Dictionary with equipment list and pagination info
        """
        skip = (page - 1) * per_page
        filters = {}
        if equipment_type:
            filters["equipment_type"] = equipment_type
        if rarity:
            filters["rarity"] = rarity
        
        equipment = []
        total = 0
        
        if self.equipment_repository:
            equipment = await self.equipment_repository.get_by_player(
                player_id,
                skip=skip,
                limit=per_page,
                filters=filters
            )
            total = await self.equipment_repository.count_by_player(player_id, filters)
        else:
            # Mock data
            equipment = [self._mock_equipment()]
            total = 1
        
        return {
            "equipment": [self._equipment_to_brief(e) for e in equipment] if self.equipment_repository else equipment,
            "total": total,
            "page": page,
            "per_page": per_page
        }
    
    async def get_equipment(
        self,
        equipment_id: str,
        player_id: str
    ) -> dict:
        """
        Get specific equipment details.
        
        Args:
            equipment_id: The equipment ID
            player_id: The player ID for ownership verification
            
        Returns:
            Dictionary with equipment data
            
        Raises:
            EquipmentNotFoundException: If equipment not found
        """
        if self.equipment_repository:
            equipment = await self.equipment_repository.get_equipment_for_player(
                equipment_id, player_id
            )
            if not equipment:
                raise EquipmentNotFoundException(equipment_id)
            return self._equipment_to_response(equipment)
        
        # Mock data
        return self._mock_equipment()
    
    async def enhance(
        self,
        equipment_id: str,
        player_id: str,
        materials: List[Dict[str, Any]] = None
    ) -> dict:
        """
        Enhance equipment to increase its level.
        
        Args:
            equipment_id: The equipment ID
            player_id: The player ID
            materials: List of enhancement materials
            
        Returns:
            Dictionary with enhancement result
        """
        equipment_data = await self.get_equipment(equipment_id, player_id)
        old_level = equipment_data.get("level", 1)
        
        # Calculate max level based on rarity
        max_levels = {
            "common": 10,
            "rare": 15,
            "epic": 20,
            "legendary": 25,
            "mythic": 30
        }
        max_level = max_levels.get(equipment_data.get("rarity", "common"), 10)
        
        if old_level >= max_level:
            raise ValidationException("Equipment is already at max level")
        
        # Calculate gold cost
        gold_cost = old_level * 100
        
        # Verify and spend gold
        if self.player_service:
            await self.player_service.spend_resources(
                player_id,
                gold=gold_cost
            )
        
        new_level = old_level + 1
        
        # Calculate stats gained
        base_stats = equipment_data.get("base_stats", {})
        stats_gained = {
            "hp": int(base_stats.get("hp", 0) * 0.1),
            "atk": int(base_stats.get("atk", 0) * 0.1),
            "def_": int(base_stats.get("def_", 0) * 0.1),
            "spd": int(base_stats.get("spd", 0) * 0.1),
            "crit": int(base_stats.get("crit", 0) * 0.1),
            "dex": int(base_stats.get("dex", 0) * 0.1)
        }
        
        # Calculate new bonus stats
        bonus_stats = equipment_data.get("bonus_stats", {})
        new_bonus = {
            "hp": bonus_stats.get("hp", 0) + stats_gained["hp"],
            "atk": bonus_stats.get("atk", 0) + stats_gained["atk"],
            "def_": bonus_stats.get("def_", 0) + stats_gained["def_"],
            "spd": bonus_stats.get("spd", 0) + stats_gained["spd"],
            "crit": bonus_stats.get("crit", 0) + stats_gained["crit"],
            "dex": bonus_stats.get("dex", 0) + stats_gained["dex"]
        }
        
        if self.equipment_repository:
            await self.equipment_repository.update_level(
                equipment_id,
                new_level,
                new_bonus
            )
        
        return {
            "equipment_id": equipment_id,
            "old_level": old_level,
            "new_level": new_level,
            "success": True,
            "stats_gained": stats_gained,
            "gold_spent": gold_cost
        }
    
    async def fuse(
        self,
        player_id: str,
        equipment_ids: List[str]
    ) -> dict:
        """
        Fuse multiple equipment into one.
        
        Args:
            player_id: The player ID
            equipment_ids: List of equipment IDs to fuse
            
        Returns:
            Dictionary with fusion result
        """
        if len(equipment_ids) < 2:
            raise ValidationException("At least 2 equipment pieces are required for fusion")
        
        # Get all equipment
        equipment_list = []
        for eq_id in equipment_ids:
            eq = await self.get_equipment(eq_id, player_id)
            equipment_list.append(eq)
        
        # Create result equipment (simplified)
        result_equipment = self._mock_equipment()
        result_equipment["id"] = f"fused-{equipment_ids[0]}"
        result_equipment["level"] = 1
        
        # Delete consumed equipment
        if self.equipment_repository:
            await self.equipment_repository.delete_multiple(equipment_ids, player_id)
        
        return {
            "result_equipment": result_equipment,
            "consumed_equipment": equipment_ids
        }
    
    def _mock_equipment(self) -> dict:
        """Return mock equipment data."""
        return {
            "id": "sample-equipment-uuid",
            "template_id": "iron_sword",
            "name": "Thanh Long Đao",
            "equipment_type": "weapon",
            "rarity": "legendary",
            "level": 1,
            "base_stats": {"hp": 0, "atk": 50, "def_": 0, "spd": 10, "crit": 5, "dex": 5},
            "bonus_stats": {"hp": 0, "atk": 0, "def_": 0, "spd": 0, "crit": 0, "dex": 0},
            "total_stats": {"hp": 0, "atk": 50, "def_": 0, "spd": 10, "crit": 5, "dex": 5},
            "substats": [],
            "set_id": None,
            "unique_effect": None,
            "equipped_by": None,
            "is_locked": False,
            "power": 120
        }
    
    def _equipment_to_brief(self, equipment) -> dict:
        """Convert equipment model to brief response."""
        return {
            "id": str(equipment.id),
            "template_id": equipment.template_id,
            "name": equipment.template_id,  # Would be template name
            "equipment_type": "weapon",  # Would be from template
            "rarity": "legendary",  # Would be from template
            "level": equipment.level,
            "power": self._calculate_power(equipment),
            "equipped_by": None
        }
    
    def _equipment_to_response(self, equipment) -> dict:
        """Convert equipment model to full response."""
        base_stats = {
            "hp": 0,
            "atk": 50,
            "def_": 0,
            "spd": 10,
            "crit": 5,
            "dex": 5
        }
        bonus_stats = {
            "hp": equipment.bonus_hp,
            "atk": equipment.bonus_atk,
            "def_": equipment.bonus_def,
            "spd": equipment.bonus_spd,
            "crit": equipment.bonus_crit,
            "dex": equipment.bonus_dex
        }
        total_stats = {
            "hp": base_stats["hp"] + bonus_stats["hp"],
            "atk": base_stats["atk"] + bonus_stats["atk"],
            "def_": base_stats["def_"] + bonus_stats["def_"],
            "spd": base_stats["spd"] + bonus_stats["spd"],
            "crit": base_stats["crit"] + bonus_stats["crit"],
            "dex": base_stats["dex"] + bonus_stats["dex"]
        }
        
        return {
            "id": str(equipment.id),
            "template_id": equipment.template_id,
            "name": equipment.template_id,
            "equipment_type": "weapon",
            "rarity": "legendary",
            "level": equipment.level,
            "base_stats": base_stats,
            "bonus_stats": bonus_stats,
            "total_stats": total_stats,
            "substats": equipment.substats or [],
            "set_id": None,
            "unique_effect": None,
            "equipped_by": None,
            "is_locked": equipment.is_locked,
            "power": self._calculate_power(equipment)
        }
    
    def _calculate_power(self, equipment) -> int:
        """Calculate equipment power rating."""
        return (
            equipment.bonus_hp +
            equipment.bonus_atk * 5 +
            equipment.bonus_def * 3 +
            equipment.bonus_spd * 2 +
            equipment.bonus_crit * 10 +
            equipment.bonus_dex * 2
        )
