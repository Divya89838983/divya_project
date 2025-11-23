"""
Test suite for module.streamlit_ui.main_display module.
Focuses on testing the display_air_quality_data function.
"""

import pytest
from unittest.mock import Mock, patch
from module.streamlit_ui.main_display import display_air_quality_data


class TestMainDisplay:
    """Test suite for main display functions."""

    def test_display_air_quality_data_with_empty_data(self):
        """Test display_air_quality_data with empty data shows error."""
        with patch('module.streamlit_ui.main_display.st') as mock_st:
            
            mock_calc = Mock()
            
            display_air_quality_data(None, "Test Location", mock_calc)
            
            # Verify error was displayed
            mock_st.error.assert_called_once()
            assert "Failed to fetch" in str(mock_st.error.call_args)

    def test_display_air_quality_data_early_return_on_no_data(self):
        """Test display_air_quality_data returns early when no data."""
        with patch('module.streamlit_ui.main_display.st') as mock_st, \
             patch('module.streamlit_ui.main_display.display_pollutant_details') as mock_pollutant, \
             patch('module.streamlit_ui.main_display.display_aqi_category') as mock_category, \
             patch('module.streamlit_ui.main_display.display_aqi_forecast') as mock_forecast:
            
            mock_calc = Mock()
            
            display_air_quality_data(None, "Test Location", mock_calc)
            
            # Verify error was shown but other functions not called
            mock_st.error.assert_called_once()
            mock_pollutant.assert_not_called()
            mock_category.assert_not_called()
            mock_forecast.assert_not_called()
