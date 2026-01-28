Kế Hoạch Phát Triển Game Đánh Theo Lượt "Ngọa Long Tam Quốc"
I. Tổng Quan
* Thể loại: Turn-based Strategy RPG
* Bối cảnh: Tam Quốc Diễn Nghĩa phong cách tiên hiệp/ngọa long
* Team: Tối đa 5 thành viên
* Bàn cờ: 9 ô vuông (3x3)
* Hệ thống: Ngũ hành tương sinh tương khắc
* Chỉ số: Dạng lục giác (Hexagon Stats)
II. Kiến Trúc Hệ Thống
1. Cấu trúc dự án
text
ngoa-long-tam-quoc/
├── main.py
├── game/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── engine.py      # Game engine chính
│   │   ├── battle_system.py
│   │   └── turn_manager.py
│   ├── characters/
│   │   ├── __init__.py
│   │   ├── base_character.py
│   │   ├── hero_factory.py
│   │   └── heroes/        # Danh sách tướng
│   ├── skills/
│   │   ├── __init__.py
│   │   ├── skill_base.py
│   │   ├── skill_factory.py
│   │   └── skill_types/
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── battle_ui.py
│   │   ├── character_ui.py
│   │   └── menu_ui.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── game_data.py
│   └── utils/
│       ├── __init__.py
│       ├── element_system.py
│       └── hexagon_stats.py
└── requirements.txt


2. Thư viện sử dụng
txt
pygame>=2.5.0
numpy>=1.24.0
python-json


III. Lộ Trình Phát Triển
Tuần 1: Thiết kế hệ thống cốt lõi
Ngày 1-2: Thiết kế hệ thống ngũ hành
python
# utils/element_system.py
ELEMENTS = {
    "Kim": {"strong": "Mộc", "weak": "Hỏa", "color": "#FFD700"},
    "Mộc": {"strong": "Thổ", "weak": "Kim", "color": "#228B22"},
    "Thủy": {"strong": "Hỏa", "weak": "Thổ", "color": "#1E90FF"},
    "Hỏa": {"strong": "Kim", "weak": "Thủy", "color": "#FF4500"},
    "Thổ": {"strong": "Thủy", "weak": "Mộc", "color": "#8B4513"}
}

def calculate_element_multiplier(attacker, defender):
    """Tính hệ số sát thương dựa trên ngũ hành"""
    if ELEMENTS[attacker]["strong"] == defender:
        return 1.5  # Tương khắc
    elif ELEMENTS[attacker]["weak"] == defender:
        return 0.7  # Bị khắc
    return 1.0


Ngày 3-4: Hệ thống chỉ số lục giác
python
# utils/hexagon_stats.py
class HexagonStats:
    def __init__(self, stats_dict):
        self.stats = {
            "HP": stats_dict.get("HP", 100),      # Máu
            "ATK": stats_dict.get("ATK", 10),     # Tấn công
            "DEF": stats_dict.get("DEF", 5),      # Phòng thủ
            "SPD": stats_dict.get("SPD", 100),    # Tốc độ
            "CRIT": stats_dict.get("CRIT", 5),    # Chí mạng
            "DEX": stats_dict.get("DEX", 10)      # Linh hoạt
        }
    
    def get_total_power(self):
        """Tính tổng sức mạnh dạng lục giác"""
        return sum(self.stats.values())


Ngày 5-7: Lớp nhân vật cơ bản
python
# characters/base_character.py
class Character:
    def __init__(self, name, element, position, stats):
        self.name = name
        self.element = element
        self.position = position  # (x, y) trong grid 3x3
        self.stats = HexagonStats(stats)
        self.current_hp = self.stats.stats["HP"]
        self.mana = 0
        self.max_mana = 100
        self.skills = []
        self.status_effects = []
        
    def take_damage(self, damage):
        self.current_hp -= damage
        return self.current_hp <= 0


Tuần 2: Hệ thống chiến đấu
Ngày 8-10: Battle System
* Turn-based system với priority dựa trên SPD
* Grid-based movement (9 ô)
* Action points system
Ngày 11-12: Mana và Skill System
* Mana tích lũy mỗi turn (10-20 điểm)
* Khi đủ 100 mana có thể dùng chiêu
* Các loại skill: Đơn thể, Đa thể, Buff, Debuff, Hồi phục
Ngày 13-14: Skill Database
python
# skills/skill_factory.py
SKILL_DATABASE = {
    "long_tran_hao": {
        "name": "Long Tran Hào",
        "mana_cost": 100,
        "type": "aoe",
        "target": "enemies",
        "damage_multiplier": 1.5,
        "description": "Gây sát thương diện rộng"
    },
    "thien_khi": {
        "name": "Thiên Khí",
        "mana_cost": 80,
        "type": "heal",
        "target": "allies",
        "heal_amount": 0.3,  # 30% max HP
        "description": "Hồi phục HP đồng đội"
    }
}


Tuần 3: Nhân vật và Team Building
Ngày 15-16: Tạo danh sách tướng Tam Quốc
* 20+ tướng từ Tam Quốc
* Mỗi tướng thuộc 1 trong 5 hệ
* Stats phân bố theo hệ:
    * Kim: Cao ATK, thấp DEF
    * Mộc: Cao HP, trung bình các stat
    * Thủy: Cao SPD và DEX
    * Hỏa: Cao CRIT, thấp HP
    * Thổ: Cao DEF, thấp SPD
Ngày 17-18: Team Composition System
* Max 5 thành viên
* Position trong grid ảnh hưởng đến:
    * Tầm đánh
    * Buff vùng
    * Nhận sát thương
Ngày 19-21: Balance và Testing
* Cân bằng chỉ số
* Test tương tác ngũ hành
* Debug combat system
Tuần 4: UI và Hoàn Thiện
Ngày 22-23: Battle UI với PyGame
* Hiển thị grid 3x3
* Health bars, mana bars
* Skill buttons
* Turn indicator
Ngày 24-25: Character Info UI
* Hiển thị hexagon stats
* Element indicators
* Status effects
Ngày 26-28: Thêm tính năng
* Save/Load system
* Level up system
* Item system cơ bản
* Sound effects
IV. Danh Sách Nhân Vật Mẫu
1. Lưu Bị (Hệ Mộc) - Tank/Support
2. Quan Vũ (Hệ Kim) - DPS cao
3. Trương Phi (Hệ Hỏa) - Burst damage
4. Gia Cát Lượng (Hệ Thủy) - Mage/Control
5. Triệu Vân (Hệ Thổ) - Balance
6. Tào Tháo (Hệ Thủy) - Tactician
7. Tôn Quyền (Hệ Mộc) - Leader
8. Lã Bố (Hệ Hỏa) - Berserker
V. Tính Năng Đặc Biệt
1. Combo System
* Khi các tướng cùng hệ đứng gần nhau
* Kích hoạt combo skill khi đủ điều kiện
2. Ultimate Skills
* Mỗi tướng có 1 ultimate skill
* Hiệu ứng hoành tráng
* Long animation
3. Weather System
* Ảnh hưởng đến element power
* Thay đổi mỗi vài turn
VI. Mở Rộng (Future Updates)
1. PvE Campaign: Cốt truyện Tam Quốc
2. PvP Mode: Đấu với người chơi khác
3. Guild System: Liên minh chiến đấu
4. Equipment System: Vũ khí, giáp
5. Pet System: Chiến mã, thú nuôi
VII. Cân Bằng Game
Nguyên tắc cân bằng:
1. Mỗi hệ có điểm mạnh/điểm yếu rõ ràng
2. Team composition quan trọng hơn individual power
3. Position strategy quan trọng
4. Mana management là chìa khóa
Công thức tính damage:
text
damage = (ATK * skill_multiplier - DEF * 0.5) * element_multiplier * (1 + CRIT/100)


VIII. Tài Nguyên Tham Khảo
1. Cốt truyện: Tam Quốc Diễn Nghĩa
2. Chiêu thức: Tham khảo từ các web ngọa long
3. Hệ thống: Ngũ hành từ Đạo giáo
4. Visual: Phong cách tranh thủy mặc Trung Hoa
IX. Timeline Tổng Quan
* Tuần 1-2: Core systems
* Tuần 3: Characters & combat
* Tuần 4: UI & Polish
* Tuần 5: Testing & Bug fixes
* Tuần 6: Additional features
X. Công Cụ Hỗ Trợ
1. Version Control: Git/GitHub
2. Project Management: Trello/Notion
3. Art Assets: Aseprite cho pixel art
4. Sound: Bfxr cho sound effects
Lưu ý: Kế hoạch này có thể điều chỉnh linh hoạt trong quá trình phát triển. Ưu tiên xây dựng MVP (Minimum Viable Product) trước khi thêm các tính năng phức tạp.
Kế Hoạch Mở Rộng Hệ Thống Nâng Cấp và Tùy Biến
I. Hệ Thống Trang Bị (Equipment System)
1. Cấu trúc trang bị
python
# game/equipment/
# ├── equipment_base.py
# ├── equipment_factory.py
# ├── equipment_types.py
# └── enhancement_system.py

class Equipment:
    def __init__(self, name, type, rarity, stats, set_bonus=None, unique_effect=None):
        self.name = name
        self.type = type  # 'weapon', 'armor', 'accessory', 'relic'
        self.rarity = rarity  # Common, Rare, Epic, Legendary, Mythic
        self.stats = stats  # Dict of stat bonuses
        self.level = 1
        self.max_level = {
            'Common': 10, 'Rare': 15, 'Epic': 20, 
            'Legendary': 25, 'Mythic': 30
        }
        self.set_bonus = set_bonus  # For equipment sets
        self.unique_effect = unique_effect  # Special ability
        
    def enhance(self, materials):
        """Nâng cấp trang bị"""
        if self.level < self.max_level[self.rarity]:
            self.level += 1
            # Tăng chỉ số theo tỷ lệ
            for stat in self.stats:
                self.stats[stat] *= (1 + 0.1 * self.level)


2. Set trang bị Tam Quốc
python
EQUIPMENT_SETS = {
    'Thanh Long Yểm Nguyệt': {
        'pieces': ['Thanh Long Đao', 'Thanh Long Giáp', 'Thanh Long Hộ Phù'],
        '2_piece': {'ATK': 15, 'CRIT': 10},
        '3_piece': {'unique_effect': 'Rồng Xanh Hộ Thể - Giảm 20% sát thương nhận vào'}
    },
    'Xích Thố': {
        'type': 'mount',
        'effect': {'SPD': 30, 'DEX': 15},
        'unique_effect': 'Phi Tích - Bỏ qua 1 lượt chờ mỗi 3 turn'
    }
}


II. Hệ Thống Nâng Cấp Nhân Vật
1. Level và Thăng Cấp (Ascension)
python
class CharacterProgression:
    def __init__(self, character):
        self.character = character
        self.level = 1
        self.exp = 0
        self.ascension_level = 0  # 0-6
        self.star_rating = 1  # 1-6 sao
        self.unlocked_passives = []  # Nội tại đã mở khóa
        
    def level_up(self, exp_amount):
        self.exp += exp_amount
        while self.exp >= self.required_exp():
            self.level += 1
            self.exp -= self.required_exp()
            self.apply_level_bonus()
            
    def ascend(self, ascension_materials):
        """Thăng cấp - mở khóa giới hạn level và nội tại"""
        if self.ascension_level < 6:
            self.ascension_level += 1
            self.level_cap += 10
            self.unlock_passive_skill()  # Mở nội tại mới
            
    def apply_level_bonus(self):
        """Tăng chỉ số theo level"""
        growth_rate = self.character.growth_rates
        for stat, rate in growth_rate.items():
            current = self.character.stats.stats[stat]
            self.character.stats.stats[stat] = current + rate


2. Hệ thống sao
python
STAR_SYSTEM = {
    1: {'stat_multiplier': 1.0, 'skill_slots': 2},
    2: {'stat_multiplier': 1.2, 'skill_slots': 2},
    3: {'stat_multiplier': 1.5, 'skill_slots': 3},
    4: {'stat_multiplier': 1.8, 'skill_slots': 3},
    5: {'stat_multiplier': 2.2, 'skill_slots': 4},
    6: {'stat_multiplier': 2.5, 'skill_slots': 4, 'unique_awakening': True}
}


III. Hệ Thống Nâng Cấp Kỹ Năng
1. Skill Tree với nhiều cấp độ
python
class SkillEnhancement:
    def __init__(self, skill):
        self.skill = skill
        self.level = 1
        self.max_level = 10
        self.branches = {
            'power': {'damage_increase': 0.05, 'cost': 100},  # Nhánh sát thương
            'efficiency': {'mana_reduction': 0.03, 'cost': 150},  # Nhánh hiệu quả
            'utility': {'effect_duration': 0.1, 'cost': 200}  # Nhánh tiện ích
        }
        self.active_branches = []
        
    def upgrade(self, branch_name, resources):
        """Nâng cấp một nhánh kỹ năng"""
        if branch_name in self.branches:
            self.level += 1
            branch = self.branches[branch_name]
            # Áp dụng buff
            if 'damage_increase' in branch:
                self.skill.damage_multiplier *= (1 + branch['damage_increase'])


2. Biến thể kỹ năng
python
SKILL_VARIANTS = {
    'basic_attack': {
        'normal': {'damage': 1.0, 'effect': None},
        'enhanced': {'damage': 1.3, 'effect': 'armor_break'},
        'ultimate': {'damage': 2.0, 'effect': 'stun', 'cooldown': 3}
    }
}


IV. Hệ Thống Nội Tại (Passive Skills)
1. Passive Skill Tree
python
# game/passives/
# ├── passive_tree.py
# ├── passive_nodes.py
# └── synergy_system.py

class PassiveTree:
    def __init__(self, character_class):
        self.class = character_class
        self.nodes = self.initialize_tree()
        self.unlocked_nodes = []
        self.skill_points = 0
        
    def initialize_tree(self):
        """Tạo cây nội tại theo class"""
        trees = {
            'Warrior': {
                'path_offense': ['Thế Công', 'Chém Xung Phong', 'Bá Vương'],
                'path_defense': ['Thế Thủ', 'Bất Khuất', 'Thiết Bích'],
                'path_hybrid': ['Võ Công Thông Thái', 'Binh Pháp']
            },
            'Mage': {
                'path_elemental': ['Ngũ Hành Thông Suốt', 'Nguyên Tố Hội Tụ'],
                'path_support': ['Hồi Phục', 'Cường Hóa', 'Giải Trừ']
            }
        }
        return trees.get(self.class, {})

class PassiveNode:
    def __init__(self, name, requirements, effects, tier):
        self.name = name
        self.requirements = requirements  # Level, ascension, other nodes
        self.effects = effects  # Stat boosts or special abilities
        self.tier = tier  # 1-3, càng cao càng mạnh
        self.unlocked = False


2. Ví dụ nội tại cho Quan Vũ
python
GUAN_YU_PASSIVES = {
    'Thanh Long Hộ Thể': {
        'tier': 1,
        'requirements': {'level': 10},
        'effects': {'DEF': 15, 'HP': 10},
        'description': 'Nhận ít hơn 15% sát thương từ Mộc hệ'
    },
    'Nghĩa Bạc Vân Thiên': {
        'tier': 2,
        'requirements': {'level': 30, 'ascension': 2},
        'effects': {'team_buff': {'ATK': 5}},
        'description': 'Đồng đội Kim hệ tăng 5% ATK'
    },
    'Vũ Thánh': {
        'tier': 3,
        'requirements': {'level': 50, 'ascension': 4, 'star': 5},
        'effects': {'unique': 'double_attack_chance'},
        'description': '20% cơ hội tấn công 2 lần'
    }
}


V. Hệ Thống Thú Cưỡi và Linh Thú
1. Mount System
python
# game/mounts/
# ├── mount_base.py
# ├── mount_types.py
# ├── dragon_system.py
# └── stable_management.py

class Mount:
    def __init__(self, name, type, rarity):
        self.name = name
        self.type = type  # 'horse', 'dragon', 'mythical'
        self.rarity = rarity
        self.level = 1
        self.exp = 0
        self.bond_level = 1  # 1-10, càng cao buff càng mạnh
        self.base_stats = {}
        self.mount_skills = []
        self.equipment_slots = []  # Yên cương, bảo giáp
        
    def calculate_team_bonus(self):
        """Tính bonus cho cả team dựa trên mount"""
        bonuses = {
            'Xích Thố': {'SPD': 10 + self.level * 2},
            'Đích Lô': {'ATK': 5 + self.level},
            'Tuyệt Ảnh': {'DEX': 8 + self.level * 1.5}
        }
        return bonuses.get(self.name, {})

class DragonCompanion(Mount):
    def __init__(self, name, element):
        super().__init__(name, 'dragon', 'Legendary')
        self.element = element
        self.dragon_breath_skill = None
        self.awakening_level = 0  # 0-5
        
    def team_element_buff(self):
        """Buff cho team cùng hệ với rồng"""
        return {
            f'{self.element}_damage': 0.1 + (0.05 * self.awakening_level),
            f'{self.element}_resistance': 0.15 + (0.05 * self.awakening_level)
        }


2. Dragon Evolution System
python
DRAGON_EVOLUTION = {
    'Hỏa Long': {
        'stages': [
            {'name': 'Hỏa Long Ấu Thể', 'level_req': 1, 'stats': {'ATK': 20}},
            {'name': 'Hỏa Long Trưởng Thành', 'level_req': 30, 'stats': {'ATK': 50, 'CRIT': 10}},
            {'name': 'Cửu U Hỏa Long', 'level_req': 60, 'stats': {'ATK': 100, 'CRIT': 20, 'AOE_damage': 15}}
        ],
        'evolution_items': ['Hỏa Long Tâm', 'Lông Vũ Bất Tử', 'Long Huyết Tinh']
    }
}


VI. Hệ Thống Formation và Team Synergy
1. Formation Buffs
python
class FormationSystem:
    def __init__(self):
        self.formations = {
            'Ngũ Hành Trận': {
                'requirements': {'characters': 5, 'elements': ['all_different']},
                'effects': {'all_stats': 5, 'element_power': 20},
                'positions': [(0,0), (0,2), (1,1), (2,0), (2,2)]
            },
            'Long Đằng Hổ Khiếu': {
                'requirements': {'characters': 3, 'specific_heroes': ['Triệu Vân', 'Trương Phi']},
                'effects': {'ATK': 15, 'SPD': 10},
                'description': 'Tăng sát thương khi tấn công từ hai bên'
            }
        }
        self.active_formation = None
        
    def calculate_formation_bonus(self, team):
        """Tính bonus dựa trên formation và vị trí"""
        if not self.active_formation:
            return {}
            
        bonus = {}
        formation = self.formations[self.active_formation]
        
        # Kiểm tra điều kiện
        if self.check_requirements(team, formation['requirements']):
            bonus.update(formation['effects'])
            
        # Bonus theo vị trí
        for i, pos in enumerate(formation['positions'][:len(team)]):
            if i < len(team):
                position_bonus = self.get_position_bonus(pos, team[i])
                bonus.update(position_bonus)
                
        return bonus


2. Team Composition Synergy
python
TEAM_SYNERGIES = {
    'Thục Hán Hero': {
        'heroes': ['Lưu Bị', 'Quan Vũ', 'Trương Phi', 'Gia Cát Lượng', 'Triệu Vân'],
        'effects': {
            '2_heroes': {'HP': 10},
            '3_heroes': {'ATK': 15},
            '4_heroes': {'DEF': 20},
            '5_heroes': {'unique': 'brotherhood_bond', 'revive_chance': 50}
        }
    },
    'Five Tigers': {
        'heroes': ['Quan Vũ', 'Trương Phi', 'Triệu Vân', 'Mã Siêu', 'Hoàng Trung'],
        'effects': {
            'complete_set': {'CRIT': 25, 'SPD': 20},
            'unique': 'tiger_roar_stun'
        }
    }
}


VII. Hệ Thống Awakening và Biến Hóa
1. Character Awakening
python
class AwakeningSystem:
    def __init__(self):
        self.awakening_levels = 6
        self.requirements = {
            1: {'level': 50, 'items': ['Thăng Cấp Thạch']},
            2: {'level': 60, 'items': ['Thăng Cấp Thạch', 'Hồn Phách Anh Hùng']},
            3: {'level': 70, 'items': ['Thăng Cấp Thạch', 'Hồn Phách Anh Hùng', 'Long Huyết']},
            # ... đến level 6
        }
        self.awakening_effects = {
            1: {'stat_boost': 10, 'unlock': 'new_skill_variant'},
            2: {'stat_boost': 20, 'unlock': 'enhanced_passive'},
            3: {'stat_boost': 30, 'unlock': 'transformation'},
            4: {'stat_boost': 40, 'unlock': 'ultimate_awakening'},
            5: {'stat_boost': 50, 'unlock': 'mythic_form'},
            6: {'stat_boost': 60, 'unlock': 'true_divinity'}
        }


2. Biến Hóa (Transformation)
python
TRANSFORMATIONS = {
    'Gia Cát Lượng': {
        'Thiên Tượng Sư': {
            'requirements': {'awakening': 3, 'items': ['Khổng Minh Thư']},
            'duration': 3,  # số turn
            'effects': {
                'stats': {'INT': 50, 'DEX': 30},
                'new_skills': ['Cầu Gió Đông', 'Bát Quái Trận'],
                'visual_change': True
            }
        }
    },
    'Lã Bố': {
        'Chiến Thần': {
            'requirements': {'awakening': 4, 'hp_below': 30},
            'effects': {
                'stats': {'ATK': 100, 'SPD': 50, 'DEF': -20},
                'berserk': True,
                'lifesteal': 0.3
            }
        }
    }
}


VIII. Hệ Thống Gacha và Thu Thập
1. Gacha System với tỷ lệ
python
class GachaSystem:
    def __init__(self):
        self.banners = {
            'standard': {
                '3_star_rate': 80,
                '4_star_rate': 18,
                '5_star_rate': 2,
                'pity_counter': 90  # Đảm bảo 5* sau 90 lần
            },
            'limited_banner': {
                'featured_hero_rate_up': 50,
                'pity_transfer': True
            }
        }
        
    def summon(self, banner_type, times=1):
        """Hệ thống gacha với bảo đảm"""
        results = []
        pity_counter = self.get_pity_counter(banner_type)
        
        for i in range(times):
            roll = random.random() * 100
            # Tính toán rarity dựa trên tỷ lệ và pity
            if pity_counter >= 89 or roll < 0.6:  # 5* rate
                rarity = 5
                pity_counter = 0
            elif roll < 5:  # 4* rate
                rarity = 4
            else:  # 3* rate
                rarity = 3
                pity_counter += 1
                
            results.append(self.get_random_item(rarity, banner_type))
            
        return results


IX. Hệ Thống Guild và Cộng Đồng
1. Guild Buffs
python
class GuildSystem:
    def __init__(self):
        self.guild_level = 1
        self.guild_tech = {
            'warfare': {'ATK_bonus': 0, 'max_level': 20},
            'defense': {'HP_bonus': 0, 'max_level': 20},
            'elemental': {'element_power': 0, 'max_level': 15},
            'mounts': {'mount_stats': 0, 'max_level': 10}
        }
        self.guild_skills = []  # Kỹ năng guild dùng trong battle
        
    def get_guild_buffs(self, member_contribution):
        """Tính buff dựa trên guild level và đóng góp"""
        buffs = {}
        for tech, data in self.guild_tech.items():
            buffs.update(self.calculate_tech_bonus(tech, data['level']))
            
        # Bonus từ guild skills
        for skill in self.guild_skills:
            if skill.active:
                buffs.update(skill.effects)
                
        return buffs


X. Hệ Thống Quan Hệ (Bond System)
1. Relationship Levels
python
class RelationshipSystem:
    def __init__(self):
        self.relationships = {}  # hero_id -> {target_id: bond_level}
        self.bond_levels = {
            1: {'name': 'Quen Biết', 'bonus': {}},
            2: {'name': 'Bạn Bè', 'bonus': {'stats': 2}},
            3: {'name': 'Thân Thiết', 'bonus': {'stats': 5}},
            4: {'name': 'Tri Kỷ', 'bonus': {'stats': 10, 'combo_skill': True}},
            5: {'name': 'Máu Mủ', 'bonus': {'stats': 20, 'combo_skill_enhanced': True}}
        }
        
    def increase_bond(self, hero1, hero2, points):
        """Tăng mối quan hệ giữa 2 tướng"""
        key = tuple(sorted([hero1.id, hero2.id]))
        if key not in self.relationships:
            self.relationships[key] = {'level': 1, 'points': 0}
            
        self.relationships[key]['points'] += points
        
        # Kiểm tra lên level
        current = self.relationships[key]
        required_points = current['level'] * 1000
        if current['points'] >= required_points:
            current['level'] += 1
            current['points'] -= required_points
            self.unlock_bond_bonus(hero1, hero2, current['level'])


2. Combo Skills từ Bond
python
BOND_COMBO_SKILLS = {
    ('Lưu Bị', 'Quan Vũ', 'Trương Phi'): {
        'required_bond': 4,
        'skill_name': 'Đào Viên Kết Nghĩa',
        'effects': {
            'damage': 3.0,
            'aoe': True,
            'additional': 'stun_all_enemies',
            'cooldown': 5
        }
    },
    ('Gia Cát Lượng', 'Chu Du'): {
        'required_bond': 3,
        'skill_name': 'Trận Phong Xích Bích',
        'effects': {
            'damage': 2.5,
            'element': ['Fire', 'Wind'],
            'dot_damage': True,
            'duration': 3
        }
    }
}


XI. Hệ Thống Tính Toán Tổng Hợp
1. Tổng hợp tất cả buffs
python
class TotalStatCalculator:
    def calculate_total_stats(self, character, team, guild, formations):
        """Tính toán tất cả buffs và bonuses"""
        base_stats = character.base_stats.copy()
        
        # Equipment bonuses
        for equip in character.equipment.values():
            if equip:
                base_stats.add(equip.get_stats(equip.level))
                
        # Mount bonuses
        if character.mount:
            base_stats.add(character.mount.get_stats())
            base_stats.add(character.mount.get_team_bonus())
            
        # Passive skill bonuses
        for passive in character.passive_skills:
            base_stats.add(passive.get_stat_bonuses())
            
        # Formation bonuses
        formation_bonus = formations.get_formation_bonus(team)
        base_stats.add(formation_bonus)
        
        # Guild bonuses
        guild_bonus = guild.get_guild_buffs(character.guild_contribution)
        base_stats.add(guild_bonus)
        
        # Synergy bonuses
        synergy_bonus = self.calculate_team_synergy(team)
        base_stats.add(synergy_bonus)
        
        # Apply star multiplier
        star_multiplier = STAR_SYSTEM[character.star_rating]['stat_multiplier']
        base_stats.multiply(star_multiplier)
        
        return base_stats


2. Dynamic Scaling System
python
class DynamicScaling:
    def __init__(self):
        self.scaling_factors = {
            'level': lambda lvl: 1 + (lvl / 100),
            'ascension': lambda asc: 1 + (asc * 0.2),
            'awakening': lambda awk: 1 + (awk * 0.3),
            'bond_level': lambda bond: 1 + (bond * 0.05)
        }
        
    def calculate_dynamic_value(self, base_value, character):
        """Tính giá trị động dựa trên nhiều yếu tố"""
        multiplier = 1.0
        for factor_name, factor_func in self.scaling_factors.items():
            factor_value = getattr(character, factor_name, 0)
            multiplier *= factor_func(factor_value)
        return base_value * multiplier


XII. Database Design cho Tính Mở Rộng
python
# Thiết kế database linh hoạt
CHARACTER_SCHEMA = {
    'base_info': ['id', 'name', 'element', 'rarity', 'base_stats'],
    'progression': ['level', 'exp', 'ascension', 'star_rating'],
    'equipment': {
        'weapon': 'equipment_id',
        'armor': 'equipment_id',
        'accessory': 'equipment_id',
        'relic': 'equipment_id'
    },
    'skills': {
        'active': ['skill_id', 'level', 'enhancements'],
        'passive': ['passive_id', 'unlocked', 'level']
    },
    'mount': 'mount_id',
    'awakening': 'awakening_level',
    'relationships': [{'target_id': 'hero_id', 'bond_level': 'int'}]
}

# JSON structure cho lưu trữ
SAVE_DATA_STRUCTURE = {
    'characters': [],  # Danh sách tướng đã có
    'inventory': {
        'equipment': [],
        'materials': [],
        'mounts': [],
        'consumables': []
    },
    'progression': {
        'story_progress': {},
        'dungeons_cleared': [],
        'achievements': []
    },
    'guild': {
        'guild_id': '',
        'contribution': 0,
        'tech_levels': {}
    },
    'settings': {
        'graphics': {},
        'audio': {},
        'controls': {}
    }
}


XIII. API Hooks cho Tính Năng Tương Lai
python
class GameAPI:
    """API cho các tính năng mở rộng trong tương lai"""
    
    def __init__(self):
        self.hooks = {
            'pre_battle': [],
            'post_battle': [],
            'character_level_up': [],
            'equipment_enhance': [],
            'skill_upgrade': []
        }
    
    def register_hook(self, hook_name, callback):
        """Đăng ký hook cho modders/developers"""
        if hook_name in self.hooks:
            self.hooks[hook_name].append(callback)
    
    def trigger_hook(self, hook_name, *args, **kwargs):
        """Kích hoạt tất cả callbacks cho một hook"""
        results = []
        for callback in self.hooks.get(hook_name, []):
            try:
                result = callback(*args, **kwargs)
                if result is not None:
                    results.append(result)
            except Exception as e:
                print(f"Hook error: {e}")
        return results


XIV. Modding Support
python
# game/mods/
# ├── mod_loader.py
# ├── mod_validator.py
# └── api_documentation.py

class ModLoader:
    def __init__(self):
        self.loaded_mods = []
        self.mod_directories = ['mods/', 'community_mods/']
    
    def load_mod(self, mod_path):
        """Tải mod từ thư mục"""
        mod_config = self.read_mod_config(mod_path)
        
        # Load các thành phần mod
        if 'characters' in mod_config:
            self.load_mod_characters(mod_config['characters'])
        
        if 'equipment' in mod_config:
            self.load_mod_equipment(mod_config['equipment'])
        
        if 'skills' in mod_config:
            self.load_mod_skills(mod_config['skills'])
        
        self.loaded_mods.append(mod_config)
    
    def create_mod_template(self):
        """Tạo template cho modders"""
        return {
            'mod_info': {
                'name': '',
                'author': '',
                'version': '1.0.0',
                'description': '',
                'dependencies': []
            },
            'characters': [],
            'equipment': [],
            'skills': [],
            'passives': [],
            'mounts': [],
            'localization': {}
        }


Hệ thống này cho phép mở rộng gần như vô hạn với:
1. Content Expansion: Thêm tướng mới, trang bị mới, kỹ năng mới
2. System Expansion: Thêm hệ thống mới như pets, crafting, housing
3. Progression Expansion: Thêm cách nâng cấp và tiến hóa mới
4. Social Expansion: Guild wars, PvP rankings, cooperative dungeons
5. Event Systems: Limited-time events, seasonal content, crossover events
