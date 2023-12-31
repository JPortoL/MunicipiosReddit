import pandas as pd
import plotly.graph_objs as go
import geopandas as gpd
import plotly.offline as pyo
import json
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
        geojson__ = json.load(geojson_file)
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
for loc in geojson__["features"]:
    loc["id"] = loc["properties"]["MPIO_CNMBR"] + ", " + DEPARTAMENTOS_INVERTIDO[loc["properties"]["DPTO_CCDGO"]] 
# Ahora puedes usar directamente la geometría en formato GeoJSON
fig = go.Figure(
    go.Choroplethmapbox(
        geojson=geojson__,
        locations=df['CDGNOMB'],
        z=df['COLOR'],
        colorscale="Greens",
        reversescale=True,
        showscale=False
        )
    )

fig.update_layout(
    mapbox_zoom=3.4,
    mapbox_center = {"lat": 4.570868, "lon": -74.2973328}
    )

fig.update_traces(
    hovertemplate="<br>%{location}</br>" +
                  "Estado: %{text}",
    text=df['COLOR'].apply(lambda x: "ELIMINADO" if x == 1 else "CON VIDA"),
)

"""## Exportar en html"""

pyo.plot(fig, filename='../MUNICIPIOSREDDIT/templates/Mapa.html')
