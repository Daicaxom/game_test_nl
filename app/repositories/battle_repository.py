"""
Battle Repository - Data access for battle state (Redis-based)
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
import json
from datetime import datetime

# Note: This is a simplified in-memory implementation.
# In production, this would use Redis for real-time battle state management.


class BattleRepository:
    """
    Repository for battle state management.
    
    Uses in-memory storage for development.
    In production, this would use Redis for:
    - Real-time battle state
    - Session management
    - Leaderboards
    """
    
    # In-memory storage (would be Redis in production)
    _active_battles: Dict[str, Dict[str, Any]] = {}
    _battle_history: Dict[str, List[Dict[str, Any]]] = {}  # player_id -> battles
    
    def __init__(self):
        """Initialize the battle repository."""
        pass
    
    async def save_active_battle(
        self,
        battle_id: str,
        battle_state: Dict[str, Any]
    ) -> None:
        """
        Save an active battle state.
        
        Args:
            battle_id: The battle ID
            battle_state: The battle state dictionary
        """
        self._active_battles[battle_id] = {
            **battle_state,
            "updated_at": datetime.utcnow().isoformat()
        }
    
    async def get_active_battle(
        self,
        battle_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get an active battle state.
        
        Args:
            battle_id: The battle ID
            
        Returns:
            Battle state dictionary or None if not found
        """
        return self._active_battles.get(battle_id)
    
    async def delete_active_battle(self, battle_id: str) -> bool:
        """
        Delete an active battle (when it ends).
        
        Args:
            battle_id: The battle ID
            
        Returns:
            True if deleted, False if not found
        """
        if battle_id in self._active_battles:
            del self._active_battles[battle_id]
            return True
        return False
    
    async def get_player_active_battle(
        self,
        player_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get a player's current active battle.
        
        Args:
            player_id: The player ID
            
        Returns:
            Battle state or None if no active battle
        """
        for battle_id, battle_state in self._active_battles.items():
            if battle_state.get("player_id") == player_id:
                return battle_state
        return None
    
    async def save_battle_result(
        self,
        player_id: str,
        battle_result: Dict[str, Any]
    ) -> None:
        """
        Save a completed battle to history.
        
        Args:
            player_id: The player ID
            battle_result: The battle result data
        """
        if player_id not in self._battle_history:
            self._battle_history[player_id] = []
        
        self._battle_history[player_id].append({
            **battle_result,
            "completed_at": datetime.utcnow().isoformat()
        })
        
        # Keep only last 100 battles per player
        if len(self._battle_history[player_id]) > 100:
            self._battle_history[player_id] = self._battle_history[player_id][-100:]
    
    async def get_battle_history(
        self,
        player_id: str,
        skip: int = 0,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Get player's battle history.
        
        Args:
            player_id: The player ID
            skip: Number of records to skip
            limit: Maximum number of records
            
        Returns:
            List of battle history entries
        """
        history = self._battle_history.get(player_id, [])
        # Return in reverse chronological order
        return list(reversed(history))[skip:skip + limit]
    
    async def count_battle_history(self, player_id: str) -> int:
        """
        Count player's battle history.
        
        Args:
            player_id: The player ID
            
        Returns:
            Number of battles in history
        """
        return len(self._battle_history.get(player_id, []))
    
    async def get_battle_stats(
        self,
        player_id: str
    ) -> Dict[str, int]:
        """
        Get player's battle statistics.
        
        Args:
            player_id: The player ID
            
        Returns:
            Dictionary with battle stats
        """
        history = self._battle_history.get(player_id, [])
        
        wins = sum(1 for b in history if b.get("victory", False))
        losses = len(history) - wins
        
        return {
            "total_battles": len(history),
            "wins": wins,
            "losses": losses,
            "win_rate": wins / len(history) if history else 0
        }
    
    async def clear_player_battles(self, player_id: str) -> None:
        """
        Clear all battle data for a player.
        
        Args:
            player_id: The player ID
        """
        # Clear active battles
        battles_to_remove = [
            battle_id
            for battle_id, battle in self._active_battles.items()
            if battle.get("player_id") == player_id
        ]
        for battle_id in battles_to_remove:
            del self._active_battles[battle_id]
        
        # Clear history
        if player_id in self._battle_history:
            del self._battle_history[player_id]
    
    async def update_battle_turn(
        self,
        battle_id: str,
        turn_number: int,
        action_log: Dict[str, Any]
    ) -> bool:
        """
        Update battle state with a new turn.
        
        Args:
            battle_id: The battle ID
            turn_number: New turn number
            action_log: The action log entry
            
        Returns:
            True if updated, False if battle not found
        """
        if battle_id not in self._active_battles:
            return False
        
        self._active_battles[battle_id]["turn_number"] = turn_number
        
        if "action_log" not in self._active_battles[battle_id]:
            self._active_battles[battle_id]["action_log"] = []
        
        self._active_battles[battle_id]["action_log"].append(action_log)
        self._active_battles[battle_id]["updated_at"] = datetime.utcnow().isoformat()
        
        return True
