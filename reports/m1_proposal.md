# VanWeather Proposal

## Motivation and Purpose

Our role: Environmental advocacy group

Target audience: Residents, policymakers, and researchers interested in Vancouver's climate trends

As climate change increasingly impacts Vancouver's weather patterns, understanding and addressing climate extremes becomes crucial for the city's ability to adapt and remain sustainable. However, the lack of accessible, comprehensive tools to analyze and visualize these extremes hampers informed decision-making and proactive measures. Our VanWeather dashboard aims to tackle this challenge by providing an interactive platform that integrates historical and recent meteorological data. This allows users to identify trends and patterns indicative of increasing extremity in Vancouver's climate. By arming users with insights into the city's climate dynamics, the dashboard facilitates informed discussions, policy formulation, and community actions to address and adapt to the impacts of climate change at the local level.


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

Below are the detailed definitions of variables extracted from the API that could be used for visualization:
- "weather_code": The most severe weather condition on a given day. Code given in WMO code (for example, 22 = snow, 29 = thunderstorm)
- "temperature_2m_xxx": Daily air temperature at 2 meters above ground. Default unit is in Celcius
- "apparent_temperature_xxx": Daily apparent temperature. Default unit is in Celcius
- "sunrise", "sunset": time for sun rise and sun set in ISO8601
- "precipitation": Sum of daily precipitation (including rain, showers and snowfall). Unit in mm 
- "rain_sum": Sum of daily rain in mm
- "snow_sum": Sum of daily snow in cm
- "preciptation_hours": The number of hours with rain
- "shortwave_radiation_sum": 	The sum of solar radiation on a given day in Megajoules
- "et0_fao_evapotranspiration": Daily sum of ET₀ Reference Evapotranspiration of a well watered grass field in mm. 
- "wind_speed_10m_max", "wind_gusts_10m_max": Maximum wind speed and gusts on a day
- "wind_direction_10m_dominant": Dominant wind direction


## Research questions and usage scenarios

Dr. Emily Wong is a climate scientist specializing in the impacts of climate change on urban environments. Her focus is on analyzing long-term weather trends to understand how global warming is affecting local climates, particularly in metropolitan areas like Vancouver.
Through our app, Dr. Wong can access a comprehensive dashboard titled "Vancouver Weather Analysis - 50 Year Trends." This tool allows her to systematically examine various weather parameters, including temperature, precipitation, wind patterns, and sunlight changes over the last five decades. She starts her investigation by exploring temperature trends, utilizing our app to visualize maximum, minimum, and mean temperature changes, which confirms her suspicion of a gradual increase in local temperatures.
Next, Dr. Wong shifts her focus to precipitation data within our app. She compares historical rainfall and snowfall data, identifying a trend of decreasing snowfall and increasing rainfall, which aligns with her hypotheses about climate change's effects on local weather patterns.
Our app also enables Dr. Wong to analyze wind speed and direction changes over time. She examines these variables to understand their influence on Vancouver's weather dynamics, finding evidence of increasing wind speeds and changes in prevalent wind directions.
Dr. Wong uses our app to study daylight and solar radiation trends. This analysis provides her with additional insights into the broader impacts of climate change, such as shifts in the duration of sunlight that could affect ecosystems and urban life.
Throughout her research, our app proves invaluable, offering Dr. Wong a robust platform for data visualization and analysis. By facilitating easy access to complex datasets and providing comprehensive visualizations, our app empowers her to derive meaningful conclusions and recommendations for urban planning and climate policy. Her findings, supported by the app’s extensive data and analytical capabilities, contribute significantly to the dialogue on urban climate resilience and adaptation strategies.


## App sketch & brief description

Create a sketch of what you envision your app to look like.
Your sketch can be hand-drawn
or put together using a graphics editor or
slide show software.
The sketch should be saved as `img/sketch.png` and linked in this section of the proposal
so that the image shows up when reading the proposal on GitHub.

