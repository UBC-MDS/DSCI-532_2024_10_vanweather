from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import matplotlib.pyplot as plt


# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#Read the CSV file
df = pd.read_csv('data/raw/van_weather_1974-01-01_2024-03-15.csv', encoding='latin-1')
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year

# Layout
app.layout = dbc.Container(
    [
    #html.Div([html.H1("VanWeather - Vancouver Climate Extreams Dash", style={'color': 'green', 'font-size': '24px', 'text-align': 'center'})]),
    dbc.Row(
            dbc.Col(
                html.H1("VanWeather - Vancouver Climate Extremes Dash", style={'color': 'navy', 'font-size': '24px', 'text-align': 'center'}),
                width={'size': 12, 'offset': 0}
            ),
            justify="center"
    ),
    dbc.Row([
            dbc.Col(
                [
                    html.Label('Date',style={'margin-bottom': '10px', 'display': 'block' }),
                    dcc.RangeSlider(
                        id='year-slider',
                        min=int(df['year'].min()),
                        max=int(df['year'].max()),
                        step=1,
                        marks={year: str(year) for year in range(int(df['year'].min()), int(df['year'].max()) + 1, 10)},
                        value=[int(df['year'].min()), int(df['year'].max())],
                        tooltip={'always_visible': True, 'placement': 'bottom'}
                    ),
                    html.Div("Filter1"),
                    html.Div("Filter2"),
                    html.Div("Filter3"),
                ], width=3), 
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
                        dbc.Col(html.Div("Dynamic time series")),
                        dbc.Col(html.Div("Dynamic time series")),
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div("Dynamic time series")),
                        dbc.Col(html.Div("Dynamic time series")),
                    ])
                ]),
            ]
        ),
        ])
    ]
)

# Server side callbacks/reactivity
@app.callback(
    Output('temperature-plot', 'figure'),
    [Input('year-slider', 'value')]
)
def update_temperature_plot(year_range):
    filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    resampled_df = filtered_df.resample('Y', on='date').mean().reset_index()
    
    fig = px.line(resampled_df, x='year', y='apparent_temperature_mean', title='Temperature Over Years')
    fig.update_xaxes(title_text='Year', showgrid=True)
    fig.update_yaxes(title_text='Temperature', showgrid=True)
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='white',
            xaxis=dict(showline=True, linecolor='black'),
            yaxis=dict(showline=True, linecolor='black')),
    fig.update_layout(yaxis=dict(range=[filtered_df['apparent_temperature_mean'].min(), filtered_df['apparent_temperature_mean'].max()]))
    return fig

# Run the app/dashboard
if __name__ == '__main__':
    # app.run(debug=True)
    app.server.run(debug=True, port=8080, host='127.0.0.1')