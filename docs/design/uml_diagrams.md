# UML Diagrams - Ngọa Long Tam Quốc

## 1. Class Diagram - Core Domain

```mermaid
classDiagram
    %% Base Classes
    class BaseEntity {
        <<abstract>>
        +String id
        +DateTime createdAt
        +DateTime updatedAt
        +int version
        +equals(other) bool
        +validate() ValidationResult
    }

    %% Character Hierarchy
    class Character {
        <<abstract>>
        +String name
        +Element element
        +GridPosition position
        +HexagonStats stats
        +int currentHp
        +int currentMana
        +List~Skill~ skills
        +List~StatusEffect~ statusEffects
        +takeDamage(damage, element) DamageResult
        +heal(amount) HealResult
        +applyStatus(effect) void
        +canAct() bool
        +getEffectiveStats() HexagonStats
    }

    class Hero {
        +Rarity rarity
        +int ascensionLevel
        +int awakeningLevel
        +int exp
        +List~PassiveSkill~ passiveSkills
        +Mount mount
        +Dict bondLevels
        +gainExp(amount) LevelUpResult
        +ascend(materials) AscensionResult
        +awaken(materials) AwakeningResult
        +equip(equipment, slot) EquipResult
    }

    class Enemy {
        +AIBehavior aiBehavior
        +List~DropItem~ dropTable
        +int expReward
        +int goldReward
        +decideAction(battleState) Action
    }

    class Boss {
        +List~BossPhase~ phases
        +int currentPhase
        +List~BossMechanic~ specialMechanics
        +MythicalTier mythicalTier
        +checkPhaseTransition() BossPhase
        +executeMechanic(mechanic) MechanicResult
        +enrage() void
    }

    %% Value Objects
    class HexagonStats {
        <<ValueObject>>
        +int hp
        +int atk
        +int def
        +int spd
        +int crit
        +int dex
        +getTotalPower() int
        +add(other) HexagonStats
        +multiply(factor) HexagonStats
    }

    class GridPosition {
        <<ValueObject>>
        +int x
        +int y
        +distanceTo(other) int
        +isAdjacent(other) bool
        +getNeighbors() List~GridPosition~
    }

    class Element {
        <<Enumeration>>
        KIM
        MOC
        THUY
        HOA
        THO
        +getStrongAgainst() Element
        +getWeakAgainst() Element
        +calculateMultiplier(defender) float
    }

    %% Relationships
    BaseEntity <|-- Character
    Character <|-- Hero
    Character <|-- Enemy
    Enemy <|-- Boss
    Character --> HexagonStats
    Character --> GridPosition
    Character --> Element
    Hero --> Mount
```

## 2. Class Diagram - Skill System

```mermaid
classDiagram
    class Skill {
        <<abstract>>
        +String name
        +String description
        +Element element
        +int manaCost
        +int cooldown
        +int level
        +TargetType targetType
        +execute(caster, targets, state) SkillResult
        +canUse(caster, state) bool
        +getValidTargets(caster, state) List~Character~
        +upgrade(resources) UpgradeResult
    }

    class ActiveSkill {
        <<abstract>>
        +Animation animation
        +List~SkillEffect~ effects
    }

    class PassiveSkill {
        +PassiveTrigger trigger
        +PassiveEffect effect
        +onTrigger(event) void
    }

    class UltimateSkill {
        +int ultimateGauge
        +Animation ultimateAnimation
        +isReady() bool
        +consume() void
    }

    class DamageSkill {
        +float damageMultiplier
        +float elementScaling
        +bool canCrit
        +float armorPenetration
        +calculateDamage(caster, target) int
    }

    class HealSkill {
        +float healMultiplier
        +bool isPercentage
        +calculateHeal(caster, target) int
    }

    class BuffSkill {
        +StatBuff statBuff
        +int duration
        +applyBuff(target) void
    }

    class DebuffSkill {
        +Debuff debuff
        +int duration
        +float successRate
        +applyDebuff(target) bool
    }

    class TargetType {
        <<Enumeration>>
        SELF
        SINGLE_ALLY
        SINGLE_ENEMY
        ALL_ALLIES
        ALL_ENEMIES
        AOE
    }

    Skill <|-- ActiveSkill
    Skill <|-- PassiveSkill
    Skill <|-- UltimateSkill
    ActiveSkill <|-- DamageSkill
    ActiveSkill <|-- HealSkill
    ActiveSkill <|-- BuffSkill
    ActiveSkill <|-- DebuffSkill
    Skill --> TargetType
    Skill --> Element
```

## 3. Class Diagram - Equipment System

```mermaid
classDiagram
    class Equipment {
        +String name
        +EquipmentType type
        +Rarity rarity
        +int level
        +int maxLevel
        +HexagonStats baseStats
        +HexagonStats bonusStats
        +String setId
        +UniqueEffect uniqueEffect
        +enhance(materials) EnhanceResult
        +getTotalStats() HexagonStats
        +getSetBonus(equippedPieces) SetBonus
    }

    class Weapon {
        +WeaponType weaponType
        +Animation attackAnimation
        +Skill specialAttack
        +getAttackBonus() int
    }

    class Armor {
        +int defenseBonus
        +float damageReduction
    }

    class Accessory {
        +SpecialEffect specialEffect
    }

    class Relic {
        +RelicPower relicPower
        +int chargeLevel
        +activate() void
    }

    class EquipmentSet {
        +String setId
        +String name
        +List~String~ pieces
        +Dict setBonus
        +getActiveBonus(equippedCount) SetBonus
    }

    class EquipmentType {
        <<Enumeration>>
        WEAPON
        ARMOR
        ACCESSORY
        RELIC
    }

    class Rarity {
        <<Enumeration>>
        COMMON
        RARE
        EPIC
        LEGENDARY
        MYTHIC
    }

    Equipment <|-- Weapon
    Equipment <|-- Armor
    Equipment <|-- Accessory
    Equipment <|-- Relic
    Equipment --> EquipmentType
    Equipment --> Rarity
    Equipment --> HexagonStats
    Equipment "many" --> "1" EquipmentSet
```

## 4. Class Diagram - Battle System

```mermaid
classDiagram
    class BattleSystem {
        +BattleState battleState
        +TurnManager turnManager
        +ActionQueue actionQueue
        +BattleLog battleLog
        +EventBus eventBus
        +startBattle(playerTeam, enemyTeam, stage) Battle
        +processTurn() TurnResult
        +executeAction(action) ActionResult
        +checkBattleEnd() BattleResult
    }

    class BattleState {
        +int turnNumber
        +Character currentActor
        +TeamState playerTeam
        +TeamState enemyTeam
        +Grid grid
        +Weather weather
        +List~BattleEffect~ activeEffects
        +getCharacterById(id) Character
        +getCharactersInRange(center, range) List~Character~
        +clone() BattleState
    }

    class TurnManager {
        +List~Character~ turnOrder
        +Dict actionPoints
        +calculateTurnOrder(characters) List~Character~
        +getNextActor() Character
        +addExtraTurn(character) void
        +skipTurn(character) void
    }

    class Action {
        <<abstract>>
        +Character actor
        +List~Character~ targets
        +ActionType actionType
        +validate(battleState) ValidationResult
        +execute(battleState) ActionResult
        +getAnimation() Animation
    }

    class AttackAction {
        +Skill skill
        +bool isCounter
        +calculateDamage() DamageCalculation
        +applyElementModifier() float
    }

    class MoveAction {
        +GridPosition destination
        +calculatePath() List~GridPosition~
        +validateMovement() bool
    }

    class SkillAction {
        +Skill skill
        +List~Character~ targets
    }

    class Grid {
        +int size
        +Dict positions
        +getOccupant(position) Character
        +isOccupied(position) bool
        +getEmptyPositions() List~GridPosition~
    }

    BattleSystem --> BattleState
    BattleSystem --> TurnManager
    BattleSystem --> Action
    Action <|-- AttackAction
    Action <|-- MoveAction
    Action <|-- SkillAction
    BattleState --> Grid
    BattleState --> TeamState
```

## 5. Class Diagram - Mount System

```mermaid
classDiagram
    class Mount {
        +String name
        +MountType type
        +Rarity rarity
        +Element element
        +int level
        +int exp
        +int bondLevel
        +HexagonStats baseStats
        +TeamBuff teamBuff
        +MountSkill mountSkill
        +getRiderBonus(rider) HexagonStats
        +getTeamBonus() TeamBuff
        +increaseBond(points) BondResult
        +evolve(materials) EvolveResult
    }

    class Horse {
        +int speedBonus
        +HorseBreed breed
    }

    class Dragon {
        +int evolutionStage
        +DragonBreath dragonBreath
        +int awakeningLevel
        +evolveStage(materials) EvolutionResult
        +useBreathAttack(targets) AttackResult
    }

    class MythicalBeast {
        +MythicalPower power
        +bool isAwakened
        +awakening() void
    }

    class MountType {
        <<Enumeration>>
        HORSE
        DRAGON
        MYTHICAL
    }

    class DragonBreath {
        +Element element
        +int damage
        +BreathEffect effect
    }

    Mount <|-- Horse
    Mount <|-- Dragon
    Mount <|-- MythicalBeast
    Mount --> MountType
    Mount --> Element
    Dragon --> DragonBreath
```

## 6. Sequence Diagram - Battle Turn

```mermaid
sequenceDiagram
    participant Player
    participant BattleSystem
    participant TurnManager
    participant Character
    participant SkillSystem
    participant DamageCalculator
    participant UI

    Player->>BattleSystem: selectAction(skillId, targets)
    BattleSystem->>TurnManager: getCurrentActor()
    TurnManager-->>BattleSystem: Character
    
    BattleSystem->>Character: canUseSkill(skillId)
    Character-->>BattleSystem: true
    
    BattleSystem->>SkillSystem: executeSkill(skill, caster, targets)
    SkillSystem->>DamageCalculator: calculateDamage(skill, caster, target)
    
    Note over DamageCalculator: Apply formulas:<br/>damage = (ATK * multiplier - DEF * 0.5)<br/>* element_modifier * (1 + CRIT/100)
    
    DamageCalculator-->>SkillSystem: damageResult
    SkillSystem->>Character: applyDamage(damage)
    Character-->>SkillSystem: DamageResult
    
    SkillSystem->>Character: applyEffects(effects)
    SkillSystem-->>BattleSystem: SkillResult
    
    BattleSystem->>UI: displayDamage(damageResult)
    BattleSystem->>UI: playAnimation(skill.animation)
    
    BattleSystem->>TurnManager: endTurn()
    TurnManager->>TurnManager: calculateNextActor()
    TurnManager-->>BattleSystem: nextActor
    
    BattleSystem->>BattleSystem: checkBattleEnd()
    BattleSystem-->>Player: TurnResult
```

## 7. Sequence Diagram - Gacha Pull

```mermaid
sequenceDiagram
    participant Player
    participant GachaService
    participant BannerSystem
    participant PityCounter
    participant HeroFactory
    participant Inventory
    participant UI

    Player->>GachaService: pull(bannerId, pullCount)
    GachaService->>BannerSystem: getBanner(bannerId)
    BannerSystem-->>GachaService: Banner
    
    loop For each pull
        GachaService->>PityCounter: getCurrentPity(bannerId)
        PityCounter-->>GachaService: pityCount
        
        GachaService->>GachaService: calculateRarity(banner, pityCount)
        
        alt 5-star pull
            GachaService->>PityCounter: resetPity(bannerId)
        else Other
            GachaService->>PityCounter: incrementPity(bannerId)
        end
        
        GachaService->>BannerSystem: getRandomHero(rarity)
        BannerSystem-->>GachaService: heroTemplate
        
        GachaService->>HeroFactory: create(heroTemplate)
        HeroFactory-->>GachaService: Hero
    end
    
    GachaService->>Inventory: addHeroes(heroes)
    Inventory-->>GachaService: success
    
    GachaService-->>UI: GachaResult
    UI->>UI: playGachaAnimation(results)
    UI-->>Player: displayResults
```

## 8. State Diagram - Boss Phases

```mermaid
stateDiagram-v2
    [*] --> Phase1_Normal: Battle Start
    
    Phase1_Normal: Phase 1 - Normal
    Phase1_Normal: HP: 100% - 70%
    Phase1_Normal: Basic attacks
    
    Phase2_Enhanced: Phase 2 - Enhanced
    Phase2_Enhanced: HP: 70% - 40%
    Phase2_Enhanced: +20% ATK
    Phase2_Enhanced: New skills unlocked
    
    Phase3_Desperate: Phase 3 - Desperate
    Phase3_Desperate: HP: 40% - 10%
    Phase3_Desperate: Special mechanics active
    Phase3_Desperate: AOE attacks
    
    Phase4_Enraged: Phase 4 - Enraged
    Phase4_Enraged: HP: 10% - 0%
    Phase4_Enraged: +100% damage
    Phase4_Enraged: Disabled healing
    
    Phase1_Normal --> Phase2_Enhanced: HP <= 70%
    Phase2_Enhanced --> Phase3_Desperate: HP <= 40%
    Phase3_Desperate --> Phase4_Enraged: HP <= 10%
    Phase4_Enraged --> [*]: HP = 0 (Victory)
    
    Phase1_Normal --> [*]: Player Team Wiped
    Phase2_Enhanced --> [*]: Player Team Wiped
    Phase3_Desperate --> [*]: Player Team Wiped
    Phase4_Enraged --> [*]: Player Team Wiped
```

## 9. State Diagram - Character States

```mermaid
stateDiagram-v2
    [*] --> Idle: Battle Start
    
    Idle --> Acting: Turn Start
    Acting --> Idle: Action Complete
    
    Idle --> Stunned: Stun Applied
    Stunned --> Idle: Stun Expired
    
    Idle --> Frozen: Freeze Applied
    Frozen --> Idle: Freeze Expired
    
    Idle --> Silenced: Silence Applied
    Silenced --> Idle: Silence Expired
    Silenced --> Acting: Turn Start (Basic Attack Only)
    
    Acting --> Transformed: Use Transform Skill
    Transformed --> Acting: Transform Expired
    
    Idle --> Dead: HP = 0
    Dead --> Revived: Revive Effect
    Revived --> Idle: Revive Complete
    
    Dead --> [*]: No Revive Available
```

## 10. Component Diagram - System Architecture

```mermaid
graph TB
    subgraph "Presentation Layer"
        UI[Game UI]
        BattleUI[Battle UI]
        MenuUI[Menu UI]
        GachaUI[Gacha UI]
    end
    
    subgraph "Application Layer"
        BS[BattleService]
        CS[CharacterService]
        GS[GachaService]
        PS[ProgressionService]
        TS[TeamService]
        SS[StoryService]
    end
    
    subgraph "Domain Layer"
        Character[Character Domain]
        Skill[Skill Domain]
        Equipment[Equipment Domain]
        Battle[Battle Domain]
        Story[Story Domain]
    end
    
    subgraph "Infrastructure Layer"
        DB[(Database)]
        Cache[(Cache)]
        EventBus[Event Bus]
        FileSystem[File System]
    end
    
    UI --> BS
    UI --> CS
    UI --> GS
    BattleUI --> BS
    MenuUI --> TS
    MenuUI --> PS
    GachaUI --> GS
    
    BS --> Battle
    BS --> Character
    CS --> Character
    CS --> Equipment
    GS --> Character
    PS --> Character
    TS --> Character
    SS --> Story
    
    Battle --> DB
    Character --> DB
    Equipment --> DB
    Story --> DB
    
    BS --> EventBus
    CS --> Cache
```

## 11. ER Diagram - Database Relationships

```mermaid
erDiagram
    PLAYER ||--o{ HERO : owns
    PLAYER ||--o{ EQUIPMENT : owns
    PLAYER ||--o{ MOUNT : owns
    PLAYER ||--|| PROGRESS : has
    
    HERO ||--o{ HERO_SKILL : has
    HERO ||--o{ HERO_EQUIPMENT : equips
    HERO }o--|| MOUNT : rides
    HERO }o--o{ HERO_BOND : "bonds with"
    
    SKILL ||--o{ HERO_SKILL : "learned by"
    SKILL ||--o{ SKILL_ENHANCEMENT : has
    
    EQUIPMENT ||--o{ HERO_EQUIPMENT : "equipped by"
    EQUIPMENT }o--|| EQUIPMENT_SET : "belongs to"
    
    CHAPTER ||--o{ STAGE : contains
    STAGE ||--o{ ENEMY_SPAWN : has
    
    BOSS ||--o{ BOSS_PHASE : has
    BOSS ||--o{ BOSS_MECHANIC : has
    
    PLAYER {
        string id PK
        string username
        int level
        int gold
        int gems
        datetime created_at
    }
    
    HERO {
        string id PK
        string player_id FK
        string template_id
        int level
        int exp
        int stars
        int ascension
        int awakening
    }
    
    EQUIPMENT {
        string id PK
        string player_id FK
        string template_id
        int level
        int rarity
        json bonus_stats
    }
    
    SKILL {
        string id PK
        string name
        string type
        int mana_cost
        int cooldown
        json effects
    }
    
    CHAPTER {
        string id PK
        int number
        string title
        bool is_mythical
    }
    
    BOSS {
        string id PK
        string name
        string element
        int hp
        string mythical_tier
    }
```

## 12. Activity Diagram - Story Progression

```mermaid
flowchart TD
    Start([Start Game]) --> Tutorial[Complete Tutorial]
    Tutorial --> Chapter1[Chapter 1: Khởi Nguồn]
    
    Chapter1 --> |Clear all stages| Boss1{Defeat Trương Giác}
    Boss1 --> |Victory| Unlock1[Unlock: Lưu Bị, Quan Vũ, Trương Phi]
    Boss1 --> |Defeat| Retry1[Retry or Level Up]
    Retry1 --> Boss1
    
    Unlock1 --> Chapter2[Chapter 2: Quần Hùng Tụ Nghĩa]
    Chapter2 --> |Clear all stages| Boss2{Defeat Lã Bố}
    Boss2 --> |Victory| Unlock2[Unlock: Tào Tháo, Tôn Kiên + Xích Thố]
    Boss2 --> |Defeat| Retry2[Retry or Level Up]
    Retry2 --> Boss2
    
    Unlock2 --> Chapter3[Chapter 3: Tam Phân Thiên Hạ]
    Chapter3 --> Boss3{Defeat Hạ Hầu Đôn}
    Boss3 --> |Victory| Unlock3[Unlock: Gia Cát Lượng, Triệu Vân]
    
    Unlock3 --> Chapter4[Chapter 4: Xích Bích Đại Chiến]
    Chapter4 --> Boss4{Defeat Tào Tháo}
    Boss4 --> |Victory| Unlock4[Unlock: Chu Du, Hoàng Cái, Lục Tốn]
    
    Unlock4 --> Chapter5[Chapter 5: Bắc Phạt Trung Nguyên]
    Chapter5 --> Boss5{Defeat Tư Mã Ý}
    Boss5 --> |Victory| Unlock5[Unlock: Khương Duy, Mã Siêu, Hoàng Trung]
    
    Unlock5 --> Chapter6[Chapter 6: Loạn Thế Chung Cục]
    Chapter6 --> Boss6{Defeat Tư Mã Viêm}
    Boss6 --> |Victory| SecretPath[Secret Path Unlocked]
    
    SecretPath --> |Level 80+, 5x 5★ Heroes| MythicalChapter[Chapter 7: Thiên Giới Đại Chiến]
    
    MythicalChapter --> TuLinh[Stage 1: Tứ Linh Thần Thú]
    TuLinh --> |Defeat all 4| ThienVuong[Stage 2: Tứ Đại Thiên Vương]
    ThienVuong --> |Defeat all 4| ThuongCo[Stage 3: Thượng Cổ Thần Ma]
    ThuongCo --> |Defeat all 3| FinalBoss{Final Boss: Hỗn Độn}
    
    FinalBoss --> |Victory| Ending([Game Complete: Thiên Hạ Vô Song])
    FinalBoss --> |Defeat| RetryFinal[Retry with better team]
    RetryFinal --> FinalBoss
```

---

## Diagram Legend

| Symbol | Meaning |
|--------|---------|
| `<<abstract>>` | Abstract class |
| `<<Enumeration>>` | Enum type |
| `<<ValueObject>>` | Immutable value object |
| `+` | Public |
| `-` | Private |
| `#` | Protected |
| `-->` | Association |
| `<\|--` | Inheritance |
| `*-->` | Composition |
| `o-->` | Aggregation |

---

*Các diagram này được viết bằng Mermaid syntax và có thể render trực tiếp trong GitHub, GitLab, hoặc các công cụ hỗ trợ Mermaid.*
