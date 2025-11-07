from dataclasses import dataclass
from typing import List

@dataclass
class Coordinates:
    lat: float
    lon: float

@dataclass
class Components:
    co: float
    no: float
    no2: float
    o3: float
    so2: float
    pm2_5: float
    pm10: float
    nh3: float

@dataclass
class Main:
    aqi: int

@dataclass
class AirQualityData:
    dt: int
    main: Main
    components: Components

@dataclass
class AirQualityResponse:
    coord: Coordinates
    list: List[AirQualityData]