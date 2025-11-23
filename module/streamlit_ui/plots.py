"""
Plotting module for the Air Quality Analysis application.
Contains functions for creating and displaying AQI plots and visualizations.
"""
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

def calculate_aqi_over_time(air_quality_list, calculate_all_aqi_values):
    """Calculate maximum AQI values over time."""
    dates = []
    max_aqi_values = []
    
    for d in air_quality_list:
        dt_human = datetime.fromtimestamp(d.dt)
        dates.append(dt_human)
        aqi_values = calculate_all_aqi_values(d.components)
        max_aqi = max(aqi_values)
        max_aqi_values.append(max_aqi)
    
    return dates, max_aqi_values

def get_aqi_ranges():
    """Get the AQI ranges and their corresponding colors."""
    return [
        (0, 50, 'Good', '#00e400'),
        (50, 100, 'Moderate', '#ffff00'),
        (100, 150, 'Unhealthy for Sensitive Groups', '#ff7e00'),
        (150, 200, 'Unhealthy', '#ff0000'),
        (200, 300, 'Very Unhealthy', '#8f3f97'),
        (300, 500, 'Hazardous', '#7e0023')
    ]

def create_aqi_plot(dates, max_aqi_values, display_name):
    """Create a Plotly figure for AQI visualization."""
    aqi_ranges = get_aqi_ranges()
    
    # Calculate plot range
    max_observed_aqi = max(max_aqi_values)
    y_max = min(max_observed_aqi * 1.1, 500)
    
    # Create plot
    fig = go.Figure()
    
    # Add colored range areas
    relevant_ranges = [r for r in aqi_ranges if r[0] <= y_max]
    if not any(r[1] >= y_max for r in relevant_ranges):
        for start, end, label, color in aqi_ranges:
            if start <= y_max <= end:
                relevant_ranges.append((start, y_max, label, color))
                break
    
    for start, end, label, color in relevant_ranges:
        actual_end = min(end, y_max)
        # Convert to integer for display purposes
        display_end = int(actual_end)
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

    # Create color list for markers
    color_list = []
    for aqi in max_aqi_values:
        matched = False
        for start, end, _, color in aqi_ranges:
            if start <= aqi <= end:
                marker_color = color
                matched = True
                break
        if not matched:
            print(f"Warning: No AQI range matched for value {aqi:.2f}")
        color_list.append(marker_color)

    # Add AQI line
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
    
    # Update layout
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
            x=1.02
        ),
        yaxis=dict(
            range=[0, y_max],
            tickmode='linear',
            dtick=max(10, int(y_max/20))
        )
    )
    
    # Add gridlines
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
    
    return fig

def display_current_air_quality(air_pollution_data, calculate_all_aqi_values):
    """Display current air quality metrics."""
    st.subheader("📊 Current Air Quality")
    components = air_pollution_data.list[0].components
    aqi_values = calculate_all_aqi_values(components)
    pollutant_names = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3']
    
    cols = st.columns(3)
    for idx, (name, value) in enumerate(zip(pollutant_names, aqi_values)):
        with cols[idx % 3]:
            raw_value = getattr(components, name.lower().replace('.', '_'))
            st.metric(
                label=name,
                value=f"AQI: {value:.1f}",
                delta=f"Raw: {raw_value:.2f}"
            )

def display_aqi_forecast(air_pollution_data, display_name, calculate_all_aqi_values):
    """Display AQI forecast plot."""
    st.subheader("📈 Air Quality Forecast")
    dates, max_aqi_values = calculate_aqi_over_time(air_pollution_data.list, calculate_all_aqi_values)
    fig = create_aqi_plot(dates, max_aqi_values, display_name)
    st.plotly_chart(fig, use_container_width=True)