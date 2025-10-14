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

    # params = {"lat": 50, "lon":50}
    # headers = {"Authorization": "Bearer "+API_KEY}  # if needed
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


print("**********")
air_pollution_json_data = read_pollution_data_from_api()
air_pollution_object_data = convert_json_to_object(air_pollution_json_data)
print("*******")
# print(air_pollution_object_data.coord.lat)    
# print(air_pollution_object_data.coord.lon)     # 12.97
print(air_pollution_object_data.list)


# all_stations = complete_data.iloc[1931:] if len(complete_data) > 1931 else complete_data.copy()
# # Convert 'From Date' to datetime
# all_stations['Date'] = pd.to_datetime(all_stations['From Date'], format='%Y-%m-%d')
# # Drop original date columns
# all_stations.drop(columns=['From Date', 'To Date'], inplace=True)
# # Check result
# print(all_stations.head())

# stations = all_stations.columns.get_level_values(0).unique().tolist()[1:-1]
# print("stations")
# print(stations)


# # Assume all_stations already has a 'Date' column
# stations = all_stations['Location'].unique()
# all_data = pd.DataFrame()
# all_data['Date'] = all_stations['Date'].unique()  # dates

# for station in stations:
#     station_data = all_stations[all_stations['Location'] == station].reset_index(drop=True)
#     all_data[(station, 'PM2.5')] = station_data['PM2.5(ug/m3)'].apply(PM25)
#     all_data[(station, 'PM10')] = station_data['PM10(ug/m3)'].apply(PM10)
#     all_data[(station, 'NO2')] = station_data['NO2(ug/m3)'].apply(NO2)
#     all_data[(station, 'SO2')] = station_data['SO2(ug/m3)'].apply(SO2)
#     all_data[(station, 'CO')] = station_data['CO(mg/m3)'].apply(CO)
#     all_data[(station, 'O3')] = station_data['Ozone(ug/m3)'].apply(O3)

# # Optional: convert columns to MultiIndex
# # After filling all_data
# all_data.columns = pd.MultiIndex.from_tuples(
#     [('Date', '')] + [col for col in all_data.columns if isinstance(col, tuple)]
# )

# top_pollutants_by_station = {}

# for station in stations:
#     level_columns = all_data[station]
#     correlation_matrix = level_columns.corr()
#     top_pollutants = correlation_matrix.abs().sum().nlargest(4).index 
#     top_pollutants_by_station[station] = list(top_pollutants)

# print("top pollutant by station")

# print(top_pollutants_by_station)




# stations = complete_data['Location'].unique()
# for station in stations:
#     station_data = complete_data[complete_data['Location'] == station]
#     print(station, station_data.shape)
#     station_data['Date']

    


print('*********')