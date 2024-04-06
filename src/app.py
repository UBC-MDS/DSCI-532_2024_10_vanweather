from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime
import altair as alt
from utils import *


# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#Read the CSV file
df = pd.read_csv('data/raw/van_weather_1974-01-01_2024-03-15.csv', encoding='latin-1', index_col='date', parse_dates=True)
df['date'] = pd.to_datetime(df.index)
df['year'] = df['date'].dt.year

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


# Date slider object
dateslider = dcc.RangeSlider(
    id='year-slider',
    min=int(df['year'].min()),
    max=int(df['year'].max()),
    step=1,
    marks={year: str(year) for year in range(int(df['year'].min()), int(df['year'].max()) + 1, 10)},
    value=[int(df['year'].min()), int(df['year'].max())],
    tooltip={'always_visible': True, 'placement': 'bottom'}
)

dropdown_time = html.Div(generateDropDownrDiv(
    valueName="agg_time",
    labelName='Aggregation for charts',
    options=['Day','Week','Month','Year'],
    value='Year')
)
dropdown_temp = html.Div(generateDropDownrDiv(
    valueName="temp_var",
    labelName='Temperature variable to visualize',
    options=['Maximum temperature (C) at 2m', 'Minimum temperature (C) at 2m', 'Mean temperature (C) at 2m',
             'Maximum apparent temperature (C)', 'Minimum apparent temperature (C)', 'Mean apparent temperature (C)'],
    value='Mean apparent temperature (C)')
)
dropdown_precipitation = html.Div(generateDropDownrDiv(
    valueName="precipitation_var",
    labelName='Precipitation variable to visualize',
    options=['Sum of precipitation (mm)', 'Sum of rain (mm)', 'Sum of snowfall (cm)', 'Hours of precipitation'],
    value='Sum of precipitation (mm)')
)
dropdown_wind = html.Div(generateDropDownrDiv(
    valueName="wind_var",
    labelName='Wind variable to visualize',
    options=['Maximum wind speed','Maximum wind gust'],
    value='Maximum wind speed')
)
dropdown_sun = html.Div(generateDropDownrDiv(
    valueName="sun_var",
    labelName='Sun variable to visualize',
    options=['Sum of shortwave radiation (MJ)','Evapotranspiration (mm)'],
    value='Sum of shortwave radiation (MJ)')
)


sidebar = dbc.Col(
    [
        html.Label('Date',style={'margin-bottom': '10px', 'display': 'block' }),
        dateslider,
        dropdown_time,
        dropdown_temp,
        dropdown_precipitation,
        dropdown_wind,
        dropdown_sun
    ], width=2.5)



# Layout
app.layout = dbc.Container(
    [
    #html.Div([html.H1("VanWeather - Vancouver Climate Extreams Dash", style={'color': 'green', 'font-size': '24px', 'text-align': 'center'})]),
    dbc.Row(
            dbc.Col(
                html.H1("VanWeather - Vancouver Climate Weather Dashboard",
                        style={'color': 'navy', 'font-size': '24px', 'text-align': 'center'}),
                width={'size': 12, 'offset': 0}
            ),
            justify="center"
    ),
    dbc.Row([sidebar,
                #md=2),
        dbc.Col(
            [
                #dbc.Row(html.Div("VanWeather - Vancouver Climate Extreams Dash")),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Div("KPI 1"),
                            html.Div("KPI 2"),
                            html.Div("KPI 3"),
                        ],
                            style={'display': 'flex', 'justify-content': 'space-around', 'align-items': 'center'}
                        ),
                    ]),
                dbc.Col(
                dcc.Graph(id='temperature-plot', config={'displayModeBar': True}),
                width=9,
                style={'background-color': 'white', 'border': '1px solid lightgray', 'border-radius': '5px', 'padding': '10px'}
            ),
                ]),
                dbc.Col([
                    dbc.Row([
                        dbc.Col(html.Div(dvc.Vega(id='precipitation-plot', spec={}))),
                        dbc.Col(html.Div(dvc.Vega(id='temp-plot', spec={})))
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div(dvc.Vega(id='wind-plot', spec={}))),
                        dbc.Col(html.Div(dvc.Vega(id='solar-plot', spec={}))),
                    ]),
                ]),
            ]
        ),
        ])
    ]
)

# Server side callbacks/reactivity

# Date option
agg_dict = {'Day': 'D', "Week": 'W', "Month": "ME", "Year": "YE"}

@app.callback(
    Output('temperature-plot', 'figure'),
    [Input('year-slider', 'value')]
)
def overall_temperature_plot(year_range):
    # filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    filtered_df = df
    resampled_df = filtered_df.resample('Y', on='date').mean().reset_index()
    resampled_df = resampled_df[: -1]
    
    fig = px.line(resampled_df, x='year', y='apparent_temperature_mean', title='Temperature Over Years')
    fig.update_xaxes(title_text='Year', showgrid=True)
    fig.update_yaxes(title_text='Temperature', showgrid=True)
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='white',
            xaxis=dict(showline=True, linecolor='black'),
            yaxis=dict(showline=True, linecolor='black'),
                      height=300),
    fig.update_layout(yaxis=dict(range=[resampled_df['apparent_temperature_mean'].min(), resampled_df['apparent_temperature_mean'].max()]))
    return fig

@app.callback(
    Output('precipitation-plot', 'spec'),
    [Input('year-slider', 'value'),
     Input('agg_time', 'value'),
     Input('precipitation_var', 'value')]
)
def update_precipitation_plot(year_range, agg_time, var):
    min_time = datetime(year_range[0], 1, 1)
    max_time = datetime(year_range[1], 1, 1)
    agg_t = agg_dict[agg_time]
    var_t = var_dict[var]
    filtered_df = filter_aggregation_col(df, var_t, agg_t, min_time, max_time)
    fig = time_series_plot_altair(filtered_df, filtered_df.name)
    return fig.to_dict()

@app.callback(
    Output('temp-plot', 'spec'),
    [Input('year-slider', 'value'),
    Input('agg_time', 'value'),
    Input('temp_var', 'value')]
)
def update_temperature_plot(year_range, agg_time, var):
    min_time = datetime(year_range[0], 1, 1)
    max_time = datetime(year_range[1], 1, 1)
    agg_t = agg_dict[agg_time]
    var_t = var_dict[var]
    filtered_df = filter_aggregation_col(df, var_t, agg_t, min_time, max_time)
    fig = time_series_plot_altair(filtered_df, filtered_df.name)
    return fig.to_dict()

@app.callback(
    Output('wind-plot', 'spec'),
    [Input('year-slider', 'value'),
    Input('agg_time', 'value'),
    Input('wind_var', 'value')]
)
def update_wind_plot(year_range, agg_time, var):
    min_time = datetime(year_range[0], 1, 1)
    max_time = datetime(year_range[1], 1, 1)
    agg_t = agg_dict[agg_time]
    var_t = var_dict[var]
    filtered_df = filter_aggregation_col(df, var_t, agg_t, min_time, max_time)
    fig = time_series_plot_altair(filtered_df, filtered_df.name)
    return fig.to_dict()

@app.callback(
    Output('solar-plot', 'spec'),
    [Input('year-slider', 'value'),
    Input('agg_time', 'value'),
    Input('sun_var', 'value')]
)
def update_wind_plot(year_range, agg_time, var):
    min_time = datetime(year_range[0], 1, 1)
    max_time = datetime(year_range[1], 1, 1)
    agg_t = agg_dict[agg_time]
    var_t = var_dict[var]
    filtered_df = filter_aggregation_col(df, var_t, agg_t, min_time, max_time)
    fig = time_series_plot_altair(filtered_df, filtered_df.name)
    return fig.to_dict()

# Run the app/dashboard
if __name__ == '__main__':
    # app.run(debug=True)
    app.server.run(debug=True, port=8080, host='127.0.0.1')
#%%
