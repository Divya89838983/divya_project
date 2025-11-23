"""
Test suite for module.core.air_quality_api module.
"""

import pytest
from unittest.mock import Mock, patch
import requests
from module.core.air_quality_api import read_pollution_data_from_api, convert_json_to_object
from module.core.air_quality_models import AirQualityResponse


@pytest.fixture
def valid_api_response():
    """Valid API response with realistic data."""
    return {
        "coord": {"lon": -93.62, "lat": 42.03},
        "list": [
            {
                "dt": 1700000000,
                "main": {"aqi": 2},
                "components": {
                    "co": 250.0, "no": 0.5, "no2": 10.0, "o3": 70.0,
                    "so2": 5.0, "pm2_5": 15.0, "pm10": 25.0, "nh3": 1.0
                }
            },
            {
                "dt": 1700003600,
                "main": {"aqi": 3},
                "components": {
                    "co": 300.0, "no": 1.0, "no2": 15.0, "o3": 80.0,
                    "so2": 10.0, "pm2_5": 25.0, "pm10": 35.0, "nh3": 2.0
                }
            }
        ]
    }


class TestAirQuality:
    """Test suite for air quality API functions."""

    @patch('module.core.air_quality_api.requests.get')
    def test_successful_api_call(self, mock_get, valid_api_response):
        """Test successful API call returns data."""
        mock_response = Mock()
        mock_response.json.return_value = valid_api_response
        mock_get.return_value = mock_response

        result = read_pollution_data_from_api(42.03, -93.62)

        assert result == valid_api_response
        assert "coord" in result
        assert "list" in result

    @patch('module.core.air_quality_api.requests.get')
    def test_api_url_format(self, mock_get, valid_api_response):
        """Test that API is called with correct URL format."""
        mock_response = Mock()
        mock_response.json.return_value = valid_api_response
        mock_get.return_value = mock_response

        lat, lon = 42.03, -93.62
        read_pollution_data_from_api(lat, lon)

        call_args = mock_get.call_args[0][0]
        assert f"lat={lat}" in call_args
        assert f"lon={lon}" in call_args
        assert "air_pollution/forecast" in call_args

    @patch('module.core.air_quality_api.requests.get')
    def test_handles_network_error(self, mock_get):
        """Test handling of network errors."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

        with pytest.raises(requests.exceptions.ConnectionError):
            read_pollution_data_from_api(42.03, -93.62)

    def test_returns_air_quality_response_object(self, valid_api_response):
        """Test that function returns AirQualityResponse object."""
        result = convert_json_to_object(valid_api_response)

        assert isinstance(result, AirQualityResponse)
        assert hasattr(result, 'coord')
        assert hasattr(result, 'list')

    def test_coordinates_and_components_accessible(self, valid_api_response):
        """Test that coordinates and pollutant components are accessible."""
        result = convert_json_to_object(valid_api_response)

        # Check coordinates
        assert result.coord.lat == 42.03
        assert result.coord.lon == -93.62

        # Check components
        first_item = result.list[0]
        assert first_item.components.co == 250.0
        assert first_item.components.pm2_5 == 15.0
        assert first_item.components.pm10 == 25.0

    def test_multiple_data_points(self, valid_api_response):
        """Test handling multiple data points in list."""
        result = convert_json_to_object(valid_api_response)

        assert len(result.list) == 2
        assert result.list[0].dt == 1700000000
        assert result.list[1].dt == 1700003600

    @patch('module.core.air_quality_api.requests.get')
    def test_full_workflow_api_to_object(self, mock_get, valid_api_response):
        """Test complete workflow from API call to object conversion."""
        mock_response = Mock()
        mock_response.json.return_value = valid_api_response
        mock_get.return_value = mock_response

        # Fetch data
        api_data = read_pollution_data_from_api(42.03, -93.62)
        
        # Convert to object
        result = convert_json_to_object(api_data)

        # Verify complete workflow works
        assert isinstance(result, AirQualityResponse)
        assert result.coord.lat == 42.03
        assert len(result.list) == 2
        assert result.list[0].components.pm2_5 == 15.0
