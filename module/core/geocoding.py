"""
Geocoding service using OpenStreetMap's Nominatim API.

Converts location names to coordinates for air quality lookups.
"""

import requests


def get_coordinates_from_location(location_name):
    """Convert location name to latitude/longitude coordinates.
    
    Args:
        location_name: City, address, or place name (e.g., "Ames, IA")
    
    Returns:
        tuple: ((lat, lon), display_name) or ((None, None), None) if not found
    """
    base_url = "https://nominatim.openstreetmap.org/search"
    
    params = {
        'q': location_name,
        'format': 'json',
        'limit': 1,  # Only need best match
        'addressdetails': 1
    }
    
    # User-Agent required by Nominatim policy
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
        else:
            print(f"No results found for location: {location_name}")
            return (None, None), None
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching coordinates: {e}")
        return (None, None), None
    except (KeyError, ValueError, IndexError) as e:
        print(f"Error parsing response: {e}")
        return (None, None), None


# Simple test when run directly
if __name__ == "__main__":
    location = "Ames, IA"
    (lat, lon), display_name = get_coordinates_from_location(location)
    
    if lat is not None and lon is not None:
        print(f"Found location: {display_name}")
        print(f"Coordinates: {lat}, {lon}")
    else:
        print(f"Could not geocode location: {location}")