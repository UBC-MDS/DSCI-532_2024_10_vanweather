import pandas as pd

df = pd.read_parquet('../data/raw/preprocessed.parquet')

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

