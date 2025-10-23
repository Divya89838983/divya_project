# importing PACKAGES:

# data analysis
import pandas as pd
import requests
from air_quality_models import AirQualityResponse, Coordinates, Components, AirQualityData, Main
from datetime import datetime
import matplotlib.pyplot as plt
from module.keys import appid

def PM25(val):
    if val<=30:
        return round(val*(50/30), 2)
    elif val>30 and val<=60:
        return round(50 + (val-30)*(50/30), 2)
    elif val>60 and val<=90:
        return round(100 + (val-60)*(100/30), 2)
    elif val>90 and val<=120:
        return round(200 + (val-90)*(100/30), 2)
    elif val>120 and val<=250:
        return round(300 +(val-120)*(100/130), 2)
    elif val>250 and val<=380:
        return round(400 +(val-250)*(10/13), 2)  
    elif val>380:
        return 500
    

def PM10(val):
    if val<=100:
        return round(val, 2)
    elif val>100 and val<=250:
        return round(100 + (val-100)*(100/150), 2)
    elif val>250 and val<=350:
        return round(200 + (val-250), 2)
    elif val>350 and val<=430:
        return round(300 + (val-350)*(100/80), 2)
    elif val>430 and val<=510:
        return round(400 +(val-430)*(100/80), 2) 
    elif val>510:
        return 500
    
def NO2(val):
    if val<=40:
        return round(val*(50/40), 2)
    elif val>40 and val<=80:
        return round(50 + (val-40)*(50/40), 2)
    elif val>80 and val<=180:
        return round(100 + (val-80), 2)
    elif val>180 and val<=280:
        return round(200 + (val-180), 2)
    elif val>280 and val<=400:
        return round(300 + (val-280)*(100/120), 2)
    elif val>400 and val<=510:
        return round(400 +(val-400)*(100/120), 2)
    elif val>510:
        return 500
    

def SO2(val):
    if val<=40:
        return round(val*(50/40), 2)
    elif val>40 and val<=80:
        return round(50 + (val-40)*(50/40), 2)
    elif val>80 and val<=380:
        return round(100 + (val-80)*(100/300), 2)
    elif val>380 and val<=800:
        return round(200 + (val-380)*(100/420), 2)
    elif val>800 and val<=1600:
        return round(300 + (val-800)*(100/800), 2)
    elif val>1600 and val<=2400:
        return round(400 +(val-1600)*(100/800), 2)
    elif val>2400:
        return 500

def CO(val):
    # CH this was quite wrong b/c of unit conversion
    # Convert µg/m³ to mg/m³ first
    val_mg = val / 1000.0
    
    if val_mg<=1:
        return round(val_mg*(50), 2)
    elif val_mg>1 and val_mg<=2:
        return round(50 + (val_mg-1)*(50), 2)
    elif val_mg>2 and val_mg<=10:
        return round(100 + (val_mg-2)*(50/4), 2)
    elif val_mg>10 and val_mg<=17:
        return round(200 + (val_mg-10)*(100/7), 2)
    elif val_mg>17 and val_mg<=34:
        return round(300 + (val_mg-17)*(100/17), 2)
    elif val_mg>34 and val_mg<=51:   
        return round(400 +(val_mg-34)*(100/17), 2)
    elif val_mg>51:
        return 500

def O3(val):
    if val<=100:
        return round(val, 2)
    elif val>100 and val<=168:
        return round(100 + (val-100)*(100/68), 2)
    elif val>168 and val<=208:
        return round(200 + (val-168)*(100/40), 2)
    elif val>208 and val<=748:
        return round(300 + (val-208)*(100/540), 2)
    elif val>748 and val<=1288:
        return round(400 +(val-748)*(100/540), 2)
    elif val>1288:
        return 500
    
# complete_data = pd.read_csv('dummy_air_quality.csv')

# convert loation to lat long using OpenMeteo's API
def get_coordinates_from_location(location_name):
    """
    Get latitude and longitude from location name (e.g., "San Francisco", "Ames, IA", "Paris, France")
    using Open-Meteo Geocoding API
    
    returns (latitude, longitude) or None if not found
    """
    
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': location_name,
        'format': 'json',
        'limit': 1,  # Just get the best match for production use
        'addressdetails': 1
    }
    headers = {
        'User-Agent': 'AirQualityApp/1.0'  # Required by Nominatim
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if data and len(data) > 0:
            result = data[0] # first result is the best match
            display_name = result.get('display_name', 'Unknown')
            print(f"Found location: {display_name}") # debug print
            
            lat = float(result['lat'])
            lon = float(result['lon'])
            return lat, lon
        else:
            print(f"No results found for location: {location_name}")
            return None, None
            
    except requests.RequestException as e:
        print(f"Error fetching coordinates: {e}")
        return None, None


'''
read_pollution_data_from_api() needs to get lat,long,pollution type and appid as arguments
'''
# CH ask the user for a location, convert to lat/long and give these to the function instead of hardcoding
def read_pollution_data_from_api():
    url = f"http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat=37.61&lon=122.38&appid={appid}"
    response = requests.get(url)
    air_pollution_data_json = response.json()
    return air_pollution_data_json

def convert_json_to_object(air_pollution_json_data):
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

# MAIN
# get lat/long from user input location
location = input("Enter a location (e.g., 'Ames, IA'): ")
lat, lon = get_coordinates_from_location(location)
print(f"{location} coordinates: {lat}, {lon}")
if lat is None:
    print("Could not get coordinates.")
    # CH: you should write a while True loop to keep asking until you get valid coordinates

air_pollution_json_data = read_pollution_data_from_api() # CH: give lat, long as aguments here instead of hardcoding
air_pollution_object_data = convert_json_to_object(air_pollution_json_data)
print("*******")
#print(air_pollution_object_data.coord.lat)    
#print(air_pollution_object_data.coord.lon)    
#print(air_pollution_object_data.list)
#print('*********')


# print out data for each time slice 
print("DateTime, AQI, PM2.5, PM10, NO2, SO2, CO, O3")
for d in air_pollution_object_data.list:
    dt_human = datetime.fromtimestamp(d.dt) # convert to human-readable format
    print(dt_human, d.main.aqi, d.components.pm2_5, PM25(d.components.pm2_5), d.components.pm10, PM10(d.components.pm10), d.components.no2, NO2(d.components.no2), d.components.so2, SO2(d.components.so2), d.components.co, CO(d.components.co), d.components.o3, O3(d.components.o3))
print('*********')

# Plot AQI over time
dates = [datetime.fromtimestamp(d.dt) for d in air_pollution_object_data.list]
aqi_values = [d.main.aqi for d in air_pollution_object_data.list] # extract AQI values
plt.plot(dates, aqi_values, marker='o')
plt.xlabel('DateTime')  
plt.ylabel('AQI')
plt.title('Air Quality Index (AQI) Over Time')
plt.xticks(rotation=90)
plt.grid()
plt.tight_layout()
plt.show()

# CH testing 0-500 AQI conversion functions
# from the first timestamp pull out the components data
# you can remove this after you;ve see the output once
components = air_pollution_object_data.list[0].components
print("Pollutant Concentration to 0-500 AQI conversions for first timestamp:")
print("PM2.5:", components.pm2_5, "->", PM25(components.pm2_5))
print("PM10:", components.pm10, "->", PM10(components.pm10))            
print("NO2:", components.no2, "->", NO2(components.no2))
print("SO2:", components.so2, "->", SO2(components.so2))
print("CO:", components.co, "->", CO(components.co))
print("O3:", components.o3, "->", O3(components.o3))

# Calculate the max 0-500 AQI for the first timestamp
aqi_values_0_500 = [
    PM25(components.pm2_5),
    PM10(components.pm10),
    NO2(components.no2),
    SO2(components.so2),
    CO(components.co),
    O3(components.o3)
]   
max_aqi_0_500 = max(aqi_values_0_500)
print("Maximum 0-500 AQI for first timestamp:", max_aqi_0_500)


def calculate_max_aqi_over_time(air_quality_list):
    """
    Calculate maximum AQI (0-500 scale) for each timestamp in the air quality data
    
    Args:
        air_quality_list: List of AirQualityData objects
    
    Returns:
        tuple: (dates_list, max_aqi_list) where:
            - dates_list: List of datetime objects
            - max_aqi_list: List of maximum AQI values (0-500 scale)
    """
    dates = []
    max_aqi_values = []
    
    for d in air_quality_list:
        # Convert timestamp to datetime
        dt_human = datetime.fromtimestamp(d.dt)
        dates.append(dt_human)
        
        # Calculate AQI for each pollutant
        aqi_values = [
            PM25(d.components.pm2_5),
            PM10(d.components.pm10),
            NO2(d.components.no2),
            SO2(d.components.so2),
            CO(d.components.co),
            O3(d.components.o3)
        ]
        
        # Get maximum AQI (worst pollutant)
        max_aqi = max(aqi_values)
        max_aqi_values.append(max_aqi)
    
    return dates, max_aqi_values


dates, max_aqi_values = calculate_max_aqi_over_time(air_pollution_object_data.list)



# plot maximum 0- 500 AQI over time
plt.figure(figsize=(12, 6))
plt.plot(dates, max_aqi_values, marker='o', linewidth=2, markersize=6)
plt.xlabel('DateTime')  
plt.ylabel('Maximum AQI (0-500 scale)')
plt.title('Maximum Air Quality Index Over Time')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()