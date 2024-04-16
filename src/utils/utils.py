import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from dash import Dash, dcc, callback, Output, Input, html
from datetime import date, datetime
import pandas as pd
import altair as alt


def generateDatePickerDiv(valueName, labelName, 
                          start_date, end_date
                          ):
    return html.Div([
        dbc.Label(labelName, className='filter_label'),
        dcc.DatePickerRange(
            id=valueName,
            clearable=True,
            start_date=date(2014, 1, 1),
            end_date=date(2024,1,1),
            # calendar_orientation='vertical'
            with_portal=True,
        )
    ])


def generateChart(id, spec):
    return dbc.Col([
            dvc.Vega(id=id, spec=spec, style={'width': '100%' }),
        ])


var_dict_swapped = {
    'temperature_2m_max': 'Maximum temperature (C) at 2m',
    'temperature_2m_min': 'Minimum temperature (C) at 2m',
    'temperature_2m_mean': 'Mean temperature (C) at 2m',
    'apparent_temperature_max': 'Maximum apparent temperature (C)',
    'apparent_temperature_min': 'Minimum apparent temperature (C)',
    'apparent_temperature_mean': 'Mean apparent temperature (C)',
    'precipitation_sum': 'Sum of precipitation (mm)',
    'rain_sum': 'Sum of rain (mm)',
    'snowfall_sum': 'Sum of snowfall (cm)',
    'precipitation_hours': 'Hours of precipitation',
    'wind_speed_10m_max': 'Maximum wind speed',
    'wind_gusts_10m_max': 'Maximum wind gust',
    'shortwave_radiation_sum': 'Sum of shortwave radiation (MJ)',
    'et0_fao_evapotranspiration': 'Evapotranspiration (mm)'
}

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
        color='#214d2e',  # Line color
        size=2  # Line thickness
    ).encode(
        x=alt.X('date:T', title='Date'),  # Temporal axis (time)
        y=alt.Y(f'{column_name}:Q', title=var_dict_swapped[column_name]),  # Quantitative axis (the data)
        tooltip=[alt.Tooltip('date:T', title='Date'), alt.Tooltip(f'{column_name}:Q', title=var_dict_swapped[column_name])]  # Tooltip for interactivity
    ).properties(
        title=f'{var_dict_swapped[column_name].capitalize()} over Time',  # Chart title
        width=500,  # Width of the chart
        height=200  # Height of the chart
    ).configure_title(
        fontSize=15,
        #font='Courier',
        anchor='start',
        color='gray'
    ).configure_view(
        stroke=None  # Remove the border around the chart
    ).configure_axis(
        grid=False,
        labelFontSize=10
    )
    return chart

def temperature_plot_altair(df):
    chart = alt.Chart(df, title='Apparant Temperature Change (°C)').mark_line(opacity=0.8, color='#214d2e').encode(
            alt.X('date:T').title('Date'),
            alt.Y('apparent_temperature_mean:Q').title('apparent temperature'),
            tooltip=[alt.Tooltip('date:T', title='Date'), alt.Tooltip(f'apparent_temperature_mean:Q', title='Mean Apparant Temperature')]
        ).properties(
            width=600,
            height=100
        ).configure_title(
            fontSize=13,
            #font='Courier',
            anchor='start',
            color='gray'
        ).configure_axis(
            labelFontSize=10,
            grid=False
        ).configure_view(
            stroke=None
        ).interactive()
    return chart


def generateDropDownrDiv(valueName, labelName, options=[], value=None):
    return html.Div([
        dbc.Label(labelName, className='filter_label'),
        dcc.Dropdown(id=valueName, options=options, value=value, className='filter_input', style={
            'font-size': "80%"},),
    ])