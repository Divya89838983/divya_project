"""
Core functionality for the Air Quality Analysis application.
This package contains the essential components for data fetching,
processing, and calculations.
"""

from .air_quality_models import (
    Coordinates,
    Components,
    Main,
    AirQualityData,
    AirQualityResponse
)
from .air_quality_api import (
    read_pollution_data_from_api,
    convert_json_to_object
)
from .aqi_calculators import calculate_all_aqi_values
from .geocoding import get_coordinates_from_location
from .visualization import (
    calculate_max_aqi_over_time,
    plot_max_aqi_over_time
)

__all__ = [
    'Coordinates',
    'Components',
    'Main',
    'AirQualityData',
    'AirQualityResponse',
    'read_pollution_data_from_api',
    'convert_json_to_object',
    'calculate_all_aqi_values',
    'get_coordinates_from_location',
    'calculate_max_aqi_over_time',
    'plot_max_aqi_over_time'
]