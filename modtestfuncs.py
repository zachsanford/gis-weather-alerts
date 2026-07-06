"""
    modtestfuncs.py

    Testing the noaa_sdk module for
    Python.
"""

import requests
import geopandas as gpd
import matplotlib.pyplot as plt
from noaa_sdk import NOAA

# Y, X point data test
def test_one():
    n = NOAA()
    print(n.points_forecast(40.7314, -73.8656, type='forecastGridData'))

# Zip code forecast test
def test_two():
    n = NOAA()
    forecasts = n.get_forecasts('97471', 'US')

    for forecast in forecasts:
        print(forecast)

# Active Alerts by Zone ID
def test_three():
    n = NOAA()
    alerts = n.active_alerts(zone_id='TXC329')

    for alert in alerts:
        print(alert)

def raw():
    response = requests.get(r'https://api.weather.gov/alerts/active?zone=ORZ023') #TXC329
    data = response.json()

    try:
        gdf = gpd.GeoDataFrame.from_features(data['features'], crs="EPSG:4326")
        m = gdf.explore("event", legend=True, tooltip=["event", "severity", "headline"], tiles="Esri.WorldTopoMap")
        out_file = 'noaa-alerts.html'
        m.save(out_file)
    except:
        print("NO GEOMETRY IN THE API RESPONSE\n\nQUITTING..")

def full_test():
    core_response = requests.get(r'https://api.weather.gov/alerts/active?area=OR') # area=OR
    core_data = core_response.json()

    print(core_data)