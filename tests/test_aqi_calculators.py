"""
Test suite for the AQI calculators module.
Tests all pollutant conversion functions (PM2.5, PM10, NO2, SO2, CO, O3).
"""

import pytest
from unittest.mock import Mock
from module.core.aqi_calculators import (
    calculate_all_aqi_values,
    PM25,
    PM10,
    NO2,
    SO2,
    CO,
    O3
)


@pytest.fixture
def mock_components():
    """Fixture that provides a mock Components object with default values."""
    components = Mock()
    components.pm2_5 = 0
    components.pm10 = 0
    components.no2 = 0
    components.so2 = 0
    components.co = 0
    components.o3 = 0
    return components


@pytest.fixture
def mock_components_normal_air():
    """Fixture that provides a Components object with normal air quality values."""
    components = Mock()
    components.pm2_5 = 15
    components.pm10 = 50
    components.no2 = 30
    components.so2 = 20
    components.co = 500  # µg/m³
    components.o3 = 50
    return components


@pytest.fixture
def mock_components_poor_air():
    """Fixture that provides a Components object with poor air quality values."""
    components = Mock()
    components.pm2_5 = 200
    components.pm10 = 400
    components.no2 = 300
    components.so2 = 1500
    components.co = 15000  # µg/m³
    components.o3 = 600
    return components


@pytest.fixture
def mock_components_hazardous_air():
    """Fixture that provides a Components object with hazardous air quality values."""
    components = Mock()
    components.pm2_5 = 400
    components.pm10 = 600
    components.no2 = 600
    components.so2 = 3000
    components.co = 60000  # µg/m³
    components.o3 = 1500
    return components


class TestCalculateAllAQIValues:
    """Test the calculate_all_aqi_values function."""

    def test_returns_list_of_six_values(self, mock_components):
        """Test that the function returns a list of 6 AQI values."""
        result = calculate_all_aqi_values(mock_components)
        assert isinstance(result, list)
        assert len(result) == 6

    def test_with_zero_values(self, mock_components):
        """Test with all zero concentration values."""
        result = calculate_all_aqi_values(mock_components)
        assert all(v >= 0 for v in result)

    def test_with_normal_values(self, mock_components_normal_air):
        """Test with normal air quality values."""
        result = calculate_all_aqi_values(mock_components_normal_air)
        # All values should be in a reasonable range (0-500)
        assert all(0 <= v <= 500 for v in result)

    def test_with_poor_values(self, mock_components_poor_air):
        """Test with poor air quality values."""
        result = calculate_all_aqi_values(mock_components_poor_air)
        assert all(0 <= v <= 500 for v in result)

    def test_with_hazardous_values(self, mock_components_hazardous_air):
        """Test with hazardous air quality values."""
        result = calculate_all_aqi_values(mock_components_hazardous_air)
        assert all(0 <= v <= 500 for v in result)


class TestPM25:
    """Test PM2.5 AQI calculation."""

    def test_pm25_zero_value(self):
        """Test PM2.5 with zero concentration."""
        result = PM25(0)
        assert result == 0.0

    def test_pm25_low_range(self):
        """Test PM2.5 in low concentration range (0-30)."""
        result = PM25(15)
        assert 0 <= result <= 50
        # At 15: AQI = 15 * (50/30) = 25.0
        assert result == 25.0

    def test_pm25_moderate_range(self):
        """Test PM2.5 in moderate range (30-60)."""
        result = PM25(45)
        assert 50 <= result <= 100
        # At 45: AQI = 50 + (45-30)*(50/30) = 50 + 25 = 75.0
        assert result == 75.0

    def test_pm25_unhealthy_range(self):
        """Test PM2.5 in unhealthy range (60-90)."""
        result = PM25(75)
        assert 100 <= result <= 200
        # At 75: AQI = 100 + (75-60)*(100/30) = 100 + 50 = 150.0
        assert result == 150.0

    def test_pm25_very_unhealthy_range(self):
        """Test PM2.5 in very unhealthy range (90-120)."""
        result = PM25(105)
        assert 200 <= result <= 300
        # At 105: AQI = 200 + (105-90)*(100/30) = 200 + 50 = 250.0
        assert result == 250.0

    def test_pm25_hazardous_range1(self):
        """Test PM2.5 in hazardous range (120-250)."""
        result = PM25(185)
        assert 300 <= result <= 400

    def test_pm25_hazardous_range2(self):
        """Test PM2.5 in hazardous range (250-380)."""
        result = PM25(315)
        assert 400 <= result <= 500

    def test_pm25_extreme_high(self):
        """Test PM2.5 with extremely high concentration."""
        result = PM25(500)
        assert result == 500

    def test_pm25_boundary_values(self):
        """Test PM2.5 at boundary values."""
        assert PM25(30) <= 50
        assert PM25(60) >= 100
        assert PM25(90) >= 200
        assert PM25(120) >= 300

    def test_pm25_returns_float(self):
        """Test that PM25 returns a float."""
        result = PM25(25)
        assert isinstance(result, float)


class TestPM10:
    """Test PM10 AQI calculation."""

    def test_pm10_zero_value(self):
        """Test PM10 with zero concentration."""
        result = PM10(0)
        assert result == 0.0

    def test_pm10_low_range(self):
        """Test PM10 in low range (0-100)."""
        result = PM10(50)
        # At 50: AQI = 50
        assert result == 50.0

    def test_pm10_moderate_range(self):
        """Test PM10 in moderate range (100-250)."""
        result = PM10(175)
        assert 100 <= result <= 200
        # At 175: AQI = 100 + (175-100)*(100/150) = 100 + 50 = 150.0
        assert result == 150.0

    def test_pm10_unhealthy_range(self):
        """Test PM10 in unhealthy range (250-350)."""
        result = PM10(300)
        assert 200 <= result <= 300
        # At 300: AQI = 200 + (300-250) = 200 + 50 = 250.0
        assert result == 250.0

    def test_pm10_very_unhealthy_range(self):
        """Test PM10 in very unhealthy range (350-430)."""
        result = PM10(390)
        assert 300 <= result <= 400

    def test_pm10_hazardous_range(self):
        """Test PM10 in hazardous range (430-510)."""
        result = PM10(470)
        assert 400 <= result <= 500

    def test_pm10_extreme_high(self):
        """Test PM10 with extremely high concentration."""
        result = PM10(600)
        assert result == 500

    def test_pm10_boundary_values(self):
        """Test PM10 at boundary values."""
        assert PM10(100) <= 100
        assert PM10(250) >= 100
        assert PM10(350) >= 200
        assert PM10(430) >= 300

    def test_pm10_returns_float(self):
        """Test that PM10 returns a float."""
        result = PM10(150)
        assert isinstance(result, float)


class TestNO2:
    """Test NO2 AQI calculation."""

    def test_no2_zero_value(self):
        """Test NO2 with zero concentration."""
        result = NO2(0)
        assert result == 0.0

    def test_no2_low_range(self):
        """Test NO2 in low range (0-40)."""
        result = NO2(20)
        assert 0 <= result <= 50
        # At 20: AQI = 20 * (50/40) = 25.0
        assert result == 25.0

    def test_no2_moderate_range(self):
        """Test NO2 in moderate range (40-80)."""
        result = NO2(60)
        assert 50 <= result <= 100
        # At 60: AQI = 50 + (60-40)*(50/40) = 50 + 25 = 75.0
        assert result == 75.0

    def test_no2_unhealthy_range(self):
        """Test NO2 in unhealthy range (80-180)."""
        result = NO2(130)
        assert 100 <= result <= 200
        # At 130: AQI = 100 + (130-80) = 100 + 50 = 150.0
        assert result == 150.0

    def test_no2_very_unhealthy_range(self):
        """Test NO2 in very unhealthy range (180-280)."""
        result = NO2(230)
        assert 200 <= result <= 300

    def test_no2_hazardous_range(self):
        """Test NO2 in hazardous range above 400."""
        result = NO2(450)
        assert 400 <= result <= 500

    def test_no2_extreme_high(self):
        """Test NO2 with extremely high concentration."""
        result = NO2(600)
        assert result == 500

    def test_no2_returns_float(self):
        """Test that NO2 returns a float."""
        result = NO2(40)
        assert isinstance(result, float)


class TestSO2:
    """Test SO2 AQI calculation."""

    def test_so2_zero_value(self):
        """Test SO2 with zero concentration."""
        result = SO2(0)
        assert result == 0.0

    def test_so2_low_range(self):
        """Test SO2 in low range (0-40)."""
        result = SO2(20)
        assert 0 <= result <= 50
        # At 20: AQI = 20 * (50/40) = 25.0
        assert result == 25.0

    def test_so2_moderate_range(self):
        """Test SO2 in moderate range (40-80)."""
        result = SO2(60)
        assert 50 <= result <= 100
        # At 60: AQI = 50 + (60-40)*(50/40) = 50 + 25 = 75.0
        assert result == 75.0

    def test_so2_unhealthy_range(self):
        """Test SO2 in unhealthy range (80-380)."""
        result = SO2(230)
        assert 100 <= result <= 200

    def test_so2_very_unhealthy_range(self):
        """Test SO2 in very unhealthy range (380-800)."""
        result = SO2(590)
        assert 200 <= result <= 300

    def test_so2_hazardous_range(self):
        """Test SO2 in hazardous range (1600-2400)."""
        result = SO2(2000)
        assert 400 <= result <= 500

    def test_so2_extreme_high(self):
        """Test SO2 with extremely high concentration."""
        result = SO2(3000)
        assert result == 500

    def test_so2_returns_float(self):
        """Test that SO2 returns a float."""
        result = SO2(40)
        assert isinstance(result, float)


class TestCO:
    """Test CO AQI calculation."""

    def test_co_zero_value(self):
        """Test CO with zero concentration."""
        result = CO(0)
        assert result == 0.0

    def test_co_low_range(self):
        """Test CO in low range (0-1 mg/m³)."""
        # 500 µg/m³ = 0.5 mg/m³
        result = CO(500)
        assert 0 <= result <= 50
        # At 0.5: AQI = 0.5 * 50 = 25.0
        assert result == 25.0

    def test_co_moderate_range(self):
        """Test CO in moderate range (1-2 mg/m³)."""
        # 1500 µg/m³ = 1.5 mg/m³
        result = CO(1500)
        assert 50 <= result <= 100

    def test_co_unhealthy_range(self):
        """Test CO in unhealthy range (2-10 mg/m³)."""
        # 6000 µg/m³ = 6 mg/m³
        result = CO(6000)
        assert 100 <= result <= 200

    def test_co_very_unhealthy_range(self):
        """Test CO in very unhealthy range (10-17 mg/m³)."""
        # 13500 µg/m³ = 13.5 mg/m³
        result = CO(13500)
        assert 200 <= result <= 300

    def test_co_hazardous_range1(self):
        """Test CO in hazardous range (17-34 mg/m³)."""
        # 25500 µg/m³ = 25.5 mg/m³
        result = CO(25500)
        assert 300 <= result <= 400

    def test_co_hazardous_range2(self):
        """Test CO in hazardous range (34-51 mg/m³)."""
        # 42500 µg/m³ = 42.5 mg/m³
        result = CO(42500)
        assert 400 <= result <= 500

    def test_co_extreme_high(self):
        """Test CO with extremely high concentration."""
        result = CO(100000)
        assert result == 500

    def test_co_unit_conversion(self):
        """Test that CO properly converts from µg/m³ to mg/m³."""
        # 1000 µg/m³ should be 1 mg/m³
        result = CO(1000)
        # At 1 mg/m³: AQI = 1 * 50 = 50.0
        assert result == 50.0

    def test_co_returns_float(self):
        """Test that CO returns a float."""
        result = CO(500)
        assert isinstance(result, float)


class TestO3:
    """Test O3 AQI calculation."""

    def test_o3_zero_value(self):
        """Test O3 with zero concentration."""
        result = O3(0)
        assert result == 0.0

    def test_o3_low_range(self):
        """Test O3 in low range (0-100)."""
        result = O3(50)
        # At 50: AQI = 50
        assert result == 50.0

    def test_o3_moderate_range(self):
        """Test O3 in moderate range (100-168)."""
        result = O3(134)
        assert 100 <= result <= 200
        # At 134: AQI = 100 + (134-100)*(100/68) = 100 + 50 ≈ 150.0
        assert 140 <= result <= 160

    def test_o3_unhealthy_range(self):
        """Test O3 in unhealthy range (168-208)."""
        result = O3(188)
        assert 200 <= result <= 300
        # At 188: AQI = 200 + (188-168)*(100/40) = 200 + 50 = 250.0
        assert result == 250.0

    def test_o3_very_unhealthy_range(self):
        """Test O3 in very unhealthy range (208-748)."""
        result = O3(478)
        assert 300 <= result <= 400

    def test_o3_hazardous_range(self):
        """Test O3 in hazardous range (748-1288)."""
        result = O3(1018)
        assert 400 <= result <= 500

    def test_o3_extreme_high(self):
        """Test O3 with extremely high concentration."""
        result = O3(2000)
        assert result == 500

    def test_o3_boundary_100(self):
        """Test O3 at boundary value 100."""
        result = O3(100)
        assert result == 100.0

    def test_o3_boundary_168(self):
        """Test O3 at boundary value 168."""
        result = O3(168)
        # At 168: AQI = 100 + (168-100)*(100/68) = 100 + 100 = 200.0
        assert result == 200.0

    def test_o3_boundary_208(self):
        """Test O3 at boundary value 208."""
        result = O3(208)
        # At 208: AQI = 200 + (208-168)*(100/40) = 200 + 100 = 300.0
        assert result == 300.0

    def test_o3_returns_number(self):
        """Test that O3 returns a number (int or float)."""
        result = O3(75)
        assert isinstance(result, (int, float))


class TestAQIValueRanges:
    """Test that AQI values stay within valid ranges (0-500)."""

    @pytest.mark.parametrize("value", [0, 50, 100, 150, 200, 250, 300, 350, 400, 500, 1000])
    def test_pm25_range(self, value):
        """Test PM25 AQI stays in valid range."""
        result = PM25(value)
        assert 0 <= result <= 500

    @pytest.mark.parametrize("value", [0, 50, 100, 200, 300, 400, 500, 600, 800])
    def test_pm10_range(self, value):
        """Test PM10 AQI stays in valid range."""
        result = PM10(value)
        assert 0 <= result <= 500

    @pytest.mark.parametrize("value", [0, 50, 100, 200, 300, 400, 500, 600])
    def test_no2_range(self, value):
        """Test NO2 AQI stays in valid range."""
        result = NO2(value)
        assert 0 <= result <= 500

    @pytest.mark.parametrize("value", [0, 50, 100, 500, 1000, 2000, 3000, 4000])
    def test_so2_range(self, value):
        """Test SO2 AQI stays in valid range."""
        result = SO2(value)
        assert 0 <= result <= 500

    @pytest.mark.parametrize("value", [0, 500, 1000, 5000, 10000, 50000, 100000])
    def test_co_range(self, value):
        """Test CO AQI stays in valid range."""
        result = CO(value)
        assert 0 <= result <= 500

    @pytest.mark.parametrize("value", [0, 50, 100, 200, 500, 1000, 1500, 2000])
    def test_o3_range(self, value):
        """Test O3 AQI stays in valid range."""
        result = O3(value)
        assert 0 <= result <= 500


class TestAQIMonotonicity:
    """Test that AQI values increase monotonically with pollutant concentration."""

    def test_pm25_monotonic(self):
        """Test that PM25 AQI increases with concentration."""
        values = [PM25(v) for v in [0, 30, 60, 90, 120, 250, 380]]
        for i in range(len(values) - 1):
            assert values[i] <= values[i + 1], f"PM25 not monotonic at indices {i}, {i+1}"

    def test_pm10_monotonic(self):
        """Test that PM10 AQI increases with concentration."""
        values = [PM10(v) for v in [0, 100, 250, 350, 430, 510]]
        for i in range(len(values) - 1):
            assert values[i] <= values[i + 1], f"PM10 not monotonic at indices {i}, {i+1}"

    def test_no2_monotonic(self):
        """Test that NO2 AQI increases with concentration."""
        values = [NO2(v) for v in [0, 40, 80, 180, 280, 400, 510]]
        for i in range(len(values) - 1):
            assert values[i] <= values[i + 1], f"NO2 not monotonic at indices {i}, {i+1}"

    def test_so2_monotonic(self):
        """Test that SO2 AQI increases with concentration."""
        values = [SO2(v) for v in [0, 40, 80, 380, 800, 1600, 2400]]
        for i in range(len(values) - 1):
            assert values[i] <= values[i + 1], f"SO2 not monotonic at indices {i}, {i+1}"

    def test_co_monotonic(self):
        """Test that CO AQI increases with concentration."""
        values = [CO(v) for v in [0, 500, 1000, 5000, 10000, 20000, 40000, 60000]]
        for i in range(len(values) - 1):
            assert values[i] <= values[i + 1], f"CO not monotonic at indices {i}, {i+1}"

    def test_o3_monotonic(self):
        """Test that O3 AQI increases with concentration."""
        values = [O3(v) for v in [0, 100, 168, 208, 748, 1288, 2000]]
        for i in range(len(values) - 1):
            assert values[i] <= values[i + 1], f"O3 not monotonic at indices {i}, {i+1}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
