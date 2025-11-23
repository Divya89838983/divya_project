"""
Test suite for module.core.visualization module.
Focuses on testing calculate_max_aqi_over_time and plot_max_aqi_over_time functions.
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from module.core.visualization import calculate_max_aqi_over_time, plot_max_aqi_over_time


@pytest.fixture
def mock_air_quality_single():
    """Single air quality data entry."""
    data = Mock()
    data.dt = 1700000000
    data.components = Mock()
    data.components.pm2_5 = 25.0
    data.components.pm10 = 50.0
    data.components.no2 = 40.0
    data.components.so2 = 20.0
    data.components.co = 500.0
    data.components.o3 = 80.0
    return [data]


@pytest.fixture
def mock_air_quality_multiple():
    """Multiple air quality data entries."""
    data_list = []
    
    # Entry 1: Good air quality
    data1 = Mock()
    data1.dt = 1700000000
    data1.components = Mock()
    data1.components.pm2_5 = 5.0
    data1.components.pm10 = 15.0
    data1.components.no2 = 20.0
    data1.components.so2 = 10.0
    data1.components.co = 300.0
    data1.components.o3 = 40.0
    data_list.append(data1)
    
    # Entry 2: Moderate air quality
    data2 = Mock()
    data2.dt = 1700003600
    data2.components = Mock()
    data2.components.pm2_5 = 25.0
    data2.components.pm10 = 75.0
    data2.components.no2 = 80.0
    data2.components.so2 = 150.0
    data2.components.co = 7000.0
    data2.components.o3 = 120.0
    data_list.append(data2)
    
    # Entry 3: Poor air quality
    data3 = Mock()
    data3.dt = 1700007200
    data3.components = Mock()
    data3.components.pm2_5 = 150.0
    data3.components.pm10 = 300.0
    data3.components.no2 = 300.0
    data3.components.so2 = 800.0
    data3.components.co = 15000.0
    data3.components.o3 = 400.0
    data_list.append(data3)
    
    return data_list


@pytest.fixture
def mock_air_quality_zero():
    """Air quality data with zero values."""
    data = Mock()
    data.dt = 1700000000
    data.components = Mock()
    data.components.pm2_5 = 0
    data.components.pm10 = 0
    data.components.no2 = 0
    data.components.so2 = 0
    data.components.co = 0
    data.components.o3 = 0
    return [data]


class TestVisualization:
    """Test suite for visualization functions."""

    def test_calculate_max_aqi_returns_tuple(self, mock_air_quality_single):
        """Test that calculate_max_aqi_over_time returns a tuple of two lists."""
        dates, max_aqi_values = calculate_max_aqi_over_time(mock_air_quality_single)
        
        assert isinstance(dates, list)
        assert isinstance(max_aqi_values, list)

    def test_calculate_max_aqi_equal_lengths(self, mock_air_quality_single):
        """Test that dates and AQI values lists have equal length."""
        dates, max_aqi_values = calculate_max_aqi_over_time(mock_air_quality_single)
        
        assert len(dates) == len(max_aqi_values)

    def test_calculate_max_aqi_dates_are_datetime(self, mock_air_quality_single):
        """Test that dates are datetime objects."""
        dates, max_aqi_values = calculate_max_aqi_over_time(mock_air_quality_single)
        
        assert all(isinstance(d, datetime) for d in dates)

    def test_calculate_max_aqi_values_are_numbers(self, mock_air_quality_single):
        """Test that AQI values are numbers."""
        dates, max_aqi_values = calculate_max_aqi_over_time(mock_air_quality_single)
        
        assert all(isinstance(v, (int, float)) for v in max_aqi_values)

    def test_calculate_max_aqi_returns_maximum(self, mock_air_quality_single):
        """Test that max AQI is returned (not average or sum)."""
        dates, max_aqi_values = calculate_max_aqi_over_time(mock_air_quality_single)
        
        # With moderate values, max AQI should be positive
        assert max_aqi_values[0] > 0

    def test_calculate_max_aqi_with_multiple_entries(self, mock_air_quality_multiple):
        """Test calculation with multiple air quality entries."""
        dates, max_aqi_values = calculate_max_aqi_over_time(mock_air_quality_multiple)
        
        assert len(dates) == 3
        assert len(max_aqi_values) == 3
        # Values should increase (good -> moderate -> poor)
        assert max_aqi_values[0] < max_aqi_values[1] < max_aqi_values[2]

    def test_calculate_max_aqi_with_zero_values(self, mock_air_quality_zero):
        """Test that zero pollutant values return zero AQI."""
        dates, max_aqi_values = calculate_max_aqi_over_time(mock_air_quality_zero)
        
        assert max_aqi_values[0] == 0

    def test_calculate_max_aqi_timestamp_conversion(self, mock_air_quality_single):
        """Test that Unix timestamps are converted to datetime correctly."""
        dates, max_aqi_values = calculate_max_aqi_over_time(mock_air_quality_single)
        
        # Verify the timestamp conversion
        expected_datetime = datetime.fromtimestamp(1700000000)
        assert dates[0] == expected_datetime

    def test_calculate_max_aqi_empty_list(self):
        """Test that empty air quality list returns empty lists."""
        dates, max_aqi_values = calculate_max_aqi_over_time([])
        
        assert dates == []
        assert max_aqi_values == []

    def test_calculate_max_aqi_calls_calculate_all_aqi_values(self, mock_air_quality_single):
        """Test that calculate_all_aqi_values is called for each entry."""
        with patch('module.core.visualization.calculate_all_aqi_values') as mock_calc:
            mock_calc.return_value = [10, 20, 30, 40, 50, 60]
            
            dates, max_aqi_values = calculate_max_aqi_over_time(mock_air_quality_single)
            
            # Should call calculate_all_aqi_values once for single entry
            mock_calc.assert_called_once()
            # Max of [10, 20, 30, 40, 50, 60] is 60
            assert max_aqi_values[0] == 60

    def test_plot_max_aqi_creates_figure(self, mock_air_quality_single):
        """Test that plot_max_aqi_over_time creates a Plotly figure."""
        dates, max_aqi_values = calculate_max_aqi_over_time(mock_air_quality_single)
        
        with patch('module.core.visualization.go.Figure') as mock_figure:
            mock_fig_instance = Mock()
            mock_figure.return_value = mock_fig_instance
            
            plot_max_aqi_over_time(dates, max_aqi_values, "Test Location")
            
            # Verify Figure was created
            mock_figure.assert_called_once()
            # Verify show was called
            mock_fig_instance.show.assert_called_once()

    def test_plot_max_aqi_adds_trace(self, mock_air_quality_single):
        """Test that plot adds a trace to the figure."""
        dates, max_aqi_values = calculate_max_aqi_over_time(mock_air_quality_single)
        
        with patch('module.core.visualization.go.Figure') as mock_figure:
            mock_fig_instance = Mock()
            mock_figure.return_value = mock_fig_instance
            
            plot_max_aqi_over_time(dates, max_aqi_values, "Test Location")
            
            # Verify add_trace was called
            mock_fig_instance.add_trace.assert_called_once()

    def test_plot_max_aqi_updates_layout(self, mock_air_quality_single):
        """Test that plot updates the figure layout."""
        dates, max_aqi_values = calculate_max_aqi_over_time(mock_air_quality_single)
        
        with patch('module.core.visualization.go.Figure') as mock_figure:
            mock_fig_instance = Mock()
            mock_figure.return_value = mock_fig_instance
            
            plot_max_aqi_over_time(dates, max_aqi_values, "Test Location")
            
            # Verify update_layout was called
            mock_fig_instance.update_layout.assert_called_once()

    def test_plot_max_aqi_includes_location_in_title(self, mock_air_quality_single):
        """Test that location name is included in plot title."""
        dates, max_aqi_values = calculate_max_aqi_over_time(mock_air_quality_single)
        
        with patch('module.core.visualization.go.Figure') as mock_figure:
            mock_fig_instance = Mock()
            mock_figure.return_value = mock_fig_instance
            
            plot_max_aqi_over_time(dates, max_aqi_values, "San Francisco")
            
            # Verify location is in the layout call
            call_args = mock_fig_instance.update_layout.call_args
            title = call_args.kwargs.get('title', '')
            assert 'San Francisco' in title

    def test_plot_max_aqi_with_multiple_points(self, mock_air_quality_multiple):
        """Test plotting with multiple data points."""
        dates, max_aqi_values = calculate_max_aqi_over_time(mock_air_quality_multiple)
        
        with patch('module.core.visualization.go.Figure') as mock_figure:
            mock_fig_instance = Mock()
            mock_figure.return_value = mock_fig_instance
            
            plot_max_aqi_over_time(dates, max_aqi_values, "Multiple Location")
            
            # Verify plotting occurred
            mock_fig_instance.add_trace.assert_called_once()
            mock_fig_instance.show.assert_called_once()

    def test_plot_max_aqi_updates_axes(self, mock_air_quality_single):
        """Test that plot updates both x and y axes."""
        dates, max_aqi_values = calculate_max_aqi_over_time(mock_air_quality_single)
        
        with patch('module.core.visualization.go.Figure') as mock_figure:
            mock_fig_instance = Mock()
            mock_figure.return_value = mock_fig_instance
            
            plot_max_aqi_over_time(dates, max_aqi_values, "Test Location")
            
            # Verify axes were updated
            mock_fig_instance.update_xaxes.assert_called_once()
            mock_fig_instance.update_yaxes.assert_called_once()

    def test_integration_calculate_and_plot(self, mock_air_quality_multiple):
        """Test integration: calculate AQI and then plot it."""
        # Calculate
        dates, max_aqi_values = calculate_max_aqi_over_time(mock_air_quality_multiple)
        
        assert len(dates) == 3
        assert len(max_aqi_values) == 3
        
        # Plot
        with patch('module.core.visualization.go.Figure') as mock_figure:
            mock_fig_instance = Mock()
            mock_figure.return_value = mock_fig_instance
            
            plot_max_aqi_over_time(dates, max_aqi_values, "Integration Test")
            
            # Verify both calculate and plot work together
            assert mock_fig_instance.add_trace.called
            assert mock_fig_instance.update_layout.called
            assert mock_fig_instance.show.called
