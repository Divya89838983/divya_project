"""
AQI forecast visualization with Plotly.

Creates interactive time series plots showing maximum AQI over time
with color-coded EPA category zones.
"""

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime


def calculate_aqi_over_time(air_quality_list, calculate_all_aqi_values):
    """Extract max AQI for each forecast timestamp.
    
    Args:
        air_quality_list: List of AirQualityData objects
        calculate_all_aqi_values: Function to compute AQI values
    
    Returns:
        tuple: (dates, max_aqi_values) as lists
    """
    dates = []
    max_aqi_values = []
    
    for data_point in air_quality_list:
        dt_human = datetime.fromtimestamp(data_point.dt)
        dates.append(dt_human)
        
        # Get AQI for all pollutants and take maximum
        aqi_values = calculate_all_aqi_values(data_point.components)
        max_aqi = max(aqi_values)
        max_aqi_values.append(max_aqi)
    
    return dates, max_aqi_values


def get_aqi_ranges():
    """EPA AQI category definitions.
    
    Returns:
        list: Tuples of (min, max, label, hex_color)
    """
    return [
        (0, 50, 'Good', '#00e400'),
        (50, 100, 'Moderate', '#ffff00'),
        (100, 150, 'Unhealthy for Sensitive Groups', '#ff7e00'),
        (150, 200, 'Unhealthy', '#ff0000'),
        (200, 300, 'Very Unhealthy', '#8f3f97'),
        (300, 500, 'Hazardous', '#7e0023')
    ]


def create_aqi_plot(dates, max_aqi_values, display_name):
    """Build Plotly figure with AQI forecast and colored zones.
    
    Args:
        dates: List of datetime objects
        max_aqi_values: List of AQI values
        display_name: Location name for title
    
    Returns:
        plotly.graph_objects.Figure
    """
    aqi_ranges = get_aqi_ranges()
    
    # Set y-axis range to fit data with 10% padding
    max_observed_aqi = max(max_aqi_values)
    y_max = min(max_observed_aqi * 1.1, 500)
    
    fig = go.Figure()
    
    # Add colored background zones for relevant AQI categories
    relevant_ranges = [r for r in aqi_ranges if r[0] <= y_max]
    if not any(r[1] >= y_max for r in relevant_ranges):
        # Partial range at top if y_max cuts through a category
        for start, end, label, color in aqi_ranges:
            if start <= y_max <= end:
                relevant_ranges.append((start, y_max, label, color))
                break
    
    for start, end, label, color in relevant_ranges:
        actual_end = min(end, y_max)
        display_end = int(actual_end)
        
        # Create filled area using polygon technique
        fig.add_trace(
            go.Scatter(
                x=dates + dates[::-1],
                y=[actual_end] * len(dates) + [start] * len(dates),
                fill='tonexty',
                fillcolor=f'rgba{tuple(list(int(color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + [0.1])}',
                line=dict(width=0),
                showlegend=True,
                name=f'{label} ({start}-{display_end})',
                hoverinfo='skip'
            )
        )

    # Assign marker colors based on AQI category
    color_list = []
    for aqi in max_aqi_values:
        matched = False
        for start, end, _, color in aqi_ranges:
            if start <= aqi <= end:
                marker_color = color
                matched = True
                break
        if not matched:  # GOTCHA: Handle edge cases above 500
            marker_color = '#7e0023'  # Default to Hazardous
        color_list.append(marker_color)

    # Add main AQI trend line with colored markers
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=max_aqi_values,
            mode='lines+markers',
            name='Max AQI',
            line=dict(width=3, color='black'),
            marker=dict(
                size=8,
                color=color_list,
                line=dict(width=1, color='black')
            ),
            hovertemplate='<b>%{x}</b><br>Max AQI: %{y:.1f}<br>Level: %{customdata}<extra></extra>',
            customdata=[next(label for start, end, label, _ in aqi_ranges if start <= aqi <= end)
                       for aqi in max_aqi_values]
        )
    )
    
    # Configure layout
    fig.update_layout(
        title=f'Maximum Air Quality Index Forecast - {display_name}',
        xaxis_title='DateTime',
        yaxis_title='Maximum AQI',
        hovermode='x unified',
        showlegend=True,
        height=500,
        legend=dict(
            groupclick="toggleitem",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.02  # Position legend outside plot area
        ),
        yaxis=dict(
            range=[0, y_max],
            tickmode='linear',
            dtick=max(10, int(y_max/20))
        )
    )
    
    # Add subtle gridlines
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
    
    return fig


def display_current_air_quality(air_pollution_data, calculate_all_aqi_values):
    """Show current AQI metrics in a 3-column grid.
    
    Args:
        air_pollution_data: AirQualityResponse object
        calculate_all_aqi_values: AQI calculation function
    """
    st.subheader("📊 Current Air Quality")
    
    # Use first data point (current conditions)
    components = air_pollution_data.list[0].components
    aqi_values = calculate_all_aqi_values(components)
    pollutant_names = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3']
    
    cols = st.columns(3)
    for idx, (name, value) in enumerate(zip(pollutant_names, aqi_values)):
        with cols[idx % 3]:
            # Get raw concentration (handle PM2.5 naming)
            raw_value = getattr(components, name.lower().replace('.', '_'))
            st.metric(
                label=name,
                value=f"AQI: {value:.1f}",
                delta=f"Raw: {raw_value:.2f}"
            )


def display_aqi_forecast(air_pollution_data, display_name, calculate_all_aqi_values):
    """Render AQI forecast chart.
    
    Args:
        air_pollution_data: AirQualityResponse object
        display_name: Location name
        calculate_all_aqi_values: AQI calculation function
    """
    st.subheader("📈 Air Quality Forecast")
    dates, max_aqi_values = calculate_aqi_over_time(
        air_pollution_data.list,
        calculate_all_aqi_values
    )
    fig = create_aqi_plot(dates, max_aqi_values, display_name)
    st.plotly_chart(fig, use_container_width=True)