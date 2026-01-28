"""
Tests for StatusEffect Value Object
Following TDD approach
"""
import pytest
from app.domain.value_objects.status_effect import StatusEffect, StatusEffectType


class TestStatusEffectCreation:
    """Test StatusEffect creation"""
    
    def test_create_buff_effect(self):
        """Should create a buff status effect"""
        effect = StatusEffect(
            id="atk_up",
            name="Attack Up",
            effect_type=StatusEffectType.BUFF,
            duration=3,
            stat_modifiers={"atk": 0.2}  # 20% ATK increase
        )
        
        assert effect.name == "Attack Up"
        assert effect.effect_type == StatusEffectType.BUFF
        assert effect.duration == 3
        assert effect.stat_modifiers["atk"] == 0.2
    
    def test_create_debuff_effect(self):
        """Should create a debuff status effect"""
        effect = StatusEffect(
            id="def_down",
            name="Defense Down",
            effect_type=StatusEffectType.DEBUFF,
            duration=2,
            stat_modifiers={"def_": -0.3}  # 30% DEF decrease
        )
        
        assert effect.name == "Defense Down"
        assert effect.effect_type == StatusEffectType.DEBUFF
        assert effect.stat_modifiers["def_"] == -0.3
    
    def test_create_dot_effect(self):
        """Should create a damage over time effect"""
        effect = StatusEffect(
            id="burn",
            name="Burning",
            effect_type=StatusEffectType.DOT,
            duration=3,
            damage_per_turn=100
        )
        
        assert effect.name == "Burning"
        assert effect.effect_type == StatusEffectType.DOT
        assert effect.damage_per_turn == 100
    
    def test_create_hot_effect(self):
        """Should create a heal over time effect"""
        effect = StatusEffect(
            id="regen",
            name="Regeneration",
            effect_type=StatusEffectType.HOT,
            duration=3,
            heal_per_turn=50
        )
        
        assert effect.name == "Regeneration"
        assert effect.effect_type == StatusEffectType.HOT
        assert effect.heal_per_turn == 50
    
    def test_create_stun_effect(self):
        """Should create a crowd control stun effect"""
        effect = StatusEffect(
            id="stun",
            name="Stunned",
            effect_type=StatusEffectType.CROWD_CONTROL,
            duration=1,
            prevents_action=True
        )
        
        assert effect.name == "Stunned"
        assert effect.effect_type == StatusEffectType.CROWD_CONTROL
        assert effect.prevents_action is True


class TestStatusEffectDuration:
    """Test StatusEffect duration mechanics"""
    
    def test_reduce_duration(self):
        """Duration should decrease each turn"""
        effect = StatusEffect(
            id="atk_up",
            name="Attack Up",
            effect_type=StatusEffectType.BUFF,
            duration=3
        )
        
        effect.reduce_duration()
        
        assert effect.duration == 2
    
    def test_effect_expired_when_duration_zero(self):
        """Effect should expire when duration reaches 0"""
        effect = StatusEffect(
            id="atk_up",
            name="Attack Up",
            effect_type=StatusEffectType.BUFF,
            duration=1
        )
        
        effect.reduce_duration()
        
        assert effect.is_expired() is True
    
    def test_effect_not_expired_with_duration(self):
        """Effect should not be expired when duration > 0"""
        effect = StatusEffect(
            id="atk_up",
            name="Attack Up",
            effect_type=StatusEffectType.BUFF,
            duration=2
        )
        
        assert effect.is_expired() is False


class TestStatusEffectStacking:
    """Test StatusEffect stacking behavior"""
    
    def test_stackable_effect_can_stack(self):
        """Stackable effects should allow multiple applications"""
        effect = StatusEffect(
            id="bleed",
            name="Bleeding",
            effect_type=StatusEffectType.DOT,
            duration=3,
            damage_per_turn=50,
            is_stackable=True,
            max_stacks=5
        )
        
        assert effect.is_stackable is True
        assert effect.max_stacks == 5
    
    def test_effect_starts_with_one_stack(self):
        """Effect should start with 1 stack"""
        effect = StatusEffect(
            id="bleed",
            name="Bleeding",
            effect_type=StatusEffectType.DOT,
            duration=3,
            is_stackable=True
        )
        
        assert effect.current_stacks == 1
    
    def test_add_stack_increases_count(self):
        """Adding stack should increase stack count"""
        effect = StatusEffect(
            id="bleed",
            name="Bleeding",
            effect_type=StatusEffectType.DOT,
            duration=3,
            damage_per_turn=50,
            is_stackable=True,
            max_stacks=5
        )
        
        effect.add_stack()
        
        assert effect.current_stacks == 2
    
    def test_cannot_exceed_max_stacks(self):
        """Stack count should not exceed max"""
        effect = StatusEffect(
            id="bleed",
            name="Bleeding",
            effect_type=StatusEffectType.DOT,
            duration=3,
            is_stackable=True,
            max_stacks=2
        )
        
        effect.add_stack()  # 2
        effect.add_stack()  # Still 2
        
        assert effect.current_stacks == 2
    
    def test_non_stackable_effect_refreshes_duration(self):
        """Non-stackable effect should refresh duration on reapply"""
        effect = StatusEffect(
            id="atk_up",
            name="Attack Up",
            effect_type=StatusEffectType.BUFF,
            duration=3,
            is_stackable=False
        )
        
        effect.reduce_duration()  # Duration = 2
        effect.refresh(5)  # Refresh with 5 turns
        
        assert effect.duration == 5


class TestStatusEffectTypes:
    """Test StatusEffect type behaviors"""
    
    def test_all_effect_types_exist(self):
        """All effect types should be defined"""
        assert StatusEffectType.BUFF is not None
        assert StatusEffectType.DEBUFF is not None
        assert StatusEffectType.DOT is not None
        assert StatusEffectType.HOT is not None
        assert StatusEffectType.CROWD_CONTROL is not None
        assert StatusEffectType.SHIELD is not None
    
    def test_buff_is_positive(self):
        """Buff should be a positive effect"""
        effect = StatusEffect(
            id="test",
            name="Test Buff",
            effect_type=StatusEffectType.BUFF,
            duration=1
        )
        
        assert effect.is_positive() is True
    
    def test_debuff_is_negative(self):
        """Debuff should be a negative effect"""
        effect = StatusEffect(
            id="test",
            name="Test Debuff",
            effect_type=StatusEffectType.DEBUFF,
            duration=1
        )
        
        assert effect.is_positive() is False
    
    def test_shield_effect_absorbs_damage(self):
        """Shield effect should have damage absorption"""
        effect = StatusEffect(
            id="shield",
            name="Protection",
            effect_type=StatusEffectType.SHIELD,
            duration=3,
            shield_amount=500
        )
        
        assert effect.shield_amount == 500


class TestStatusEffectCalculation:
    """Test StatusEffect value calculations"""
    
    def test_get_dot_damage_scales_with_stacks(self):
        """DOT damage should scale with stacks"""
        effect = StatusEffect(
            id="bleed",
            name="Bleeding",
            effect_type=StatusEffectType.DOT,
            duration=3,
            damage_per_turn=50,
            is_stackable=True,
            max_stacks=5
        )
        
        effect.add_stack()  # 2 stacks
        
        total_damage = effect.get_tick_damage()
        
        assert total_damage == 100  # 50 * 2 stacks
    
    def test_get_hot_heal_scales_with_stacks(self):
        """HOT heal should scale with stacks"""
        effect = StatusEffect(
            id="regen",
            name="Regeneration",
            effect_type=StatusEffectType.HOT,
            duration=3,
            heal_per_turn=50,
            is_stackable=True,
            max_stacks=3
        )
        
        effect.add_stack()  # 2 stacks
        
        total_heal = effect.get_tick_heal()
        
        assert total_heal == 100  # 50 * 2 stacks
