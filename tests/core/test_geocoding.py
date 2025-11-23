"""
Test suite for module.core.geocoding module.
Focuses on testing get_coordinates_from_location function comprehensively.
"""

import pytest
from unittest.mock import Mock, patch
import requests
from module.core.geocoding import get_coordinates_from_location


class TestGeocoding:
    """Test suite for geocoding functions."""

    def test_successful_geocoding(self):
        """Test successful geocoding returns correct coordinates and display name."""
        with patch('module.core.geocoding.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = [
                {
                    'lat': '40.2338',
                    'lon': '-93.6103',
                    'display_name': 'Ames, Iowa, United States'
                }
            ]
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            (lat, lon), display_name = get_coordinates_from_location("Ames, IA")
            
            assert lat == 40.2338
            assert lon == -93.6103
            assert display_name == 'Ames, Iowa, United States'
            
            # Verify API was called with correct parameters
            mock_get.assert_called_once()
            call_args = mock_get.call_args
            assert 'Ames, IA' in str(call_args)

    def test_location_not_found(self):
        """Test that non-existent location returns None values."""
        with patch('module.core.geocoding.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = []
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            (lat, lon), display_name = get_coordinates_from_location("NonexistentPlace12345")
            
            assert lat is None
            assert lon is None
            assert display_name is None

    def test_network_error_handling(self):
        """Test that network errors are handled gracefully."""
        with patch('module.core.geocoding.requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError("Network error")
            
            (lat, lon), display_name = get_coordinates_from_location("New York")
            
            assert lat is None
            assert lon is None
            assert display_name is None

    def test_timeout_error_handling(self):
        """Test that timeout errors are handled gracefully."""
        with patch('module.core.geocoding.requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.Timeout("Request timeout")
            
            (lat, lon), display_name = get_coordinates_from_location("Paris")
            
            assert lat is None
            assert lon is None
            assert display_name is None

    def test_http_error_handling(self):
        """Test that HTTP errors (4xx, 5xx) are handled gracefully."""
        with patch('module.core.geocoding.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")
            mock_get.return_value = mock_response
            
            (lat, lon), display_name = get_coordinates_from_location("London")
            
            assert lat is None
            assert lon is None
            assert display_name is None

    def test_malformed_response_missing_lat(self):
        """Test handling of response missing latitude."""
        with patch('module.core.geocoding.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = [
                {
                    'lon': '-93.6103',
                    'display_name': 'Ames, Iowa'
                }
            ]
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            (lat, lon), display_name = get_coordinates_from_location("Ames")
            
            assert lat is None
            assert lon is None
            assert display_name is None

    def test_malformed_response_missing_lon(self):
        """Test handling of response missing longitude."""
        with patch('module.core.geocoding.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = [
                {
                    'lat': '40.2338',
                    'display_name': 'Ames, Iowa'
                }
            ]
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            (lat, lon), display_name = get_coordinates_from_location("Ames")
            
            assert lat is None
            assert lon is None
            assert display_name is None

    def test_response_missing_display_name(self):
        """Test that missing display_name defaults to 'Unknown'."""
        with patch('module.core.geocoding.requests.get') as mock_get:
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

    def test_multiple_results_uses_first(self):
        """Test that when multiple results are returned, the first one is used."""
        with patch('module.core.geocoding.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = [
                {
                    'lat': '40.7128',
                    'lon': '-74.0060',
                    'display_name': 'New York, NY, USA'
                },
                {
                    'lat': '40.7000',
                    'lon': '-74.0100',
                    'display_name': 'New York, Other'
                }
            ]
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            (lat, lon), display_name = get_coordinates_from_location("New York")
            
            # Should use the first result
            assert lat == 40.7128
            assert lon == -74.0060
            assert display_name == 'New York, NY, USA'

    def test_string_coordinates_converted_to_float(self):
        """Test that string coordinates are properly converted to float."""
        with patch('module.core.geocoding.requests.get') as mock_get:
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
            
            assert isinstance(lat, float)
            assert isinstance(lon, float)
            assert lat == 48.8566
            assert lon == 2.3522

    def test_api_request_headers(self):
        """Test that proper User-Agent header is sent in API request."""
        with patch('module.core.geocoding.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = [
                {
                    'lat': '40.2338',
                    'lon': '-93.6103',
                    'display_name': 'Ames, IA'
                }
            ]
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            get_coordinates_from_location("Ames, IA")
            
            # Verify headers were sent
            call_args = mock_get.call_args
            headers = call_args.kwargs.get('headers', {})
            assert 'User-Agent' in headers

    def test_api_request_parameters(self):
        """Test that correct parameters are sent to API."""
        with patch('module.core.geocoding.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = [
                {
                    'lat': '40.2338',
                    'lon': '-93.6103',
                    'display_name': 'Ames, IA'
                }
            ]
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            get_coordinates_from_location("San Francisco")
            
            # Verify parameters
            call_args = mock_get.call_args
            params = call_args.kwargs.get('params', {})
            assert params['q'] == 'San Francisco'
            assert params['format'] == 'json'
            assert params['limit'] == 1

    def test_empty_location_string(self):
        """Test that empty location string is handled."""
        with patch('module.core.geocoding.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = []
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            (lat, lon), display_name = get_coordinates_from_location("")
            
            # Should still make the request and handle empty results
            mock_get.assert_called_once()
            assert lat is None
            assert lon is None
            assert display_name is None

    def test_special_characters_in_location(self):
        """Test that special characters in location names are handled."""
        with patch('module.core.geocoding.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = [
                {
                    'lat': '48.8566',
                    'lon': '2.3522',
                    'display_name': 'Île-de-France, Paris'
                }
            ]
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            (lat, lon), display_name = get_coordinates_from_location("Île-de-France")
            
            assert lat == 48.8566
            assert lon == 2.3522
            assert display_name == 'Île-de-France, Paris'
