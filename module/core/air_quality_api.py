"""
OpenWeather Air Pollution API client.

Fetches air quality data and converts JSON responses to typed objects.
"""

import requests
from .air_quality_models import AirQualityResponse, Coordinates, PollutantComponents, AirQualityData, AQIInfo
from keys import appid


def read_pollution_data_from_api(lat, lon):
    """Fetch air pollution forecast from OpenWeather API.
    
    Args:
        lat: Latitude in decimal degrees
        lon: Longitude in decimal degrees
    
    Returns:
        dict: Raw JSON response from API
    """
    url = f"http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={lat}&lon={lon}&appid={appid}"
    response = requests.get(url)
    return response.json()


def convert_json_to_object(air_pollution_json_data):
    """Convert API JSON to structured AirQualityResponse object.
    
    Args:
        air_pollution_json_data: Raw JSON from API
    
    Returns:
        AirQualityResponse: Typed object with coordinates and forecast list
    """
    coord = Coordinates(**air_pollution_json_data["coord"])
    
    # Convert each forecast item to typed objects
    air_quality_list = [
        AirQualityData(
            dt=item["dt"],
            main=AQIInfo(**item["main"]),
            components=PollutantComponents(**item["components"])
        )
        for item in air_pollution_json_data["list"]
    ]
    
    return AirQualityResponse(coord=coord, list=air_quality_list)