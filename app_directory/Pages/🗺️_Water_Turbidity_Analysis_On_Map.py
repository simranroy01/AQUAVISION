import folium
import streamlit as st
from folium.plugins import Draw
from streamlit_folium import st_folium
import ee
import geemap

# Initialize Earth Engine
try:
    ee.Initialize(project='ee-simranroy186')  # Initialize with your project ID
except ee.EEException:
    ee.Authenticate()  # Authenticate if not already authenticated
    ee.Initialize()

# Set up the Streamlit app
st.title("Draw a Rectangle on the Map")

# Create a Folium map with rectangle drawing functionality
m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

# Add Draw plugin to the map
draw = Draw(
    draw_options={
        'polyline': False,
        'polygon': False,
        'circle': False,
        'rectangle': True,  # Allow only rectangle drawing
        'marker': False,
        'circlemarker': False
    }
)
draw.add_to(m)

# Render the map in Streamlit
output = st_folium(m, width=700, height=500)

# Capture the selected area (bounding box) from the drawn rectangle
if output and "all_drawings" in output and output["all_drawings"]:
    # Extract the geometry of the drawn rectangle (bounding box)
    drawn_geometry = output["all_drawings"][0]["geometry"]
    st.write("Bounding box coordinates:", drawn_geometry)

    # Extract the four corner coordinates (minLat, minLon, maxLat, maxLon) from the drawn area
    coordinates = drawn_geometry['coordinates'][0]
    min_lon, min_lat = coordinates[0]
    max_lon, max_lat = coordinates[2]

    # Convert the drawn rectangle to an Earth Engine geometry (bounding box)
    ee_geometry = ee.Geometry.Rectangle([min_lon, min_lat, max_lon, max_lat])

    # Load Sentinel-2 data
    sentinel = ee.ImageCollection("COPERNICUS/S2") \
        .select(['B2', 'B3', 'B4', 'B8']) \
        .filterDate('2023-01-01', '2024-01-01') \
        .filterBounds(ee_geometry) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))

    # Check if the collection is empty
    if sentinel.size().getInfo() == 0:
        st.write("No Sentinel-2 images found for the selected area.")
    else:
        # Calculate median image and scale to reflect value range
        sentinel_median = sentinel.median().multiply(0.0001)

        # Calculate NDWI
        ndwi = sentinel_median.normalizedDifference(['B3', 'B8']).rename('NDWI')

        # Threshold NDWI to identify water regions
        thr = ndwi.gt(0.1)

        # Mask Sentinel-2 images based on NDWI
        sen_mask = sentinel_median.updateMask(thr)

        # Calculate NDTI
        ndti = sen_mask.normalizedDifference(['B4', 'B3']).rename('NDTI')

        # Visualization parameters for NDWI and NDTI
        vis_params_ndwi = {'palette': ['blue', 'white', 'green'], 'min': -1, 'max': 1}
        vis_params_ndti = {'palette': ['blue', 'green', 'yellow', 'orange', 'red'], 'min': -1, 'max': 1}

        # Get the map IDs for NDWI and NDTI
        ndwi_map_id = ndwi.getMapId(vis_params_ndwi)
        ndti_map_id = ndti.getMapId(vis_params_ndti)

        # Add NDWI and NDTI layers to the folium map using TileLayer
        folium.TileLayer(
            tiles=ndwi_map_id['tile_fetcher'].url_format,
            attr="NDWI",
            overlay=True,
            name="NDWI",
            opacity=0.5
        ).add_to(m)

        folium.TileLayer(
            tiles=ndti_map_id['tile_fetcher'].url_format,
            attr="NDTI",
            overlay=True,
            name="NDTI",
            opacity=0.5
        ).add_to(m)

        # Add a layer control for toggling between layers
        folium.LayerControl().add_to(m)

        # Render the map in Streamlit with added layers
        st_folium(m, width=700, height=500)

