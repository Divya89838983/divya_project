"""
AQI visualization helper functions for the Streamlit UI.
"""
import streamlit as st
from ..core.aqi_calculators import calculate_all_aqi_values

def get_aqi_category(value):
    """Get the AQI category and color based on the value."""
    if value <= 50:
        return "Good", "#00e400"
    elif value <= 100:
        return "Moderate", "#ffff00"
    elif value <= 150:
        return "Unhealthy for Sensitive Groups", "#ff7e00"
    elif value <= 200:
        return "Unhealthy", "#ff0000"
    elif value <= 300:
        return "Very Unhealthy", "#8f3f97"
    else:
        return "Hazardous", "#7e0023"

def display_aqi_category(value):
    """Display the AQI category with appropriate styling."""
    category, color = get_aqi_category(value)
    st.markdown(
        f'<div style="padding: 10px; border-radius: 5px; background-color: {color}; '
        f'color: {"black" if color in ["#00e400", "#ffff00"] else "white"};">'
        f'AQI Category: {category}</div>',
        unsafe_allow_html=True
    )

def display_pollutant_details(components, calculate_all_aqi_values):
    """Display detailed information about each pollutant."""
    st.subheader("📊 Pollutant Details")
    
    aqi_values = calculate_all_aqi_values(components)
    pollutant_names = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3']
    descriptions = [
        "Fine particulate matter (≤2.5 µm)",
        "Coarse particulate matter (≤10 µm)",
        "Nitrogen dioxide",
        "Sulfur dioxide",
        "Carbon monoxide",
        "Ozone"
    ]
    
    cols = st.columns(3)
    for idx, (name, value, desc) in enumerate(zip(pollutant_names, aqi_values, descriptions)):
        with cols[idx % 3]:
            raw_value = getattr(components, name.lower().replace('.', '_'))
            category, color = get_aqi_category(value)
            
            st.markdown(
                f'<div style="padding: 10px; border-radius: 5px; '
                f'border: 2px solid {color};">'
                f'<h4 style="margin: 0;">{name}</h4>'
                f'<p style="margin: 5px 0; font-size: 0.8em;">{desc}</p>'
                f'<p style="margin: 5px 0;">AQI: {value:.1f}</p>'
                f'<p style="margin: 5px 0; font-size: 0.9em;">Raw: {raw_value:.2f}</p>'
                f'<p style="margin: 5px 0; color: {color};">{category}</p>'
                f'</div>',
                unsafe_allow_html=True
            )