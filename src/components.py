from utils import generateDatePickerDiv, generateDropDownrDiv
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from dash import html

from_date = '2014-01-01'
to_date = '2024-01-01'

temp_change = 0
temp_over_30 = 0
preci_change = 0

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
        value='Sum of shortwave radiation (MJ)'),
    html.Button('Reload Dataframe', id='reload-button', n_clicks=0)
], className='filter_container')

mainContainer = dbc.Container(
    [dbc.Col(
            [
                dbc.Row(html.Div("VanWeather - Vancouver Climate Tracker", className='title_bucket')),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.Div('Days over 30°C:'),
                                html.Div(temp_over_30, id='temp-over-30', className="kpi_highlight"),
                                html.Div('(during selected period)'),
                            ], className='kpi_card'),
                            html.Div([
                                html.Div('Temperature changes(°C):'),
                                html.Div(f'{temp_change:.2f}', id='temp-change', className="kpi_highlight"),
                                html.Div(id='temp-prev-period-info'),
                            ], className='kpi_card'),
                            html.Div([
                                html.Div('Precipitation changes(mm):'),
                                html.Div(preci_change, id='preci-change', className="kpi_highlight"),
                                html.Div(id='pre-prev-period-info'),
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