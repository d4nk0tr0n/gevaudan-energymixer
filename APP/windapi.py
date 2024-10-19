# https://open-meteo.com/en/docs/historical-weather-api
# https://open-meteo.com/en/docs/historical-weather-api#hourly=wind_speed_10m,wind_speed_100m&temporal_resolution=hourly_3&models=best_match

import openmeteo_requests

import requests_cache
from retry_requests import retry

cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

url = "https://archive-api.open-meteo.com/v1/archive"

default_params = {
    "start_date": "2023-01-01",
    "end_date": "2023-12-31",
    "hourly": ["wind_speed_10m", "wind_speed_100m"],
    "temporal_resolution": "hourly_6",
    "models": "best_match"
}

def get_wind_data(lat, lon, extra_data:bool=False):
    result = {}
    params = {
        "latitude": lat,
        "longitude": lon,
    }
    params.update(default_params)
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]
    result["coordinates"] = (response.Latitude(), response.Longitude())
    result["elevation"] = response.Elevation()
    if extra_data:
        result["timezone"] = (response.Timezone(), response.TimezoneAbbreviation())
        result["timezone-difference"] = response.UtcOffsetSeconds()
    
    hourly = response.Hourly()
    hourly_wind_speed_10m = hourly.Variables(0).ValuesAsNumpy()
    hourly_wind_speed_100m = hourly.Variables(1).ValuesAsNumpy()

    result["10m_year"] = sum(hourly_wind_speed_10m.tolist())/len(hourly_wind_speed_10m.tolist())
    result["100m_year"] = sum(hourly_wind_speed_100m.tolist())/len(hourly_wind_speed_100m.tolist())
    return result

if __name__ == '__main__':
    result = get_wind_data(52.52, 13.41) # prague
    print(result)
