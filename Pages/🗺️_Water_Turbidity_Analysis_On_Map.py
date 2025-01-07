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

# Create a Folium map with rectangle drawing functionality
def create_map(center=[20.5937, 78.9629], zoom_start=5):
    m = folium.Map(location=center, zoom_start=zoom_start)

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
    return m

# Capture the area drawn on the map (bounding box)
def capture_drawn_area(output):
    if output and "all_drawings" in output and output["all_drawings"]:
        # Extract the geometry of the drawn rectangle (bounding box)
        drawn_geometry = output["all_drawings"][0]["geometry"]
        return drawn_geometry
    return None

# Function to process the Sentinel-2 data based on the selected area
def process_area(drawn_area, folium_map):
    # Extract the four corner coordinates (minLat, minLon, maxLat, maxLon) from the drawn area
    coordinates = drawn_area['coordinates'][0]
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
        return folium_map  # No images found, return the map without adding layers
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
        ).add_to(folium_map)

        folium.TileLayer(
            tiles=ndti_map_id['tile_fetcher'].url_format,
            attr="NDTI",
            overlay=True,
            name="NDTI",
            opacity=0.5
        ).add_to(folium_map)

        # Add a layer control for toggling between layers
        folium.LayerControl().add_to(folium_map)

        return folium_map

# Main function to render the map and process the selected area
def main():
    st.title("Draw a Rectangle on the Map")

    # Create the map
    m = create_map()

    # Render the map in Streamlit
    output = st_folium(m, width=700, height=500)

    # Capture the selected area (bounding box)
    drawn_area = capture_drawn_area(output)

    if drawn_area:
        st.write("Bounding box coordinates:", drawn_area)
        # Process the selected area and add the layers to the existing map
        m = process_area(drawn_area, m)
        st_folium(m, width=700, height=500)

if __name__ == "__main__":
    main()
