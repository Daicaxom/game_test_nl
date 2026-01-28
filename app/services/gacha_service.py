"""
Gacha Service - Business logic for gacha system
"""
import random
from typing import Optional, Dict, Any, List
from uuid import uuid4

from app.core.exceptions import (
    InsufficientGemsException,
    GachaException
)


# Hero pool by rarity
HERO_POOL = {
    3: ["quan_binh", "hoang_can_binh", "dan_binh"],
    4: ["truong_liao", "xu_chu", "dien_vi", "hoa_huu", "cam_ninh"],
    5: ["quan_vu", "truong_phi", "trieu_van", "luu_bi", "gia_cat_luong"]
}

# Banner configurations
BANNERS = {
    "standard": {
        "id": "standard",
        "name": "Banner Tiêu Chuẩn",
        "rates": {3: 80, 4: 18, 5: 2},
        "pity_counter": 90,
        "cost_single": 160,
        "cost_multi": 1440,
        "featured": None
    },
    "limited": {
        "id": "limited_quan_vu",
        "name": "Banner Quan Vũ",
        "rates": {3: 75, 4: 20, 5: 5},
        "pity_counter": 80,
        "cost_single": 160,
        "cost_multi": 1440,
        "featured": "quan_vu",
        "featured_rate_up": 50
    }
}


class GachaService:
    """
    Service for gacha operations.
    
    Handles:
    - Banner management
    - Gacha pulls
    - Pity system
    - History tracking
    """
    
    # In-memory pity counter (would be stored in database)
    _pity_counters: Dict[str, Dict[str, int]] = {}
    _pull_history: Dict[str, List[Dict]] = {}
    
    def __init__(
        self,
        player_service=None,
        hero_repository=None
    ):
        """
        Initialize the gacha service.
        
        Args:
            player_service: Optional PlayerService for resource management
            hero_repository: Optional HeroRepository to create new heroes
        """
        self.player_service = player_service
        self.hero_repository = hero_repository
    
    async def get_banners(self) -> List[dict]:
        """
        Get all active gacha banners.
        
        Returns:
            List of banner information
        """
        return [
            {
                "id": banner["id"],
                "name": banner["name"],
                "rates": banner["rates"],
                "cost_single": banner["cost_single"],
                "cost_multi": banner["cost_multi"],
                "featured": banner.get("featured")
            }
            for banner in BANNERS.values()
        ]
    
    async def get_banner(self, banner_id: str) -> dict:
        """
        Get specific banner details.
        
        Args:
            banner_id: The banner ID
            
        Returns:
            Banner information
            
        Raises:
            GachaException: If banner not found
        """
        # Find banner
        for banner in BANNERS.values():
            if banner["id"] == banner_id:
                return {
                    "id": banner["id"],
                    "name": banner["name"],
                    "rates": banner["rates"],
                    "cost_single": banner["cost_single"],
                    "cost_multi": banner["cost_multi"],
                    "featured": banner.get("featured"),
                    "pity_counter": banner["pity_counter"]
                }
        
        raise GachaException(f"Banner '{banner_id}' not found")
    
    async def pull(
        self,
        player_id: str,
        banner_id: str,
        pull_count: int = 1
    ) -> dict:
        """
        Perform gacha pulls.
        
        Args:
            player_id: The player ID
            banner_id: The banner to pull from
            pull_count: Number of pulls (1 or 10)
            
        Returns:
            Dictionary with pull results
        """
        if pull_count not in [1, 10]:
            raise GachaException("Invalid pull count. Must be 1 or 10.")
        
        # Get banner
        banner = await self.get_banner(banner_id)
        
        # Calculate cost
        cost = banner["cost_single"] if pull_count == 1 else banner["cost_multi"]
        
        # Verify and spend gems
        if self.player_service:
            await self.player_service.spend_resources(
                player_id,
                gems=cost
            )
        
        # Perform pulls
        results = []
        for _ in range(pull_count):
            result = self._perform_single_pull(player_id, banner)
            results.append(result)
        
        # Save to history
        self._save_pull_history(player_id, banner_id, results)
        
        return {
            "banner_id": banner_id,
            "pull_count": pull_count,
            "gems_spent": cost,
            "results": results,
            "pity_counter": self._get_pity_counter(player_id, banner_id)
        }
    
    async def get_pity(self, player_id: str, banner_id: str) -> dict:
        """
        Get player's pity counter for a banner.
        
        Args:
            player_id: The player ID
            banner_id: The banner ID
            
        Returns:
            Pity information
        """
        pity = self._get_pity_counter(player_id, banner_id)
        banner = await self.get_banner(banner_id)
        
        return {
            "player_id": player_id,
            "banner_id": banner_id,
            "current_pity": pity,
            "pity_threshold": banner["pity_counter"],
            "pulls_until_guaranteed": banner["pity_counter"] - pity
        }
    
    async def get_history(
        self,
        player_id: str,
        page: int = 1,
        per_page: int = 20
    ) -> dict:
        """
        Get player's gacha history.
        
        Args:
            player_id: The player ID
            page: Page number
            per_page: Items per page
            
        Returns:
            Paginated history
        """
        history = self._pull_history.get(player_id, [])
        total = len(history)
        
        skip = (page - 1) * per_page
        items = history[skip:skip + per_page]
        
        return {
            "history": items,
            "total": total,
            "page": page,
            "per_page": per_page
        }
    
    def _perform_single_pull(
        self,
        player_id: str,
        banner: dict
    ) -> dict:
        """
        Perform a single gacha pull.
        
        Args:
            player_id: The player ID
            banner: The banner configuration
            
        Returns:
            Pull result
        """
        banner_id = banner["id"]
        pity = self._get_pity_counter(player_id, banner_id)
        
        # Determine rarity
        roll = random.random() * 100
        
        # Check pity
        pity_threshold = banner.get("pity_counter", 90)
        if pity >= pity_threshold - 1:
            rarity = 5
            self._reset_pity_counter(player_id, banner_id)
        elif roll < banner["rates"][5]:
            rarity = 5
            self._reset_pity_counter(player_id, banner_id)
        elif roll < banner["rates"][5] + banner["rates"][4]:
            rarity = 4
            self._increment_pity_counter(player_id, banner_id)
        else:
            rarity = 3
            self._increment_pity_counter(player_id, banner_id)
        
        # Select hero
        hero_pool = HERO_POOL[rarity]
        
        # Check for featured hero
        if rarity == 5 and banner.get("featured"):
            featured_rate = banner.get("featured_rate_up", 50)
            if random.random() * 100 < featured_rate:
                hero_id = banner["featured"]
            else:
                hero_id = random.choice(hero_pool)
        else:
            hero_id = random.choice(hero_pool)
        
        return {
            "hero_id": hero_id,
            "rarity": rarity,
            "is_new": True,  # Would check against existing heroes
            "is_featured": hero_id == banner.get("featured")
        }
    
    def _get_pity_counter(self, player_id: str, banner_id: str) -> int:
        """Get current pity counter."""
        if player_id not in self._pity_counters:
            self._pity_counters[player_id] = {}
        return self._pity_counters[player_id].get(banner_id, 0)
    
    def _increment_pity_counter(self, player_id: str, banner_id: str) -> None:
        """Increment pity counter."""
        if player_id not in self._pity_counters:
            self._pity_counters[player_id] = {}
        current = self._pity_counters[player_id].get(banner_id, 0)
        self._pity_counters[player_id][banner_id] = current + 1
    
    def _reset_pity_counter(self, player_id: str, banner_id: str) -> None:
        """Reset pity counter after getting 5-star."""
        if player_id not in self._pity_counters:
            self._pity_counters[player_id] = {}
        self._pity_counters[player_id][banner_id] = 0
    
    def _save_pull_history(
        self,
        player_id: str,
        banner_id: str,
        results: List[dict]
    ) -> None:
        """Save pull results to history."""
        if player_id not in self._pull_history:
            self._pull_history[player_id] = []
        
        from datetime import datetime
        
        for result in results:
            self._pull_history[player_id].append({
                "banner_id": banner_id,
                "hero_id": result["hero_id"],
                "rarity": result["rarity"],
                "timestamp": datetime.utcnow().isoformat()
            })
        
        # Keep only last 500 pulls
        if len(self._pull_history[player_id]) > 500:
            self._pull_history[player_id] = self._pull_history[player_id][-500:]
