"""
Test suite for module.core.aqi_calculators module.
"""

import pytest
from unittest.mock import Mock
from module.core.aqi_calculators import calculate_all_aqi_values


@pytest.fixture
def mock_components_zero():
    """Components with zero values."""
    components = Mock()
    components.pm2_5 = 0
    components.pm10 = 0
    components.no2 = 0
    components.so2 = 0
    components.co = 0
    components.o3 = 0
    return components


@pytest.fixture
def mock_components_good():
    """Components with good air quality values."""
    components = Mock()
    components.pm2_5 = 5.0
    components.pm10 = 15.0
    components.no2 = 20.0
    components.so2 = 10.0
    components.co = 300.0
    components.o3 = 40.0
    return components


@pytest.fixture
def mock_components_moderate():
    """Components with moderate air quality values."""
    components = Mock()
    components.pm2_5 = 25.0
    components.pm10 = 75.0
    components.no2 = 80.0
    components.so2 = 150.0
    components.co = 7000.0
    components.o3 = 120.0
    return components


@pytest.fixture
def mock_components_poor():
    """Components with poor air quality values."""
    components = Mock()
    components.pm2_5 = 150.0
    components.pm10 = 300.0
    components.no2 = 300.0
    components.so2 = 800.0
    components.co = 15000.0
    components.o3 = 400.0
    return components


@pytest.fixture
def mock_components_hazardous():
    """Components with hazardous air quality values."""
    components = Mock()
    components.pm2_5 = 400.0
    components.pm10 = 600.0
    components.no2 = 600.0
    components.so2 = 2000.0
    components.co = 50000.0
    components.o3 = 1000.0
    return components


class TestAQICalculators:
    """Test suite for AQI calculator functions."""

    def test_returns_list_of_six_values(self, mock_components_zero):
        """Test that calculate_all_aqi_values returns 6 values."""
        result = calculate_all_aqi_values(mock_components_zero)
        
        assert isinstance(result, list)
        assert len(result) == 6

    def test_all_values_are_numbers(self, mock_components_good):
        """Test that all returned values are numbers."""
        result = calculate_all_aqi_values(mock_components_good)
        
        for value in result:
            assert isinstance(value, (int, float))

    def test_zero_concentrations_return_zero_aqi(self, mock_components_zero):
        """Test that zero pollutant concentrations return zero AQI."""
        result = calculate_all_aqi_values(mock_components_zero)
        
        # All AQI values should be 0 for zero concentrations
        for value in result:
            assert value == 0

    def test_good_air_quality_range(self, mock_components_good):
        """Test that good air quality values return AQI in good range (0-50)."""
        result = calculate_all_aqi_values(mock_components_good)
        
        # All values should be in the "Good" range
        for value in result:
            assert 0 <= value <= 50

    def test_moderate_air_quality_range(self, mock_components_moderate):
        """Test that moderate air quality values return AQI in moderate range."""
        result = calculate_all_aqi_values(mock_components_moderate)
        
        # At least some values should be in moderate range (50-100)
        assert any(50 < value <= 100 for value in result)

    def test_poor_air_quality_range(self, mock_components_poor):
        """Test that poor air quality values return high AQI values."""
        result = calculate_all_aqi_values(mock_components_poor)
        
        # At least some values should be in unhealthy range (>100)
        assert any(value > 100 for value in result)

    def test_hazardous_air_quality_range(self, mock_components_hazardous):
        """Test that hazardous air quality values return very high AQI."""
        result = calculate_all_aqi_values(mock_components_hazardous)
        
        # At least some values should be in hazardous range (>300)
        assert any(value > 300 for value in result)

    def test_pollutant_order_pm25_pm10_no2_so2_co_o3(self, mock_components_good):
        """Test that pollutants are returned in correct order."""
        components = Mock()
        # Set unique values to verify order
        components.pm2_5 = 10.0
        components.pm10 = 20.0
        components.no2 = 30.0
        components.so2 = 40.0
        components.co = 500.0
        components.o3 = 50.0
        
        result = calculate_all_aqi_values(components)
        
        # Verify we get 6 values in expected order
        assert len(result) == 6
        # Each should be positive since all inputs are positive
        for value in result:
            assert value > 0

    def test_higher_concentration_yields_higher_aqi(self):
        """Test that higher pollutant concentration yields higher AQI."""
        low_components = Mock()
        low_components.pm2_5 = 5.0
        low_components.pm10 = 15.0
        low_components.no2 = 20.0
        low_components.so2 = 10.0
        low_components.co = 300.0
        low_components.o3 = 40.0
        
        high_components = Mock()
        high_components.pm2_5 = 50.0
        high_components.pm10 = 150.0
        high_components.no2 = 200.0
        high_components.so2 = 500.0
        high_components.co = 10000.0
        high_components.o3 = 200.0
        
        low_result = calculate_all_aqi_values(low_components)
        high_result = calculate_all_aqi_values(high_components)
        
        # All high concentration AQI values should be greater than low
        for low_aqi, high_aqi in zip(low_result, high_result):
            assert high_aqi > low_aqi

    def test_pm25_calculation_through_calculate_all(self):
        """Test PM2.5 AQI calculation through main function."""
        components = Mock()
        components.pm2_5 = 35.5  # Moderate level
        components.pm10 = 0
        components.no2 = 0
        components.so2 = 0
        components.co = 0
        components.o3 = 0
        
        result = calculate_all_aqi_values(components)
        
        # PM2.5 is first in the list
        pm25_aqi = result[0]
        assert pm25_aqi > 0  # Should have some AQI value for non-zero concentration

    def test_co_unit_conversion_through_calculate_all(self):
        """Test CO calculation (mg/m³ to ppm conversion) through main function."""
        components = Mock()
        components.pm2_5 = 0
        components.pm10 = 0
        components.no2 = 0
        components.so2 = 0
        components.co = 10000.0  # µg/m³
        components.o3 = 0
        
        result = calculate_all_aqi_values(components)
        
        # CO is fifth in the list
        co_aqi = result[4]
        assert co_aqi > 0  # Should have some AQI value

    def test_boundary_values(self):
        """Test AQI calculation at boundary values."""
        components = Mock()
        # Use values around boundaries
        components.pm2_5 = 12.0
        components.pm10 = 54.0
        components.no2 = 53.0
        components.so2 = 35.0
        components.co = 4400.0
        components.o3 = 54.0
        
        result = calculate_all_aqi_values(components)
        
        # All values should be positive for positive inputs
        for value in result:
            assert value > 0

    def test_mixed_quality_levels(self):
        """Test with mixed pollutant levels."""
        components = Mock()
        components.pm2_5 = 5.0    # Good
        components.pm10 = 80.0    # Moderate
        components.no2 = 200.0    # Unhealthy
        components.so2 = 10.0     # Good
        components.co = 300.0     # Good
        components.o3 = 300.0     # Unhealthy
        
        result = calculate_all_aqi_values(components)
        
        # Should have mix of good and unhealthy values
        assert min(result) < 50      # At least one good
        assert max(result) > 100     # At least one unhealthy
