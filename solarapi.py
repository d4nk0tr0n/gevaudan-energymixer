# https://developer.nrel.gov/docs/solar/pvwatts/v8/

import requests

default_data = {
    "api_key":"Lfm6k2s2KkBhagoa3wzJdf1kvzVYmTIDxVZHmiqF",
    "system_capacity":1,
    "tilt":0, #0-90
    "azimuth":0, #0-359
    "module_type":0,
    "array_type":1,
    "losses":0
}

def get_solar_data(lat, lon, radius:int=100, extra_data: bool=False):
    return_data = {}
    data = {
        "lat":lat,
        "lon":lon,
        "radius":radius
    }
    data.update(default_data)

    generated_data = "&".join([f"{a}={b}" for a,b in data.items()])

    r = requests.get(f"https://developer.nrel.gov/api/pvwatts/v8.json?{generated_data}")
    if r.status_code == 200:
        return_data["solrad_monthly"] = r.json()["outputs"]["solrad_monthly"]
        return_data["solrad_annual"] = r.json()["outputs"]["solrad_annual"]
        if extra_data:
            return_data["X-Ratelimit-Limit"] = r.headers["X-Ratelimit-Limit"]
            return_data["X-Ratelimit-Remaining"] = r.headers["X-Ratelimit-Remaining"]
        return_data["Error"] = None
    elif r.status_code == 422:
        return_data["Error"] = "\n".join(r.json()["errors"])
    else:
        return_data["Error"] = r.status_code
    return return_data

if __name__ == '__main__':
    result = get_solar_data(52.52, 13.41, extra_data=True)
    print(result)
