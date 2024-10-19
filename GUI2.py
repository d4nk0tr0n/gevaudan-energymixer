from dash import Dash, dcc, html, Input, Output
from geopy import ArcGIS
import solarapi
import windapi
import math
import folium
from dash.exceptions import PreventUpdate
from flask import Flask
import base64
import io

server = Flask(__name__)
app = Dash(__name__, server=server)

nom = ArcGIS()
mainLatitude = 0
mainLongitude = 0
solar_fraction = 0.5

# Funkce pro výpočet energie

def estimate_sunlight_hours(latitude):
    global solar_fraction
    # Definujeme pásma a přibližné hodnoty slunečního svitu za rok (v hodinách)
    if latitude >= 0 and latitude <= 15:
        solar_fraction = 0.6
        return 2500 + (3500 - 2500) * (15 - latitude) / 15
    elif latitude > 15 and latitude <= 30:
        solar_fraction = 0.5
        return 2000 + (2500 - 2000) * (30 - latitude) / 15
    elif latitude > 30 and latitude <= 50:
        solar_fraction = 0.4
        return 1600 + (2500 - 1600) * (50 - latitude) / 20
    elif latitude > 50 and latitude <= 60:
        solar_fraction = 0.2
        return 1000 + (1600 - 1000) * (60 - latitude) / 10
    else:
        solar_fraction= 0.1
        return 1000  # Pro oblasti nad 60° zeměpisné šířk
    
def calculate_solar_energy():
    panel_area = 2  # m²
    panel_efficiency = 0.2  # Účinnost panelu
    sunlight_hours_per_year =estimate_sunlight_hours(mainLatitude)
    solar_annual = solarapi.get_solar_data(mainLatitude, mainLongitude)["solrad_annual"]  # Pouze jako placeholder
    return (panel_area * panel_efficiency * solar_annual * sunlight_hours_per_year) / 1000  # kWh


def calculate_wind_energy():
    air_density = 1.225  # kg/m³
    turbine_area = 50  # m²
    turbine_efficiency = 0.4  # Účinnost turbíny
    wind_hours_per_year = 4400  # Počet hodin větru ročně
    wind_speed = windapi.get_wind_data(mainLatitude, mainLongitude)["100m_year"]  # Pouze jako placeholder
    power = 0.5 * air_density * turbine_area * (wind_speed ** 3) * turbine_efficiency
    return (power * wind_hours_per_year) / 1000  # kWh

def calculate_panels_and_turbines(required_energy, solar_energy_per_panel, wind_energy_per_turbine, solar_fraction):
    solar_energy_required = required_energy * solar_fraction
    wind_energy_required = required_energy * (1 - solar_fraction)
    
    num_solar_panels = math.ceil(solar_energy_required / solar_energy_per_panel)
    if num_solar_panels > 10000:
            
            redestribution = math.ceil((num_solar_panels / 10)*solar_energy_per_panel)
            num_wind_turbines = math.ceil((wind_energy_required + redestribution) / wind_energy_per_turbine)
            num_solar_panels = num_solar_panels / 100
            return num_solar_panels, num_wind_turbines

    num_wind_turbines = math.ceil(wind_energy_required / wind_energy_per_turbine)
    
    return num_solar_panels, num_wind_turbines

# Hlavní rozhraní
app.layout = html.Div([
    dcc.Input(id='city-input', type='text', placeholder='Zadejte město', style={'margin': '10px'}),
    dcc.Input(id='power-input', type='number', placeholder='Zadejte požadovaný výkon (kWh)', style={'margin': '10px'}),
    html.Button('Vypočítat', id='submit-button', n_clicks=0),
    html.Div(id='output-results', style={'margin': '10px'}),
    dcc.Graph(id='city-map', style={'height': '400px'})
])

@app.callback(
    Output('output-results', 'children'),
    Output('city-map', 'figure'),
    Input('submit-button', 'n_clicks'),
    Input('city-input', 'value'),
    Input('power-input', 'value')
)
def update_output(n_clicks, city_name, required_power):
    if n_clicks == 0 or not city_name or not required_power:
        raise PreventUpdate

    # Získání souřadnic města
    location = nom.geocode(city_name)
    if location:
        global mainLatitude, mainLongitude
        latitude, longitude = location.latitude, location.longitude
        mainLatitude = latitude
        mainLongitude = longitude

        # Výpočet solární a větrné energie
        solar_energy_per_panel = calculate_solar_energy()
        wind_energy_per_turbine = calculate_wind_energy()
        num_panels, num_turbines = calculate_panels_and_turbines(
            required_power, solar_energy_per_panel, wind_energy_per_turbine, solar_fraction)

        # Vytvoření mapy
        map_figure = folium.Map(location=[latitude, longitude], zoom_start=10)
        folium.Marker([latitude, longitude], tooltip=city_name).add_to(map_figure)

        # Uložení mapy do HTML
        map_io = io.BytesIO()
        map_figure.save(map_io, close_file=False)
        map_data = base64.b64encode(map_io.getvalue()).decode()

        return (f"Počet solárních panelů: {num_panels}, Počet větrných turbín: {num_turbines}", {
            'data': [{
                'type': 'scattermapbox',
                'lat': [latitude],
                'lon': [longitude],
                'mode': 'markers',
                'marker': {'size': 12},
                'text': [city_name]
            }],
            'layout': {
                'mapbox': {
                    'style': 'open-street-map',
                    'center': {'lat': latitude, 'lon': longitude},
                    'zoom': 10
                },
                'height': 400
            }
        })

    return 'Město nebylo nalezeno.', {}

if __name__ == '__main__':
    app.run(debug=True)
