import solarapi
import windapi

lat = 49
lon = 2

solardata = solarapi.get_solar_data(lat, lon)
# solardata = {'solrad_monthly': [0.5307464330193986, 1.184326927274343, 1.931438747520723, 3.846643905680439, 4.849817028076789, 5.041786296619597, 5.104023526605352, 4.344052618260738, 2.738151114006399, 1.543040026957731, 0.7953718684680713, 0.4058236475249457], 'solrad_annual': 2.692935178334544, 'Error': None}
solar_annual = solardata["solrad_annual"]  # 2.692935178334544 kWh

winddata = windapi.get_wind_data(lat, lon)
# winddata = {'coordinates': (52.5483283996582, 13.407821655273438), 'elevation': 38.0, '10m_year': 13.895421531000366, '100m_year': 23.24586934651414}
windata_10m = winddata["10m_year"]  # 13.895421531000366 m/s
windata_100m = winddata["100m_year"]  # 23.24586934651414 m/s

print(solardata)
print(winddata)

# Funkce pro výpočet roční výroby energie z turbíny
def calculate_energy(provozní_výkon_kW, kapacitní_faktor, hodiny_rok=8760):
    """
    Vypočítá roční výrobu elektřiny z větrné turbíny nebo solárního panelu.
    :param provozní_výkon_kW: Instalovaný výkon (v kW).
    :param kapacitní_faktor: Kapacitní faktor (0-1), což je průměrná účinnost zařízení.
    :param hodiny_rok: Počet hodin v roce (defaultně 8760 hodin).
    :return: Roční výroba elektřiny v kWh.
    """
    return provozní_výkon_kW * kapacitní_faktor * hodiny_rok

# Funkce pro výpočet návratnosti investice
def calculate_payback(pořizovací_náklady, roční_výnos):
    """
    Vypočítá dobu návratnosti investice do větrné turbíny nebo solárního panelu.
    :param pořizovací_náklady: Pořizovací náklady na zařízení.
    :param roční_výnos: Roční výnos z prodeje elektřiny (v Kč).
    :return: Doba návratnosti v letech.
    """
    return pořizovací_náklady / roční_výnos

# Parametry pro malou turbínu
malá_turbína = {
    'pořizovací_náklady': 100000,  # cena v Kč
    'instalovaný_výkon_kW': 2,  # výkon v kW
    'kapacitní_faktor': 0.25,  # odhadovaný kapacitní faktor (25%)
    'cena_za_kWh': 5,  # cena elektřiny v Kč
    'průměrná_r_větru_m_s': windata_10m  # průměrná rychlost větru na 10m (m/s)
}

# Parametry pro velkou turbínu
velká_turbína = {
    'pořizovací_náklady': 50000000,  # cena v Kč
    'instalovaný_výkon_kW': 2000,  # výkon v kW
    'kapacitní_faktor': 0.40,  # odhadovaný kapacitní faktor (40%)
    'cena_za_kWh': 5,  # cena elektřiny v Kč
    'průměrná_r_větru_m_s': windata_100m  # průměrná rychlost větru na 100m (m/s)
}

# Parametry pro solární panely
solární_panel = {
    'pořizovací_náklady': 100000,  # cena v Kč pro systém (např. pro 5 kW instalace)
    'instalovaný_výkon_kW': 5,  # výkon solárního systému v kW
    'kapacitní_faktor': 0.15,  # odhadovaný kapacitní faktor (15%) pro solární panely
    'cena_za_kWh': 5,  # cena elektřiny v Kč
    'solární_radiace': solar_annual  # roční solární radiace (kWh/m²)
}

# Výpočet pro malou turbínu
roční_výroba_malá = calculate_energy(malá_turbína['instalovaný_výkon_kW'], malá_turbína['kapacitní_faktor'])
roční_výnos_malá = roční_výroba_malá * malá_turbína['cena_za_kWh']
návratnost_malá = calculate_payback(malá_turbína['pořizovací_náklady'], roční_výnos_malá)

# Výpočet pro velkou turbínu
roční_výroba_velká = calculate_energy(velká_turbína['instalovaný_výkon_kW'], velká_turbína['kapacitní_faktor'])
roční_výnos_velká = roční_výroba_velká * velká_turbína['cena_za_kWh']
návratnost_velká = calculate_payback(velká_turbína['pořizovací_náklady'], roční_výnos_velká)

# Výpočet pro solární panely
roční_výroba_solar = calculate_energy(solární_panel['instalovaný_výkon_kW'], solární_panel['kapacitní_faktor'])
roční_výnos_solar = roční_výroba_solar * solární_panel['cena_za_kWh']
návratnost_solar = calculate_payback(solární_panel['pořizovací_náklady'], roční_výnos_solar)

# Výstupy pro turbíny a solární panely
print("\nVýsledky pro malou turbínu:")
print(f"Roční výroba energie: {roční_výroba_malá:.2f} kWh")
print(f"Roční výnos: {roční_výnos_malá:.2f} Kč")
print(f"Návratnost investice: {návratnost_malá:.2f} let\n")

print("Výsledky pro velkou turbínu:")
print(f"Roční výroba energie: {roční_výroba_velká:.2f} kWh")
print(f"Roční výnos: {roční_výnos_velká:.2f} Kč")
print(f"Návratnost investice: {návratnost_velká:.2f} let\n")

print("Výsledky pro solární panely:")
print(f"Roční výroba energie: {roční_výroba_solar:.2f} kWh")
print(f"Roční výnos: {roční_výnos_solar:.2f} Kč")
print(f"Návratnost investice: {návratnost_solar:.2f} let")

