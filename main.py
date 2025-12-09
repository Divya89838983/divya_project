"""
Air Quality Analysis - Streamlit Web Application.

Main entry point for the air quality dashboard. Users enter a location
to view current air quality and 5-day forecast with EPA AQI calculations.
"""

import streamlit as st
from module.streamlit_ui.location import get_location_data
from module.streamlit_ui.main_display import display_air_quality_data
from module.core.aqi_calculators import calculate_all_aqi_values
from module.core.air_quality_api import read_pollution_data_from_api, convert_json_to_object


def fetch_air_quality_data(lat, lon):
    """Fetch and parse air quality data from OpenWeather API.
    
    Args:
        lat: Latitude
        lon: Longitude
    
    Returns:
        AirQualityResponse object or None if fetch fails
    """
    try:
        json_data = read_pollution_data_from_api(lat, lon)
        return convert_json_to_object(json_data)
    except Exception:
        return None


def setup_page():
    """Configure Streamlit page settings and header."""
    st.set_page_config(
        page_title="Air Quality Analysis",
        page_icon="🌍",
        layout="wide"
    )
    st.title("🌍 Air Quality Analysis")
    st.write("Enter a location to analyze its air quality data")


def display_footer():
    """Show application credits."""
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit • Data from OpenWeatherMap")


def main():
    """Main application flow."""
    setup_page()
    
    # Step 1: Get location from user
    lat, lon, display_name = get_location_data()
    
    # Step 2: Fetch and display air quality if location valid
    if lat and lon:
        with st.spinner("Fetching air quality data..."):
            air_pollution_data = fetch_air_quality_data(lat, lon)
            display_air_quality_data(
                air_pollution_data,
                display_name,
                calculate_all_aqi_values
            )
    
    display_footer()


if __name__ == "__main__":
    main()