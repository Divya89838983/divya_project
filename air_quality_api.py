"""
Functions for interacting with OpenWeatherMap's Air Quality API.
"""

import requests
from air_quality_models import AirQualityResponse, Coordinates, Components, AirQualityData, Main
from keys import appid

def read_pollution_data_from_api(lat, lon):
    """
    Fetch air pollution data from OpenWeatherMap API for given coordinates
    
    Args:
        lat: Latitude
        lon: Longitude
    
    Returns:
        dict: JSON response from the API
    """
    url = f"http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={lat}&lon={lon}&appid={appid}"
    response = requests.get(url)
    air_pollution_data_json = response.json()
    return air_pollution_data_json

def convert_json_to_object(air_pollution_json_data):
    """
    Convert API JSON response to AirQualityResponse object
    
    Args:
        air_pollution_json_data: JSON data from the API
    
    Returns:
        AirQualityResponse: Object containing structured air quality data
    """
    coord = Coordinates(**air_pollution_json_data["coord"])
    air_quality_list = [
        AirQualityData(
            dt=item["dt"],
            main=Main(**item["main"]),
            components=Components(**item["components"])
        )
        for item in air_pollution_json_data["list"]
    ]
    return AirQualityResponse(coord=coord, list=air_quality_list)