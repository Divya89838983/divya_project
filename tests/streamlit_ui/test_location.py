"""
Test suite for module.streamlit_ui.location module.
Focuses on testing get_coordinates_from_location function.
"""

import pytest
from unittest.mock import Mock, patch
from module.streamlit_ui.location import get_coordinates_from_location


class TestLocation:
    """Test suite for location functions."""

    def test_get_coordinates_from_location_success(self):
        """Test get_coordinates_from_location with successful API response."""
        with patch('module.streamlit_ui.location.requests.get') as mock_get:
            
            mock_response = Mock()
            mock_response.json.return_value = [
                {
                    'lat': '48.8566',
                    'lon': '2.3522',
                    'display_name': 'Paris, France'
                }
            ]
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            (lat, lon), display_name = get_coordinates_from_location("Paris")
            
            assert lat == 48.8566
            assert lon == 2.3522
            assert display_name == 'Paris, France'

    def test_get_coordinates_from_location_not_found(self):
        """Test get_coordinates_from_location with no results."""
        with patch('module.streamlit_ui.location.requests.get') as mock_get:
            
            mock_response = Mock()
            mock_response.json.return_value = []
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            (lat, lon), display_name = get_coordinates_from_location("NonexistentPlace")
            
            assert lat is None
            assert lon is None
            assert display_name is None

    def test_get_coordinates_from_location_handles_exception(self):
        """Test get_coordinates_from_location handles exceptions gracefully."""
        with patch('module.streamlit_ui.location.requests.get') as mock_get:
            
            mock_get.side_effect = Exception("Network error")
            
            (lat, lon), display_name = get_coordinates_from_location("New York")
            
            assert lat is None
            assert lon is None
            assert display_name is None

    def test_get_coordinates_api_parameters(self):
        """Test that correct parameters are sent to geocoding API."""
        with patch('module.streamlit_ui.location.requests.get') as mock_get:
            
            mock_response = Mock()
            mock_response.json.return_value = [
                {'lat': '40.0', 'lon': '-93.0', 'display_name': 'Test'}
            ]
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            get_coordinates_from_location("San Francisco")
            
            # Verify API call parameters
            call_args = mock_get.call_args
            params = call_args.kwargs.get('params', {})
            assert params['q'] == 'San Francisco'
            assert params['format'] == 'json'
            assert params['limit'] == 1
            
            # Verify headers
            headers = call_args.kwargs.get('headers', {})
            assert 'User-Agent' in headers

    def test_get_coordinates_from_location_missing_lat(self):
        """Test handling of response missing latitude."""
        with patch('module.streamlit_ui.location.requests.get') as mock_get:
            
            mock_response = Mock()
            mock_response.json.return_value = [
                {
                    'lon': '-93.6103',
                    'display_name': 'Test Location'
                }
            ]
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            (lat, lon), display_name = get_coordinates_from_location("Test")
            
            assert lat is None
            assert lon is None
            assert display_name is None

    def test_get_coordinates_from_location_missing_display_name(self):
        """Test that missing display_name defaults to 'Unknown'."""
        with patch('module.streamlit_ui.location.requests.get') as mock_get:
            
            mock_response = Mock()
            mock_response.json.return_value = [
                {
                    'lat': '51.5074',
                    'lon': '-0.1278'
                }
            ]
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            (lat, lon), display_name = get_coordinates_from_location("London")
            
            assert lat == 51.5074
            assert lon == -0.1278
            assert display_name == 'Unknown'
