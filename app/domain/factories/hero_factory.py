"""
HeroFactory - Factory for creating Hero instances from predefined templates
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from uuid import uuid4

from app.domain.entities.hero import Hero
from app.domain.value_objects.element import Element
from app.domain.value_objects.hexagon_stats import HexagonStats
from app.domain.value_objects.grid_position import GridPosition


@dataclass
class HeroTemplate:
    """
    Template for creating heroes.
    
    Attributes:
        template_id: Unique identifier for the template
        name: Hero name
        element: Ngũ Hành element
        base_*: Base stats for the hero
        rarity: Base rarity (1-6)
        description: Hero description
        default_skills: List of default skill template IDs
    """
    
    template_id: str
    name: str
    element: Element
    base_hp: int
    base_atk: int
    base_def: int
    base_spd: int
    base_crit: int
    base_dex: int
    rarity: int = 3
    description: str = ""
    default_skills: List[str] = field(default_factory=list)
    growth_rates: Dict[str, float] = field(default_factory=dict)


class HeroFactory:
    """
    Factory class for creating Hero instances from predefined templates.
    
    Contains templates for famous Three Kingdoms heroes with
    stat distributions based on their element type:
    - Kim (Metal): High ATK, low DEF
    - Mộc (Wood): High HP, balanced
    - Thủy (Water): High SPD, high DEX
    - Hỏa (Fire): High CRIT, low HP
    - Thổ (Earth): High DEF, low SPD
    """
    
    def __init__(self, load_all: bool = False):
        """
        Initialize factory with predefined templates.
        
        Args:
            load_all: If True, loads all 200 heroes from hero_data module.
                     If False (default), only loads the original 14 heroes.
        """
        self._templates: Dict[str, HeroTemplate] = {}
        self._initialize_templates()
        
        if load_all:
            self._load_all_heroes_from_data()
    
    def _initialize_templates(self) -> None:
        """Initialize all predefined hero templates"""
        
        # === Thục Hán Heroes ===
        
        # Lưu Bị - Mộc (Wood) - Tank/Support
        self._templates["luu_bi"] = HeroTemplate(
            template_id="luu_bi",
            name="Lưu Bị",
            element=Element.MOC,
            base_hp=1300,
            base_atk=85,
            base_def=80,
            base_spd=90,
            base_crit=10,
            base_dex=15,
            rarity=5,
            description="Hoàng Đế Thục Hán, nhân từ đức độ, lãnh đạo Ngũ Hổ Tướng",
            default_skills=["basic_attack", "nhan_duc"],
            growth_rates={"HP": 15, "ATK": 5, "DEF": 6, "SPD": 4, "CRIT": 1, "DEX": 2}
        )
        
        # Quan Vũ - Kim (Metal) - DPS
        self._templates["quan_vu"] = HeroTemplate(
            template_id="quan_vu",
            name="Quan Vũ",
            element=Element.KIM,
            base_hp=1100,
            base_atk=130,
            base_def=70,
            base_spd=95,
            base_crit=18,
            base_dex=20,
            rarity=5,
            description="Võ Thánh, sử dụng Thanh Long Yểm Nguyệt Đao, nghĩa khí ngút trời",
            default_skills=["basic_attack", "long_tran_hao"],
            growth_rates={"HP": 8, "ATK": 12, "DEF": 4, "SPD": 5, "CRIT": 2, "DEX": 3}
        )
        
        # Trương Phi - Hỏa (Fire) - Burst DPS
        self._templates["truong_phi"] = HeroTemplate(
            template_id="truong_phi",
            name="Trương Phi",
            element=Element.HOA,
            base_hp=950,
            base_atk=125,
            base_def=55,
            base_spd=100,
            base_crit=25,
            base_dex=18,
            rarity=5,
            description="Yến Nhân Trương Dực Đức, hổ tướng thần dũng, tiếng thét rung trời",
            default_skills=["basic_attack", "truong_ba_xa_mau"],
            growth_rates={"HP": 6, "ATK": 10, "DEF": 3, "SPD": 6, "CRIT": 4, "DEX": 2}
        )
        
        # Gia Cát Lượng - Thủy (Water) - Mage/Control
        self._templates["gia_cat_luong"] = HeroTemplate(
            template_id="gia_cat_luong",
            name="Gia Cát Lượng",
            element=Element.THUY,
            base_hp=900,
            base_atk=90,
            base_def=60,
            base_spd=115,
            base_crit=12,
            base_dex=30,
            rarity=5,
            description="Khổng Minh, Ngọa Long tiên sinh, trí tuệ siêu phàm",
            default_skills=["basic_attack", "thien_khi", "bat_quai_tran"],
            growth_rates={"HP": 5, "ATK": 6, "DEF": 3, "SPD": 10, "CRIT": 2, "DEX": 5}
        )
        
        # Triệu Vân - Thổ (Earth) - Balanced
        self._templates["trieu_van"] = HeroTemplate(
            template_id="trieu_van",
            name="Triệu Vân",
            element=Element.THO,
            base_hp=1150,
            base_atk=105,
            base_def=95,
            base_spd=85,
            base_crit=15,
            base_dex=22,
            rarity=5,
            description="Triệu Tử Long, thường thắng tướng quân, trung thành bất khuất",
            default_skills=["basic_attack", "thich_tho_trung_thien"],
            growth_rates={"HP": 10, "ATK": 7, "DEF": 8, "SPD": 4, "CRIT": 2, "DEX": 3}
        )
        
        # === Ngụy Quốc Heroes ===
        
        # Tào Tháo - Thủy (Water) - Tactician
        self._templates["tao_thao"] = HeroTemplate(
            template_id="tao_thao",
            name="Tào Tháo",
            element=Element.THUY,
            base_hp=1000,
            base_atk=100,
            base_def=75,
            base_spd=110,
            base_crit=15,
            base_dex=25,
            rarity=5,
            description="Ngụy Vũ Đế, gian hùng thiên hạ, mưu lược siêu quần",
            default_skills=["basic_attack", "quan_thao_kinh_luoc"],
            growth_rates={"HP": 7, "ATK": 7, "DEF": 5, "SPD": 8, "CRIT": 2, "DEX": 4}
        )
        
        # Hạ Hầu Đôn - Kim (Metal) - DPS
        self._templates["ha_hau_don"] = HeroTemplate(
            template_id="ha_hau_don",
            name="Hạ Hầu Đôn",
            element=Element.KIM,
            base_hp=1050,
            base_atk=120,
            base_def=75,
            base_spd=90,
            base_crit=16,
            base_dex=18,
            rarity=4,
            description="Độc nhãn tướng quân, dũng mãnh vô song",
            default_skills=["basic_attack", "do_nhat_ngan_kim"],
            growth_rates={"HP": 8, "ATK": 10, "DEF": 5, "SPD": 5, "CRIT": 2, "DEX": 2}
        )
        
        # === Đông Ngô Heroes ===
        
        # Tôn Quyền - Mộc (Wood) - Leader
        self._templates["ton_quyen"] = HeroTemplate(
            template_id="ton_quyen",
            name="Tôn Quyền",
            element=Element.MOC,
            base_hp=1200,
            base_atk=90,
            base_def=85,
            base_spd=95,
            base_crit=12,
            base_dex=18,
            rarity=5,
            description="Đông Ngô Đại Đế, mãnh hổ giang đông",
            default_skills=["basic_attack", "dong_ngo_chinh_phuc"],
            growth_rates={"HP": 12, "ATK": 6, "DEF": 7, "SPD": 5, "CRIT": 2, "DEX": 3}
        )
        
        # Chu Du - Hỏa (Fire) - Strategist
        self._templates["chu_du"] = HeroTemplate(
            template_id="chu_du",
            name="Chu Du",
            element=Element.HOA,
            base_hp=880,
            base_atk=95,
            base_def=55,
            base_spd=105,
            base_crit=22,
            base_dex=25,
            rarity=5,
            description="Chu Công Cẩn, kỳ tài quân sự, hỏa thiêu Xích Bích",
            default_skills=["basic_attack", "xich_bich_dai_chien"],
            growth_rates={"HP": 5, "ATK": 7, "DEF": 3, "SPD": 7, "CRIT": 4, "DEX": 4}
        )
        
        # === Độc Lập / Khác ===
        
        # Lã Bố - Hỏa (Fire) - Berserker
        self._templates["la_bo"] = HeroTemplate(
            template_id="la_bo",
            name="Lã Bố",
            element=Element.HOA,
            base_hp=900,
            base_atk=145,
            base_def=50,
            base_spd=110,
            base_crit=28,
            base_dex=22,
            rarity=5,
            description="Thiên hạ vô song, phi tướng cưỡi Xích Thố",
            default_skills=["basic_attack", "phuong_thien_hoat_kich"],
            growth_rates={"HP": 5, "ATK": 14, "DEF": 2, "SPD": 7, "CRIT": 5, "DEX": 3}
        )
        
        # Điêu Thuyền - Thủy (Water) - Support
        self._templates["dieu_thuyen"] = HeroTemplate(
            template_id="dieu_thuyen",
            name="Điêu Thuyền",
            element=Element.THUY,
            base_hp=850,
            base_atk=70,
            base_def=50,
            base_spd=120,
            base_crit=10,
            base_dex=35,
            rarity=4,
            description="Tứ đại mỹ nhân, bí kế liên hoàn",
            default_skills=["basic_attack", "bi_nguyet_tu_hoa"],
            growth_rates={"HP": 5, "ATK": 4, "DEF": 3, "SPD": 10, "CRIT": 1, "DEX": 6}
        )
        
        # Mã Siêu - Thổ (Earth) - Cavalry
        self._templates["ma_sieu"] = HeroTemplate(
            template_id="ma_sieu",
            name="Mã Siêu",
            element=Element.THO,
            base_hp=1100,
            base_atk=115,
            base_def=90,
            base_spd=88,
            base_crit=18,
            base_dex=20,
            rarity=5,
            description="Cẩm Mã Siêu, Tây Lương kỹ binh thống lĩnh",
            default_skills=["basic_attack", "tay_luong_thiet_ky"],
            growth_rates={"HP": 9, "ATK": 9, "DEF": 8, "SPD": 4, "CRIT": 2, "DEX": 3}
        )
        
        # Hoàng Trung - Kim (Metal) - Archer
        self._templates["hoang_trung"] = HeroTemplate(
            template_id="hoang_trung",
            name="Hoàng Trung",
            element=Element.KIM,
            base_hp=980,
            base_atk=125,
            base_def=65,
            base_spd=92,
            base_crit=22,
            base_dex=25,
            rarity=4,
            description="Lão tướng bách phát bách trúng, tiễn pháp vô song",
            default_skills=["basic_attack", "bach_phat_bach_trung"],
            growth_rates={"HP": 7, "ATK": 11, "DEF": 4, "SPD": 5, "CRIT": 3, "DEX": 3}
        )
    
    def get_template(self, template_id: str) -> Optional[HeroTemplate]:
        """
        Get a hero template by ID.
        
        Args:
            template_id: Template identifier
            
        Returns:
            HeroTemplate if found, None otherwise
        """
        return self._templates.get(template_id)
    
    def get_all_templates(self) -> List[HeroTemplate]:
        """
        Get all available hero templates.
        
        Returns:
            List of all HeroTemplate instances
        """
        return list(self._templates.values())
    
    def get_templates_by_element(self, element: Element) -> List[HeroTemplate]:
        """
        Get all hero templates with a specific element.
        
        Args:
            element: Element to filter by
            
        Returns:
            List of matching HeroTemplate instances
        """
        return [t for t in self._templates.values() if t.element == element]
    
    def get_templates_by_rarity(self, rarity: int) -> List[HeroTemplate]:
        """
        Get all hero templates with a specific rarity.
        
        Args:
            rarity: Rarity level (1-6)
            
        Returns:
            List of matching HeroTemplate instances
        """
        return [t for t in self._templates.values() if t.rarity == rarity]
    
    def create_hero(self, template_id: str, position: GridPosition) -> Hero:
        """
        Create a new Hero instance from a template.
        
        Args:
            template_id: ID of the template to use
            position: Initial grid position
            
        Returns:
            New Hero instance
            
        Raises:
            ValueError: If template not found
        """
        template = self.get_template(template_id)
        if not template:
            raise ValueError(f"Template not found: {template_id}")
        
        stats = HexagonStats(
            hp=template.base_hp,
            atk=template.base_atk,
            def_=template.base_def,
            spd=template.base_spd,
            crit=template.base_crit,
            dex=template.base_dex
        )
        
        hero = Hero(
            id=str(uuid4()),
            name=template.name,
            element=template.element,
            position=position,
            stats=stats,
            template_id=template.template_id,
            rarity=template.rarity,
            skills=template.default_skills.copy(),
            growth_rates=template.growth_rates.copy()
        )
        
        return hero
    
    def _load_all_heroes_from_data(self) -> None:
        """
        Load all 200 heroes from the hero_data module.
        This adds heroes that are not in the original hardcoded templates.
        """
        from app.data.hero_data import get_all_heroes
        
        element_map = {
            "KIM": Element.KIM,
            "MOC": Element.MOC,
            "THUY": Element.THUY,
            "HOA": Element.HOA,
            "THO": Element.THO,
        }
        
        for hero_data in get_all_heroes():
            hero_id = hero_data["id"]
            
            # Skip if already exists (prefer original templates)
            if hero_id in self._templates:
                continue
            
            element = element_map.get(hero_data["element"], Element.THO)
            
            self._templates[hero_id] = HeroTemplate(
                template_id=hero_id,
                name=hero_data["name"],
                element=element,
                base_hp=hero_data["base_hp"],
                base_atk=hero_data["base_atk"],
                base_def=hero_data["base_def"],
                base_spd=hero_data["base_spd"],
                base_crit=hero_data["base_crit"],
                base_dex=hero_data["base_dex"],
                rarity=hero_data["base_rarity"],
                description=hero_data.get("description", ""),
                default_skills=["basic_attack"],
                growth_rates={
                    "HP": hero_data["growth_hp"],
                    "ATK": hero_data["growth_atk"],
                    "DEF": hero_data["growth_def"],
                    "SPD": hero_data["growth_spd"],
                    "CRIT": hero_data["growth_crit"],
                    "DEX": hero_data["growth_dex"],
                }
            )
    
    def get_hero_count(self) -> int:
        """Get the total number of available hero templates."""
        return len(self._templates)
