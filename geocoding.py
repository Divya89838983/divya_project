import requests

def geocode_location(location):
    """
    Geocode a location using OpenStreetMap Nominatim API
    
    Args:
        location (str): Location to geocode (e.g., "Ames, IA")
    
    Returns:
        dict: Dictionary containing lat, lon, or None if error
    """

    # Nominatim API endpoint
    base_url = "https://nominatim.openstreetmap.org/search"
    
    # Parameters for the API request
    params = {
        'q': location,           # Query string
        'format': 'json',        # Response format
        'limit': 1               # Limit to 1 result
    }
    
    # Set a proper User-Agent header (required by Nominatim)
    headers = {
        'User-Agent': 'GeoCodingScript/1.0 (student.project@example.com)'
    }
    

    try:
        # Make the API request
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the JSON response
        data = response.json()
        
        if data:
            result = data[0]  # Get the first (best) result
            return {
                'latitude': float(result['lat']),
                'longitude': float(result['lon']),
            }
        else:
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    except (KeyError, ValueError, IndexError) as e:
        print(f"Error parsing response: {e}")
        return None
            
  

# Example usage
if __name__ == "__main__":
    # Geocode Ames, IA
    location = "Ames, IA"
    result = geocode_location(location)
    
    if result:
        print(f"Location: {location}")
        print(f"Latitude: {result['latitude']}")
        print(f"Longitude: {result['longitude']}")
        
    else:
        print(f"Could not geocode location: {location}")
    
    