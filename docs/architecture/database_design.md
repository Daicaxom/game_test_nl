# Database Design - Ngọa Long Tam Quốc

## 1. Tổng Quan

Thiết kế database cho game "Ngọa Long Tam Quốc" sử dụng hybrid approach:
- **PostgreSQL** cho dữ liệu quan hệ (players, characters, equipment)
- **Redis** cho cache và real-time data
- **MongoDB** cho game logs và analytics (optional)

---

## 2. Database Schema

### 2.1 ERD Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DATABASE SCHEMA                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                     │
│  │   players   │───<│   heroes    │───<│hero_skills  │                     │
│  └─────────────┘    └─────────────┘    └─────────────┘                     │
│        │                  │                                                 │
│        │                  │            ┌─────────────┐                     │
│        │                  └───────────<│hero_equips  │                     │
│        │                               └─────────────┘                     │
│        │                                      │                            │
│        │            ┌─────────────┐           │                            │
│        └───────────<│  equipment  │───────────┘                            │
│        │            └─────────────┘                                        │
│        │                  │                                                │
│        │            ┌─────────────┐                                        │
│        │            │equip_sets   │                                        │
│        │            └─────────────┘                                        │
│        │                                                                   │
│        │            ┌─────────────┐    ┌─────────────┐                     │
│        └───────────<│   mounts    │───<│mount_skills │                     │
│        │            └─────────────┘    └─────────────┘                     │
│        │                                                                   │
│        │            ┌─────────────┐    ┌─────────────┐                     │
│        └───────────<│  progress   │───<│stage_clears │                     │
│        │            └─────────────┘    └─────────────┘                     │
│        │                                                                   │
│        │            ┌─────────────┐                                        │
│        └───────────<│  inventory  │                                        │
│                     └─────────────┘                                        │
│                                                                            │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                     │
│  │  chapters   │───<│   stages    │───<│enemy_spawns │                     │
│  └─────────────┘    └─────────────┘    └─────────────┘                     │
│        │                                                                   │
│        │            ┌─────────────┐    ┌─────────────┐                     │
│        └───────────<│   bosses    │───<│boss_phases  │                     │
│                     └─────────────┘    └─────────────┘                     │
│                                                                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Table Definitions

### 3.1 Core Tables

#### players
```sql
CREATE TABLE players (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username        VARCHAR(50) UNIQUE NOT NULL,
    email           VARCHAR(255) UNIQUE NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    display_name    VARCHAR(100),
    level           INT DEFAULT 1,
    exp             BIGINT DEFAULT 0,
    gold            BIGINT DEFAULT 0,
    gems            INT DEFAULT 0,
    stamina         INT DEFAULT 100,
    max_stamina     INT DEFAULT 100,
    stamina_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    vip_level       INT DEFAULT 0,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login      TIMESTAMP,
    is_active       BOOLEAN DEFAULT true,
    
    CONSTRAINT chk_level CHECK (level >= 1 AND level <= 100),
    CONSTRAINT chk_gold CHECK (gold >= 0),
    CONSTRAINT chk_gems CHECK (gems >= 0)
);

CREATE INDEX idx_players_username ON players(username);
CREATE INDEX idx_players_email ON players(email);
CREATE INDEX idx_players_level ON players(level);
```

#### hero_templates (Static Data)
```sql
CREATE TABLE hero_templates (
    id              VARCHAR(50) PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    title           VARCHAR(200),
    element         VARCHAR(10) NOT NULL,
    base_rarity     INT NOT NULL,
    hero_class      VARCHAR(50) NOT NULL,
    -- Base stats at level 1
    base_hp         INT NOT NULL,
    base_atk        INT NOT NULL,
    base_def        INT NOT NULL,
    base_spd        INT NOT NULL,
    base_crit       INT NOT NULL,
    base_dex        INT NOT NULL,
    -- Growth rates per level
    growth_hp       DECIMAL(5,2) NOT NULL,
    growth_atk      DECIMAL(5,2) NOT NULL,
    growth_def      DECIMAL(5,2) NOT NULL,
    growth_spd      DECIMAL(5,2) NOT NULL,
    growth_crit     DECIMAL(5,2) NOT NULL,
    growth_dex      DECIMAL(5,2) NOT NULL,
    -- Metadata
    description     TEXT,
    lore            TEXT,
    icon_url        VARCHAR(500),
    model_url       VARCHAR(500),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_element CHECK (element IN ('KIM', 'MOC', 'THUY', 'HOA', 'THO')),
    CONSTRAINT chk_rarity CHECK (base_rarity BETWEEN 1 AND 6)
);
```

#### heroes (Player's Heroes)
```sql
CREATE TABLE heroes (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id       UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    template_id     VARCHAR(50) NOT NULL REFERENCES hero_templates(id),
    level           INT DEFAULT 1,
    exp             INT DEFAULT 0,
    stars           INT DEFAULT 1,
    ascension_level INT DEFAULT 0,
    awakening_level INT DEFAULT 0,
    -- Current stats (calculated)
    current_hp      INT NOT NULL,
    current_atk     INT NOT NULL,
    current_def     INT NOT NULL,
    current_spd     INT NOT NULL,
    current_crit    INT NOT NULL,
    current_dex     INT NOT NULL,
    -- Equipment slots
    weapon_id       UUID REFERENCES equipment(id),
    armor_id        UUID REFERENCES equipment(id),
    accessory_id    UUID REFERENCES equipment(id),
    relic_id        UUID REFERENCES equipment(id),
    -- Mount
    mount_id        UUID REFERENCES mounts(id),
    -- Metadata
    is_locked       BOOLEAN DEFAULT false,
    is_favorite     BOOLEAN DEFAULT false,
    acquired_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_level CHECK (level >= 1 AND level <= 100),
    CONSTRAINT chk_stars CHECK (stars BETWEEN 1 AND 6),
    CONSTRAINT chk_ascension CHECK (ascension_level BETWEEN 0 AND 6),
    CONSTRAINT chk_awakening CHECK (awakening_level BETWEEN 0 AND 6)
);

CREATE INDEX idx_heroes_player ON heroes(player_id);
CREATE INDEX idx_heroes_template ON heroes(template_id);
CREATE INDEX idx_heroes_stars ON heroes(stars);
```

### 3.2 Skill Tables

#### skill_templates (Static Data)
```sql
CREATE TABLE skill_templates (
    id              VARCHAR(50) PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    description     TEXT,
    skill_type      VARCHAR(20) NOT NULL,
    element         VARCHAR(10),
    mana_cost       INT NOT NULL,
    cooldown        INT DEFAULT 0,
    target_type     VARCHAR(20) NOT NULL,
    damage_multiplier DECIMAL(5,2),
    heal_multiplier DECIMAL(5,2),
    buff_stats      JSONB,
    debuff_effects  JSONB,
    special_effects JSONB,
    animation_id    VARCHAR(50),
    icon_url        VARCHAR(500),
    
    CONSTRAINT chk_skill_type CHECK (skill_type IN ('ACTIVE', 'PASSIVE', 'ULTIMATE')),
    CONSTRAINT chk_target_type CHECK (target_type IN ('SELF', 'SINGLE_ALLY', 'SINGLE_ENEMY', 'ALL_ALLIES', 'ALL_ENEMIES', 'AOE'))
);
```

#### hero_skills
```sql
CREATE TABLE hero_skills (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hero_id         UUID NOT NULL REFERENCES heroes(id) ON DELETE CASCADE,
    skill_id        VARCHAR(50) NOT NULL REFERENCES skill_templates(id),
    level           INT DEFAULT 1,
    is_unlocked     BOOLEAN DEFAULT true,
    enhanced_branch VARCHAR(20),
    enhanced_level  INT DEFAULT 0,
    
    CONSTRAINT unique_hero_skill UNIQUE (hero_id, skill_id),
    CONSTRAINT chk_skill_level CHECK (level BETWEEN 1 AND 10)
);

CREATE INDEX idx_hero_skills_hero ON hero_skills(hero_id);
```

### 3.3 Equipment Tables

#### equipment_templates (Static Data)
```sql
CREATE TABLE equipment_templates (
    id              VARCHAR(50) PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    equipment_type  VARCHAR(20) NOT NULL,
    base_rarity     INT NOT NULL,
    set_id          VARCHAR(50),
    -- Base stats
    base_hp         INT DEFAULT 0,
    base_atk        INT DEFAULT 0,
    base_def        INT DEFAULT 0,
    base_spd        INT DEFAULT 0,
    base_crit       INT DEFAULT 0,
    base_dex        INT DEFAULT 0,
    -- Special effect
    unique_effect   JSONB,
    required_level  INT DEFAULT 1,
    required_element VARCHAR(10),
    description     TEXT,
    icon_url        VARCHAR(500),
    
    CONSTRAINT chk_equip_type CHECK (equipment_type IN ('WEAPON', 'ARMOR', 'ACCESSORY', 'RELIC'))
);
```

#### equipment_sets (Static Data)
```sql
CREATE TABLE equipment_sets (
    id              VARCHAR(50) PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    description     TEXT,
    two_piece_bonus JSONB,
    three_piece_bonus JSONB,
    four_piece_bonus JSONB
);
```

#### equipment (Player's Equipment)
```sql
CREATE TABLE equipment (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id       UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    template_id     VARCHAR(50) NOT NULL REFERENCES equipment_templates(id),
    level           INT DEFAULT 1,
    -- Bonus stats from enhancement
    bonus_hp        INT DEFAULT 0,
    bonus_atk       INT DEFAULT 0,
    bonus_def       INT DEFAULT 0,
    bonus_spd       INT DEFAULT 0,
    bonus_crit      INT DEFAULT 0,
    bonus_dex       INT DEFAULT 0,
    -- Random substats
    substats        JSONB,
    -- Metadata
    is_locked       BOOLEAN DEFAULT false,
    acquired_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_equip_level CHECK (level BETWEEN 1 AND 30)
);

CREATE INDEX idx_equipment_player ON equipment(player_id);
CREATE INDEX idx_equipment_template ON equipment(template_id);
```

### 3.4 Mount Tables

#### mount_templates (Static Data)
```sql
CREATE TABLE mount_templates (
    id              VARCHAR(50) PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    mount_type      VARCHAR(20) NOT NULL,
    element         VARCHAR(10),
    base_rarity     INT NOT NULL,
    -- Base stats
    base_hp         INT DEFAULT 0,
    base_atk        INT DEFAULT 0,
    base_def        INT DEFAULT 0,
    base_spd        INT DEFAULT 0,
    -- Team buff
    team_buff       JSONB,
    -- Evolution stages (for dragons)
    evolution_stages JSONB,
    description     TEXT,
    model_url       VARCHAR(500),
    
    CONSTRAINT chk_mount_type CHECK (mount_type IN ('HORSE', 'DRAGON', 'MYTHICAL'))
);
```

#### mounts (Player's Mounts)
```sql
CREATE TABLE mounts (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id       UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    template_id     VARCHAR(50) NOT NULL REFERENCES mount_templates(id),
    level           INT DEFAULT 1,
    exp             INT DEFAULT 0,
    bond_level      INT DEFAULT 1,
    evolution_stage INT DEFAULT 0,
    awakening_level INT DEFAULT 0,
    acquired_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_mount_level CHECK (level BETWEEN 1 AND 100),
    CONSTRAINT chk_bond_level CHECK (bond_level BETWEEN 1 AND 10)
);

CREATE INDEX idx_mounts_player ON mounts(player_id);
```

### 3.5 Story & Progress Tables

#### chapters (Static Data)
```sql
CREATE TABLE chapters (
    id              VARCHAR(50) PRIMARY KEY,
    chapter_number  INT UNIQUE NOT NULL,
    title           VARCHAR(200) NOT NULL,
    description     TEXT,
    is_mythical     BOOLEAN DEFAULT false,
    unlock_requirements JSONB,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### stages (Static Data)
```sql
CREATE TABLE stages (
    id              VARCHAR(50) PRIMARY KEY,
    chapter_id      VARCHAR(50) NOT NULL REFERENCES chapters(id),
    stage_number    INT NOT NULL,
    name            VARCHAR(200) NOT NULL,
    description     TEXT,
    difficulty      INT NOT NULL,
    recommended_power INT,
    stamina_cost    INT DEFAULT 10,
    waves           INT DEFAULT 1,
    is_boss_stage   BOOLEAN DEFAULT false,
    first_clear_rewards JSONB,
    repeat_rewards  JSONB,
    star_conditions JSONB,
    
    CONSTRAINT unique_chapter_stage UNIQUE (chapter_id, stage_number)
);

CREATE INDEX idx_stages_chapter ON stages(chapter_id);
```

#### bosses (Static Data)
```sql
CREATE TABLE bosses (
    id              VARCHAR(50) PRIMARY KEY,
    stage_id        VARCHAR(50) REFERENCES stages(id),
    name            VARCHAR(100) NOT NULL,
    title           VARCHAR(200),
    element         VARCHAR(10) NOT NULL,
    mythical_tier   VARCHAR(20),
    -- Stats
    hp              BIGINT NOT NULL,
    atk             INT NOT NULL,
    def             INT NOT NULL,
    spd             INT NOT NULL,
    crit            INT NOT NULL,
    dex             INT NOT NULL,
    -- Skills
    skills          JSONB NOT NULL,
    -- Mechanics
    special_mechanics JSONB,
    description     TEXT,
    lore            TEXT,
    
    CONSTRAINT chk_mythical_tier CHECK (mythical_tier IN (NULL, 'TU_LINH', 'THIEN_VUONG', 'THUONG_CO', 'HON_DON'))
);
```

#### boss_phases (Static Data)
```sql
CREATE TABLE boss_phases (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    boss_id         VARCHAR(50) NOT NULL REFERENCES bosses(id),
    phase_number    INT NOT NULL,
    hp_threshold    DECIMAL(5,2) NOT NULL,
    name            VARCHAR(100),
    stat_modifiers  JSONB,
    new_skills      JSONB,
    special_effects JSONB,
    
    CONSTRAINT unique_boss_phase UNIQUE (boss_id, phase_number)
);
```

#### player_progress
```sql
CREATE TABLE player_progress (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id       UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    chapter_id      VARCHAR(50) NOT NULL REFERENCES chapters(id),
    is_unlocked     BOOLEAN DEFAULT false,
    is_completed    BOOLEAN DEFAULT false,
    unlocked_at     TIMESTAMP,
    completed_at    TIMESTAMP,
    
    CONSTRAINT unique_player_chapter UNIQUE (player_id, chapter_id)
);

CREATE INDEX idx_progress_player ON player_progress(player_id);
```

#### stage_clears
```sql
CREATE TABLE stage_clears (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id       UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    stage_id        VARCHAR(50) NOT NULL REFERENCES stages(id),
    stars           INT DEFAULT 0,
    best_time       INT, -- in seconds
    clear_count     INT DEFAULT 0,
    first_clear_at  TIMESTAMP,
    last_clear_at   TIMESTAMP,
    
    CONSTRAINT unique_player_stage UNIQUE (player_id, stage_id),
    CONSTRAINT chk_stars CHECK (stars BETWEEN 0 AND 3)
);

CREATE INDEX idx_stage_clears_player ON stage_clears(player_id);
```

### 3.6 Team & Formation Tables

#### teams
```sql
CREATE TABLE teams (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id       UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    name            VARCHAR(100),
    slot_number     INT NOT NULL,
    formation_id    VARCHAR(50) REFERENCES formations(id),
    is_default      BOOLEAN DEFAULT false,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_player_slot UNIQUE (player_id, slot_number),
    CONSTRAINT chk_slot CHECK (slot_number BETWEEN 1 AND 10)
);
```

#### team_members
```sql
CREATE TABLE team_members (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    team_id         UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    hero_id         UUID NOT NULL REFERENCES heroes(id) ON DELETE CASCADE,
    position_x      INT NOT NULL,
    position_y      INT NOT NULL,
    
    CONSTRAINT unique_team_position UNIQUE (team_id, position_x, position_y),
    CONSTRAINT unique_team_hero UNIQUE (team_id, hero_id),
    CONSTRAINT chk_position CHECK (position_x BETWEEN 0 AND 2 AND position_y BETWEEN 0 AND 2)
);

CREATE INDEX idx_team_members_team ON team_members(team_id);
```

#### formations (Static Data)
```sql
CREATE TABLE formations (
    id              VARCHAR(50) PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    description     TEXT,
    requirements    JSONB,
    position_bonuses JSONB,
    formation_effect JSONB,
    unlock_condition JSONB
);
```

### 3.7 Inventory & Items

#### item_templates (Static Data)
```sql
CREATE TABLE item_templates (
    id              VARCHAR(50) PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    item_type       VARCHAR(20) NOT NULL,
    rarity          INT DEFAULT 1,
    description     TEXT,
    use_effect      JSONB,
    max_stack       INT DEFAULT 9999,
    is_tradeable    BOOLEAN DEFAULT false,
    icon_url        VARCHAR(500),
    
    CONSTRAINT chk_item_type CHECK (item_type IN ('CONSUMABLE', 'MATERIAL', 'QUEST', 'CURRENCY'))
);
```

#### inventory
```sql
CREATE TABLE inventory (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id       UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    item_id         VARCHAR(50) NOT NULL REFERENCES item_templates(id),
    quantity        INT DEFAULT 1,
    
    CONSTRAINT unique_player_item UNIQUE (player_id, item_id),
    CONSTRAINT chk_quantity CHECK (quantity >= 0)
);

CREATE INDEX idx_inventory_player ON inventory(player_id);
```

### 3.8 Social Features

#### hero_bonds
```sql
CREATE TABLE hero_bonds (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id       UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    hero1_template  VARCHAR(50) NOT NULL REFERENCES hero_templates(id),
    hero2_template  VARCHAR(50) NOT NULL REFERENCES hero_templates(id),
    bond_level      INT DEFAULT 1,
    bond_points     INT DEFAULT 0,
    
    CONSTRAINT unique_bond UNIQUE (player_id, hero1_template, hero2_template),
    CONSTRAINT chk_bond_level CHECK (bond_level BETWEEN 1 AND 5)
);
```

#### guilds
```sql
CREATE TABLE guilds (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(100) UNIQUE NOT NULL,
    description     TEXT,
    level           INT DEFAULT 1,
    exp             BIGINT DEFAULT 0,
    leader_id       UUID NOT NULL REFERENCES players(id),
    max_members     INT DEFAULT 30,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_guild_level CHECK (level BETWEEN 1 AND 50)
);

CREATE INDEX idx_guilds_name ON guilds(name);
```

#### guild_members
```sql
CREATE TABLE guild_members (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guild_id        UUID NOT NULL REFERENCES guilds(id) ON DELETE CASCADE,
    player_id       UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    role            VARCHAR(20) DEFAULT 'MEMBER',
    contribution    BIGINT DEFAULT 0,
    joined_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_guild_member UNIQUE (player_id),
    CONSTRAINT chk_role CHECK (role IN ('LEADER', 'OFFICER', 'MEMBER'))
);

CREATE INDEX idx_guild_members_guild ON guild_members(guild_id);
```

### 3.9 Gacha & Pity System

#### banners (Semi-static, rotates)
```sql
CREATE TABLE banners (
    id              VARCHAR(50) PRIMARY KEY,
    name            VARCHAR(200) NOT NULL,
    banner_type     VARCHAR(20) NOT NULL,
    featured_heroes JSONB,
    rates           JSONB NOT NULL,
    start_time      TIMESTAMP NOT NULL,
    end_time        TIMESTAMP NOT NULL,
    is_active       BOOLEAN DEFAULT false,
    
    CONSTRAINT chk_banner_type CHECK (banner_type IN ('STANDARD', 'LIMITED', 'ELEMENT', 'EVENT'))
);
```

#### player_pity
```sql
CREATE TABLE player_pity (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id       UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    banner_type     VARCHAR(20) NOT NULL,
    pity_count      INT DEFAULT 0,
    guaranteed_5star BOOLEAN DEFAULT false,
    last_5star_at   TIMESTAMP,
    
    CONSTRAINT unique_player_banner UNIQUE (player_id, banner_type)
);
```

#### gacha_history
```sql
CREATE TABLE gacha_history (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id       UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    banner_id       VARCHAR(50) NOT NULL REFERENCES banners(id),
    result_type     VARCHAR(20) NOT NULL,
    result_id       VARCHAR(50) NOT NULL,
    rarity          INT NOT NULL,
    pulled_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_gacha_history_player ON gacha_history(player_id);
CREATE INDEX idx_gacha_history_time ON gacha_history(pulled_at);
```

---

## 4. Redis Cache Schema

### 4.1 Player Session
```
Key: session:{player_id}
TTL: 24 hours
Value: {
    "player_id": "uuid",
    "username": "string",
    "token": "jwt_token",
    "last_activity": "timestamp"
}
```

### 4.2 Battle State
```
Key: battle:{battle_id}
TTL: 1 hour
Value: {
    "battle_id": "uuid",
    "player_id": "uuid",
    "state": "battle_state_json",
    "turn_number": int,
    "started_at": "timestamp"
}
```

### 4.3 Leaderboard
```
Key: leaderboard:power
Type: Sorted Set
Members: player_id
Score: total_power
```

### 4.4 Real-time Stamina
```
Key: stamina:{player_id}
TTL: None (managed by app)
Value: {
    "current": int,
    "max": int,
    "last_update": "timestamp"
}
```

---

## 5. Indexes & Optimization

### 5.1 Composite Indexes
```sql
-- For team queries
CREATE INDEX idx_heroes_player_stars ON heroes(player_id, stars DESC);

-- For equipment searches
CREATE INDEX idx_equipment_player_type ON equipment(player_id, template_id);

-- For leaderboards
CREATE INDEX idx_players_level_power ON players(level DESC, id);

-- For gacha history
CREATE INDEX idx_gacha_player_time ON gacha_history(player_id, pulled_at DESC);
```

### 5.2 Partial Indexes
```sql
-- Active players only
CREATE INDEX idx_active_players ON players(level) WHERE is_active = true;

-- Unlocked heroes only  
CREATE INDEX idx_unlocked_heroes ON heroes(player_id) WHERE is_locked = false;

-- Boss stages only
CREATE INDEX idx_boss_stages ON stages(chapter_id) WHERE is_boss_stage = true;
```

---

## 6. Database Triggers

### 6.1 Auto-update timestamps
```sql
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_players_updated
    BEFORE UPDATE ON players
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_heroes_updated
    BEFORE UPDATE ON heroes
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
```

### 6.2 Hero stats recalculation
```sql
CREATE OR REPLACE FUNCTION recalculate_hero_stats()
RETURNS TRIGGER AS $$
DECLARE
    template RECORD;
BEGIN
    SELECT * INTO template FROM hero_templates WHERE id = NEW.template_id;
    
    NEW.current_hp = template.base_hp + (NEW.level - 1) * template.growth_hp;
    NEW.current_atk = template.base_atk + (NEW.level - 1) * template.growth_atk;
    NEW.current_def = template.base_def + (NEW.level - 1) * template.growth_def;
    NEW.current_spd = template.base_spd + (NEW.level - 1) * template.growth_spd;
    NEW.current_crit = template.base_crit + (NEW.level - 1) * template.growth_crit;
    NEW.current_dex = template.base_dex + (NEW.level - 1) * template.growth_dex;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_hero_stats
    BEFORE INSERT OR UPDATE OF level, ascension_level, awakening_level ON heroes
    FOR EACH ROW
    EXECUTE FUNCTION recalculate_hero_stats();
```

---

## 7. Sample Data

### 7.1 Hero Templates
```sql
INSERT INTO hero_templates (id, name, title, element, base_rarity, hero_class, 
    base_hp, base_atk, base_def, base_spd, base_crit, base_dex,
    growth_hp, growth_atk, growth_def, growth_spd, growth_crit, growth_dex)
VALUES
    ('luu_bi', 'Lưu Bị', 'Hoàng Thúc', 'MOC', 5, 'TANK', 
     1200, 80, 100, 90, 5, 15, 50, 3, 5, 2, 0.2, 0.5),
    ('quan_vu', 'Quan Vũ', 'Võ Thánh', 'KIM', 5, 'DPS',
     1000, 120, 80, 95, 15, 10, 40, 5, 3, 2.5, 0.5, 0.3),
    ('truong_phi', 'Trương Phi', 'Ích Đức', 'HOA', 5, 'BERSERKER',
     900, 150, 60, 100, 20, 8, 35, 7, 2, 3, 0.8, 0.2),
    ('gia_cat_luong', 'Gia Cát Lượng', 'Ngọa Long', 'THUY', 5, 'MAGE',
     800, 130, 50, 110, 10, 20, 30, 6, 1.5, 3.5, 0.3, 0.7),
    ('trieu_van', 'Triệu Vân', 'Tử Long', 'THO', 5, 'BALANCE',
     1000, 100, 90, 105, 12, 12, 42, 4.5, 4, 3, 0.4, 0.4);
```

### 7.2 Chapters
```sql
INSERT INTO chapters (id, chapter_number, title, description, is_mythical)
VALUES
    ('ch_1', 1, 'Khởi Nguồn - Loạn Thế Anh Hùng', 'Cuối thời Đông Hán, thiên hạ đại loạn...', false),
    ('ch_2', 2, 'Quần Hùng Tụ Nghĩa', 'Đổng Trác chuyên quyền, các chư hầu liên minh...', false),
    ('ch_3', 3, 'Tam Phân Thiên Hạ', 'Tào Tháo thống nhất phương Bắc...', false),
    ('ch_4', 4, 'Xích Bích Đại Chiến', 'Tào Tháo dẫn 80 vạn đại quân nam hạ...', false),
    ('ch_5', 5, 'Bắc Phạt Trung Nguyên', 'Gia Cát Lượng sáu lần Bắc phạt...', false),
    ('ch_6', 6, 'Loạn Thế Chung Cục', 'Ba nước suy yếu, nhà Tấn thống nhất...', false),
    ('ch_7', 7, 'Thiên Giới Đại Chiến', 'Cổng đến Thiên Giới mở ra...', true);
```

### 7.3 Mythical Bosses
```sql
INSERT INTO bosses (id, stage_id, name, title, element, mythical_tier, hp, atk, def, spd, crit, dex, skills)
VALUES
    ('thanh_long', 'stage_7_1', 'Thanh Long', 'Đông Phương Thần Thú', 'MOC', 'TU_LINH',
     50000, 2000, 1500, 150, 15, 20,
     '{"skills": ["long_quyen_chan_thien", "moc_chi_phuc_sinh", "thuong_long_trieu_vu"]}'),
    ('bach_ho', 'stage_7_2', 'Bạch Hổ', 'Tây Phương Thần Thú', 'KIM', 'TU_LINH',
     55000, 2500, 1200, 160, 25, 18,
     '{"skills": ["bach_ho_liet_khong", "kim_chi_loi_trao", "sat_phat_chi_khi"]}'),
    ('hon_don', 'stage_7_final', 'Hỗn Độn', 'Thủy Tổ Vạn Ma', 'ALL', 'HON_DON',
     200000, 5000, 3000, 200, 30, 25,
     '{"skills": ["hon_don_so_khai", "diet_the", "tan_the", "hong_hoang_chi_luc"]}');
```

---

## 8. Migration Strategy

### 8.1 Version Control
- Sử dụng Flyway hoặc Alembic cho database migrations
- Đặt tên theo format: `V{version}__{description}.sql`

### 8.2 Rollback Plan
- Mỗi migration có rollback script tương ứng
- Backup trước khi chạy production migrations

---

*Xem thêm Backend Design và Frontend Design để biết cách tích hợp database vào ứng dụng.*
