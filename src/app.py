from func import *
from datetime import datetime
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from dash import Dash, dcc, callback, Output, Input, html
from datetime import date, datetime
import pandas as pd
import altair as alt

# import sys
# sys.path.append('src/')

# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

df = pd.read_csv('../data/raw/van_weather_1974-01-01_2024-03-15.csv', encoding='latin-1', index_col='date', parse_dates=True)
df['date'] = pd.to_datetime(df.index)
df['year'] = df['date'].dt.year

from_date = '2013-01-01'
to_date = '2023-01-01'

var_dict = {
    'Maximum temperature (C) at 2m':'temperature_2m_max',
    'Minimum temperature (C) at 2m':'temperature_2m_min',
    'Mean temperature (C) at 2m':'temperature_2m_mean',
    'Maximum apparent temperature (C)':'apparent_temperature_max',
    'Minimum apparent temperature (C)':'apparent_temperature_min',
    'Mean apparent temperature (C)':'apparent_temperature_mean',
    'Sum of precipitation (mm)':'precipitation_sum',
    'Sum of rain (mm)':'rain_sum',
    'Sum of snowfall (cm)':'snowfall_sum',
    'Hours of precipitation':'precipitation_hours',
    'Maximum wind speed':'wind_speed_10m_max',
    'Maximum wind gust':'wind_gusts_10m_max',
    'Sum of shortwave radiation (MJ)':'shortwave_radiation_sum',
    'Evapotranspiration (mm)':'et0_fao_evapotranspiration'
}

temp_increase = 0.2
days_over_30 = 12
preci_decrease = 300

# Import customized css file
html.Div(id='Header', children=[
    html.Link(
        rel='stylesheet',
        href='assets/app.css'
    )
])
# Layout
filterContainer = html.Div([
    generateDatePickerDiv(
        valueName='dateRange', 
        labelName='Date Range',
        start_date=from_date,
        end_date=to_date),
    generateDropDownrDiv(
        valueName="agg_time",
        labelName='Aggregation for charts',
        options=['Day','Week','Month','Year'],
        value='Year'),
    generateDropDownrDiv(
        valueName="temp_var",
        labelName='Temperature variables',
        options=['Maximum temperature (C) at 2m', 'Minimum temperature (C) at 2m', 'Mean temperature (C) at 2m',
                'Maximum apparent temperature (C)', 'Minimum apparent temperature (C)', 'Mean apparent temperature (C)'],
        value='Mean apparent temperature (C)'),
    generateDropDownrDiv(
        valueName="precipitation_var",
        labelName='Precipitation variables',
        options=['Sum of precipitation (mm)', 'Sum of rain (mm)', 'Sum of snowfall (cm)', 'Hours of precipitation'],
        value='Sum of precipitation (mm)'),
    generateDropDownrDiv(
        valueName="wind_var",
        labelName='Wind variables',
        options=['Maximum wind speed','Maximum wind gust'],
        value='Maximum wind speed'),
    generateDropDownrDiv(
        valueName="sun_var",
        labelName='Sun variables',
        options=['Sum of shortwave radiation (MJ)','Evapotranspiration (mm)'],
        value='Sum of shortwave radiation (MJ)')
], className='filter_container')

mainContainer = dbc.Container(
    [dbc.Col(
            [
                dbc.Row(html.Div("VanWeather - Vancouver Climate Extreams Dash", className='title_bucket')),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.Div('Temperature increased by'),
                                html.Div(f'{temp_increase}°C', className="kpi_highlight"),
                                html.Div('In past 10 years.'),
                            ], className='kpi_card'),
                            html.Div([
                                html.Div('In past 10 years, temperature of'),
                                html.Div(f'{days_over_30} Days', className="kpi_highlight"),
                                html.Div('are over 30°C.'),
                            ], className='kpi_card'),
                            html.Div([
                                html.Div('Precipitation decreased by'),
                                html.Div(f'{preci_decrease}mm', className="kpi_highlight"),
                                html.Div('In past 10 years.'),
                            ], className='kpi_card'),
                        ],
                            style={'display': 'flex', 'justify-content': 'space-around', 'align-items': 'center'}
                        ),
                    ], width=5),
                    dbc.Col(dvc.Vega(id='temperature-plot', spec={}, style={'width': '100%'}), width=7),
                ]),
                dbc.Col([
                    dbc.Row([
                        dbc.Col(html.Div(dvc.Vega(id='temp-plot', spec={})), width=6),
                        dbc.Col(html.Div(dvc.Vega(id='precipitation-plot', spec={})), width=6),
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div(dvc.Vega(id='wind-plot', spec={})), width=6),
                        dbc.Col(html.Div(dvc.Vega(id='solar-plot', spec={})), width=6),
                    ])
                ]),
            ]
        )])

app.layout = html.Div([
    html.Div([filterContainer], className='nav_bar'), 
    html.Div([mainContainer], className='left_div'),
], className='main_div')

# Date option
agg_dict = {'Day': 'D', "Week": 'W', "Month": "ME", "Year": "YE"}

# Server side callbacks/reactivity
@callback(
    Output('temperature-plot', 'spec'),
    Input('dateRange', 'start_date'),
    Input('dateRange', 'end_date')
)
def update_temperature_plot(start_date, end_date):

    if not start_date:
        start_date = '2013-01-01'
    if not end_date:
        end_date = '2023-01-01'

    filtered_df = df[(df['date'] >= datetime.strptime(start_date, '%Y-%m-%d')) & (df['date'] <= datetime.strptime(end_date, '%Y-%m-%d'))]
    print(filtered_df.shape)
    return (
        alt.Chart(filtered_df, title='Apparant Temperature Change (°C)').mark_line(opacity=0.8, color='#214d2e').encode(
            alt.X('date').title('Date'),
            alt.Y('apparent_temperature_mean').title('apparent temperature'),
        ).properties(
            width=600,
            height=100
        ).configure_axis(
            labelFontSize=10,
            grid=False
        ).configure_view(
            stroke=None
        ).interactive().to_dict()
    )

@app.callback(
    Output('precipitation-plot', 'spec'),
    [Input('dateRange', 'start_date'),
     Input('dateRange', 'end_date'),
     Input('agg_time', 'value'),
     Input('precipitation_var', 'value')]
)
def update_precipitation_plot(start_date, end_date, agg_time, var):
    if not start_date:
        start_date = '2013-01-01'
    if not end_date:
        end_date = '2023-01-01'

    min_time = datetime.strptime(start_date, '%Y-%m-%d')#.date()
    max_time = datetime.strptime(end_date, '%Y-%m-%d')#.date()
    agg_t = agg_dict[agg_time]
    var_t = var_dict[var]
    filtered_df = filter_aggregation_col(df, var_t, agg_t, min_time, max_time)
    altplot = time_series_plot_altair(filtered_df, filtered_df.name)
    return altplot.to_dict()

@app.callback(
    Output('temp-plot', 'spec'),
    [Input('dateRange', 'start_date'),
     Input('dateRange', 'end_date'),
     Input('agg_time', 'value'),
     Input('temp_var', 'value')]
)
def update_temperature_plot(start_date, end_date, agg_time, var):
    if not start_date:
        start_date = '2013-01-01'
    if not end_date:
        end_date = '2023-01-01'

    min_time = datetime.strptime(start_date, '%Y-%m-%d')#.date()
    max_time = datetime.strptime(end_date, '%Y-%m-%d')#.date()
    agg_t = agg_dict[agg_time]
    var_t = var_dict[var]
    filtered_df = filter_aggregation_col(df, var_t, agg_t, min_time, max_time)
    altplot = time_series_plot_altair(filtered_df, filtered_df.name)
    return altplot.to_dict()

@app.callback(
    Output('wind-plot', 'spec'),
    [Input('dateRange', 'start_date'),
     Input('dateRange', 'end_date'),
     Input('agg_time', 'value'),
     Input('wind_var', 'value')]
)
def update_wind_plot(start_date, end_date, agg_time, var):
    if not start_date:
        start_date = '2013-01-01'
    if not end_date:
        end_date = '2023-01-01'

    min_time = datetime.strptime(start_date, '%Y-%m-%d')#.date()
    max_time = datetime.strptime(end_date, '%Y-%m-%d')#.date()
    agg_t = agg_dict[agg_time]
    var_t = var_dict[var]
    filtered_df = filter_aggregation_col(df, var_t, agg_t, min_time, max_time)
    altplot = time_series_plot_altair(filtered_df, filtered_df.name)
    return altplot.to_dict()

@app.callback(
    Output('solar-plot', 'spec'),
    [Input('dateRange', 'start_date'),
     Input('dateRange', 'end_date'),
     Input('agg_time', 'value'),
     Input('sun_var', 'value')]
)
def update_solar_plot(start_date, end_date, agg_time, var):
    if not start_date:
        start_date = '2013-01-01'
    if not end_date:
        end_date = '2023-01-01'

    min_time = datetime.strptime(start_date, '%Y-%m-%d')#.date()
    max_time = datetime.strptime(end_date, '%Y-%m-%d')#.date()
    agg_t = agg_dict[agg_time]
    var_t = var_dict[var]
    filtered_df = filter_aggregation_col(df, var_t, agg_t, min_time, max_time)
    altplot = time_series_plot_altair(filtered_df, filtered_df.name)
    return altplot.to_dict()

# Run the app/dashboard
if __name__ == '__main__':
    # app.run(debug=True)
    app.server.run(debug=True, port=8080, host='127.0.0.1')
