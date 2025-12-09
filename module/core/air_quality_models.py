"""
Air Quality Data Models.

Data structures for OpenWeather Air Pollution API responses.
All models use dataclasses for type-safe representation.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Coordinates:
    """Geographic coordinates in decimal degrees."""
    lat: float
    lon: float


@dataclass
class PollutantComponents:
    """Pollutant concentrations in µg/m³.
    
    Note: pm2_5 uses underscore instead of dot due to Python naming rules.
    """
    co: float
    no: float
    no2: float
    o3: float
    so2: float
    pm2_5: float  # Fine particles (≤2.5μm)
    pm10: float   # Coarse particles (≤10μm)
    nh3: float


@dataclass
class AQIInfo:
    """OpenWeather's AQI (1-5 scale).
    
    Note: Different from EPA AQI (0-500) calculated separately.
    """
    aqi: int


@dataclass
class AirQualityData:
    """Single timestamped measurement point."""
    dt: int  # Unix timestamp
    main: AQIInfo
    components: PollutantComponents


@dataclass
class AirQualityResponse:
    """Complete API response with location and forecast data."""
    coord: Coordinates
    list: List[AirQualityData]