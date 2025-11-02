# Main script for Air Quality Index analysis and visualization

from geocoding import get_coordinates_from_location
from air_quality_api import read_pollution_data_from_api, convert_json_to_object
from aqi_calculators import calculate_all_aqi_values
from visualization import calculate_max_aqi_over_time, plot_max_aqi_over_time

def main():
    """
    Main function to run the Air Quality Analysis application
    """
    # Get location input with retry logic
    while True:
        location = input("Enter a location (e.g., 'Ames, IA'): ")
        (lat, lon), display_name = get_coordinates_from_location(location)
        if lat is not None and lon is not None:
            print(f"Found location: {display_name}")
            print(f"Coordinates: {lat}, {lon}")
            break
        print("Could not get coordinates. Please try again with a different location.")

    # Fetch and process air quality data
    air_pollution_json_data = read_pollution_data_from_api(lat, lon)
    air_pollution_object_data = convert_json_to_object(air_pollution_json_data)

    # Calculate and display initial AQI values
    components = air_pollution_object_data.list[0].components
    aqi_values = calculate_all_aqi_values(components)
    pollutant_names = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3']
    
    print("\nPollutant Concentration to 0-500 AQI conversions for first timestamp:")
    for name, value in zip(pollutant_names, aqi_values):
        print(f"{name}: {getattr(components, name.lower().replace('.', '_'))} -> {value}")

    # Calculate and plot maximum AQI over time
    dates, max_aqi_values = calculate_max_aqi_over_time(air_pollution_object_data.list)
    plot_max_aqi_over_time(dates, max_aqi_values, display_name or location) 

if __name__ == "__main__":
    main()