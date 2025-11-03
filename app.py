"""
Streamlit web application for Air Quality Analysis
"""

import streamlit as st
from module.streamlit_ui.location import get_location_data
from module.streamlit_ui.main_display import display_air_quality_data
from module.core.aqi_calculators import calculate_all_aqi_values
from module.core.air_quality_api import read_pollution_data_from_api, convert_json_to_object

def fetch_air_quality_data(lat, lon):
    """Fetch air quality data from OpenWeatherMap API."""
    try:
        json_data = read_pollution_data_from_api(lat, lon)
        return convert_json_to_object(json_data)
    except:
        return None

# UI Functions
def setup_page():
    """Configure the Streamlit page."""
    st.set_page_config(page_title="Air Quality Analysis", page_icon="🌍", layout="wide")
    st.title("🌍 Air Quality Analysis")
    st.write("Enter a location to analyze its air quality data")

def display_footer():
    """Display the application footer."""
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit • Data from OpenWeatherMap")

def main():
    """Main application function."""
    setup_page()
    
    # Get location data from user input
    lat, lon, display_name = get_location_data()
    
    if lat and lon:
        with st.spinner("Fetching air quality data..."):
            air_pollution_data = fetch_air_quality_data(lat, lon)
            display_air_quality_data(air_pollution_data, display_name, calculate_all_aqi_values)
    
    display_footer()

if __name__ == "__main__":
    main()