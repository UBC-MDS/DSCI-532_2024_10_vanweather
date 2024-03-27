# VanWeather Proposal

## Motivation and Purpose

In a few sentences, provide motivation for why you are creating a dashboard:

- Who is your target audience, and what role are you embodying?
- What is the problem the target audience is facing and why is it important to solve?
- How can your dashboard assist in solving this problem for the intended target audience?


## Description of the data

We will be visualizing a dataset of approximately 18000 rows of Vancouver daily weather data queried via an open-mateo 
API. More information about the data source can be explored here: https://open-meteo.com/en/docs.

Within the query extraction code, we have specified a latitude and longitude to represent Vancouver as per below:
VAN_LAT = 49.2497
VAN_LONG = -123.1193
The specific coordinate selected to present Vancouver is selected based on reference of this website 
https://latitude.to/map/ca/canada/cities/vancouver. It is actually quite close to King Edward Canada Line station. 

For the time period, we extracted data from 1/1/1974 to 3/15/2024, a period of 50 years. Each row of data contains 
many variable of interests that could be helpful in identifying the noteable trend in Vancouver weather over this long 
period. 

Below are the list of variables, grouped into important factors affecting how we perceive weather.
- Overall weather: "weather_code"
- Temperature: "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean", "apparent_temperature_max", "apparent_temperature_min", "apparent_temperature_mean"
- Sun: "sunrise", "sunset", "shortwave_radiation_sum", "et0_fao_evapotranspiration"
- Precipitation: "precipitation_sum", "rain_sum", "snowfall_sum", "precipitation_hours"
- Wind: "wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant"

Using these variables or a combination of these variables, we will conduct visualization and derive better understanding 
on how exactly Vancouver weather has really changed over the past 50 years. 

## Research questions and usage scenarios


The purpose of this section is to get you to think in more detail about
how your target audience will use the app you're designing
and to account for these detailed needs in the proposal.




## App sketch & brief description

Create a sketch of what you envision your app to look like.
Your sketch can be hand-drawn
or put together using a graphics editor or
slide show software.
The sketch should be saved as `img/sketch.png` and linked in this section of the proposal
so that the image shows up when reading the proposal on GitHub.

