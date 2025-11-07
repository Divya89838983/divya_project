import requests

def get_coordinates_from_location(location_name):
    """
    Get latitude and longitude from location name (e.g., "San Francisco", "Ames, IA", "Paris, France")
    using OpenStreetMap's Nominatim API
    
    Args:
        location_name (str): Location to geocode
    
    Returns:
        tuple: ((latitude, longitude), display_name) or ((None, None), None) if not found
    """

    # Nominatim API endpoint
    base_url = "https://nominatim.openstreetmap.org/search"
    
    # Parameters for the API request
    params = {
        'q': location_name,
        'format': 'json',
        'limit': 1,
        'addressdetails': 1
    }
    
    # Set a proper User-Agent header (required by Nominatim)
    headers = {
        'User-Agent': 'AirQualityApp/1.0'  
    }
    

    try:
        # Make the API request
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the JSON response
        data = response.json()
        
        if data and len(data) > 0:
            result = data[0]  # Get the first (best) result
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

# Example usage
if __name__ == "__main__":
    # Test with a sample location
    location = "Ames, IA"
    (lat, lon), display_name = get_coordinates_from_location(location)
    
    if lat is not None and lon is not None:
        print(f"Found location: {display_name}")
        print(f"Coordinates: {lat}, {lon}")
    else:
        print(f"Could not geocode location: {location}")