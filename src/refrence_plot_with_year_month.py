import pandas as pd
import altair as alt

# Load the data
df = pd.read_csv("../data/raw/van_weather_1974-01-01_2024-03-15.csv", index_col='date', parse_dates=True)

def filter_for_month(column_name, month, start_year, end_year):
    # Create a boolean mask where the month is May and the year is within the specified range
    mask = (df.index.month == month) & (df.index.year >= start_year) & (df.index.year <= end_year)
    filtered_df = df.loc[mask]

    if column_name not in filtered_df.columns:
        raise ValueError(f"Column {column_name} does not exist in the DataFrame")

    # Resample the data by year and take the mean for each May
    aggregated_df = filtered_df[column_name].resample('A').mean()
    return aggregated_df.reset_index()


df_may = filter_for_month('temperature_2m_max', 5, 2000, 2022)

# Create the Altair line chart
chart = alt.Chart(df_may).mark_line(
    point=True,  # Add points to the line
    color='steelblue',  # Line color
    size=3  # Line thickness
).encode(
    x=alt.X('date:T', title='Date'),  # Specify temporal type
    y=alt.Y('temperature_2m_max:Q', title='Temperature (°C)'),  # Specify quantitative type
    tooltip=['date:T', 'temperature_2m_max:Q']
).properties(
    title='Average Temperature in May (2000-2022)',
    width=800,
    height=400
).configure_title(
    fontSize=20,
    font='Courier',
    anchor='start',
    color='gray'
).configure_view(
    strokeOpacity=0  # Remove the border around the chart
)

chart
