"""
Tests for HexagonStats Value Object
Following TDD approach - tests written first
"""
import pytest
from app.domain.value_objects.hexagon_stats import HexagonStats


class TestHexagonStatsCreation:
    """Test HexagonStats initialization"""
    
    def test_create_with_all_stats(self):
        """Should create stats with all six attributes"""
        stats = HexagonStats(
            hp=1000,
            atk=100,
            def_=80,
            spd=95,
            crit=15,
            dex=20
        )
        assert stats.hp == 1000
        assert stats.atk == 100
        assert stats.def_ == 80
        assert stats.spd == 95
        assert stats.crit == 15
        assert stats.dex == 20
    
    def test_create_with_default_values(self):
        """Should create stats with default values"""
        stats = HexagonStats.default()
        assert stats.hp == 100
        assert stats.atk == 10
        assert stats.def_ == 5
        assert stats.spd == 100
        assert stats.crit == 5
        assert stats.dex == 10
    
    def test_create_from_dict(self):
        """Should create stats from dictionary"""
        data = {
            "HP": 500,
            "ATK": 50,
            "DEF": 30,
            "SPD": 80,
            "CRIT": 10,
            "DEX": 15
        }
        stats = HexagonStats.from_dict(data)
        assert stats.hp == 500
        assert stats.atk == 50
        assert stats.def_ == 30
        assert stats.spd == 80
        assert stats.crit == 10
        assert stats.dex == 15
    
    def test_create_from_dict_with_missing_values_uses_defaults(self):
        """Should use defaults for missing keys"""
        data = {"HP": 200, "ATK": 30}
        stats = HexagonStats.from_dict(data)
        assert stats.hp == 200
        assert stats.atk == 30
        assert stats.def_ == 5  # default
        assert stats.spd == 100  # default


class TestHexagonStatsImmutability:
    """Test that HexagonStats is immutable"""
    
    def test_stats_are_frozen(self):
        """Should not allow attribute modification"""
        stats = HexagonStats(hp=100, atk=10, def_=5, spd=100, crit=5, dex=10)
        with pytest.raises((AttributeError, TypeError)):
            stats.hp = 200


class TestHexagonStatsCalculations:
    """Test HexagonStats calculation methods"""
    
    def test_get_total_power(self):
        """Should calculate sum of all stats"""
        stats = HexagonStats(hp=100, atk=50, def_=30, spd=60, crit=10, dex=20)
        assert stats.get_total_power() == 270
    
    def test_add_stats(self):
        """Should add two stats together"""
        stats1 = HexagonStats(hp=100, atk=50, def_=30, spd=60, crit=10, dex=20)
        stats2 = HexagonStats(hp=50, atk=25, def_=15, spd=30, crit=5, dex=10)
        result = stats1.add(stats2)
        
        assert result.hp == 150
        assert result.atk == 75
        assert result.def_ == 45
        assert result.spd == 90
        assert result.crit == 15
        assert result.dex == 30
    
    def test_add_returns_new_instance(self):
        """Add should return a new instance, not modify existing"""
        stats1 = HexagonStats(hp=100, atk=50, def_=30, spd=60, crit=10, dex=20)
        stats2 = HexagonStats(hp=50, atk=25, def_=15, spd=30, crit=5, dex=10)
        result = stats1.add(stats2)
        
        assert result is not stats1
        assert result is not stats2
        assert stats1.hp == 100  # Original unchanged
    
    def test_multiply_stats(self):
        """Should multiply all stats by factor"""
        stats = HexagonStats(hp=100, atk=50, def_=30, spd=60, crit=10, dex=20)
        result = stats.multiply(1.5)
        
        assert result.hp == 150
        assert result.atk == 75
        assert result.def_ == 45
        assert result.spd == 90
        assert result.crit == 15
        assert result.dex == 30
    
    def test_multiply_rounds_down(self):
        """Multiplication should result in integers (rounded down)"""
        stats = HexagonStats(hp=100, atk=50, def_=30, spd=60, crit=10, dex=20)
        result = stats.multiply(1.33)
        
        assert isinstance(result.hp, int)
        assert result.hp == 133


class TestHexagonStatsSerialization:
    """Test HexagonStats serialization"""
    
    def test_to_dict(self):
        """Should convert to dictionary"""
        stats = HexagonStats(hp=100, atk=50, def_=30, spd=60, crit=10, dex=20)
        data = stats.to_dict()
        
        assert data == {
            "HP": 100,
            "ATK": 50,
            "DEF": 30,
            "SPD": 60,
            "CRIT": 10,
            "DEX": 20
        }
    
    def test_round_trip_conversion(self):
        """Should survive dict -> object -> dict conversion"""
        original = {"HP": 500, "ATK": 100, "DEF": 80, "SPD": 95, "CRIT": 15, "DEX": 20}
        stats = HexagonStats.from_dict(original)
        result = stats.to_dict()
        assert result == original


class TestHexagonStatsEquality:
    """Test HexagonStats equality comparison"""
    
    def test_equal_stats_are_equal(self):
        """Two stats with same values should be equal"""
        stats1 = HexagonStats(hp=100, atk=50, def_=30, spd=60, crit=10, dex=20)
        stats2 = HexagonStats(hp=100, atk=50, def_=30, spd=60, crit=10, dex=20)
        assert stats1 == stats2
    
    def test_different_stats_are_not_equal(self):
        """Two stats with different values should not be equal"""
        stats1 = HexagonStats(hp=100, atk=50, def_=30, spd=60, crit=10, dex=20)
        stats2 = HexagonStats(hp=200, atk=50, def_=30, spd=60, crit=10, dex=20)
        assert stats1 != stats2
    
    def test_hash_for_equal_stats(self):
        """Equal stats should have same hash"""
        stats1 = HexagonStats(hp=100, atk=50, def_=30, spd=60, crit=10, dex=20)
        stats2 = HexagonStats(hp=100, atk=50, def_=30, spd=60, crit=10, dex=20)
        assert hash(stats1) == hash(stats2)
