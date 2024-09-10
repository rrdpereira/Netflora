import folium
import geopandas as gpd
import branca.colormap as cm
import json
import os

with open('processing/variable.json', 'r') as file:
    variables = json.load(file)

crs = variables['crs']
algorithm = variables['algorithm']

gdf_path = f'results/shapefiles/outshape_{algorithm}.shp'

gdf = gpd.read_file(gdf_path)

# Check if the directory exists, if not, create it
html_directory = "results/html/"
if not os.path.exists(html_directory):
    os.makedirs(html_directory)
    print(f"Directory {html_directory} created.")
else:
    print(f"Directory {html_directory} already exists.")

def createMap(output_html="results/html/output_map.html"):
    
    gdf_reproj = gdf.to_crs(epsg=4326)

    # Calculate the centroid of the shapefile to center the map
    centroide = gdf_reproj.unary_union.centroid

    # Convert GeoDataFrame to GeoJSON format
    geojson_data = gdf_reproj.to_json()

    # Create a Folium map with the center and zoom level
    mapa = folium.Map(location=[centroide.y, centroide.x], zoom_start=17, tiles=None)

    # Add OpenStreetMap and Google Maps Satellite layers
    _add_layers(mapa)

    # Define color palette for different class IDs
    paleta_cores = cm.linear.Set1_09.scale(0, gdf_reproj['class_id'].max())

    # Add GeoJSON layer to the map with the color style
    geojson_layer = folium.GeoJson(
        geojson_data,
        name='Shapefile',
        style_function=lambda feature: {
            'fillColor': _get_color(feature, paleta_cores),
            'color': 'black',
            'weight': 1,
            'opacity': 0.8,
            'fillOpacity': 1
        }
    ).add_to(mapa)

    # Add color palette legend
    paleta_cores.caption = 'Classes'
    paleta_cores.add_to(mapa)
    folium.LayerControl().add_to(mapa)

    # Save the map as an HTML file
    mapa.save(output_html)

    return output_html

def _add_layers(mapa):
    # Add OpenStreetMap
    folium.TileLayer(
        tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        name='OpenStreetMap'
    ).add_to(mapa)

    # Add Google Maps Satellite tiles
    google_maps_api_key = "YOUR_GOOGLE_MAPS_API_KEY"  # Replace with your actual Google Maps API key
    folium.TileLayer(
        tiles=f'https://mt1.google.com/vt/lyrs=s&x={{x}}&y={{y}}&z={{z}}&key={google_maps_api_key}',
        attr='Map data &copy; <a href="https://www.google.com/intl/en/help/terms_maps/">Google</a>',
        name='Google Satellite',
        overlay=False
    ).add_to(mapa)

def _get_color(feature, paleta_cores):
    class_id = feature['properties']['class_id']
    return paleta_cores(class_id)

if __name__ == '__main__':
    html_path = createMap()
    print(f"Map saved to {html_path}")