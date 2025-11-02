"""
Streamlit web application for Air Quality Analysis
"""

import streamlit as st
from datetime import datetime
from geocoding import get_coordinates_from_location
from air_quality_api import read_pollution_data_from_api, convert_json_to_object
from aqi_calculators import calculate_all_aqi_values
from visualization import calculate_max_aqi_over_time

# Configure the Streamlit page
st.set_page_config(
    page_title="Air Quality Analysis",
    page_icon="🌍",
    layout="wide"
)

# Add a title
st.title("🌍 Air Quality Analysis")
st.write("Enter a location to analyze its air quality data")

# Location input
location = st.text_input("Enter a location (e.g., 'Ames, IA', 'Paris, France')", "")

if location:
    # Get coordinates
    (lat, lon), display_name = get_coordinates_from_location(location)
    
    if lat is not None and lon is not None:
        st.success(f"📍 Found location: {display_name}")
        
        # Create two columns for coordinates
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"Latitude: {lat}")
        with col2:
            st.info(f"Longitude: {lon}")
        
        # Fetch and process air quality data
        with st.spinner("Fetching air quality data..."):
            air_pollution_json_data = read_pollution_data_from_api(lat, lon)
            air_pollution_object_data = convert_json_to_object(air_pollution_json_data)
        
        # Show current pollutant levels
        st.subheader("📊 Current Air Quality")
        components = air_pollution_object_data.list[0].components
        aqi_values = calculate_all_aqi_values(components)
        pollutant_names = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3']
        
        # Create a grid of metrics for each pollutant
        cols = st.columns(3)
        for idx, (name, value) in enumerate(zip(pollutant_names, aqi_values)):
            with cols[idx % 3]:
                raw_value = getattr(components, name.lower().replace('.', '_'))
                st.metric(
                    label=name,
                    value=f"AQI: {value:.1f}",
                    delta=f"Raw: {raw_value:.2f}"
                )
        
        # Calculate and display AQI over time
        st.subheader("📈 Air Quality Forecast")
        dates, max_aqi_values = calculate_max_aqi_over_time(air_pollution_object_data.list)
        
        # Create Plotly figure with color ranges
        import plotly.graph_objects as go
        
        # Define AQI ranges and their colors
        aqi_ranges = [
            (0, 50, 'Good', '#00e400'),      # Green
            (51, 100, 'Moderate', '#ffff00'), # Yellow
            (101, 150, 'Unhealthy for Sensitive Groups', '#ff7e00'),  # Orange
            (151, 200, 'Unhealthy', '#ff0000'),  # Red
            (201, 300, 'Very Unhealthy', '#8f3f97'),  # Purple
            (301, 500, 'Hazardous', '#7e0023')   # Maroon
        ]

        # Calculate the maximum AQI in our data and add some padding
        max_observed_aqi = max(max_aqi_values)
        y_max = min(max_observed_aqi * 1.1, 500)  # Add 10% padding but don't exceed 500
        
        # Filter ranges to show only those relevant to our data
        relevant_ranges = [r for r in aqi_ranges if r[0] <= y_max]
        if not any(r[1] >= y_max for r in relevant_ranges):
            # Add one more range if needed
            for start, end, label, color in aqi_ranges:
                if start <= y_max <= end:
                    relevant_ranges.append((start, y_max, label, color))
                    break

        fig = go.Figure()

        # Add colored ranges as filled areas
        for start, end, label, color in relevant_ranges:
            actual_end = min(end, y_max)
            fig.add_trace(
                go.Scatter(
                    x=dates + dates[::-1],
                    y=[actual_end] * len(dates) + [start] * len(dates),
                    fill='tonexty',
                    fillcolor=f'rgba{tuple(list(int(color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + [0.1])}',
                    line=dict(width=0),
                    showlegend=True,
                    name=f'{label} ({start}-{actual_end})',
                    hoverinfo='skip'
                )
            )

        # Add the actual AQI line on top
        fig.add_trace(
            go.Scatter(
                x=dates,
                y=max_aqi_values,
                mode='lines+markers',
                name='Max AQI',
                line=dict(
                    width=3,
                    color='black'
                ),
                marker=dict(
                    size=8,
                    color=[
                        next(color for start, end, _, color in aqi_ranges 
                             if start <= aqi <= end)
                        for aqi in max_aqi_values
                    ],
                    line=dict(width=1, color='black')
                ),
                hovertemplate=(
                    '<b>%{x}</b><br>' +
                    'Max AQI: %{y:.1f}<br>' +
                    'Level: ' + 
                    '%{customdata}<extra></extra>'
                ),
                customdata=[
                    next(label for start, end, label, _ in aqi_ranges 
                         if start <= aqi <= end)
                    for aqi in max_aqi_values
                ]
            )
        )

        fig.update_layout(
            title=f'Maximum Air Quality Index Forecast - {display_name}',
            xaxis_title='DateTime',
            yaxis_title='Maximum AQI',
            hovermode='x unified',
            showlegend=True,
            height=500,
            # Update legend to group items
            legend=dict(
                groupclick="toggleitem",
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=1.02
            ),
            # Set y-axis range to show detail
            yaxis=dict(
                range=[0, y_max],
                tickmode='linear',
                dtick=max(10, int(y_max/20))  # Dynamic tick spacing
            )
        )

        # Add gridlines
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
        
        # Display the plot
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error(f"Could not find coordinates for: {location}")
        st.warning("Please try a different location name or format (e.g., 'City, Country')")

# Add footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit • Data from OpenWeatherMap")