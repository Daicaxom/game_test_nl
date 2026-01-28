"""
BattleService - Orchestrates battle mechanics
"""
from typing import List, Dict, Any, Optional
from uuid import uuid4

from app.domain.entities.battle import Battle, BattleState, BattleResult
from app.domain.entities.character import Character
from app.domain.entities.hero import Hero
from app.domain.entities.enemy import Enemy
from app.utils.damage_calculator import DamageCalculator


class BattleService:
    """
    Service for managing battle operations.
    
    Responsibilities:
    - Starting and ending battles
    - Executing attacks and skills
    - Managing turn order
    - Calculating rewards
    """
    
    def __init__(self, damage_calculator: Optional[DamageCalculator] = None):
        """
        Initialize BattleService.
        
        Args:
            damage_calculator: Optional DamageCalculator instance
        """
        self.damage_calculator = damage_calculator or DamageCalculator()
    
    def start_battle(
        self,
        player_id: str,
        stage_id: str,
        player_team: List[Hero],
        enemy_team: List[Enemy],
        mana_per_turn: int = 20
    ) -> Battle:
        """
        Start a new battle.
        
        Args:
            player_id: ID of the player
            stage_id: ID of the stage
            player_team: List of player heroes
            enemy_team: List of enemies
            mana_per_turn: Mana generated each turn
            
        Returns:
            Initialized Battle instance
        """
        battle = Battle(
            id=str(uuid4()),
            player_id=player_id,
            stage_id=stage_id,
            player_team=player_team,
            enemy_team=enemy_team,
            state=BattleState.IN_PROGRESS,
            mana_per_turn=mana_per_turn
        )
        
        # Calculate initial turn order
        battle.calculate_turn_order()
        
        # Process first turn start
        battle.process_turn_start()
        
        return battle
    
    def execute_attack(
        self,
        battle: Battle,
        attacker_id: str,
        target_id: str,
        skill_multiplier: float = 1.0
    ) -> Dict[str, Any]:
        """
        Execute a basic attack.
        
        Args:
            battle: Current battle instance
            attacker_id: ID of attacking character
            target_id: ID of target character
            skill_multiplier: Damage multiplier
            
        Returns:
            Dictionary with attack results
        """
        attacker = battle.get_character_by_id(attacker_id)
        target = battle.get_character_by_id(target_id)
        
        if not attacker or not target:
            return {"success": False, "error": "Character not found"}
        
        if not target.is_alive:
            return {"success": False, "error": "Target is already dead"}
        
        # Calculate element multiplier
        element_multiplier = attacker.element.calculate_multiplier(target.element)
        
        # Roll for crit
        is_crit = self.damage_calculator.roll_crit(attacker.stats.crit)
        
        # Calculate damage
        damage = self.damage_calculator.calculate_damage(
            attacker_stats=attacker.stats,
            defender_stats=target.stats,
            skill_multiplier=skill_multiplier,
            attacker_element=attacker.element,
            defender_element=target.element,
            is_crit=is_crit
        )
        
        # Apply damage
        damage_result = target.take_damage(damage)
        
        # Log action
        battle.log_action({
            "type": "attack",
            "attacker_id": attacker_id,
            "target_id": target_id,
            "damage": damage,
            "is_crit": is_crit,
            "element_multiplier": element_multiplier,
            "target_died": damage_result.is_dead
        })
        
        return {
            "success": True,
            "damage": damage,
            "is_crit": is_crit,
            "element_multiplier": element_multiplier,
            "target_hp": target.current_hp,
            "target_died": damage_result.is_dead
        }
    
    def execute_skill(
        self,
        battle: Battle,
        caster_id: str,
        skill_id: str,
        target_ids: List[str],
        mana_cost: int = 50,
        skill_multiplier: float = 1.5
    ) -> Dict[str, Any]:
        """
        Execute a skill.
        
        Args:
            battle: Current battle instance
            caster_id: ID of skill caster
            skill_id: ID of the skill to use
            target_ids: IDs of targets
            mana_cost: Mana cost of the skill
            skill_multiplier: Damage/heal multiplier
            
        Returns:
            Dictionary with skill results
        """
        caster = battle.get_character_by_id(caster_id)
        
        if not caster:
            return {"success": False, "error": "Caster not found"}
        
        # Check mana
        if caster.current_mana < mana_cost:
            return {"success": False, "error": "Insufficient mana"}
        
        # Use mana
        caster.use_mana(mana_cost)
        
        # Process each target
        results = []
        for target_id in target_ids:
            target = battle.get_character_by_id(target_id)
            if not target or not target.is_alive:
                continue
            
            # Calculate and apply damage
            is_crit = self.damage_calculator.roll_crit(caster.stats.crit)
            damage = self.damage_calculator.calculate_damage(
                attacker_stats=caster.stats,
                defender_stats=target.stats,
                skill_multiplier=skill_multiplier,
                attacker_element=caster.element,
                defender_element=target.element,
                is_crit=is_crit
            )
            
            damage_result = target.take_damage(damage)
            results.append({
                "target_id": target_id,
                "damage": damage,
                "is_crit": is_crit,
                "target_died": damage_result.is_dead
            })
        
        # Log action
        battle.log_action({
            "type": "skill",
            "caster_id": caster_id,
            "skill_id": skill_id,
            "mana_cost": mana_cost,
            "targets": results
        })
        
        return {
            "success": True,
            "skill_id": skill_id,
            "mana_cost": mana_cost,
            "remaining_mana": caster.current_mana,
            "targets": results
        }
    
    def execute_heal(
        self,
        battle: Battle,
        caster_id: str,
        target_ids: List[str],
        mana_cost: int = 50,
        heal_multiplier: float = 0.3
    ) -> Dict[str, Any]:
        """
        Execute a healing skill.
        
        Args:
            battle: Current battle instance
            caster_id: ID of healer
            target_ids: IDs of targets to heal
            mana_cost: Mana cost
            heal_multiplier: Heal amount as percentage of max HP
            
        Returns:
            Dictionary with heal results
        """
        caster = battle.get_character_by_id(caster_id)
        
        if not caster:
            return {"success": False, "error": "Caster not found"}
        
        if caster.current_mana < mana_cost:
            return {"success": False, "error": "Insufficient mana"}
        
        caster.use_mana(mana_cost)
        
        results = []
        for target_id in target_ids:
            target = battle.get_character_by_id(target_id)
            if not target or not target.is_alive:
                continue
            
            heal_amount = self.damage_calculator.calculate_heal(
                target_max_hp=target.stats.hp,
                heal_multiplier=heal_multiplier
            )
            
            heal_result = target.heal(heal_amount)
            results.append({
                "target_id": target_id,
                "heal_amount": heal_result.actual_heal,
                "new_hp": target.current_hp
            })
        
        battle.log_action({
            "type": "heal",
            "caster_id": caster_id,
            "mana_cost": mana_cost,
            "targets": results
        })
        
        return {
            "success": True,
            "mana_cost": mana_cost,
            "remaining_mana": caster.current_mana,
            "targets": results
        }
    
    def advance_turn(self, battle: Battle) -> Dict[str, Any]:
        """
        Advance to the next turn.
        
        Args:
            battle: Current battle instance
            
        Returns:
            Dictionary with new turn info
        """
        old_turn = battle.turn_number
        battle.next_turn()
        battle.process_turn_start()
        
        return {
            "old_turn": old_turn,
            "new_turn": battle.turn_number,
            "current_actor_id": battle.get_current_actor().id if battle.get_current_actor() else None,
            "is_player_turn": battle.is_player_turn()
        }
    
    def calculate_rewards(self, battle: Battle) -> Dict[str, Any]:
        """
        Calculate battle rewards.
        
        Args:
            battle: Completed battle instance
            
        Returns:
            Dictionary with rewards
        """
        total_exp = 0
        total_gold = 0
        drops = []
        
        for enemy in battle.enemy_team:
            if isinstance(enemy, Enemy):
                total_exp += enemy.exp_reward
                total_gold += enemy.gold_reward
                
                # Process drop table
                for drop in enemy.drop_table:
                    # TODO: Roll for drops
                    pass
        
        return {
            "exp": total_exp,
            "gold": total_gold,
            "drops": drops,
            "stars": self._calculate_stars(battle)
        }
    
    def _calculate_stars(self, battle: Battle) -> int:
        """
        Calculate star rating for battle completion.
        
        Args:
            battle: Completed battle
            
        Returns:
            Star rating (0-3)
        """
        if battle.state != BattleState.VICTORY:
            return 0
        
        stars = 3
        
        # Lose star for each dead hero
        dead_heroes = sum(1 for h in battle.player_team if not h.is_alive)
        stars -= dead_heroes
        
        # Minimum 1 star for victory
        return max(1, stars)
    
    def get_ai_action(self, battle: Battle, enemy: Enemy) -> Dict[str, Any]:
        """
        Get AI action for an enemy.
        
        Args:
            battle: Current battle
            enemy: Enemy to get action for
            
        Returns:
            Dictionary describing the action
        """
        # Simple AI: attack lowest HP hero
        living_heroes = battle.get_living_heroes()
        if not living_heroes:
            return {"action": "pass"}
        
        # Target lowest HP hero
        target = min(living_heroes, key=lambda h: h.current_hp)
        
        # Decide if to use skill
        if enemy.should_use_skill() and enemy.current_mana >= 50:
            return {
                "action": "skill",
                "skill_id": enemy.skills[0] if enemy.skills else None,
                "target_ids": [target.id]
            }
        
        return {
            "action": "attack",
            "target_id": target.id
        }
