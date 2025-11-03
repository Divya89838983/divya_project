"""
Functions for visualizing air quality data using Plotly.
"""

from datetime import datetime
import plotly.graph_objects as go
from .aqi_calculators import calculate_all_aqi_values

def plot_max_aqi_over_time(dates, max_aqi_values, location):
    """
    Plot the maximum AQI (0-500 scale) over time using Plotly
    
    Args:
        dates: List of datetime objects
        max_aqi_values: List of maximum AQI values (0-500 scale)
        location: Name of the location being analyzed
    """
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=max_aqi_values,
            mode='lines+markers',
            name=f'Max AQI - {location}',
            line=dict(width=2),
            marker=dict(size=8),
            hovertemplate='<b>%{x}</b><br>' +
                         f'Location: {location}<br>' +
                         'Max AQI: %{y:.1f}<extra></extra>'
        )
    )

    fig.update_layout(
        title=f'Maximum Air Quality Index Over Time - {location}',
        xaxis_title='DateTime',
        yaxis_title='Maximum AQI (0-500 scale)',
        hovermode='x unified',
        showlegend=True,
        height=600,
        width=1200
    )

    # Add gridlines
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')

    fig.show()

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
        aqi_values = calculate_all_aqi_values(d.components)
        
        # Get maximum AQI (worst pollutant)
        max_aqi = max(aqi_values)
        max_aqi_values.append(max_aqi)
    
    return dates, max_aqi_values