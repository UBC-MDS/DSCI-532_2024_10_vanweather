from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime
import altair as alt

def filter_aggregation_col(df, column_name, agg_time="YE", start_time="2000-01-01", end_time="2023-01-01"):
    start_time = pd.to_datetime(start_time)
    end_time = pd.to_datetime(end_time)

    # Filter DataFrame based on time range
    filtered_df = df.loc[start_time:end_time]

    # Aggregate the specified column based on agg_time
    aggregated_df = filtered_df[column_name].resample(agg_time).mean()

    # Clear the data if the year is chosen and a full year does not exist for start/end year
    if agg_time == 'YE':
        # Find the start year and end year
        start_year = start_time.year
        end_year = end_time.year

        # Check if the start year and end year form a full year range
        if (start_time != pd.Timestamp(f"{start_year}-01-01")):
            aggregated_df = aggregated_df.iloc[1:]

        if (end_time != pd.Timestamp(f"{end_year}-12-31")):
            aggregated_df = aggregated_df.iloc[:-1]

    return aggregated_df

def time_series_plot_altair(df, column_name='temperature_2m_max'):
    # Ensure the dataframe has the expected date column after resetting the index
    df = df.reset_index().rename(columns={df.index.name: 'date'})

    # Create the Altair line chart
    chart = alt.Chart(df).mark_line(
        point=True,  # Add points to the line for each data point
        color='steelblue',  # Line color
        size=2  # Line thickness
    ).encode(
        x=alt.X('date:T', title='Date'),  # Temporal axis (time)
        y=alt.Y(f'{column_name}:Q', title='Temperature (°C)'),  # Quantitative axis (the data)
        tooltip=[alt.Tooltip('date:T', title='Date'), alt.Tooltip(f'{column_name}:Q', title='Temperature (°C)')]  # Tooltip for interactivity
    ).properties(
        title=f'{column_name.capitalize()} over Time',  # Chart title
        width=500,  # Width of the chart
        height=300  # Height of the chart
    ).configure_title(
        fontSize=15,
        font='Courier',
        anchor='start',
        color='gray'
    ).configure_view(
        strokeOpacity=0  # Remove the border around the chart
    )
    return chart

def generateDropDownrDiv(valueName, labelName, options=[], value=None):
    return html.Div([
        dbc.Label(labelName, className='filter_label'),
        dcc.Dropdown(id=valueName, options=options, value=value, className='filter_input'),
    ])