"""
SkillFactory - Factory for creating Skill instances from predefined templates
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from uuid import uuid4

from app.domain.entities.skill import Skill, ActiveSkill, PassiveSkill, SkillType, TargetType
from app.domain.value_objects.element import Element


@dataclass
class SkillTemplate:
    """
    Template for creating skills.
    
    Attributes:
        template_id: Unique identifier for the template
        name: Skill name
        description: Skill description
        mana_cost: Mana required to use
        cooldown: Cooldown in turns
        skill_type: Type of skill
        target_type: Who can be targeted
        damage_multiplier: Damage scaling
        heal_multiplier: Heal scaling
        element: Optional element type
        buff_stats: Stats to buff
        debuff_effects: Effects to apply
        duration: Effect duration
        aoe_range: Range for AOE skills
    """
    
    template_id: str
    name: str
    description: str
    mana_cost: int
    cooldown: int
    skill_type: SkillType
    target_type: TargetType
    damage_multiplier: float = 1.0
    heal_multiplier: float = 0.0
    element: Optional[Element] = None
    buff_stats: Dict[str, int] = field(default_factory=dict)
    debuff_effects: Dict[str, int] = field(default_factory=dict)
    duration: int = 0
    aoe_range: int = 0


class SkillFactory:
    """
    Factory class for creating Skill instances from predefined templates.
    
    Contains templates for various skills:
    - Basic attacks
    - Damage skills (single/AOE)
    - Healing skills
    - Buff/Debuff skills
    - Ultimate skills
    """
    
    def __init__(self):
        """Initialize factory with predefined templates"""
        self._templates: Dict[str, SkillTemplate] = {}
        self._initialize_templates()
    
    def _initialize_templates(self) -> None:
        """Initialize all predefined skill templates"""
        
        # === Basic Skills ===
        
        self._templates["basic_attack"] = SkillTemplate(
            template_id="basic_attack",
            name="Đánh Thường",
            description="Tấn công cơ bản gây sát thương vật lý",
            mana_cost=0,
            cooldown=0,
            skill_type=SkillType.DAMAGE,
            target_type=TargetType.SINGLE_ENEMY,
            damage_multiplier=1.0,
            element=None  # Neutral
        )
        
        # === Damage Skills - Single Target ===
        
        self._templates["manh_ho_xung_phong"] = SkillTemplate(
            template_id="manh_ho_xung_phong",
            name="Mãnh Hổ Xung Phong",
            description="Xông vào địch như mãnh hổ, gây sát thương lớn cho một mục tiêu",
            mana_cost=50,
            cooldown=2,
            skill_type=SkillType.DAMAGE,
            target_type=TargetType.SINGLE_ENEMY,
            damage_multiplier=1.8,
            element=None
        )
        
        self._templates["phuong_thien_hoat_kich"] = SkillTemplate(
            template_id="phuong_thien_hoat_kich",
            name="Phương Thiên Hoạt Kích",
            description="Múa kích tung hoành, gây sát thương chí mạng cho một mục tiêu",
            mana_cost=80,
            cooldown=3,
            skill_type=SkillType.DAMAGE,
            target_type=TargetType.SINGLE_ENEMY,
            damage_multiplier=2.5,
            element=Element.HOA
        )
        
        self._templates["bach_phat_bach_trung"] = SkillTemplate(
            template_id="bach_phat_bach_trung",
            name="Bách Phát Bách Trúng",
            description="Bắn tên chính xác, luôn trúng yếu huyệt địch",
            mana_cost=60,
            cooldown=2,
            skill_type=SkillType.DAMAGE,
            target_type=TargetType.SINGLE_ENEMY,
            damage_multiplier=2.0,
            element=Element.KIM
        )
        
        self._templates["do_nhat_ngan_kim"] = SkillTemplate(
            template_id="do_nhat_ngan_kim",
            name="Độ Nhất Ngạn Kim",
            description="Đao pháp sắc bén, cắt ngang thép gai",
            mana_cost=55,
            cooldown=2,
            skill_type=SkillType.DAMAGE,
            target_type=TargetType.SINGLE_ENEMY,
            damage_multiplier=1.9,
            element=Element.KIM
        )
        
        # === Damage Skills - AOE ===
        
        self._templates["long_tran_hao"] = SkillTemplate(
            template_id="long_tran_hao",
            name="Long Trần Hào",
            description="Múa đao Thanh Long, gây sát thương diện rộng",
            mana_cost=100,
            cooldown=3,
            skill_type=SkillType.DAMAGE,
            target_type=TargetType.ALL_ENEMIES,
            damage_multiplier=1.5,
            element=Element.KIM,
            aoe_range=1
        )
        
        self._templates["truong_ba_xa_mau"] = SkillTemplate(
            template_id="truong_ba_xa_mau",
            name="Trương Bá Xà Mâu",
            description="Xà Mâu quét ngang, gây sát thương và hỗn loạn địch",
            mana_cost=90,
            cooldown=3,
            skill_type=SkillType.DAMAGE,
            target_type=TargetType.ALL_ENEMIES,
            damage_multiplier=1.4,
            element=Element.HOA,
            aoe_range=1
        )
        
        self._templates["xich_bich_dai_chien"] = SkillTemplate(
            template_id="xich_bich_dai_chien",
            name="Xích Bích Đại Chiến",
            description="Ngọn lửa Xích Bích thiêu đốt toàn bộ địch",
            mana_cost=120,
            cooldown=4,
            skill_type=SkillType.DAMAGE,
            target_type=TargetType.ALL_ENEMIES,
            damage_multiplier=1.8,
            element=Element.HOA,
            aoe_range=2
        )
        
        self._templates["bat_quai_tran"] = SkillTemplate(
            template_id="bat_quai_tran",
            name="Bát Quái Trận",
            description="Bày trận bát quái, gây sát thương và làm chậm địch",
            mana_cost=80,
            cooldown=3,
            skill_type=SkillType.DAMAGE,
            target_type=TargetType.ALL_ENEMIES,
            damage_multiplier=1.3,
            element=Element.THUY,
            debuff_effects={"spd": -20},
            duration=2,
            aoe_range=1
        )
        
        self._templates["tay_luong_thiet_ky"] = SkillTemplate(
            template_id="tay_luong_thiet_ky",
            name="Tây Lương Thiết Kỵ",
            description="Xung phong thiết kỵ, gây sát thương và đẩy lùi địch",
            mana_cost=85,
            cooldown=3,
            skill_type=SkillType.DAMAGE,
            target_type=TargetType.ALL_ENEMIES,
            damage_multiplier=1.4,
            element=Element.THO,
            aoe_range=1
        )
        
        # === Healing Skills ===
        
        self._templates["thien_khi"] = SkillTemplate(
            template_id="thien_khi",
            name="Thiên Khí",
            description="Thu hồi thiên khí, hồi phục HP cho đồng đội",
            mana_cost=80,
            cooldown=2,
            skill_type=SkillType.HEAL,
            target_type=TargetType.ALL_ALLIES,
            heal_multiplier=0.3,  # 30% max HP
            element=Element.THUY
        )
        
        self._templates["nhan_duc"] = SkillTemplate(
            template_id="nhan_duc",
            name="Nhân Đức",
            description="Đức độ lan tỏa, hồi phục HP và tăng sĩ khí",
            mana_cost=70,
            cooldown=3,
            skill_type=SkillType.HEAL,
            target_type=TargetType.ALL_ALLIES,
            heal_multiplier=0.25,
            element=Element.MOC,
            buff_stats={"atk": 10},
            duration=2
        )
        
        self._templates["hoi_phuc_don"] = SkillTemplate(
            template_id="hoi_phuc_don",
            name="Hồi Phục Đơn",
            description="Hồi phục HP cho một đồng đội",
            mana_cost=40,
            cooldown=1,
            skill_type=SkillType.HEAL,
            target_type=TargetType.SINGLE_ALLY,
            heal_multiplier=0.4,
            element=None
        )
        
        # === Buff Skills ===
        
        self._templates["co_vu_si_khi"] = SkillTemplate(
            template_id="co_vu_si_khi",
            name="Cổ Vũ Sĩ Khí",
            description="Tăng sĩ khí toàn đội, tăng ATK và CRIT",
            mana_cost=60,
            cooldown=3,
            skill_type=SkillType.BUFF,
            target_type=TargetType.ALL_ALLIES,
            buff_stats={"atk": 20, "crit": 15},
            duration=3,
            element=None
        )
        
        self._templates["thich_tho_trung_thien"] = SkillTemplate(
            template_id="thich_tho_trung_thien",
            name="Thích Thổ Trung Thiên",
            description="Tăng phòng thủ và HP cho bản thân",
            mana_cost=50,
            cooldown=2,
            skill_type=SkillType.BUFF,
            target_type=TargetType.SELF,
            buff_stats={"def_": 30, "hp": 200},
            duration=3,
            element=Element.THO
        )
        
        self._templates["dong_ngo_chinh_phuc"] = SkillTemplate(
            template_id="dong_ngo_chinh_phuc",
            name="Đông Ngô Chinh Phục",
            description="Lệnh chinh phục, tăng sức mạnh toàn đội",
            mana_cost=70,
            cooldown=3,
            skill_type=SkillType.BUFF,
            target_type=TargetType.ALL_ALLIES,
            buff_stats={"atk": 15, "def_": 15, "spd": 10},
            duration=2,
            element=Element.MOC
        )
        
        self._templates["quan_thao_kinh_luoc"] = SkillTemplate(
            template_id="quan_thao_kinh_luoc",
            name="Quản Thao Kinh Lược",
            description="Chiến lược tài tình, tăng SPD và DEX toàn đội",
            mana_cost=65,
            cooldown=3,
            skill_type=SkillType.BUFF,
            target_type=TargetType.ALL_ALLIES,
            buff_stats={"spd": 25, "dex": 15},
            duration=2,
            element=Element.THUY
        )
        
        # === Debuff Skills ===
        
        self._templates["khi_the_ap_dao"] = SkillTemplate(
            template_id="khi_the_ap_dao",
            name="Khí Thế Áp Đảo",
            description="Áp đảo tinh thần, giảm ATK và DEF địch",
            mana_cost=55,
            cooldown=2,
            skill_type=SkillType.DEBUFF,
            target_type=TargetType.ALL_ENEMIES,
            debuff_effects={"atk": -15, "def_": -15},
            duration=2,
            element=None
        )
        
        self._templates["bi_nguyet_tu_hoa"] = SkillTemplate(
            template_id="bi_nguyet_tu_hoa",
            name="Bí Nguyệt Tu Hoa",
            description="Mỹ nhân kế, làm mê hoặc và giảm tốc địch",
            mana_cost=60,
            cooldown=3,
            skill_type=SkillType.DEBUFF,
            target_type=TargetType.ALL_ENEMIES,
            debuff_effects={"spd": -30, "crit": -10},
            duration=2,
            element=Element.THUY
        )
        
        self._templates["hoa_cong"] = SkillTemplate(
            template_id="hoa_cong",
            name="Hỏa Công",
            description="Phóng hỏa, gây sát thương theo thời gian",
            mana_cost=70,
            cooldown=3,
            skill_type=SkillType.DEBUFF,
            target_type=TargetType.ALL_ENEMIES,
            debuff_effects={"dot": 50},  # Damage over time
            duration=3,
            element=Element.HOA
        )
    
    def get_template(self, template_id: str) -> Optional[SkillTemplate]:
        """
        Get a skill template by ID.
        
        Args:
            template_id: Template identifier
            
        Returns:
            SkillTemplate if found, None otherwise
        """
        return self._templates.get(template_id)
    
    def get_all_templates(self) -> List[SkillTemplate]:
        """
        Get all available skill templates.
        
        Returns:
            List of all SkillTemplate instances
        """
        return list(self._templates.values())
    
    def get_skills_by_type(self, skill_type: SkillType) -> List[SkillTemplate]:
        """
        Get all skill templates of a specific type.
        
        Args:
            skill_type: Type to filter by
            
        Returns:
            List of matching SkillTemplate instances
        """
        return [t for t in self._templates.values() if t.skill_type == skill_type]
    
    def get_skills_by_element(self, element: Element) -> List[SkillTemplate]:
        """
        Get all skill templates with a specific element.
        
        Args:
            element: Element to filter by
            
        Returns:
            List of matching SkillTemplate instances
        """
        return [t for t in self._templates.values() if t.element == element]
    
    def create_skill(self, template_id: str) -> ActiveSkill:
        """
        Create a new Skill instance from a template.
        
        Args:
            template_id: ID of the template to use
            
        Returns:
            New ActiveSkill instance
            
        Raises:
            ValueError: If template not found
        """
        template = self.get_template(template_id)
        if not template:
            raise ValueError(f"Skill template not found: {template_id}")
        
        skill = ActiveSkill(
            id=str(uuid4()),
            name=template.name,
            description=template.description,
            mana_cost=template.mana_cost,
            cooldown=template.cooldown,
            skill_type=template.skill_type,
            target_type=template.target_type,
            damage_multiplier=template.damage_multiplier,
            heal_multiplier=template.heal_multiplier,
            element=template.element,
            buff_stats=template.buff_stats.copy(),
            debuff_effects=template.debuff_effects.copy(),
            duration=template.duration,
            aoe_range=template.aoe_range
        )
        
        return skill
