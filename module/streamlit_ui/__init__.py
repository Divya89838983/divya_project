"""
Streamlit UI Components.

Presentation layer with location input, AQI display, and interactive plots.
Depends on core module for business logic.
"""

from .location import get_location_data, display_location_info
from .plots import display_current_air_quality, display_aqi_forecast
from .aqi_display import display_pollutant_details, display_aqi_category, get_aqi_category
from module.core.geocoding import get_coordinates_from_location