from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime
import altair as alt


# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

#Read the CSV file
df = pd.read_csv('/Users/katherinechen/Desktop/532_lab/DSCI-532_2024_10_vanweather/data/raw/van_weather_1974-01-01_2024-03-15.csv', encoding='latin-1', index_col='date', parse_dates=True)
df['date'] = pd.to_datetime(df.index)
df['year'] = df['date'].dt.year

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
        y=alt.Y(f'{column_name}:Q', title=column_name.capitalize()),
        tooltip=[alt.Tooltip('date:T', title='Date'), alt.Tooltip(f'{column_name}:Q', title='Temperature (°C)')]  # Tooltip for interactivity
    ).properties(
        title=f'{column_name.capitalize()} over Time',  # Chart title
        width=800,  # Width of the chart
        height=400  # Height of the chart
    ).configure_title(
        fontSize=20,
        font='Courier',
        anchor='start',
        color='gray'
    ).configure_view(
        strokeOpacity=0  # Remove the border around the chart
    )
    return chart

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
                        dbc.Col(html.Div(dvc.Vega(id='precipitation-plot', spec={}))),
                        dbc.Col(html.Div("Dynamic time series")),
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div(dvc.Vega(id='temp-plot', spec={}))),
                        dbc.Col(html.Div("Dynamic time series")),
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div(dvc.Vega(id='wind-plot', spec={}))),
                        dbc.Col(html.Div("Dynamic time series")),
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div(dvc.Vega(id='solar-plot', spec={}))),
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
    # filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    filtered_df = df
    resampled_df = filtered_df.resample('Y', on='date').mean().reset_index()
    resampled_df = resampled_df[: -1]
    
    fig = px.line(resampled_df, x='year', y='apparent_temperature_mean', title='Temperature Over Years')
    fig.update_xaxes(title_text='Year', showgrid=True)
    fig.update_yaxes(title_text='Temperature', showgrid=True)
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='white',
            xaxis=dict(showline=True, linecolor='black'),
            yaxis=dict(showline=True, linecolor='black')),
    fig.update_layout(yaxis=dict(range=[filtered_df['apparent_temperature_mean'].min(), filtered_df['apparent_temperature_mean'].max()]))
    return fig



@app.callback(
    Output('precipitation-plot', 'spec'),
    [Input('year-slider', 'value')]
)
def update_precipitation_plot(year_range):
    min_time = datetime(year_range[0], 1, 1)
    max_time = datetime(year_range[1], 1, 1)
    print(min_time, max_time)
    filtered_df = filter_aggregation_col(df, 'precipitation_sum', "YE", min_time, max_time)
    fig = time_series_plot_altair(filtered_df, filtered_df.name)
    return fig.to_dict()

@app.callback(
    Output('temp-plot', 'spec'),
    [Input('year-slider', 'value')]
)
def update_temperature_plot(year_range):
    min_time = datetime(year_range[0], 1, 1)
    max_time = datetime(year_range[1], 1, 1)
    print(min_time, max_time)
    filtered_df = filter_aggregation_col(df, 'temperature_2m_max', "YE", min_time, max_time)
    fig = time_series_plot_altair(filtered_df, filtered_df.name)
    return fig.to_dict()

@app.callback(
    Output('wind-plot', 'spec'),
    [Input('year-slider', 'value')]
)
def update_wind_plot(year_range):
    min_time = datetime(year_range[0], 1, 1)
    max_time = datetime(year_range[1], 1, 1)
    print(min_time, max_time)
    filtered_df = filter_aggregation_col(df, 'wind_speed_10m_max', "YE", min_time, max_time)
    fig = time_series_plot_altair(filtered_df, filtered_df.name)
    return fig.to_dict()

@app.callback(
    Output('solar-plot', 'spec'),
    [Input('year-slider', 'value')]
)
def update_wind_plot(year_range):
    min_time = datetime(year_range[0], 1, 1)
    max_time = datetime(year_range[1], 1, 1)
    print(min_time, max_time)
    filtered_df = filter_aggregation_col(df, 'shortwave_radiation_sum', "YE", min_time, max_time)
    fig = time_series_plot_altair(filtered_df, filtered_df.name)
    return fig.to_dict()


# Time aggregator input ['D', 'W', 'ME', 'YE']
# Start time in YYYY-MM-DD
# End time in YYYY-MM-DD



# Run the app/dashboard
if __name__ == '__main__':
    # app.run(debug=True)
    app.server.run(debug=True, port=8080, host='127.0.0.1')