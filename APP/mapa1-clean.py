import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from geopy.geocoders import Nominatim  
import solarapi


# Vytvoření aplikace Dash
app = dash.Dash(__name__)

# Geocoder pro převod města na souřadnice
geolocator = Nominatim(user_agent="geoapiExercises")

mainLatitude = None
mainLongitude = None
priblizeni = 1

# Funkce pro získání souřadnic na základě města
def get_coordinates(city_name):
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None  # Pokud se nenašlo, vrací None

# Základní mapa s pomocí plotly express
def create_map(lat=None, lon=None, city_name=None):
    global priblizeni
    fig = px.scatter_mapbox(
        lat=[lat] if lat and lon else [], lon=[lon] if lat and lon else [],
        zoom=priblizeni, height=600
    )
    fig.update_layout(mapbox_style="open-street-map")
    
    # Přidání města na mapu
    if lat is not None and lon is not None:
        fig.add_scattermapbox(
            lat=[lat],
            lon=[lon],
            mode="markers",
            marker=dict(size=12, color="red"),
            text=[city_name],
            showlegend=False
        )
    
    return fig

# Layout aplikace
app.layout = html.Div([
    html.H1("Interactive Map with City Search"),
    dcc.Input(id='city-input', type='text', placeholder="Enter city name", style={'width': '50%'}),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    dcc.Graph(id='map-graph',config={'scrollZoom': True}),
    html.H2("Data o slunci"),
    html.Div(id='generated-output-data')
])

# Callback pro aktualizaci mapy
@app.callback(
    [Output('map-graph', 'figure'),],
    [Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('city-input', 'value')]
)
def update_map(n_clicks, city_name):
    global mainLatitude, mainLongitude, priblizeni
    if n_clicks > 0 and city_name:  # Pokud uživatel klikl a zadal město
        lat, lon = get_coordinates(city_name)
        if lat and lon:
            mainLatitude = lat
            mainLongitude = lon
            priblizeni = 10
            #generatedData = list(solarapi.get_solar_data(mainLatitude, mainLongitude).values())
            return create_map(lat, lon, city_name)
    return create_map()

def update_output():
    return list(solarapi.get_solar_data(mainLatitude, mainLongitude).values())


# Spuštění aplikace
if __name__ == '__main__':
    app.run_server(debug=True)
