"""
Functions for converting raw pollutant measurements to standardized AQI values.
Each function converts a specific pollutant's concentration to the 0-500 AQI scale.
"""

def calculate_all_aqi_values(components):
    """Calculate AQI values for all pollutants."""
    return [
        PM25(components.pm2_5),
        PM10(components.pm10),
        NO2(components.no2),
        SO2(components.so2),
        CO(components.co),
        O3(components.o3)
    ]

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
    """Calculate AQI for O3 (Ozone)."""
    if val <= 100:
        return round(val, 2)
    elif val <= 168:
        return round(100 + (val-100)*(100/68), 2)
    elif val <= 208:
        return round(200 + (val-168)*(100/40), 2)
    elif val <= 748:
        return round(300 + (val-208)*(100/540), 2)
    elif val <= 1288:
        return round(400 + (val-748)*(100/540), 2)
    else:
        return 500