# importing PACKAGES:

# data analysis
import pandas as pd
import requests
from air_quality_models import AirQualityResponse, Coordinates, Components, AirQualityData, Main


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
    if val<=1:
        return round(val*(50), 2)
    elif val>1 and val<=2:
        return round(50 + (val-1)*(50), 2)
    elif val>2 and val<=10:
        return round(100 + (val-2)*(50/4), 2)
    elif val>10 and val<=17:
        return round(200 + (val-10)*(100/7), 2)
    elif val>17 and val<=34:
        return round(300 + (val-17)*(100/17), 2)
    elif val>17 and val<=51:
        return round(400 +(val-34)*(100/17), 2)
    elif val>51:
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
    
complete_data = pd.read_csv('dummy_air_quality.csv')

def read_pollution_data_from_api():
    url = "http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat=37.61&lon=122.38&appid=35f1ed7f152fe596d9684a0b73a60a9b"
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

air_pollution_json_data = read_pollution_data_from_api()
air_pollution_object_data = convert_json_to_object(air_pollution_json_data)
print("*******")
print(air_pollution_object_data.coord.lat)    
print(air_pollution_object_data.coord.lon)    
print(air_pollution_object_data.list)
print('*********')
