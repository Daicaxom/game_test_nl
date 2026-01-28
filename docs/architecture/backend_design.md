# Backend Design - Ngọa Long Tam Quốc

## 1. Tổng Quan Kiến Trúc

### 1.1 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        BACKEND ARCHITECTURE                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                         API GATEWAY                                   │  │
│  │  (Kong / AWS API Gateway / nginx)                                    │  │
│  │  - Rate Limiting                                                      │  │
│  │  - Authentication                                                     │  │
│  │  - Load Balancing                                                     │  │
│  │  - SSL Termination                                                    │  │
│  └─────────────────────────────┬─────────────────────────────────────────┘  │
│                                │                                            │
│  ┌─────────────────────────────▼─────────────────────────────────────────┐  │
│  │                      MICROSERVICES LAYER                              │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐     │  │
│  │  │    Auth     │ │   Player    │ │   Battle    │ │    Gacha    │     │  │
│  │  │   Service   │ │   Service   │ │   Service   │ │   Service   │     │  │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘     │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐     │  │
│  │  │  Character  │ │  Equipment  │ │    Story    │ │    Guild    │     │  │
│  │  │   Service   │ │   Service   │ │   Service   │ │   Service   │     │  │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘     │  │
│  └─────────────────────────────┬─────────────────────────────────────────┘  │
│                                │                                            │
│  ┌─────────────────────────────▼─────────────────────────────────────────┐  │
│  │                      MESSAGE BROKER                                   │  │
│  │  (RabbitMQ / Apache Kafka)                                           │  │
│  │  - Event Sourcing                                                     │  │
│  │  - Async Processing                                                   │  │
│  │  - Service Communication                                              │  │
│  └─────────────────────────────┬─────────────────────────────────────────┘  │
│                                │                                            │
│  ┌─────────────────────────────▼─────────────────────────────────────────┐  │
│  │                      DATA LAYER                                       │  │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐          │  │
│  │  │PostgreSQL │  │   Redis   │  │  MongoDB  │  │    S3     │          │  │
│  │  │  Primary  │  │   Cache   │  │   Logs    │  │  Assets   │          │  │
│  │  └───────────┘  └───────────┘  └───────────┘  └───────────┘          │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| API Gateway | Kong / nginx | Routing, Rate limiting, Auth |
| Backend Framework | FastAPI (Python) | High-performance async API |
| Authentication | JWT + OAuth2 | Secure authentication |
| Database | PostgreSQL | Primary data storage |
| Cache | Redis | Session, Leaderboard, Real-time |
| Message Queue | RabbitMQ | Event processing |
| Search | Elasticsearch | Hero/Equipment search |
| Monitoring | Prometheus + Grafana | Metrics & Alerts |
| Logging | ELK Stack | Centralized logging |

---

## 2. Project Structure

```
ngoa-long-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py            # Environment configuration
│   │   └── database.py            # Database connection
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── router.py          # API routes aggregator
│   │   │   ├── auth.py            # Authentication endpoints
│   │   │   ├── players.py         # Player endpoints
│   │   │   ├── heroes.py          # Hero management
│   │   │   ├── battles.py         # Battle system
│   │   │   ├── gacha.py           # Gacha system
│   │   │   ├── equipment.py       # Equipment management
│   │   │   ├── story.py           # Story progression
│   │   │   ├── teams.py           # Team management
│   │   │   ├── guilds.py          # Guild system
│   │   │   └── shop.py            # In-game shop
│   │   └── deps.py                # Dependencies
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py            # JWT, password hashing
│   │   ├── permissions.py         # Role-based access
│   │   └── exceptions.py          # Custom exceptions
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── entities/
│   │   │   ├── __init__.py
│   │   │   ├── character.py
│   │   │   ├── hero.py
│   │   │   ├── enemy.py
│   │   │   ├── boss.py
│   │   │   ├── skill.py
│   │   │   ├── equipment.py
│   │   │   ├── mount.py
│   │   │   └── battle.py
│   │   ├── value_objects/
│   │   │   ├── __init__.py
│   │   │   ├── element.py
│   │   │   ├── hexagon_stats.py
│   │   │   └── grid_position.py
│   │   └── events/
│   │       ├── __init__.py
│   │       ├── battle_events.py
│   │       └── player_events.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── player_service.py
│   │   ├── hero_service.py
│   │   ├── battle_service.py
│   │   ├── gacha_service.py
│   │   ├── equipment_service.py
│   │   ├── story_service.py
│   │   ├── team_service.py
│   │   └── guild_service.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── player_repository.py
│   │   ├── hero_repository.py
│   │   ├── equipment_repository.py
│   │   └── battle_repository.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── player.py
│   │   ├── hero.py
│   │   ├── battle.py
│   │   ├── equipment.py
│   │   └── common.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── player.py
│   │   ├── hero.py
│   │   ├── equipment.py
│   │   └── battle.py
│   └── utils/
│       ├── __init__.py
│       ├── element_system.py
│       ├── damage_calculator.py
│       └── validators.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── migrations/
│   └── versions/
├── scripts/
│   ├── seed_data.py
│   └── benchmark.py
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── alembic.ini
└── README.md
```

---

## 3. API Design

### 3.1 RESTful API Endpoints

#### Authentication
```
POST   /api/v1/auth/register         # Đăng ký
POST   /api/v1/auth/login             # Đăng nhập
POST   /api/v1/auth/refresh           # Refresh token
POST   /api/v1/auth/logout            # Đăng xuất
GET    /api/v1/auth/me                # Thông tin user hiện tại
```

#### Players
```
GET    /api/v1/players/{id}           # Lấy thông tin player
PUT    /api/v1/players/{id}           # Cập nhật profile
GET    /api/v1/players/{id}/stats     # Stats tổng quan
GET    /api/v1/players/{id}/inventory # Inventory
```

#### Heroes
```
GET    /api/v1/heroes                 # Danh sách hero của player
GET    /api/v1/heroes/{id}            # Chi tiết hero
POST   /api/v1/heroes/{id}/level-up   # Nâng cấp level
POST   /api/v1/heroes/{id}/ascend     # Thăng cấp
POST   /api/v1/heroes/{id}/awaken     # Giác ngộ
POST   /api/v1/heroes/{id}/equip      # Trang bị item
DELETE /api/v1/heroes/{id}/equip/{slot} # Tháo trang bị
POST   /api/v1/heroes/{id}/skills/{skillId}/upgrade # Nâng skill
```

#### Battles
```
POST   /api/v1/battles/start          # Bắt đầu trận đấu
POST   /api/v1/battles/{id}/action    # Thực hiện action
GET    /api/v1/battles/{id}/state     # Lấy state hiện tại
POST   /api/v1/battles/{id}/end       # Kết thúc trận
GET    /api/v1/battles/history        # Lịch sử trận đấu
```

#### Gacha
```
GET    /api/v1/gacha/banners          # Danh sách banner
GET    /api/v1/gacha/banners/{id}     # Chi tiết banner
POST   /api/v1/gacha/pull             # Quay gacha
GET    /api/v1/gacha/history          # Lịch sử gacha
GET    /api/v1/gacha/pity             # Pity counter
```

#### Story
```
GET    /api/v1/story/chapters         # Danh sách chapter
GET    /api/v1/story/chapters/{id}    # Chi tiết chapter
GET    /api/v1/story/stages/{id}      # Chi tiết stage
POST   /api/v1/story/stages/{id}/start # Bắt đầu stage
GET    /api/v1/story/progress         # Tiến độ story
```

#### Teams
```
GET    /api/v1/teams                  # Danh sách team
POST   /api/v1/teams                  # Tạo team mới
GET    /api/v1/teams/{id}             # Chi tiết team
PUT    /api/v1/teams/{id}             # Cập nhật team
DELETE /api/v1/teams/{id}             # Xóa team
PUT    /api/v1/teams/{id}/formation   # Đổi formation
```

#### Equipment
```
GET    /api/v1/equipment              # Danh sách equipment
GET    /api/v1/equipment/{id}         # Chi tiết equipment
POST   /api/v1/equipment/{id}/enhance # Cường hóa
POST   /api/v1/equipment/fuse         # Phân giải/ghép
```

### 3.2 API Response Format

```python
# Success Response
{
    "success": true,
    "data": { ... },
    "meta": {
        "timestamp": "2024-01-15T10:30:00Z",
        "request_id": "uuid"
    }
}

# Error Response
{
    "success": false,
    "error": {
        "code": "HERO_NOT_FOUND",
        "message": "Hero with id xxx not found",
        "details": { ... }
    },
    "meta": {
        "timestamp": "2024-01-15T10:30:00Z",
        "request_id": "uuid"
    }
}

# Paginated Response
{
    "success": true,
    "data": [ ... ],
    "pagination": {
        "page": 1,
        "per_page": 20,
        "total": 100,
        "total_pages": 5
    },
    "meta": { ... }
}
```

---

## 4. Service Implementation

### 4.1 Battle Service

```python
# services/battle_service.py

from typing import List, Optional
from uuid import UUID
from app.domain.entities import Battle, Character, Action
from app.domain.value_objects import BattleState, ActionResult
from app.repositories import BattleRepository, HeroRepository
from app.core.exceptions import BattleException
from app.utils.damage_calculator import DamageCalculator

class BattleService:
    def __init__(
        self,
        battle_repo: BattleRepository,
        hero_repo: HeroRepository,
        damage_calc: DamageCalculator
    ):
        self.battle_repo = battle_repo
        self.hero_repo = hero_repo
        self.damage_calc = damage_calc
    
    async def start_battle(
        self,
        player_id: UUID,
        stage_id: str,
        team_id: UUID
    ) -> Battle:
        """Khởi tạo trận đấu mới"""
        # Validate stage unlock
        stage = await self._validate_stage(player_id, stage_id)
        
        # Load player team
        team = await self.hero_repo.get_team_with_heroes(team_id)
        if not team:
            raise BattleException("Team not found")
        
        # Create enemy team from stage
        enemies = await self._create_enemies(stage)
        
        # Initialize battle
        battle = Battle(
            player_id=player_id,
            stage_id=stage_id,
            player_team=team,
            enemy_team=enemies,
            state=BattleState.IN_PROGRESS
        )
        
        # Calculate turn order
        battle.calculate_turn_order()
        
        # Save to Redis for real-time access
        await self.battle_repo.save_active_battle(battle)
        
        return battle
    
    async def execute_action(
        self,
        battle_id: UUID,
        action: Action
    ) -> ActionResult:
        """Thực hiện action trong battle"""
        battle = await self.battle_repo.get_active_battle(battle_id)
        if not battle:
            raise BattleException("Battle not found or ended")
        
        # Validate it's player's turn
        if not battle.is_player_turn():
            raise BattleException("Not player's turn")
        
        # Validate action
        if not action.validate(battle.state):
            raise BattleException("Invalid action")
        
        # Execute action
        result = await self._process_action(battle, action)
        
        # Check for battle end
        battle_result = battle.check_end_condition()
        if battle_result:
            return await self._end_battle(battle, battle_result)
        
        # Process AI turns
        while not battle.is_player_turn() and not battle.is_ended():
            ai_action = battle.current_actor.decide_action(battle.state)
            await self._process_action(battle, ai_action)
        
        # Save updated state
        await self.battle_repo.save_active_battle(battle)
        
        return result
    
    async def _process_action(
        self,
        battle: Battle,
        action: Action
    ) -> ActionResult:
        """Xử lý một action"""
        actor = battle.current_actor
        
        if action.type == ActionType.ATTACK:
            damage = self.damage_calc.calculate(
                attacker=actor,
                defender=action.target,
                skill=action.skill
            )
            action.target.take_damage(damage)
            result = ActionResult(
                type=ActionType.ATTACK,
                damage=damage,
                effects=action.skill.effects if action.skill else []
            )
            
        elif action.type == ActionType.SKILL:
            result = await self._execute_skill(actor, action.skill, action.targets)
            
        elif action.type == ActionType.MOVE:
            actor.position = action.destination
            result = ActionResult(type=ActionType.MOVE)
        
        # Process status effects
        battle.process_turn_end()
        
        # Next turn
        battle.next_turn()
        
        return result
    
    async def _execute_skill(
        self,
        caster: Character,
        skill: Skill,
        targets: List[Character]
    ) -> ActionResult:
        """Thực hiện skill"""
        # Deduct mana
        caster.current_mana -= skill.mana_cost
        
        # Calculate effects for each target
        effects = []
        for target in targets:
            if skill.skill_type == SkillType.DAMAGE:
                damage = self.damage_calc.calculate_skill_damage(
                    caster, target, skill
                )
                target.take_damage(damage)
                effects.append(DamageEffect(target=target, damage=damage))
                
            elif skill.skill_type == SkillType.HEAL:
                heal = self.damage_calc.calculate_heal(caster, skill)
                target.heal(heal)
                effects.append(HealEffect(target=target, amount=heal))
                
            elif skill.skill_type == SkillType.BUFF:
                target.apply_buff(skill.buff)
                effects.append(BuffEffect(target=target, buff=skill.buff))
                
            elif skill.skill_type == SkillType.DEBUFF:
                if skill.check_success(caster, target):
                    target.apply_debuff(skill.debuff)
                    effects.append(DebuffEffect(target=target, debuff=skill.debuff))
        
        # Set cooldown
        skill.current_cooldown = skill.cooldown
        
        return ActionResult(
            type=ActionType.SKILL,
            skill=skill,
            effects=effects
        )
```

### 4.2 Gacha Service

```python
# services/gacha_service.py

import random
from typing import List
from uuid import UUID
from app.domain.entities import Hero
from app.repositories import GachaRepository, HeroRepository, PlayerRepository
from app.core.exceptions import GachaException

class GachaService:
    PITY_THRESHOLD = 90
    SOFT_PITY_START = 75
    BASE_5STAR_RATE = 0.006  # 0.6%
    BASE_4STAR_RATE = 0.051  # 5.1%
    
    def __init__(
        self,
        gacha_repo: GachaRepository,
        hero_repo: HeroRepository,
        player_repo: PlayerRepository
    ):
        self.gacha_repo = gacha_repo
        self.hero_repo = hero_repo
        self.player_repo = player_repo
    
    async def pull(
        self,
        player_id: UUID,
        banner_id: str,
        pull_count: int = 1
    ) -> List[GachaPullResult]:
        """Thực hiện gacha pull"""
        # Validate
        if pull_count not in [1, 10]:
            raise GachaException("Invalid pull count")
        
        banner = await self.gacha_repo.get_banner(banner_id)
        if not banner or not banner.is_active:
            raise GachaException("Banner not available")
        
        player = await self.player_repo.get(player_id)
        cost = banner.cost * pull_count
        
        if player.gems < cost:
            raise GachaException("Not enough gems")
        
        # Get pity counter
        pity = await self.gacha_repo.get_pity(player_id, banner.banner_type)
        
        results = []
        for i in range(pull_count):
            result = await self._single_pull(banner, pity)
            results.append(result)
            
            # Update pity
            if result.rarity == 5:
                pity.count = 0
                pity.guaranteed_featured = False
            else:
                pity.count += 1
        
        # Deduct gems
        await self.player_repo.update_gems(player_id, -cost)
        
        # Save pity
        await self.gacha_repo.save_pity(pity)
        
        # Add heroes to player
        for result in results:
            if result.result_type == 'hero':
                await self.hero_repo.add_hero_to_player(
                    player_id, result.item_id
                )
        
        # Save history
        await self.gacha_repo.save_history(player_id, banner_id, results)
        
        return results
    
    async def _single_pull(
        self,
        banner: Banner,
        pity: PityCounter
    ) -> GachaPullResult:
        """Thực hiện một lần pull"""
        # Calculate rates with pity
        rate_5star = self._calculate_5star_rate(pity.count)
        
        roll = random.random()
        
        if pity.count >= self.PITY_THRESHOLD - 1 or roll < rate_5star:
            # 5-star pull
            rarity = 5
            hero_pool = banner.get_5star_pool()
            
            # Check guaranteed featured
            if banner.featured_heroes and pity.guaranteed_featured:
                hero = random.choice(banner.featured_heroes)
            else:
                # 50/50 chance for featured
                if banner.featured_heroes and random.random() < 0.5:
                    hero = random.choice(banner.featured_heroes)
                else:
                    hero = random.choice(hero_pool)
                    pity.guaranteed_featured = True
                    
        elif roll < rate_5star + self.BASE_4STAR_RATE:
            # 4-star pull
            rarity = 4
            hero_pool = banner.get_4star_pool()
            hero = random.choice(hero_pool)
        else:
            # 3-star pull
            rarity = 3
            hero_pool = banner.get_3star_pool()
            hero = random.choice(hero_pool)
        
        return GachaPullResult(
            result_type='hero',
            item_id=hero.id,
            rarity=rarity,
            is_new=await self._check_new(pity.player_id, hero.id)
        )
    
    def _calculate_5star_rate(self, pity_count: int) -> float:
        """Tính tỷ lệ 5-star với soft pity"""
        if pity_count < self.SOFT_PITY_START:
            return self.BASE_5STAR_RATE
        
        # Increase rate after soft pity
        extra_pity = pity_count - self.SOFT_PITY_START
        return self.BASE_5STAR_RATE + (extra_pity * 0.06)  # +6% per pull after soft pity
```

### 4.3 Hero Service

```python
# services/hero_service.py

from typing import List, Optional
from uuid import UUID
from app.domain.entities import Hero
from app.repositories import HeroRepository
from app.core.exceptions import HeroException

class HeroService:
    def __init__(self, hero_repo: HeroRepository):
        self.hero_repo = hero_repo
    
    async def get_player_heroes(
        self,
        player_id: UUID,
        filters: Optional[HeroFilter] = None
    ) -> List[Hero]:
        """Lấy danh sách hero của player"""
        return await self.hero_repo.get_by_player(player_id, filters)
    
    async def level_up(
        self,
        hero_id: UUID,
        player_id: UUID,
        exp_items: List[ExpItem]
    ) -> LevelUpResult:
        """Nâng cấp level hero"""
        hero = await self._get_and_validate_hero(hero_id, player_id)
        
        # Calculate total exp
        total_exp = sum(item.exp_value * item.quantity for item in exp_items)
        
        # Check level cap based on ascension
        max_level = self._get_max_level(hero.ascension_level)
        
        old_level = hero.level
        hero.exp += total_exp
        
        # Level up loop
        while hero.exp >= self._get_required_exp(hero.level) and hero.level < max_level:
            hero.exp -= self._get_required_exp(hero.level)
            hero.level += 1
            hero.recalculate_stats()
        
        # Cap exp if max level
        if hero.level >= max_level:
            hero.exp = 0
        
        # Deduct items
        await self.hero_repo.consume_exp_items(player_id, exp_items)
        
        # Save
        await self.hero_repo.save(hero)
        
        return LevelUpResult(
            hero_id=hero_id,
            old_level=old_level,
            new_level=hero.level,
            stats=hero.stats
        )
    
    async def ascend(
        self,
        hero_id: UUID,
        player_id: UUID,
        materials: List[Material]
    ) -> AscensionResult:
        """Thăng cấp hero"""
        hero = await self._get_and_validate_hero(hero_id, player_id)
        
        if hero.ascension_level >= 6:
            raise HeroException("Max ascension reached")
        
        # Check materials
        required = self._get_ascension_materials(
            hero.template_id, 
            hero.ascension_level + 1
        )
        if not self._validate_materials(materials, required):
            raise HeroException("Insufficient materials")
        
        # Check level requirement
        required_level = self._get_ascension_level_requirement(hero.ascension_level)
        if hero.level < required_level:
            raise HeroException(f"Need level {required_level} to ascend")
        
        # Perform ascension
        hero.ascension_level += 1
        hero.unlock_passive(hero.ascension_level)
        hero.recalculate_stats()
        
        # Consume materials
        await self.hero_repo.consume_materials(player_id, materials)
        await self.hero_repo.save(hero)
        
        return AscensionResult(
            hero_id=hero_id,
            new_ascension_level=hero.ascension_level,
            unlocked_passive=hero.get_latest_passive(),
            new_level_cap=self._get_max_level(hero.ascension_level)
        )
    
    async def equip(
        self,
        hero_id: UUID,
        player_id: UUID,
        equipment_id: UUID,
        slot: EquipmentSlot
    ) -> EquipResult:
        """Trang bị item cho hero"""
        hero = await self._get_and_validate_hero(hero_id, player_id)
        equipment = await self.hero_repo.get_equipment(equipment_id, player_id)
        
        if not equipment:
            raise HeroException("Equipment not found")
        
        if equipment.type != slot.equipment_type:
            raise HeroException(f"Cannot equip {equipment.type} to {slot} slot")
        
        # Check element requirement
        if equipment.required_element and equipment.required_element != hero.element:
            raise HeroException("Element requirement not met")
        
        # Unequip current item if any
        old_equipment = hero.get_equipped(slot)
        if old_equipment:
            old_equipment.equipped_by = None
        
        # Equip new item
        hero.equip(equipment, slot)
        equipment.equipped_by = hero_id
        
        # Recalculate stats
        hero.recalculate_stats()
        
        await self.hero_repo.save(hero)
        await self.hero_repo.save_equipment(equipment)
        
        return EquipResult(
            hero_id=hero_id,
            slot=slot,
            equipment=equipment,
            unequipped=old_equipment,
            new_stats=hero.stats
        )
```

---

## 5. Domain Events

### 5.1 Event System

```python
# domain/events/base.py

from abc import ABC
from datetime import datetime
from uuid import UUID, uuid4
from typing import Dict, Any

class DomainEvent(ABC):
    def __init__(self):
        self.event_id = uuid4()
        self.timestamp = datetime.utcnow()
        self.version = 1
    
    @property
    def event_type(self) -> str:
        return self.__class__.__name__
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "timestamp": self.timestamp.isoformat(),
            "version": self.version,
            "payload": self._get_payload()
        }
    
    def _get_payload(self) -> Dict[str, Any]:
        raise NotImplementedError


# domain/events/battle_events.py

class BattleStartedEvent(DomainEvent):
    def __init__(self, battle_id: UUID, player_id: UUID, stage_id: str):
        super().__init__()
        self.battle_id = battle_id
        self.player_id = player_id
        self.stage_id = stage_id
    
    def _get_payload(self):
        return {
            "battle_id": str(self.battle_id),
            "player_id": str(self.player_id),
            "stage_id": self.stage_id
        }


class BattleEndedEvent(DomainEvent):
    def __init__(
        self, 
        battle_id: UUID, 
        player_id: UUID, 
        result: str,
        rewards: List[Dict]
    ):
        super().__init__()
        self.battle_id = battle_id
        self.player_id = player_id
        self.result = result
        self.rewards = rewards
    
    def _get_payload(self):
        return {
            "battle_id": str(self.battle_id),
            "player_id": str(self.player_id),
            "result": self.result,
            "rewards": self.rewards
        }


class HeroLevelUpEvent(DomainEvent):
    def __init__(self, hero_id: UUID, player_id: UUID, old_level: int, new_level: int):
        super().__init__()
        self.hero_id = hero_id
        self.player_id = player_id
        self.old_level = old_level
        self.new_level = new_level
```

### 5.2 Event Handler

```python
# services/event_handler.py

from app.domain.events import *
from app.services import NotificationService, AchievementService, AnalyticsService

class EventHandler:
    def __init__(
        self,
        notification_service: NotificationService,
        achievement_service: AchievementService,
        analytics_service: AnalyticsService
    ):
        self.notification = notification_service
        self.achievement = achievement_service
        self.analytics = analytics_service
    
    async def handle(self, event: DomainEvent):
        """Route event to appropriate handlers"""
        handlers = {
            "BattleEndedEvent": self._handle_battle_ended,
            "HeroLevelUpEvent": self._handle_hero_level_up,
            "GachaPullEvent": self._handle_gacha_pull,
        }
        
        handler = handlers.get(event.event_type)
        if handler:
            await handler(event)
        
        # Always log to analytics
        await self.analytics.log_event(event)
    
    async def _handle_battle_ended(self, event: BattleEndedEvent):
        if event.result == "victory":
            # Check achievements
            await self.achievement.check_battle_achievements(
                event.player_id,
                event.stage_id
            )
            
            # Push notification for milestone
            stage_info = await self._get_stage_info(event.stage_id)
            if stage_info.is_boss_stage:
                await self.notification.send(
                    event.player_id,
                    "Boss Defeated!",
                    f"You defeated {stage_info.boss_name}!"
                )
    
    async def _handle_hero_level_up(self, event: HeroLevelUpEvent):
        # Check for level milestone achievements
        if event.new_level in [20, 40, 60, 80, 100]:
            await self.achievement.check_level_milestone(
                event.player_id,
                event.hero_id,
                event.new_level
            )
```

---

## 6. Security

### 6.1 Authentication

```python
# core/security.py

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(
    data: dict, 
    expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None
```

### 6.2 Rate Limiting

```python
# core/rate_limit.py

from fastapi import Request, HTTPException
from app.config import redis_client

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.rpm = requests_per_minute
    
    async def check(self, request: Request, identifier: str):
        key = f"rate_limit:{identifier}:{request.url.path}"
        
        current = await redis_client.incr(key)
        if current == 1:
            await redis_client.expire(key, 60)
        
        if current > self.rpm:
            raise HTTPException(
                status_code=429,
                detail="Too many requests"
            )

# Usage in endpoint
@router.post("/gacha/pull")
@limiter.limit("10/minute")
async def gacha_pull(...):
    ...
```

---

## 7. Caching Strategy

### 7.1 Cache Layers

```python
# utils/cache.py

from functools import wraps
from typing import Optional, Callable
import json
from app.config import redis_client

def cache(ttl: int = 300, key_prefix: str = ""):
    """Decorator for caching function results"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Check cache
            cached = await redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Store in cache
            await redis_client.setex(
                cache_key, 
                ttl, 
                json.dumps(result, default=str)
            )
            
            return result
        return wrapper
    return decorator

# Usage
@cache(ttl=3600, key_prefix="hero_template")
async def get_hero_template(template_id: str):
    return await db.fetch_one(
        "SELECT * FROM hero_templates WHERE id = :id",
        {"id": template_id}
    )
```

### 7.2 Cache Invalidation

```python
class CacheInvalidator:
    @staticmethod
    async def invalidate_player_cache(player_id: str):
        patterns = [
            f"player:{player_id}:*",
            f"heroes:{player_id}:*",
            f"inventory:{player_id}:*"
        ]
        for pattern in patterns:
            keys = await redis_client.keys(pattern)
            if keys:
                await redis_client.delete(*keys)
    
    @staticmethod
    async def invalidate_hero_cache(hero_id: str):
        await redis_client.delete(f"hero:{hero_id}")
```

---

## 8. Testing Strategy

### 8.1 Unit Tests

```python
# tests/unit/test_damage_calculator.py

import pytest
from app.utils.damage_calculator import DamageCalculator
from app.domain.entities import Hero, Enemy
from app.domain.value_objects import Element, HexagonStats

class TestDamageCalculator:
    def setup_method(self):
        self.calc = DamageCalculator()
    
    def test_basic_damage_calculation(self):
        attacker = Hero(
            stats=HexagonStats(atk=100, crit=0)
        )
        defender = Enemy(
            stats=HexagonStats(def_=50)
        )
        
        damage = self.calc.calculate(attacker, defender)
        
        # damage = (ATK * 1.0 - DEF * 0.5) = 100 - 25 = 75
        assert damage == 75
    
    def test_element_advantage(self):
        attacker = Hero(
            element=Element.HOA,
            stats=HexagonStats(atk=100, crit=0)
        )
        defender = Enemy(
            element=Element.KIM,
            stats=HexagonStats(def_=50)
        )
        
        damage = self.calc.calculate(attacker, defender)
        
        # Hỏa khắc Kim -> x1.5
        # (100 - 25) * 1.5 = 112.5 -> 112
        assert damage == 112
    
    def test_critical_hit(self):
        attacker = Hero(
            stats=HexagonStats(atk=100, crit=100)  # 100% crit
        )
        defender = Enemy(
            stats=HexagonStats(def_=0)
        )
        
        damage = self.calc.calculate(attacker, defender)
        
        # 100 * 2.0 (crit multiplier) = 200
        assert damage == 200
```

### 8.2 Integration Tests

```python
# tests/integration/test_battle_flow.py

import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
class TestBattleFlow:
    async def test_complete_battle_flow(self, authenticated_client: AsyncClient):
        # Start battle
        response = await authenticated_client.post(
            "/api/v1/battles/start",
            json={"stage_id": "stage_1_1", "team_id": "test_team_id"}
        )
        assert response.status_code == 200
        battle_id = response.json()["data"]["battle_id"]
        
        # Execute actions until battle ends
        while True:
            state_response = await authenticated_client.get(
                f"/api/v1/battles/{battle_id}/state"
            )
            state = state_response.json()["data"]
            
            if state["status"] != "in_progress":
                break
            
            # Simple attack action
            action_response = await authenticated_client.post(
                f"/api/v1/battles/{battle_id}/action",
                json={
                    "action_type": "attack",
                    "target_id": state["enemies"][0]["id"]
                }
            )
            assert action_response.status_code == 200
        
        # Verify rewards
        assert state["status"] in ["victory", "defeat"]
        if state["status"] == "victory":
            assert "rewards" in state
```

---

## 9. Deployment

### 9.1 Docker Configuration

```dockerfile
# docker/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY migrations/ ./migrations/
COPY alembic.ini .

# Environment variables
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 9.2 Docker Compose

```yaml
# docker/docker-compose.yml

version: '3.8'

services:
  api:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/ngoa_long
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
      - redis
    volumes:
      - ../app:/app/app

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=ngoa_long
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "15672:15672"

volumes:
  postgres_data:
  redis_data:
```

---

## 10. Monitoring & Logging

### 10.1 Prometheus Metrics

```python
# utils/metrics.py

from prometheus_client import Counter, Histogram, Gauge

# Request metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

# Game metrics
ACTIVE_BATTLES = Gauge(
    'active_battles_total',
    'Number of active battles'
)

GACHA_PULLS = Counter(
    'gacha_pulls_total',
    'Total gacha pulls',
    ['banner_type', 'rarity']
)
```

### 10.2 Structured Logging

```python
# config/logging.py

import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }
        
        if hasattr(record, 'request_id'):
            log_obj['request_id'] = record.request_id
        
        if record.exc_info:
            log_obj['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_obj)
```

---

*Tài liệu này mô tả thiết kế Backend cho game Ngọa Long Tam Quốc. Xem thêm Frontend Design để biết cách tích hợp với giao diện người dùng.*
