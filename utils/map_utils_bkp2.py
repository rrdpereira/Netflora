import folium
import geopandas as gpd
import branca.colormap as cm
import json

with open('processing/variable.json', 'r') as file:
    variables = json.load(file)

crs = variables['crs']
algorithm = variables['algorithm']


gdf_path = f'results/shapefiles/resultados_{algorithm}.shp'

gdf = gpd.read_file(gdf_path)

def createMap(output_html="output_map.html"):
    
    gdf_reproj = gdf.to_crs(epsg=4326)

    # Calculate the centroid of the shapefile to center the map
    centroide = gdf_reproj.unary_union.centroid

    # Convert GeoDataFrame to GeoJSON format
    geojson_data = gdf_reproj.to_json()

    # Create a Folium map with the center and zoom level
    mapa = folium.Map(location=[centroide.y, centroide.x], zoom_start=17, tiles=None)

    # Add OpenStreetMap and Esri Satellite layers
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
    folium.TileLayer(
        tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attr='OpenStreetMap',
        name='OpenStreetMap').add_to(mapa)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Esri Satellite',
        overlay=False
    ).add_to(mapa)

# def _add_layers(mapa):
#     folium.TileLayer(
#         tiles='OpenStreetMap',
#         name='OpenStreetMap',
#         attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
#     ).add_to(mapa)

#     # You can also add a simpler tiles option (e.g., Stamen Toner)
#     folium.TileLayer(
#         tiles='Stamen Toner',
#         name='Toner',
#         attr='Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under ODbL.'
#     ).add_to(mapa)

def _get_color(feature, paleta_cores):
    class_id = feature['properties']['class_id']
    return paleta_cores(class_id)

if __name__ == '__main__':
    html_path = createMap()
    print(f"Map saved to {html_path}")