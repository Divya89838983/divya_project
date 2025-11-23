"""
Test suite for module.streamlit_ui.plots module.
Focuses on testing main plotting and calculation functions.
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from module.streamlit_ui.plots import (
    calculate_aqi_over_time,
    get_aqi_ranges,
    create_aqi_plot,
    display_aqi_forecast
)


class TestPlots:
    """Test suite for plotting functions."""

    def test_calculate_aqi_over_time_returns_tuple(self):
        """Test calculate_aqi_over_time returns tuple of lists."""
        # Mock air quality data
        data = Mock()
        data.dt = 1700000000
        data.components = Mock()
        
        mock_calc = Mock(return_value=[50, 40, 30, 20, 10, 60])
        
        dates, max_aqi = calculate_aqi_over_time([data], mock_calc)
        
        assert isinstance(dates, list)
        assert isinstance(max_aqi, list)

    def test_calculate_aqi_over_time_equal_lengths(self):
        """Test that dates and AQI lists have equal length."""
        data1 = Mock()
        data1.dt = 1700000000
        data1.components = Mock()
        
        data2 = Mock()
        data2.dt = 1700003600
        data2.components = Mock()
        
        mock_calc = Mock(return_value=[50, 40, 30, 20, 10, 60])
        
        dates, max_aqi = calculate_aqi_over_time([data1, data2], mock_calc)
        
        assert len(dates) == len(max_aqi)
        assert len(dates) == 2

    def test_calculate_aqi_over_time_returns_maximum(self):
        """Test that maximum AQI is returned for each entry."""
        data = Mock()
        data.dt = 1700000000
        data.components = Mock()
        
        mock_calc = Mock(return_value=[50, 40, 30, 20, 10, 60])
        
        dates, max_aqi = calculate_aqi_over_time([data], mock_calc)
        
        # Max of [50, 40, 30, 20, 10, 60] is 60
        assert max_aqi[0] == 60

    def test_calculate_aqi_over_time_converts_timestamps(self):
        """Test that Unix timestamps are converted to datetime."""
        data = Mock()
        data.dt = 1700000000
        data.components = Mock()
        
        mock_calc = Mock(return_value=[50, 40, 30, 20, 10, 60])
        
        dates, max_aqi = calculate_aqi_over_time([data], mock_calc)
        
        assert isinstance(dates[0], datetime)
        assert dates[0] == datetime.fromtimestamp(1700000000)

    def test_get_aqi_ranges_returns_six_ranges(self):
        """Test get_aqi_ranges returns six AQI ranges."""
        ranges = get_aqi_ranges()
        
        assert len(ranges) == 6

    def test_get_aqi_ranges_correct_structure(self):
        """Test get_aqi_ranges returns correct structure."""
        ranges = get_aqi_ranges()
        
        for r in ranges:
            assert len(r) == 4  # (start, end, label, color)
            assert isinstance(r[0], int)  # start
            assert isinstance(r[1], int)  # end
            assert isinstance(r[2], str)  # label
            assert isinstance(r[3], str)  # color
            assert r[3].startswith('#')   # color format

    def test_get_aqi_ranges_sequential(self):
        """Test that AQI ranges are sequential."""
        ranges = get_aqi_ranges()
        
        # Good: 0-50, Moderate: 50-100, etc.
        assert ranges[0] == (0, 50, 'Good', '#00e400')
        assert ranges[1] == (50, 100, 'Moderate', '#ffff00')
        assert ranges[-1][1] == 500  # Last range ends at 500

    def test_create_aqi_plot_returns_figure(self):
        """Test create_aqi_plot returns a Plotly figure."""
        with patch('module.streamlit_ui.plots.go.Figure') as mock_figure:
            mock_fig = Mock()
            mock_figure.return_value = mock_fig
            
            dates = [datetime.now()]
            max_aqi = [75]
            
            result = create_aqi_plot(dates, max_aqi, "Test Location")
            
            assert result == mock_fig
            mock_figure.assert_called_once()

    def test_create_aqi_plot_adds_traces(self):
        """Test create_aqi_plot adds traces to the figure."""
        with patch('module.streamlit_ui.plots.go.Figure') as mock_figure:
            mock_fig = Mock()
            mock_figure.return_value = mock_fig
            
            dates = [datetime.now()]
            max_aqi = [75]
            
            create_aqi_plot(dates, max_aqi, "Test Location")
            
            # Should add traces (colored areas + line)
            assert mock_fig.add_trace.call_count > 0

    def test_create_aqi_plot_updates_layout(self):
        """Test create_aqi_plot updates figure layout."""
        with patch('module.streamlit_ui.plots.go.Figure') as mock_figure:
            mock_fig = Mock()
            mock_figure.return_value = mock_fig
            
            dates = [datetime.now()]
            max_aqi = [75]
            
            create_aqi_plot(dates, max_aqi, "San Francisco")
            
            mock_fig.update_layout.assert_called_once()
            # Verify location is in title
            call_args = mock_fig.update_layout.call_args
            assert 'San Francisco' in str(call_args)

    def test_create_aqi_plot_includes_location_in_title(self):
        """Test that location name is included in plot title."""
        with patch('module.streamlit_ui.plots.go.Figure') as mock_figure:
            mock_fig = Mock()
            mock_figure.return_value = mock_fig
            
            dates = [datetime.now()]
            max_aqi = [100]
            
            create_aqi_plot(dates, max_aqi, "Paris, France")
            
            call_args = mock_fig.update_layout.call_args
            assert 'Paris, France' in str(call_args)

    def test_display_aqi_forecast_creates_subheader(self):
        """Test display_aqi_forecast creates subheader."""
        with patch('module.streamlit_ui.plots.st') as mock_st, \
             patch('module.streamlit_ui.plots.create_aqi_plot') as mock_plot:
            
            data = Mock()
            data.list = [Mock(), Mock()]
            for item in data.list:
                item.dt = 1700000000
                item.components = Mock()
            
            mock_calc = Mock(return_value=[50, 40, 30, 20, 10, 60])
            mock_plot.return_value = Mock()
            
            display_aqi_forecast(data, "Test Location", mock_calc)
            
            mock_st.subheader.assert_called()

    def test_display_aqi_forecast_calls_calculate_aqi_over_time(self):
        """Test display_aqi_forecast calculates AQI over time."""
        with patch('module.streamlit_ui.plots.st') as mock_st, \
             patch('module.streamlit_ui.plots.create_aqi_plot') as mock_plot:
            
            data = Mock()
            data.list = [Mock(), Mock()]
            for item in data.list:
                item.dt = 1700000000
                item.components = Mock()
            
            mock_calc = Mock(return_value=[50, 40, 30, 20, 10, 60])
            mock_plot.return_value = Mock()
            
            display_aqi_forecast(data, "Test Location", mock_calc)
            
            # Should be called once per item in data.list
            assert mock_calc.call_count == 2

    def test_display_aqi_forecast_displays_plotly_chart(self):
        """Test display_aqi_forecast displays plotly chart."""
        with patch('module.streamlit_ui.plots.st') as mock_st, \
             patch('module.streamlit_ui.plots.create_aqi_plot') as mock_plot:
            
            data = Mock()
            data.list = [Mock()]
            data.list[0].dt = 1700000000
            data.list[0].components = Mock()
            
            mock_calc = Mock(return_value=[50, 40, 30, 20, 10, 60])
            mock_fig = Mock()
            mock_plot.return_value = mock_fig
            
            display_aqi_forecast(data, "Test Location", mock_calc)
            
            mock_st.plotly_chart.assert_called_once()

    def test_integration_calculate_and_display(self):
        """Test integration: calculate AQI over time and display forecast."""
        with patch('module.streamlit_ui.plots.st') as mock_st, \
             patch('module.streamlit_ui.plots.create_aqi_plot') as mock_plot:
            
            # Create multiple data points
            data = Mock()
            data.list = []
            for i in range(3):
                item = Mock()
                item.dt = 1700000000 + i * 3600
                item.components = Mock()
                data.list.append(item)
            
            mock_calc = Mock(return_value=[50, 40, 30, 20, 10, 60])
            mock_fig = Mock()
            mock_plot.return_value = mock_fig
            
            # Test full workflow
            display_aqi_forecast(data, "Integration Test", mock_calc)
            
            # Verify all components called
            assert mock_st.subheader.called
            assert mock_calc.call_count == 3
            mock_plot.assert_called_once()
            mock_st.plotly_chart.assert_called_once()
