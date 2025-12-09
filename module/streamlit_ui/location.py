"""
Location input and display UI components.

Handles user location searches and displays results on an interactive map.
"""

import streamlit as st
import pandas as pd
from module.core.geocoding import get_coordinates_from_location


def display_location_info(lat, lon, display_name):
    """Show location confirmation and map.
    
    Args:
        lat: Latitude
        lon: Longitude  
        display_name: Formatted location name from geocoding service
    """
    st.success(f"📍 Found location: {display_name}")
    
    # Create single-point map data
    map_data = pd.DataFrame({
        'lat': [lat],
        'lon': [lon],
        'size': [100]  # Marker size
    })
    st.map(map_data, zoom=11, size='size', use_container_width=True)


def get_location_data():
    """Handle location input and validation.
    
    Returns:
        tuple: (lat, lon, display_name) or (None, None, None) if invalid
    """
    # Preserve input across reruns
    if 'location_input' not in st.session_state:
        st.session_state.location_input = ""

    location = st.text_input(
        "Enter a location (e.g., 'Ames, IA', 'Paris, France')",
        key="location_input"
    )
    
    if location:
        # Show spinner during API call
        with st.spinner("🔍 Searching for location..."):
            (lat, lon), display_name = get_coordinates_from_location(location)
        
        if lat and lon:
            display_location_info(lat, lon, display_name)
            return lat, lon, display_name
        else:
            st.error(f"Could not find coordinates for: {location}")
            st.warning("Please try a different location name or format (e.g., 'City, Country')")
            return None, None, None
    
    return None, None, None