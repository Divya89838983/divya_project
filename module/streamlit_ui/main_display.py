"""
Main dashboard layout and display orchestration.

Coordinates the display of current AQI status and forecast chart.
"""

import streamlit as st
from .aqi_display import (
    display_pollutant_details,
    display_aqi_category
)
from .plots import display_aqi_forecast


def display_air_quality_data(air_pollution_data, display_name, calculate_all_aqi_values):
    """Render complete air quality dashboard.
    
    Args:
        air_pollution_data: AirQualityResponse object or None
        display_name: Location name for titles
        calculate_all_aqi_values: AQI calculation function
    """
    if not air_pollution_data:
        st.error("Failed to fetch air quality data. Please try again.")
        return

    # Calculate current conditions (first data point)
    current_components = air_pollution_data.list[0].components
    current_aqi_values = calculate_all_aqi_values(current_components)
    max_aqi = max(current_aqi_values)  # Worst pollutant determines overall AQI
    
    # Current status section
    st.header("Current Air Quality Status")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        display_pollutant_details(current_components, calculate_all_aqi_values)
    
    with col2:
        st.subheader("Overall AQI Status")
        st.markdown(f"### {max_aqi:.1f}")
        display_aqi_category(max_aqi)
    
    # Forecast section
    st.header("Air Quality Forecast")
    display_aqi_forecast(air_pollution_data, display_name, calculate_all_aqi_values)