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

'''
    Function: map_alerts()

    Pass the two-letter state abbreviation into the function. Function
    calls NOAA REST API and gathers all Alerts for the state. From there,
    the function processes the API response into a mappable dataframe.
    It then maps the data and saves the result to an HTML file.
'''

def map_alerts(location):

    # Gather alerts from NOAA
    print(f"Gathering Alerts for {location}...")
    core_response = requests.get(rf'https://api.weather.gov/alerts/active?area={location}') # area=OR
    core_data = core_response.json()
    print(f"...Found {len(core_data["features"])} alerts.")
    print(f"Mapping found alerts for {location}...")

    # Temp list to convert into a geodataframe
    temp_tbl = []

    # GEOMETRY HANDLING
    # Iterate through all alerts
    for feature in core_data["features"]:

        # Map all used properties
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

        # Checking to see if geometry is present in the
        # returned NOAA data. If not, get geometry from
        # referenced ZONE in the data. Overwrite NULL
        # geometry with the referenced geometry. If the
        # geometry is present, map it.
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

    # Create geodataframe from the temp list
    gdf = gpd.GeoDataFrame.from_features(temp_tbl, crs="EPSG:4326")

    # NOAA result description features '\n'. For mapping in HTML
    # those need to be replaced with '<br>' tags.
    gdf["Description"] = gdf["Description"].str.replace("\n", "<br>")
    print("...Complete.")

    # Create auxillary mapping items (legend, tooltips, tilemap, etc.)
    m = gdf.explore(
        "Event",
        legend=True,
        cmap="plasma",
        tooltip=[
            "Event",
            "Status",
            "Severity",
            "Headline",
            "Description",
            "Effective",
            "Expires"
        ],
        tiles="Esri.WorldTopoMap"
    )

    # Specify output file and write to it.
    out_file = f'noaa-alerts-{location}.html'
    print(f"Saving to file: {out_file}...")
    m.save(out_file)
    print("...File saved.")

    # DONE
    print("DONE")