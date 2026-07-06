"""
    modtestfuncs.py

    Testing the noaa_sdk module for
    Python.
"""

import requests
import geopandas as gpd
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

def full_test(location):
    print(f"Gathering Alerts for {location}...")
    core_response = requests.get(rf'https://api.weather.gov/alerts/active?area={location}') # area=OR
    core_data = core_response.json()
    print(f"...Found {len(core_data["features"])} alerts.")
    print(f"Mapping found alerts for {location}...")

    temp_tbl = []

    # Gather zones

    for feature in core_data["features"]:
        alert_props = feature["properties"]
        props = {
            "Alert_id": feature.get("id"),
            "Event": alert_props.get("event"),
            "Headline": alert_props.get("headline"),
            "Description": alert_props.get("description"),
            "Severity": alert_props.get("severity"),
            "Urgency": alert_props.get("urgency"),
            "Certainty": alert_props.get("certainty"),
            "Effective": alert_props.get("effective"),
            "Expires": alert_props.get("expires"),
            "Status": alert_props.get("status"),
            "Message_type": alert_props.get("messageType"),
            "Sender": alert_props.get("senderName")
        }

        if feature["geometry"] is None:
            temp_zones = feature["properties"]["affectedZones"]

            if len(temp_zones) > 1 and len(temp_zones):
                for zone in temp_zones:
                    zone_response = requests.get(zone).json()
                    feature["geometry"] = zone_response["geometry"]
            elif len(temp_zones) == 1:
                zone_response = requests.get(temp_zones[0]).json()
                feature["geometry"] = zone_response["geometry"]
            else:
                print("No Active Alerts in Oregon. QUITTING...")

            temp_tbl.append({
                "type": "Feature",
                "geometry": feature["geometry"],
                "properties": props
            })
        else:
            temp_tbl.append({
                "type": "Feature",
                "geometry": feature["geometry"],
                "properties": props
            })

    gdf = gpd.GeoDataFrame.from_features(temp_tbl, crs="EPSG:4326")
    gdf["Description"] = gdf["Description"].str.replace("\n", "<br>")
    print("...Complete.")
    m = gdf.explore("Event", legend=True, cmap="plasma", tooltip=["Event", "Status", "Severity", "Headline", "Description", "Effective", "Expires"], tiles="Esri.WorldTopoMap")
    out_file = 'noaa-alerts-full.html'
    print(f"Saving to file: {out_file}...")
    m.save(out_file)
    print("...File saved.")
    print("DONE")