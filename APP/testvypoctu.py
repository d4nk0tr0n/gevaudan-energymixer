import math

# Parametry pro solární panely
panel_area = 1.6  # m² - Plocha jednoho solárního panelu
panel_efficiency = 0.18  # Účinnost panelu
solar_irradiance = 1000  # W/m² - Průměrné sluneční záření
sunlight_hours_per_year = 2000  # Počet hodin slunečního svitu za rok

# Parametry pro větrné turbíny
air_density = 1.225  # kg/m³ - Hustota vzduchu
turbine_area = 50  # m² - Plocha turbíny
wind_speed = 6  # m/s - Průměrná rychlost větru
turbine_efficiency = 0.4  # Účinnost turbíny
wind_hours_per_year = 3000  # Počet hodin větru ročně

# Požadovaná produkce energie (kWh)
required_energy = 10000  # kWh ročně

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
solar_energy_per_panel = calculate_solar_energy(panel_area, panel_efficiency, solar_irradiance, sunlight_hours_per_year)
wind_energy_per_turbine = calculate_wind_energy(air_density, turbine_area, wind_speed, turbine_efficiency, wind_hours_per_year)

# Výpočet počtu panelů a turbín potřebných k dosažení požadované produkce energie
def calculate_panels_and_turbines(required_energy, solar_energy_per_panel, wind_energy_per_turbine, solar_fraction=0.5):
    solar_energy_required = required_energy * solar_fraction
    wind_energy_required = required_energy * (1 - solar_fraction)
    
    num_solar_panels = math.ceil(solar_energy_required / solar_energy_per_panel)
    num_wind_turbines = math.ceil(wind_energy_required / wind_energy_per_turbine)
    
    return num_solar_panels, num_wind_turbines

# Poměr solární a větrné energie (např. 50% solární, 50% větrné)
solar_fraction = 0.5

# Výpočet počtu panelů a turbín
num_panels, num_turbines = calculate_panels_and_turbines(required_energy, solar_energy_per_panel, wind_energy_per_turbine, solar_fraction)

print(f"Počet solárních panelů: {num_panels}")
print(f"Počet větrných turbín: {num_turbines}")

