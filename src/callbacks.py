from utils import filter_aggregation_col, time_series_plot_altair, RefreshData, temperature_plot_altair
from datetime import datetime
from dash import Dash, dcc, callback, Output, Input, html
from datetime import date, datetime
import altair as alt
from data import df, var_dict
alt.data_transformers.enable('vegafusion')

# Date option
agg_dict = {'Day': 'D', "Week": 'W', "Month": "ME", "Year": "YE"}

# default start_date and end_date
from_date = '2014-01-01'
to_date = '2024-01-01'

# Server side callbacks/reactivity
# high-level temperature plot
@callback(
    Output('temperature-plot', 'spec'),
    Input('dateRange', 'start_date'),
    Input('dateRange', 'end_date')
)
def update_temperature_plot(start_date, end_date):

    if not start_date:
        start_date = from_date
    if not end_date:
        end_date = to_date

    min_time = datetime.strptime(start_date, '%Y-%m-%d')#.date()
    max_time = datetime.strptime(end_date, '%Y-%m-%d')#.date()
    filtered_df = df.loc[min_time:max_time]
    altplot = temperature_plot_altair(filtered_df)
    return altplot.to_dict(format="vega")

# For first kpi
@callback(
    Output('temp-change', 'children'),
    Output('temp-prev-period-info', 'children'),
    Input('dateRange', 'start_date'),
    Input('dateRange', 'end_date')
)
def temp_change_cal(start_date, end_date):

    if not start_date:
        start_date = from_date
    if not end_date:
        end_date = to_date

    min_time = datetime.strptime(start_date, '%Y-%m-%d')#.date()
    max_time = datetime.strptime(end_date, '%Y-%m-%d')#.date()
    time_diff = max_time - min_time
    select_period = df.loc[min_time:max_time]
    temp_select = select_period['temperature_2m_mean'].mean()
    prev_period = df.loc[min_time-time_diff:min_time]
    temp_prev = prev_period['temperature_2m_mean'].mean()
    str_change = str(round(temp_select - temp_prev, 2))
    days = time_diff.days
    output_str = f'(mean past {days} vs previous {days} days)'
    return str_change, output_str

# For second kpi
@callback(
    Output('temp-over-30', 'children'),
    Input('dateRange', 'start_date'),
    Input('dateRange', 'end_date')
)
def temp_over30_cal(start_date, end_date):

    if not start_date:
        start_date = from_date
    if not end_date:
        end_date = to_date

    min_time = datetime.strptime(start_date, '%Y-%m-%d')#.date()
    max_time = datetime.strptime(end_date, '%Y-%m-%d')#.date()
    select_period = df.loc[min_time:max_time]
    max_temp = select_period['temperature_2m_max']
    cnt = 0
    for i in max_temp:
        if i >=30:
            cnt += 1
    return cnt

# For third kpi
@callback(
    Output('preci-change', 'children'),
    Output('pre-prev-period-info', 'children'),
    Input('dateRange', 'start_date'),
    Input('dateRange', 'end_date')
)
def preci_cal(start_date, end_date):

    if not start_date:
        start_date = from_date
    if not end_date:
        end_date = to_date

    min_time = datetime.strptime(start_date, '%Y-%m-%d')#.date()
    max_time = datetime.strptime(end_date, '%Y-%m-%d')#.date()
    select_period = df.loc[min_time:max_time]
    time_diff = max_time - min_time
    select_period = df.loc[min_time:max_time]
    preci_select = select_period['precipitation_sum'].sum()
    prev_period = df.loc[min_time-time_diff:min_time]
    preci_prev = prev_period['precipitation_sum'].sum()
    str_change = round(preci_select-preci_prev,0)

    days = time_diff.days
    output_str = f'(mean past {days} vs previous {days} days)'

    return str_change, output_str

# dynamic precipitation plot
@callback(
    Output('precipitation-plot', 'spec'),
    [Input('dateRange', 'start_date'),
     Input('dateRange', 'end_date'),
     Input('agg_time', 'value'),
     Input('precipitation_var', 'value')]
)
def update_precipitation_plot(start_date, end_date, agg_time, var):
    if not start_date:
        start_date = from_date
    if not end_date:
        end_date = to_date

    min_time = datetime.strptime(start_date, '%Y-%m-%d')#.date()
    max_time = datetime.strptime(end_date, '%Y-%m-%d')#.date()
    agg_t = agg_dict[agg_time]
    var_t = var_dict[var]
    filtered_df = filter_aggregation_col(df, var_t, agg_t, min_time, max_time)
    altplot = time_series_plot_altair(filtered_df, filtered_df.name)
    return altplot.to_dict(format="vega")

# dynamic temperature plot
@callback(
    Output('temp-plot', 'spec'),
    [Input('dateRange', 'start_date'),
     Input('dateRange', 'end_date'),
     Input('agg_time', 'value'),
     Input('temp_var', 'value')]
)
def update_temp_plot(start_date, end_date, agg_time, var):
    if not start_date:
        start_date = from_date
    if not end_date:
        end_date = to_date

    min_time = datetime.strptime(start_date, '%Y-%m-%d')#.date()
    max_time = datetime.strptime(end_date, '%Y-%m-%d')#.date()
    agg_t = agg_dict[agg_time]
    var_t = var_dict[var]
    filtered_df = filter_aggregation_col(df, var_t, agg_t, min_time, max_time)
    altplot = time_series_plot_altair(filtered_df, filtered_df.name)
    return altplot.to_dict(format="vega")

# dynamic wind plot
@callback(
    Output('wind-plot', 'spec'),
    [Input('dateRange', 'start_date'),
     Input('dateRange', 'end_date'),
     Input('agg_time', 'value'),
     Input('wind_var', 'value')]
)
def update_wind_plot(start_date, end_date, agg_time, var):
    if not start_date:
        start_date = from_date
    if not end_date:
        end_date = to_date

    min_time = datetime.strptime(start_date, '%Y-%m-%d')#.date()
    max_time = datetime.strptime(end_date, '%Y-%m-%d')#.date()
    agg_t = agg_dict[agg_time]
    var_t = var_dict[var]
    filtered_df = filter_aggregation_col(df, var_t, agg_t, min_time, max_time)
    altplot = time_series_plot_altair(filtered_df, filtered_df.name)
    return altplot.to_dict(format="vega")

# dynamic solar plot
@callback(
    Output('solar-plot', 'spec'),
    [Input('dateRange', 'start_date'),
     Input('dateRange', 'end_date'),
     Input('agg_time', 'value'),
     Input('sun_var', 'value')]
)
def update_solar_plot(start_date, end_date, agg_time, var):
    if not start_date:
        start_date = from_date
    if not end_date:
        end_date = to_date

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