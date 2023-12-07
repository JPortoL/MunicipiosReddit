import pandas as pd
import folium
from folium import Choropleth, GeoJson
import geopandas as gpd
from Constantes import DEPARTAMENTOS_INVERTIDO

"""## Importar json con las ubicaciones"""
import json

def encontrar_llave(diccionario, valor_buscado):
    for llave, valor in diccionario.items():
        if valor == valor_buscado:
            return llave
    return None

geojson_path = "../MUNICIPIOSREDDIT/dataset/MunicipiosModificados2.geojson"

with open(geojson_path, 'r', encoding='utf-8') as geojson_file:
    geojson_data = json.load(geojson_file)
    # Aquí puedes trabajar con el objeto GeoJSON

"""## Cargar base de datos"""

# Lee el GeoDataFrame desde el archivo GeoJSON
gdf = gpd.read_file(geojson_path)

"""## Crear mapa"""

# Convierte el GeoDataFrame a un DataFrame de pandas
df = pd.DataFrame({
    "CDGNOMB": gdf["MPIO_CNMBR"] + ", " + gdf["DPTO_CCDGO"].map(DEPARTAMENTOS_INVERTIDO),
    "COLOR": gdf["COLOR"]
})

# Ahora puedes usar directamente la geometría en formato GeoJSON
m = folium.Map(location=[4.570868, -74.2973328], zoom_start=3.4)

Choropleth(
    geo_data=geojson_data,
    name='choropleth',
    data=df,
    columns=['CDGNOMB', 'COLOR'],
    key_on='feature.properties.MPIO_CNMBR',
    fill_color='Greens',
    fill_opacity=0,
    line_opacity=0.2,
    line_color='black',
    line_weight=0.1,
    legend_name='Estado'
).add_to(m)

# Agregar etiquetas
for loc in geojson_data["features"]:
    loc["id"] = loc["properties"]["MPIO_CNMBR"] + ", " + DEPARTAMENTOS_INVERTIDO[loc["properties"]["DPTO_CCDGO"]]
    GeoJson(loc["geometry"], name=loc["id"]).add_to(m)

# Mostrar el mapa
m.save('../MUNICIPIOSREDDIT/templates/Mapa.html')
