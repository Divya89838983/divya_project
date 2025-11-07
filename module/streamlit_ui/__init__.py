"""
Streamlit UI components for the Air Quality Analysis application.
"""

from .location import get_location_data, display_location_info, get_coordinates_from_location
from .plots import display_current_air_quality, display_aqi_forecast
from .aqi_display import display_pollutant_details, display_aqi_category, get_aqi_category