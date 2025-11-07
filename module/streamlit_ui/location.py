"""
Location handling module for the Air Quality Analysis application.
"""
import streamlit as st
import requests

def get_coordinates_from_location(location_name):
    """Get coordinates from location name using Nominatim API."""
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {'q': location_name, 'format': 'json', 'limit': 1, 'addressdetails': 1}
    headers = {'User-Agent': 'AirQualityApp/1.0'}
    
    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if data and len(data) > 0:
            result = data[0]
            display_name = result.get('display_name', 'Unknown')
            lat = float(result['lat'])
            lon = float(result['lon'])
            return (lat, lon), display_name
        return (None, None), None
    except:
        return (None, None), None

def display_location_info(lat, lon, display_name):
    """Display location information in the Streamlit UI."""
    st.success(f"📍 Found location: {display_name}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"Latitude: {lat}")
    with col2:
        st.info(f"Longitude: {lon}")

def get_location_data():
    """Get location data from user input."""
    # Initialize session state for location if not exists
    if 'location_input' not in st.session_state:
        st.session_state.location_input = ""

    # Get location input from user
    location = st.text_input(
        "Enter a location (e.g., 'Ames, IA', 'Paris, France')",
        key="location_input"
    )
    
    if location:
        # Get coordinates
        (lat, lon), display_name = get_coordinates_from_location(location)
        
        if lat and lon:
            display_location_info(lat, lon, display_name)
            return lat, lon, display_name
        else:
            st.error(f"Could not find coordinates for: {location}")
            st.warning("Please try a different location name or format (e.g., 'City, Country')")
            return None, None, None
    
    return None, None, None