import solarapi
import windapi

lat = 33
lon = 44
wantedPower = 100000  #MWh
rozpocet = 10000000000
dostupnaPlocha = 1000 #ha

#konstantní hodnoty
ucinnostPanelu = 0.2
vykonPanelu = 400 #W na panel
zivotnostPanelu = 30 #let
plochaPanelu = 2 #m2 panel
porizovaciCenaPanelu = 1900 #Kc na panel
jaksevyplati = 0.1

porizovaciCenaTurbiny = 150000000 #kc za turbinu
zivotnostTurbiny = 25 #let
vykonTurbiny = 2700 #kW na turbínu
plochaTurbiny = 15000 #m2 pro jednu velkou turbínu
ratedVitr = 15 #m/s
minVitr = 4 #m/s
maxVitr = 25 #m/s

solardata = solarapi.get_solar_data(lat, lon)
#print(solardata)
# solardata = {'solrad_monthly': [0.5307464330193986, 1.184326927274343, 1.931438747520723, 3.846643905680439, 4.849817028076789, 5.041786296619597, 5.104023526605352, 4.344052618260738, 2.738151114006399, 1.543040026957731, 0.7953718684680713, 0.4058236475249457], 'solrad_annual': 2.692935178334544, 'Error': None}
solar_annual = solardata["solrad_annual"]  # 2.692935178334544 kWh

winddata = windapi.get_wind_data(lat, lon)
# winddata = {'coordinates': (52.5483283996582, 13.407821655273438), 'elevation': 38.0, '10m_year': 13.895421531000366, '100m_year': 23.24586934651414}
#windata_10m = winddata["10m_year"]  # 13.895421531000366 m/s
windata_annual= winddata["100m_year"]  # 23.24586934651414 m/s





#vypocet struktury
def estimate_sunlight_hours(latitude):
    global jaksevyplati
    # Definujeme pásma a přibližné hodnoty slunečního svitu za rok (v hodinách)
    if latitude >= 0 and latitude <= 15:
        jaksevyplati = 0.6
        return 2500 + (3500 - 2500) * (15 - latitude) / 15
    elif latitude > 15 and latitude <= 30:
        jaksevyplati = 0.5
        return 2000 + (2500 - 2000) * (30 - latitude) / 15
    elif latitude > 30 and latitude <= 50:
        jaksevyplati = 0.4
        return 1600 + (2500 - 1600) * (50 - latitude) / 20
    elif latitude > 50 and latitude <= 60:
        jaksevyplati = 0.3
        return 1000 + (1600 - 1000) * (60 - latitude) / 10
    else:
        jaksevyplati = 0.2
        return 1000  # Pro oblasti nad 60° zeměpisné šířky

def do_magic(pozadovanyVykon, budget):
    global ucinnostPanelu,  vykonPanelu, zivotnostPanelu, plochaPanelu, porizovaciCenaPanelu, porizovaciCenaTurbiny, zivotnostTurbiny, vykonTurbiny, plochaTurbiny, ratedVitr, minVitr, maxVitr,solar_annual,windata_annual
    ePanely = solar_annual * ucinnostPanelu * estimate_sunlight_hours(lat) * 2 #kWh
    eTurbiny = (vykonTurbiny *  0.42 * 0.30 * 8760)  #kWh
    print("vykon panelu",ePanely)
    print("vykon turbiny",eTurbiny)
    jednotkovyVykon = ePanely + eTurbiny
    youneed = (pozadovanyVykon * 1000) / jednotkovyVykon
    mnozstviTurbin = pozadovanyVykon * (1 - jaksevyplati)
    print(mnozstviTurbin)
    mnozstviPanelu = pozadovanyVykon * jaksevyplati
    print(mnozstviPanelu)


do_magic(wantedPower, rozpocet)

