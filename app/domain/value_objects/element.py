"""
Element Value Object - Ngũ Hành System
Represents the Five Elements: Kim, Mộc, Thủy, Hỏa, Thổ
"""
from enum import Enum
from typing import Dict


class Element(Enum):
    """
    Ngũ Hành (Five Elements) enum with relationships.
    
    Tương Khắc (Conquering cycle):
    - Kim khắc Mộc (Metal conquers Wood)
    - Mộc khắc Thổ (Wood conquers Earth)
    - Thổ khắc Thủy (Earth conquers Water)
    - Thủy khắc Hỏa (Water conquers Fire)
    - Hỏa khắc Kim (Fire conquers Metal)
    """
    
    KIM = "Kim"      # Metal
    MOC = "Mộc"      # Wood
    THUY = "Thủy"    # Water
    HOA = "Hỏa"      # Fire
    THO = "Thổ"      # Earth
    
    def get_strong_against(self) -> "Element":
        """Return the element this element conquers (tương khắc)"""
        relationships: Dict[Element, Element] = {
            Element.KIM: Element.MOC,
            Element.MOC: Element.THO,
            Element.THO: Element.THUY,
            Element.THUY: Element.HOA,
            Element.HOA: Element.KIM,
        }
        return relationships[self]
    
    def get_weak_against(self) -> "Element":
        """Return the element this element is conquered by (bị khắc)"""
        relationships: Dict[Element, Element] = {
            Element.KIM: Element.HOA,
            Element.MOC: Element.KIM,
            Element.THO: Element.MOC,
            Element.THUY: Element.THO,
            Element.HOA: Element.THUY,
        }
        return relationships[self]
    
    def calculate_multiplier(self, defender: "Element") -> float:
        """
        Calculate damage multiplier based on element matchup.
        
        Args:
            defender: The defending element
            
        Returns:
            1.5 if attacker is strong against defender
            0.7 if attacker is weak against defender
            1.0 for neutral matchup
        """
        if self.get_strong_against() == defender:
            return 1.5  # Tương khắc - advantage
        elif self.get_weak_against() == defender:
            return 0.7  # Bị khắc - disadvantage
        return 1.0  # Neutral
    
    def get_color(self) -> str:
        """Return the hex color code for this element"""
        colors: Dict[Element, str] = {
            Element.KIM: "#FFD700",   # Gold
            Element.MOC: "#228B22",   # Forest Green
            Element.THUY: "#1E90FF",  # Dodger Blue
            Element.HOA: "#FF4500",   # Orange Red
            Element.THO: "#8B4513",   # Saddle Brown
        }
        return colors[self]
