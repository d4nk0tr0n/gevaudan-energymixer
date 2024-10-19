from geopy import ArcGIS
import solarapi
import windapi
import math

nom = ArcGIS()
#globalní proměnné
MainLatitude = 0
MainLongitude = 0
solar_annual = 0.00001
windata_annual = 0.000001

# funkce
def location(city_name):
    global MainLatitude, MainLongitude
    location = nom.geocode(city_name)
    if location:
        MainLatitude, MainLongitude = location.latitude, location.longitude
    else:
        return None, None
    
panel_area = 2  # m² - Plocha jednoho solárního panelu
panel_efficiency = 0.2  # Účinnost panelu

# Parametry pro větrné turbíny
air_density = 1.225  # kg/m³ - Hustota vzduchu
turbine_area = 50  # m² - Plocha turbíny
turbine_efficiency = 0.4  # Účinnost turbíny
wind_hours_per_year = 4400  # Počet hodin větru ročně

# Požadovaná produkce energie (kWh)
required_energy = 10000000  # kWh ročně

city_name = str(input("Zadejte město: "))
location(city_name)

def solarcall():
    global MainLatitude, MainLongitude, solar_annual
    solardata = solarapi.get_solar_data(MainLatitude, MainLongitude)
    #print(solardata)
    # solardata = {'solrad_monthly': [0.5307464330193986, 1.184326927274343, 1.931438747520723, 3.846643905680439, 4.849817028076789, 5.041786296619597, 5.104023526605352, 4.344052618260738, 2.738151114006399, 1.543040026957731, 0.7953718684680713, 0.4058236475249457], 'solrad_annual': 2.692935178334544, 'Error': None}
    solar_annual = solardata["solrad_annual"]  # 2.692935178334544 kWh
    
    return(solar_annual)

    
def windcall():
    global MainLatitude, MainLongitude
    winddata = windapi.get_wind_data(MainLatitude, MainLongitude)
    # winddata = {'coordinates': (52.5483283996582, 13.407821655273438), 'elevation': 38.0, '10m_year': 13.895421531000366, '100m_year': 23.24586934651414}
    #windata_10m = winddata["10m_year"]  # 13.895421531000366 m/s
    windata_annual= winddata["100m_year"]  # 23.24586934651414 
    return(windata_annual)



#vypocet struktury
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
    



# Výpočet energie produkované jedním solárním panelem za rok (kWh)
def calculate_solar_energy(panel_area, panel_efficiency, solar_irradiance, sunlight_hours_per_year):
    energy = (panel_area * panel_efficiency * solar_irradiance * sunlight_hours_per_year) / 1000  # kWh
    return energy

# Výpočet energie produkované jednou větrnou turbínou za rok (kWh)
def calculate_wind_energy(air_density, turbine_area, wind_speed, turbine_efficiency, wind_hours_per_year):
    power = 0.5 * air_density * turbine_area * (wind_speed ** 3) * turbine_efficiency  # výkon ve wattech
    energy = (power * wind_hours_per_year) / 1000  # přepočet na kWh
    return energy

# Výpočty energie z jednoho solárního panelu a jedné větrné turbíny
solar_energy_per_panel = calculate_solar_energy(panel_area, panel_efficiency, solarcall(), estimate_sunlight_hours(MainLatitude))
wind_energy_per_turbine = calculate_wind_energy(air_density, turbine_area, windcall(), turbine_efficiency, wind_hours_per_year)

# Výpočet počtu panelů a turbín potřebných k dosažení požadované produkce energie
def calculate_panels_and_turbines(required_energy, solar_energy_per_panel, wind_energy_per_turbine, solar_fraction=0.5):
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



# Výpočet počtu panelů a turbín


    
#program
print("Souřadnice města "+city_name,"jsou", MainLatitude, MainLongitude)
pozadovanyVykon = float(input("Zadejte pozadovany vykonv v kWh: "))

num_panels, num_turbines = calculate_panels_and_turbines(pozadovanyVykon, solar_energy_per_panel, wind_energy_per_turbine, solar_fraction)

print(f"Počet solárních panelů: {num_panels}")
print(f"Počet větrných turbín: {num_turbines}")