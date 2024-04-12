from utils import filter_aggregation_col, time_series_plot_altair
from datetime import datetime
from dash import Dash, dcc, callback, Output, Input, html
from datetime import date, datetime
import altair as alt
from data import df, var_dict
alt.data_transformers.enable('vegafusion')

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
        ).interactive().to_dict(format="vega")
    )

@callback(
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
    return altplot.to_dict(format="vega")

@callback(
    Output('temp-plot', 'spec'),
    [Input('dateRange', 'start_date'),
     Input('dateRange', 'end_date'),
     Input('agg_time', 'value'),
     Input('temp_var', 'value')]
)
def update_temp_plot(start_date, end_date, agg_time, var):
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
    return altplot.to_dict(format="vega")

@callback(
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
    return altplot.to_dict(format="vega")

@callback(
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
    return altplot.to_dict(format="vega")

## Refresh button to get data
@callback(
    Output('reload-button', 'n_clicks'),
    [Input('reload-button', 'n_clicks')]
)
def reload_dataframe_callback(n_clicks):
    global df
    df = RefreshData()
    return n_clicks