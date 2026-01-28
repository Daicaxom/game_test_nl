"""
Story Service - Business logic for story and stages
"""
from typing import Optional, Dict, Any, List

from app.core.exceptions import (
    StageNotFoundException,
    InsufficientStaminaException,
    ValidationException
)


# Story data (would be in database)
CHAPTERS = [
    {
        "id": "chapter_1",
        "chapter_number": 1,
        "title": "Khởi Nghĩa Hoàng Cân",
        "description": "Loạn Hoàng Cân nổi dậy, thiên hạ đại loạn",
        "is_mythical": False,
        "stages": [
            {
                "id": "stage_1_1",
                "stage_number": 1,
                "name": "Hoàng Cân Chi Loạn",
                "difficulty": 1,
                "recommended_power": 1000,
                "stamina_cost": 10,
                "waves": 3,
                "is_boss_stage": False
            },
            {
                "id": "stage_1_2",
                "stage_number": 2,
                "name": "Tiêu Diệt Phản Quân",
                "difficulty": 2,
                "recommended_power": 1500,
                "stamina_cost": 10,
                "waves": 3,
                "is_boss_stage": False
            },
            {
                "id": "stage_1_3",
                "stage_number": 3,
                "name": "Đối Đầu Trương Giác",
                "difficulty": 3,
                "recommended_power": 2000,
                "stamina_cost": 15,
                "waves": 1,
                "is_boss_stage": True
            }
        ]
    },
    {
        "id": "chapter_2",
        "chapter_number": 2,
        "title": "Đổng Trác Loạn Kinh",
        "description": "Đổng Trác kiểm soát triều đình",
        "is_mythical": False,
        "stages": [
            {
                "id": "stage_2_1",
                "stage_number": 1,
                "name": "Kinh Thành Hỗn Loạn",
                "difficulty": 3,
                "recommended_power": 2500,
                "stamina_cost": 12,
                "waves": 3,
                "is_boss_stage": False
            }
        ]
    }
]


class StoryService:
    """
    Service for story and stage operations.
    
    Handles:
    - Chapter management
    - Stage progression
    - Rewards
    """
    
    def __init__(self, player_service=None, battle_service=None):
        """
        Initialize the story service.
        
        Args:
            player_service: Optional PlayerService
            battle_service: Optional BattleService
        """
        self.player_service = player_service
        self.battle_service = battle_service
        # In-memory progress tracking (would be in database in production)
        self._player_progress: Dict[str, Dict[str, Any]] = {}
    
    async def get_chapters(self, player_id: str) -> List[dict]:
        """
        Get all story chapters with progress.
        
        Args:
            player_id: The player ID
            
        Returns:
            List of chapters with unlock status
        """
        progress = self._get_player_progress(player_id)
        
        chapters = []
        for chapter in CHAPTERS:
            chapter_info = {
                "id": chapter["id"],
                "chapter_number": chapter["chapter_number"],
                "title": chapter["title"],
                "description": chapter["description"],
                "is_mythical": chapter["is_mythical"],
                "is_unlocked": self._is_chapter_unlocked(player_id, chapter),
                "stage_count": len(chapter["stages"]),
                "stages_cleared": progress.get("chapters", {}).get(chapter["id"], {}).get("cleared", 0)
            }
            chapters.append(chapter_info)
        
        return chapters
    
    async def get_chapter(self, player_id: str, chapter_id: str) -> dict:
        """
        Get chapter details with stages.
        
        Args:
            player_id: The player ID
            chapter_id: The chapter ID
            
        Returns:
            Chapter details with stages
        """
        chapter = self._find_chapter(chapter_id)
        if not chapter:
            raise ValidationException(f"Chapter '{chapter_id}' not found")
        
        progress = self._get_player_progress(player_id)
        chapter_progress = progress.get("chapters", {}).get(chapter_id, {})
        
        stages = []
        for stage in chapter["stages"]:
            stage_info = {
                **stage,
                "is_unlocked": self._is_stage_unlocked(player_id, chapter_id, stage),
                "stars": chapter_progress.get("stages", {}).get(stage["id"], {}).get("stars", 0),
                "cleared": stage["id"] in chapter_progress.get("cleared_stages", [])
            }
            stages.append(stage_info)
        
        return {
            "id": chapter["id"],
            "chapter_number": chapter["chapter_number"],
            "title": chapter["title"],
            "description": chapter["description"],
            "is_mythical": chapter["is_mythical"],
            "stages": stages
        }
    
    async def get_stage(self, stage_id: str) -> dict:
        """
        Get stage details.
        
        Args:
            stage_id: The stage ID
            
        Returns:
            Stage details
            
        Raises:
            StageNotFoundException: If stage not found
        """
        for chapter in CHAPTERS:
            for stage in chapter["stages"]:
                if stage["id"] == stage_id:
                    return {
                        **stage,
                        "chapter_id": chapter["id"],
                        "chapter_title": chapter["title"],
                        "first_clear_rewards": {
                            "gold": stage["difficulty"] * 500,
                            "gems": stage["difficulty"] * 10,
                            "exp": stage["difficulty"] * 100
                        },
                        "repeat_rewards": {
                            "gold": stage["difficulty"] * 100,
                            "exp": stage["difficulty"] * 50
                        }
                    }
        
        raise StageNotFoundException(stage_id)
    
    async def start_stage(
        self,
        player_id: str,
        stage_id: str,
        team_id: str
    ) -> dict:
        """
        Start a stage battle.
        
        Args:
            player_id: The player ID
            stage_id: The stage ID
            team_id: The team ID to use
            
        Returns:
            Battle initialization data
        """
        stage = await self.get_stage(stage_id)
        
        # Check stamina
        if self.player_service:
            resources = await self.player_service.get_resources(player_id)
            if resources["stamina"] < stage["stamina_cost"]:
                raise InsufficientStaminaException(
                    required=stage["stamina_cost"],
                    available=resources["stamina"]
                )
            
            # Spend stamina
            await self.player_service.spend_resources(
                player_id,
                stamina=stage["stamina_cost"]
            )
        
        return {
            "stage_id": stage_id,
            "team_id": team_id,
            "stamina_spent": stage["stamina_cost"],
            "message": f"Stage '{stage['name']}' started"
        }
    
    async def get_progress(self, player_id: str) -> dict:
        """
        Get player's story progress.
        
        Args:
            player_id: The player ID
            
        Returns:
            Progress information
        """
        progress = self._get_player_progress(player_id)
        
        total_stages = sum(len(c["stages"]) for c in CHAPTERS)
        cleared_stages = sum(
            len(cp.get("cleared_stages", []))
            for cp in progress.get("chapters", {}).values()
        )
        
        total_stars = sum(
            sum(s.get("stars", 0) for s in cp.get("stages", {}).values())
            for cp in progress.get("chapters", {}).values()
        )
        max_stars = total_stages * 3
        
        return {
            "player_id": player_id,
            "chapters_cleared": progress.get("chapters_cleared", 0),
            "total_chapters": len(CHAPTERS),
            "stages_cleared": cleared_stages,
            "total_stages": total_stages,
            "stars_earned": total_stars,
            "max_stars": max_stars,
            "current_chapter": progress.get("current_chapter", "chapter_1")
        }
    
    async def complete_stage(
        self,
        player_id: str,
        stage_id: str,
        stars: int
    ) -> dict:
        """
        Record stage completion.
        
        Args:
            player_id: The player ID
            stage_id: The stage ID
            stars: Stars earned (0-3)
            
        Returns:
            Rewards and progress update
        """
        stage = await self.get_stage(stage_id)
        progress = self._get_player_progress(player_id)
        
        chapter_id = stage["chapter_id"]
        if chapter_id not in progress.get("chapters", {}):
            progress.setdefault("chapters", {})[chapter_id] = {
                "cleared_stages": [],
                "stages": {}
            }
        
        chapter_progress = progress["chapters"][chapter_id]
        first_clear = stage_id not in chapter_progress["cleared_stages"]
        
        # Update progress
        if first_clear:
            chapter_progress["cleared_stages"].append(stage_id)
        
        # Update stars if better
        current_stars = chapter_progress.get("stages", {}).get(stage_id, {}).get("stars", 0)
        if stars > current_stars:
            chapter_progress.setdefault("stages", {})[stage_id] = {"stars": stars}
        
        # Calculate rewards
        if first_clear:
            rewards = stage["first_clear_rewards"]
        else:
            rewards = stage["repeat_rewards"]
        
        # Add rewards to player
        if self.player_service:
            await self.player_service.add_resources(
                player_id,
                gold=rewards.get("gold", 0),
                gems=rewards.get("gems", 0) if first_clear else 0
            )
            await self.player_service.add_experience(player_id, rewards.get("exp", 0))
        
        return {
            "stage_id": stage_id,
            "stars": stars,
            "first_clear": first_clear,
            "rewards": rewards
        }
    
    def _get_player_progress(self, player_id: str) -> Dict[str, Any]:
        """Get or initialize player progress."""
        if player_id not in self._player_progress:
            self._player_progress[player_id] = {
                "chapters": {},
                "chapters_cleared": 0,
                "current_chapter": "chapter_1"
            }
        return self._player_progress[player_id]
    
    def _find_chapter(self, chapter_id: str) -> Optional[dict]:
        """Find chapter by ID."""
        for chapter in CHAPTERS:
            if chapter["id"] == chapter_id:
                return chapter
        return None
    
    def _is_chapter_unlocked(self, player_id: str, chapter: dict) -> bool:
        """Check if chapter is unlocked for player."""
        if chapter["chapter_number"] == 1:
            return True
        
        # Previous chapter must be cleared
        prev_chapter = CHAPTERS[chapter["chapter_number"] - 2]
        progress = self._get_player_progress(player_id)
        prev_progress = progress.get("chapters", {}).get(prev_chapter["id"], {})
        
        return len(prev_progress.get("cleared_stages", [])) >= len(prev_chapter["stages"])
    
    def _is_stage_unlocked(
        self,
        player_id: str,
        chapter_id: str,
        stage: dict
    ) -> bool:
        """Check if stage is unlocked for player."""
        if stage["stage_number"] == 1:
            # First stage in chapter, check if chapter is unlocked
            chapter = self._find_chapter(chapter_id)
            return self._is_chapter_unlocked(player_id, chapter)
        
        # Previous stage must be cleared
        progress = self._get_player_progress(player_id)
        chapter_progress = progress.get("chapters", {}).get(chapter_id, {})
        
        chapter = self._find_chapter(chapter_id)
        prev_stage = chapter["stages"][stage["stage_number"] - 2]
        
        return prev_stage["id"] in chapter_progress.get("cleared_stages", [])
