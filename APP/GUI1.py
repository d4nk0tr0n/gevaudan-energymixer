from flask import Flask, render_template, request, redirect, url_for
from geopy import ArcGIS
import solarapi
import windapi
import math
import folium
import os

app = Flask(__name__)
nom = ArcGIS()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city_name = request.form['city']
        required_power = float(request.form['power'])

        # Získání souřadnic města
        location = nom.geocode(city_name)
        if location:
            latitude, longitude = location.latitude, location.longitude

            # Výpočet solární a větrné energie
            solar_energy_per_panel = calculate_solar_energy()
            wind_energy_per_turbine = calculate_wind_energy()

            num_panels, num_turbines = calculate_panels_and_turbines(
                required_power, solar_energy_per_panel, wind_energy_per_turbine)

            # Zobrazit mapu
            map_object = folium.Map(location=[latitude, longitude], zoom_start=10)
            folium.Marker([latitude, longitude], tooltip=city_name).add_to(map_object)

            # Uložit mapu do HTML
            map_path = 'static/city_map.html'
            map_object.save(map_path)

            return render_template('results.html', city=city_name,
                                   num_panels=num_panels,
                                   num_turbines=num_turbines,
                                   map_path=map_path)
        else:
            return render_template('index.html', error='Město nebylo nalezeno.')

    return render_template('index.html')

def calculate_solar_energy():
    panel_area = 2  # m²
    panel_efficiency = 0.2  # Účinnost panelu
    # Odhadované sluneční záření a hodiny slunečního svitu
    solar_annual = solarapi.get_solar_data(0, 0)["solrad_annual"]  # Pouze jako placeholder
    return (panel_area * panel_efficiency * solar_annual) / 1000  # kWh

def calculate_wind_energy():
    air_density = 1.225  # kg/m³
    turbine_area = 50  # m²
    turbine_efficiency = 0.4  # Účinnost turbíny
    wind_hours_per_year = 4400  # Počet hodin větru ročně
    wind_speed = windapi.get_wind_data(0, 0)["100m_year"]  # Pouze jako placeholder
    power = 0.5 * air_density * turbine_area * (wind_speed ** 3) * turbine_efficiency
    return (power * wind_hours_per_year) / 1000  # kWh

def calculate_panels_and_turbines(required_energy, solar_energy_per_panel, wind_energy_per_turbine, solar_fraction=0.5):
    solar_energy_required = required_energy * solar_fraction
    wind_energy_required = required_energy * (1 - solar_fraction)

    num_solar_panels = math.ceil(solar_energy_required / solar_energy_per_panel)
    num_wind_turbines = math.ceil(wind_energy_required / wind_energy_per_turbine)

    return num_solar_panels, num_wind_turbines

if __name__ == '__main__':
    app.run(debug=True)
