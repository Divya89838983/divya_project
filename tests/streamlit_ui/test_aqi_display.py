"""
Test suite for module.streamlit_ui.aqi_display module.
Focuses on testing the main display functions comprehensively.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from module.streamlit_ui.aqi_display import (
    get_aqi_category,
    display_aqi_category,
    display_pollutant_details
)


class TestAQIDisplay:
    """Test suite for AQI display functions."""

    def test_get_aqi_category_good(self):
        """Test get_aqi_category returns correct category for good air quality."""
        category, color = get_aqi_category(25)
        
        assert category == "Good"
        assert color == "#00e400"

    def test_get_aqi_category_moderate(self):
        """Test get_aqi_category returns correct category for moderate air quality."""
        category, color = get_aqi_category(75)
        
        assert category == "Moderate"
        assert color == "#ffff00"

    def test_get_aqi_category_unhealthy_sensitive(self):
        """Test get_aqi_category returns correct category for unhealthy for sensitive groups."""
        category, color = get_aqi_category(125)
        
        assert category == "Unhealthy for Sensitive Groups"
        assert color == "#ff7e00"

    def test_get_aqi_category_unhealthy(self):
        """Test get_aqi_category returns correct category for unhealthy air quality."""
        category, color = get_aqi_category(175)
        
        assert category == "Unhealthy"
        assert color == "#ff0000"

    def test_get_aqi_category_very_unhealthy(self):
        """Test get_aqi_category returns correct category for very unhealthy air quality."""
        category, color = get_aqi_category(250)
        
        assert category == "Very Unhealthy"
        assert color == "#8f3f97"

    def test_get_aqi_category_hazardous(self):
        """Test get_aqi_category returns correct category for hazardous air quality."""
        category, color = get_aqi_category(350)
        
        assert category == "Hazardous"
        assert color == "#7e0023"

    def test_get_aqi_category_boundary_50(self):
        """Test get_aqi_category at boundary value 50."""
        category, color = get_aqi_category(50)
        
        assert category == "Good"
        assert color == "#00e400"

    def test_get_aqi_category_boundary_100(self):
        """Test get_aqi_category at boundary value 100."""
        category, color = get_aqi_category(100)
        
        assert category == "Moderate"
        assert color == "#ffff00"

    def test_display_aqi_category_renders_html(self):
        """Test display_aqi_category renders HTML with correct styling."""
        with patch('module.streamlit_ui.aqi_display.st') as mock_st:
            
            display_aqi_category(75)
            
            # Verify markdown was called
            mock_st.markdown.assert_called_once()
            call_args = mock_st.markdown.call_args
            html_content = call_args[0][0]
            
            # Verify content includes category
            assert "Moderate" in html_content
            assert "#ffff00" in html_content
            assert "unsafe_allow_html=True" in str(call_args)

    def test_display_aqi_category_good_uses_black_text(self):
        """Test display_aqi_category uses black text for good air quality."""
        with patch('module.streamlit_ui.aqi_display.st') as mock_st:
            
            display_aqi_category(25)
            
            call_args = mock_st.markdown.call_args
            html_content = call_args[0][0]
            
            # Good category should use black text
            assert "black" in html_content

    def test_display_aqi_category_hazardous_uses_white_text(self):
        """Test display_aqi_category uses white text for hazardous air quality."""
        with patch('module.streamlit_ui.aqi_display.st') as mock_st:
            
            display_aqi_category(350)
            
            call_args = mock_st.markdown.call_args
            html_content = call_args[0][0]
            
            # Hazardous category should use white text
            assert "white" in html_content

    def test_display_pollutant_details_creates_subheader(self):
        """Test display_pollutant_details creates subheader."""
        with patch('module.streamlit_ui.aqi_display.st') as mock_st:
            
            # Mock components
            components = Mock()
            components.pm2_5 = 25.0
            components.pm10 = 50.0
            components.no2 = 40.0
            components.so2 = 20.0
            components.co = 500.0
            components.o3 = 80.0
            
            # Mock calculate function
            mock_calc = Mock(return_value=[50, 40, 30, 20, 10, 60])
            
            display_pollutant_details(components, mock_calc)
            
            # Verify subheader was called
            mock_st.subheader.assert_called_once()
            assert "Pollutant" in str(mock_st.subheader.call_args)

    def test_display_pollutant_details_creates_three_columns(self):
        """Test display_pollutant_details creates three columns."""
        with patch('module.streamlit_ui.aqi_display.st') as mock_st:
            
            # Mock components
            components = Mock()
            components.pm2_5 = 25.0
            components.pm10 = 50.0
            components.no2 = 40.0
            components.so2 = 20.0
            components.co = 500.0
            components.o3 = 80.0
            
            # Mock calculate function
            mock_calc = Mock(return_value=[50, 40, 30, 20, 10, 60])
            
            display_pollutant_details(components, mock_calc)
            
            # Verify columns was called with 3
            mock_st.columns.assert_called_once_with(3)

    def test_display_pollutant_details_calls_calculate_aqi(self):
        """Test display_pollutant_details calls the calculate function."""
        with patch('module.streamlit_ui.aqi_display.st') as mock_st:
            
            # Mock components
            components = Mock()
            components.pm2_5 = 25.0
            components.pm10 = 50.0
            components.no2 = 40.0
            components.so2 = 20.0
            components.co = 500.0
            components.o3 = 80.0
            
            # Mock calculate function
            mock_calc = Mock(return_value=[50, 40, 30, 20, 10, 60])
            
            display_pollutant_details(components, mock_calc)
            
            # Verify calculate was called with components
            mock_calc.assert_called_once_with(components)

    def test_display_pollutant_details_displays_all_pollutants(self):
        """Test display_pollutant_details displays all six pollutants."""
        with patch('module.streamlit_ui.aqi_display.st') as mock_st:
            
            # Mock components
            components = Mock()
            components.pm2_5 = 25.0
            components.pm10 = 50.0
            components.no2 = 40.0
            components.so2 = 20.0
            components.co = 500.0
            components.o3 = 80.0
            
            # Mock calculate function
            mock_calc = Mock(return_value=[50, 40, 30, 20, 10, 60])
            
            # Mock columns
            col_mock = MagicMock()
            mock_st.columns.return_value = [col_mock, col_mock, col_mock]
            
            display_pollutant_details(components, mock_calc)
            
            # Verify markdown was called 6 times (once per pollutant)
            assert mock_st.markdown.call_count == 6

    def test_display_pollutant_details_includes_pollutant_names(self):
        """Test display_pollutant_details includes correct pollutant names."""
        with patch('module.streamlit_ui.aqi_display.st') as mock_st:
            
            # Mock components
            components = Mock()
            components.pm2_5 = 25.0
            components.pm10 = 50.0
            components.no2 = 40.0
            components.so2 = 20.0
            components.co = 500.0
            components.o3 = 80.0
            
            # Mock calculate function
            mock_calc = Mock(return_value=[50, 40, 30, 20, 10, 60])
            
            # Mock columns
            col_mock = MagicMock()
            mock_st.columns.return_value = [col_mock, col_mock, col_mock]
            
            display_pollutant_details(components, mock_calc)
            
            # Collect all markdown calls
            markdown_calls = [str(call) for call in mock_st.markdown.call_args_list]
            all_markdown = ' '.join(markdown_calls)
            
            # Verify all pollutant names are present
            assert 'PM2.5' in all_markdown
            assert 'PM10' in all_markdown
            assert 'NO2' in all_markdown
            assert 'SO2' in all_markdown
            assert 'CO' in all_markdown
            assert 'O3' in all_markdown

    def test_display_pollutant_details_includes_raw_values(self):
        """Test display_pollutant_details includes raw pollutant values."""
        with patch('module.streamlit_ui.aqi_display.st') as mock_st:
            
            # Mock components
            components = Mock()
            components.pm2_5 = 25.5
            components.pm10 = 50.3
            components.no2 = 40.2
            components.so2 = 20.1
            components.co = 500.7
            components.o3 = 80.9
            
            # Mock calculate function
            mock_calc = Mock(return_value=[50, 40, 30, 20, 10, 60])
            
            # Mock columns
            col_mock = MagicMock()
            mock_st.columns.return_value = [col_mock, col_mock, col_mock]
            
            display_pollutant_details(components, mock_calc)
            
            # Collect all markdown calls
            markdown_calls = [str(call) for call in mock_st.markdown.call_args_list]
            all_markdown = ' '.join(markdown_calls)
            
            # Verify raw values are included
            assert 'Raw:' in all_markdown or '25.5' in all_markdown

    def test_integration_display_functions(self):
        """Test integration of get_aqi_category and display functions."""
        with patch('module.streamlit_ui.aqi_display.st') as mock_st:
            
            # Test full workflow
            # 1. Get category
            category, color = get_aqi_category(150)
            assert category == "Unhealthy for Sensitive Groups"
            
            # 2. Display category
            display_aqi_category(150)
            assert mock_st.markdown.called
            
            # 3. Display pollutant details
            components = Mock()
            components.pm2_5 = 150.0
            components.pm10 = 200.0
            components.no2 = 180.0
            components.so2 = 100.0
            components.co = 5000.0
            components.o3 = 160.0
            
            mock_calc = Mock(return_value=[150, 140, 130, 120, 110, 160])
            
            display_pollutant_details(components, mock_calc)
            
            # Verify all components were called
            assert mock_st.subheader.called
            assert mock_st.columns.called
            mock_calc.assert_called_with(components)
