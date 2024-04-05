
#%%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("../data/raw/van_weather_1974-01-01_2024-03-15.csv", index_col='date', parse_dates=True)
df.shape
# Time aggregator input ['D', 'W', 'ME', 'YE']
# Start time in YYYY-MM-DD
# End time in YYYY-MM-DD

def filter_aggregation_col(column_name, agg_time, start_time, end_time):
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
df_agg = filter_aggregation_col('temperature_2m_max', 'YE', '1990-01-15', '2024-03-01')


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



# Now call the function and pass the DataFrame
alt_chart = time_series_plot_altair(df_agg)
alt_chart

# %%
