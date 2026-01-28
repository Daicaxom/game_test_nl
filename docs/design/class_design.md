# Class Design Document - Ngọa Long Tam Quốc

## Tổng Quan Thiết Kế

Tài liệu này mô tả thiết kế class cho game "Ngọa Long Tam Quốc" theo tiêu chuẩn Solution Architecture top 0.1%. Thiết kế tuân theo các nguyên tắc SOLID, Clean Architecture và Domain-Driven Design.

---

## 1. Core Domain Classes

### 1.1 Entity Classes

```
┌─────────────────────────────────────────────────────────────┐
│                    ENTITY LAYER                             │
├─────────────────────────────────────────────────────────────┤
│  BaseEntity                                                 │
│  ├── Character                                              │
│  │   ├── Hero                                               │
│  │   ├── Enemy                                              │
│  │   └── Boss                                               │
│  ├── Equipment                                              │
│  │   ├── Weapon                                             │
│  │   ├── Armor                                              │
│  │   ├── Accessory                                          │
│  │   └── Relic                                              │
│  ├── Skill                                                  │
│  │   ├── ActiveSkill                                        │
│  │   ├── PassiveSkill                                       │
│  │   └── UltimateSkill                                      │
│  ├── Mount                                                  │
│  │   ├── Horse                                              │
│  │   ├── Dragon                                             │
│  │   └── MythicalBeast                                      │
│  └── Item                                                   │
│      ├── Consumable                                         │
│      ├── Material                                           │
│      └── QuestItem                                          │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 BaseEntity

```python
class BaseEntity:
    """Base class cho tất cả entities"""
    
    Attributes:
        id: str                 # UUID unique identifier
        created_at: datetime    # Timestamp tạo
        updated_at: datetime    # Timestamp cập nhật
        version: int           # Optimistic locking version
    
    Methods:
        + equals(other: BaseEntity) -> bool
        + hash() -> int
        + validate() -> ValidationResult
```

### 1.3 Character Class Hierarchy

```python
class Character(BaseEntity):
    """Abstract base class cho nhân vật"""
    
    Attributes:
        name: str
        element: Element           # Enum: KIM, MOC, THUY, HOA, THO
        position: GridPosition     # (x, y) trong grid 3x3
        stats: HexagonStats
        current_hp: int
        current_mana: int
        level: int
        skills: List[Skill]
        status_effects: List[StatusEffect]
        equipment_slots: Dict[SlotType, Equipment]
    
    Methods:
        + take_damage(damage: int, element: Element) -> DamageResult
        + heal(amount: int) -> HealResult
        + apply_status(effect: StatusEffect) -> None
        + remove_status(effect_type: StatusType) -> None
        + can_act() -> bool
        + get_effective_stats() -> HexagonStats
        + move_to(position: GridPosition) -> MoveResult


class Hero(Character):
    """Player-controlled character"""
    
    Additional Attributes:
        rarity: Rarity             # 1-6 stars
        ascension_level: int       # 0-6
        awakening_level: int       # 0-6
        exp: int
        passive_skills: List[PassiveSkill]
        mount: Optional[Mount]
        bond_levels: Dict[str, int]  # hero_id -> bond level
        growth_rates: Dict[str, float]
    
    Additional Methods:
        + gain_exp(amount: int) -> LevelUpResult
        + ascend(materials: List[Material]) -> AscensionResult
        + awaken(materials: List[Material]) -> AwakeningResult
        + equip(equipment: Equipment, slot: SlotType) -> EquipResult
        + learn_skill(skill: Skill) -> LearnResult


class Enemy(Character):
    """AI-controlled enemy"""
    
    Additional Attributes:
        ai_behavior: AIBehavior
        drop_table: List[DropItem]
        exp_reward: int
        gold_reward: int
    
    Additional Methods:
        + decide_action(battle_state: BattleState) -> Action


class Boss(Enemy):
    """Special enemy with phases and mechanics"""
    
    Additional Attributes:
        phases: List[BossPhase]
        current_phase: int
        special_mechanics: List[BossMechanic]
        enrage_timer: int
        mythical_tier: MythicalTier  # For Chapter 7 bosses
    
    Additional Methods:
        + check_phase_transition() -> Optional[BossPhase]
        + execute_mechanic(mechanic: BossMechanic) -> MechanicResult
        + enrage() -> None
```

---

## 2. Value Objects

### 2.1 HexagonStats

```python
class HexagonStats(ValueObject):
    """Immutable stats object dạng lục giác"""
    
    Attributes:
        hp: int          # Hit Points
        atk: int         # Attack
        def_: int        # Defense  
        spd: int         # Speed
        crit: int        # Critical Rate (%)
        dex: int         # Dexterity
    
    Methods:
        + get_total_power() -> int
        + add(other: HexagonStats) -> HexagonStats
        + multiply(factor: float) -> HexagonStats
        + apply_buff(buff: StatBuff) -> HexagonStats
        + to_dict() -> Dict[str, int]
        
    Factory Methods:
        + from_dict(data: Dict) -> HexagonStats
        + default() -> HexagonStats
```

### 2.2 GridPosition

```python
class GridPosition(ValueObject):
    """Vị trí trên bàn cờ 3x3"""
    
    Attributes:
        x: int  # 0-2
        y: int  # 0-2
    
    Methods:
        + distance_to(other: GridPosition) -> int
        + is_adjacent(other: GridPosition) -> bool
        + get_neighbors() -> List[GridPosition]
        + is_valid() -> bool
    
    Constants:
        GRID_SIZE = 3
        ALL_POSITIONS = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]
```

### 2.3 Element

```python
class Element(Enum):
    """Ngũ Hành enum với quan hệ tương sinh tương khắc"""
    
    KIM = "Kim"    # Metal - Strong vs Mộc, Weak vs Hỏa
    MOC = "Mộc"    # Wood - Strong vs Thổ, Weak vs Kim
    THUY = "Thủy"  # Water - Strong vs Hỏa, Weak vs Thổ
    HOA = "Hỏa"    # Fire - Strong vs Kim, Weak vs Thủy
    THO = "Thổ"    # Earth - Strong vs Thủy, Weak vs Mộc
    
    Methods:
        + get_strong_against() -> Element
        + get_weak_against() -> Element
        + calculate_multiplier(defender: Element) -> float
        + get_color() -> str
```

---

## 3. Skill System Classes

### 3.1 Skill Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                    SKILL SYSTEM                             │
├─────────────────────────────────────────────────────────────┤
│  Skill (Abstract)                                           │
│  ├── ActiveSkill                                            │
│  │   ├── DamageSkill                                        │
│  │   │   ├── SingleTargetDamage                             │
│  │   │   └── AOEDamage                                      │
│  │   ├── HealSkill                                          │
│  │   │   ├── SingleHeal                                     │
│  │   │   └── GroupHeal                                      │
│  │   ├── BuffSkill                                          │
│  │   └── DebuffSkill                                        │
│  ├── PassiveSkill                                           │
│  │   ├── StatPassive                                        │
│  │   ├── TriggerPassive                                     │
│  │   └── AuraPassive                                        │
│  └── UltimateSkill                                          │
│      ├── TransformationUltimate                             │
│      └── ComboUltimate                                      │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Skill Base Class

```python
class Skill(BaseEntity):
    """Abstract base class cho skills"""
    
    Attributes:
        name: str
        description: str
        element: Optional[Element]
        mana_cost: int
        cooldown: int
        current_cooldown: int
        level: int
        max_level: int
        target_type: TargetType  # SELF, SINGLE_ALLY, SINGLE_ENEMY, ALL_ALLIES, ALL_ENEMIES, AOE
        range: int
        enhancements: List[SkillEnhancement]
    
    Abstract Methods:
        + execute(caster: Character, targets: List[Character], battle_state: BattleState) -> SkillResult
        + can_use(caster: Character, battle_state: BattleState) -> bool
        + get_valid_targets(caster: Character, battle_state: BattleState) -> List[Character]
    
    Methods:
        + upgrade(resources: Resources) -> UpgradeResult
        + reduce_cooldown(amount: int) -> None
        + reset_cooldown() -> None


class DamageSkill(ActiveSkill):
    """Skill gây sát thương"""
    
    Additional Attributes:
        damage_multiplier: float
        element_scaling: float
        can_crit: bool
        armor_penetration: float
        additional_effects: List[SkillEffect]
    
    Methods:
        + calculate_damage(caster: Character, target: Character) -> int
        + apply_effects(target: Character) -> List[EffectResult]
```

---

## 4. Battle System Classes

### 4.1 Battle Core

```python
class BattleSystem:
    """Core battle management"""
    
    Attributes:
        battle_state: BattleState
        turn_manager: TurnManager
        action_queue: ActionQueue
        battle_log: BattleLog
        event_bus: EventBus
    
    Methods:
        + start_battle(player_team: Team, enemy_team: Team, stage: Stage) -> Battle
        + process_turn() -> TurnResult
        + execute_action(action: Action) -> ActionResult
        + check_battle_end() -> Optional[BattleResult]
        + end_battle() -> BattleReward


class BattleState:
    """Immutable battle state snapshot"""
    
    Attributes:
        turn_number: int
        current_actor: Character
        player_team: TeamState
        enemy_team: TeamState
        grid: Grid
        weather: Weather
        active_effects: List[BattleEffect]
    
    Methods:
        + get_character_by_id(id: str) -> Optional[Character]
        + get_characters_in_range(center: GridPosition, range: int) -> List[Character]
        + clone() -> BattleState


class TurnManager:
    """Quản lý thứ tự turn dựa trên SPD"""
    
    Attributes:
        turn_order: List[Character]
        action_points: Dict[str, int]
    
    Methods:
        + calculate_turn_order(characters: List[Character]) -> List[Character]
        + get_next_actor() -> Character
        + add_extra_turn(character: Character) -> None
        + skip_turn(character: Character) -> None
```

### 4.2 Action Classes

```python
class Action(ABC):
    """Abstract base for all battle actions"""
    
    Attributes:
        actor: Character
        targets: List[Character]
        action_type: ActionType
    
    Abstract Methods:
        + validate(battle_state: BattleState) -> ValidationResult
        + execute(battle_state: BattleState) -> ActionResult
        + get_animation() -> Animation


class AttackAction(Action):
    """Basic attack action"""
    
    Additional Attributes:
        skill: Optional[Skill]
        is_counter: bool
    
    Methods:
        + calculate_damage() -> DamageCalculation
        + apply_element_modifier() -> float


class MoveAction(Action):
    """Grid movement action"""
    
    Additional Attributes:
        destination: GridPosition
    
    Methods:
        + calculate_path() -> List[GridPosition]
        + validate_movement() -> bool
```

---

## 5. Equipment System Classes

### 5.1 Equipment Hierarchy

```python
class Equipment(BaseEntity):
    """Base equipment class"""
    
    Attributes:
        name: str
        type: EquipmentType     # WEAPON, ARMOR, ACCESSORY, RELIC
        rarity: Rarity
        level: int
        max_level: int
        base_stats: HexagonStats
        bonus_stats: HexagonStats
        set_id: Optional[str]
        unique_effect: Optional[UniqueEffect]
        required_level: int
        required_element: Optional[Element]
    
    Methods:
        + enhance(materials: List[Material]) -> EnhanceResult
        + get_total_stats() -> HexagonStats
        + get_set_bonus(equipped_pieces: int) -> SetBonus


class Weapon(Equipment):
    """Vũ khí"""
    
    Additional Attributes:
        weapon_type: WeaponType  # SWORD, SPEAR, BOW, STAFF, etc.
        attack_animation: Animation
        special_attack: Optional[Skill]
    
    Methods:
        + get_attack_bonus() -> int


class EquipmentSet:
    """Equipment set với set bonuses"""
    
    Attributes:
        set_id: str
        name: str
        pieces: List[str]  # equipment_ids
        set_bonuses: Dict[int, SetBonus]  # piece_count -> bonus
    
    Methods:
        + get_active_bonus(equipped_count: int) -> SetBonus
```

---

## 6. Progression System Classes

### 6.1 Character Progression

```python
class CharacterProgression:
    """Quản lý progression của hero"""
    
    Attributes:
        hero: Hero
        exp_table: Dict[int, int]  # level -> required_exp
        ascension_requirements: Dict[int, AscensionRequirement]
        awakening_requirements: Dict[int, AwakeningRequirement]
    
    Methods:
        + calculate_required_exp(target_level: int) -> int
        + can_ascend() -> bool
        + can_awaken() -> bool
        + get_unlocked_passives() -> List[PassiveSkill]


class StarSystem:
    """Hệ thống sao"""
    
    Attributes:
        current_stars: int  # 1-6
        duplicates_required: Dict[int, int]  # star_level -> duplicates_needed
    
    Methods:
        + upgrade_star(duplicates: List[Hero]) -> StarUpgradeResult
        + get_stat_multiplier() -> float
        + get_skill_slots() -> int
```

---

## 7. Mount System Classes

```python
class Mount(BaseEntity):
    """Base mount class"""
    
    Attributes:
        name: str
        type: MountType       # HORSE, DRAGON, MYTHICAL
        rarity: Rarity
        element: Optional[Element]
        level: int
        exp: int
        bond_level: int       # 1-10
        base_stats: HexagonStats
        team_buff: TeamBuff
        mount_skill: Optional[MountSkill]
        equipment_slots: List[MountEquipmentSlot]
    
    Methods:
        + get_rider_bonus(rider: Hero) -> HexagonStats
        + get_team_bonus() -> TeamBuff
        + increase_bond(points: int) -> BondResult
        + evolve(materials: List[Material]) -> EvolveResult


class Dragon(Mount):
    """Special dragon mount với evolution system"""
    
    Additional Attributes:
        evolution_stage: int
        dragon_breath: DragonBreath
        awakening_level: int
    
    Methods:
        + evolve_stage(materials: List[Material]) -> EvolutionResult
        + use_breath_attack(targets: List[Character]) -> AttackResult
```

---

## 8. Team & Formation Classes

```python
class Team:
    """Team configuration"""
    
    Attributes:
        id: str
        name: str
        members: List[Hero]     # Max 5
        formation: Formation
        active_synergies: List[Synergy]
    
    Methods:
        + add_member(hero: Hero, position: GridPosition) -> AddResult
        + remove_member(hero_id: str) -> RemoveResult
        + set_formation(formation: Formation) -> None
        + calculate_synergies() -> List[Synergy]
        + get_total_power() -> int
        + validate() -> ValidationResult


class Formation:
    """Battle formation với position bonuses"""
    
    Attributes:
        name: str
        positions: Dict[int, GridPosition]  # member_index -> position
        requirements: FormationRequirement
        position_bonuses: Dict[GridPosition, PositionBonus]
        formation_effect: FormationEffect
    
    Methods:
        + get_position_bonus(position: GridPosition, character: Character) -> HexagonStats
        + check_requirements(team: Team) -> bool
        + activate(team: Team) -> FormationActivation


class Synergy:
    """Team synergy bonuses"""
    
    Attributes:
        synergy_id: str
        name: str
        required_heroes: List[str]  # hero_ids
        tier_effects: Dict[int, SynergyEffect]  # hero_count -> effect
    
    Methods:
        + get_active_tier(present_heroes: List[Hero]) -> int
        + get_effect(tier: int) -> SynergyEffect
```

---

## 9. Story & Campaign Classes

```python
class Chapter:
    """Story chapter"""
    
    Attributes:
        chapter_id: str
        number: int
        title: str
        description: str
        stages: List[Stage]
        boss_stage: BossStage
        unlock_requirements: UnlockRequirement
        rewards: ChapterReward
        is_mythical: bool  # Chapter 7 flag
    
    Methods:
        + get_progress(player_progress: PlayerProgress) -> ChapterProgress
        + is_unlocked(player: Player) -> bool
        + get_boss() -> Boss


class Stage:
    """Individual battle stage"""
    
    Attributes:
        stage_id: str
        name: str
        enemies: List[EnemySpawn]
        waves: int
        difficulty: Difficulty
        recommended_power: int
        stamina_cost: int
        first_clear_rewards: List[Reward]
        repeat_rewards: List[Reward]
        star_conditions: List[StarCondition]
    
    Methods:
        + create_battle(player_team: Team) -> Battle
        + calculate_rewards(stars: int, is_first_clear: bool) -> List[Reward]


class BossStage(Stage):
    """Boss battle stage với special mechanics"""
    
    Additional Attributes:
        boss: Boss
        phases: List[BossPhase]
        special_rules: List[BattleRule]
        mythical_tier: Optional[MythicalTier]  # For Chapter 7
    
    Methods:
        + get_phase_conditions() -> List[PhaseCondition]
        + apply_special_rules(battle: Battle) -> None
```

---

## 10. Design Patterns Used

### 10.1 Patterns Summary

| Pattern | Usage | Location |
|---------|-------|----------|
| **Factory** | Character, Skill, Equipment creation | `*Factory` classes |
| **Strategy** | AI behaviors, Damage calculation | `AIBehavior`, `DamageCalculator` |
| **Observer** | Battle events, UI updates | `EventBus`, `BattleObserver` |
| **State** | Boss phases, Character states | `BossPhase`, `CharacterState` |
| **Command** | Battle actions | `Action` classes |
| **Composite** | Skill effects, Buff stacking | `CompositeEffect` |
| **Builder** | Complex object construction | `CharacterBuilder`, `TeamBuilder` |
| **Repository** | Data access | `*Repository` classes |
| **Specification** | Validation rules | `*Specification` classes |

### 10.2 Example: Factory Pattern

```python
class HeroFactory:
    """Factory cho tạo heroes"""
    
    @staticmethod
    def create(hero_id: str, template: HeroTemplate) -> Hero:
        """Create hero từ template"""
        hero = Hero(
            id=generate_uuid(),
            name=template.name,
            element=template.element,
            rarity=template.base_rarity,
            stats=HexagonStats.from_dict(template.base_stats),
            growth_rates=template.growth_rates
        )
        
        # Add default skills
        for skill_id in template.default_skills:
            skill = SkillFactory.create(skill_id)
            hero.skills.append(skill)
        
        return hero
    
    @staticmethod  
    def create_from_gacha(banner: Banner) -> Hero:
        """Create hero từ gacha pull"""
        # Gacha logic...
        pass
```

---

## 11. Interface Definitions

```python
# Core interfaces

class ICharacter(ABC):
    @abstractmethod
    def take_damage(self, damage: int, element: Element) -> DamageResult: pass
    
    @abstractmethod
    def heal(self, amount: int) -> HealResult: pass
    
    @abstractmethod
    def can_act(self) -> bool: pass


class ISkill(ABC):
    @abstractmethod
    def execute(self, caster: ICharacter, targets: List[ICharacter]) -> SkillResult: pass
    
    @abstractmethod
    def can_use(self, caster: ICharacter) -> bool: pass


class IBattleObserver(ABC):
    @abstractmethod
    def on_turn_start(self, character: ICharacter) -> None: pass
    
    @abstractmethod
    def on_damage_dealt(self, source: ICharacter, target: ICharacter, damage: int) -> None: pass
    
    @abstractmethod
    def on_character_death(self, character: ICharacter) -> None: pass
    
    @abstractmethod
    def on_battle_end(self, result: BattleResult) -> None: pass


class IRepository(ABC, Generic[T]):
    @abstractmethod
    def get_by_id(self, id: str) -> Optional[T]: pass
    
    @abstractmethod
    def get_all(self) -> List[T]: pass
    
    @abstractmethod
    def save(self, entity: T) -> T: pass
    
    @abstractmethod
    def delete(self, id: str) -> bool: pass
```

---

## 12. Dependency Graph

```
┌──────────────────────────────────────────────────────────────────┐
│                     DEPENDENCY LAYERS                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                    PRESENTATION LAYER                      │  │
│  │  BattleUI  |  CharacterUI  |  MenuUI  |  StoryUI          │  │
│  └─────────────────────────┬──────────────────────────────────┘  │
│                            │                                     │
│                            ▼                                     │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                   APPLICATION LAYER                        │  │
│  │  BattleService | CharacterService | GachaService |         │  │
│  │  ProgressionService | TeamService | StoryService           │  │
│  └─────────────────────────┬──────────────────────────────────┘  │
│                            │                                     │
│                            ▼                                     │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                     DOMAIN LAYER                           │  │
│  │  Character | Skill | Equipment | Mount | Battle | Team     │  │
│  │  Formation | Chapter | Stage | Synergy | Element           │  │
│  └─────────────────────────┬──────────────────────────────────┘  │
│                            │                                     │
│                            ▼                                     │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                 INFRASTRUCTURE LAYER                       │  │
│  │  Database | FileSystem | Network | Cache | EventBus        │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

*Tài liệu này là phần thiết kế class cơ bản. Xem thêm các diagram chi tiết trong các file tiếp theo.*
