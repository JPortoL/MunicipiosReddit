import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from Constantes import DEPARTAMENTOS

def load_geodata(file_path):
    data_geo = gpd.read_file(file_path)
    data_geo["COLOR"] = 0  # Inicializar con 0 en lugar de crear una lista
    return data_geo

def cambiador_color(data_geo, df_eliminados):
    for index in df_eliminados.index:
            for column in df_eliminados.columns:
                municipio = df_eliminados.at[index, column]
                if pd.notna(municipio) and municipio.upper() in data_geo['MPIO_CNMBR'].str.upper().values:
                    data = data_geo.loc[data_geo['MPIO_CNMBR'].str.upper() == municipio.upper(), 'COLOR']
                    if data.values[0] == 1:
                        print(municipio, "ya había sido eliminado")
                    if len(data) > 1:
                        print(municipio, f"está en {len(data)} departamentos")
                    
                    data_geo.loc[data_geo['MPIO_CNMBR'].str.upper() == municipio.upper(), 'COLOR'] = 1
                elif pd.notna(municipio) and ("," in municipio):
                    municipio, departamento = municipio.split(", ")
                    municipio_upper = municipio.upper()
                    data = data_geo.loc[(data_geo['MPIO_CNMBR'].str.upper() == municipio_upper) & (data_geo["DPTO_CCDGO"] == DEPARTAMENTOS[departamento.title()]), 'COLOR']
                    
                    if data.values.size > 0 and data.values[0] == 1:
                        print(municipio, "ya había sido eliminado")
                    data_geo.loc[(data_geo['MPIO_CNMBR'].str.upper() == municipio_upper) & (data_geo["DPTO_CCDGO"] == DEPARTAMENTOS[departamento.title()]), 'COLOR'] = 1
                elif pd.notna(municipio):
                    print(municipio, "no está en el Dataset")
    
    data_geo.to_file("../MUNICIPIOSREDDIT/dataset/MunicipiosModificados.geojson", driver='GeoJSON')

def plot_colored_map(data_geo, dia):
    color_dict = {0: 'limegreen', 1: 'white'}
    cmap = colors.ListedColormap(list(color_dict.values()))
    norm = colors.Normalize(vmin=0, vmax=1)

    fig, ax = plt.subplots(figsize=(10, 10))
    plt.title(f"Día {dia}")
    data_geo.boundary.plot(ax=ax, color='black', linewidth=0.1)
    data_geo.plot(column='COLOR', ax=ax, cmap=cmap, norm=norm)
    plt.show()

if __name__ == "__main__":
    file_path = "../MUNICIPIOSREDDIT/dataset/MunicipiosVeredas19MB.json"
    link_eliminados = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRwZO7dV-5-s9J2op0T2ZZCrJ2yJ27keeGRBCYrlMa91Bwf2pt2mFbaHCDoFlx2_sziGQ8J_tfbKnFQ/pub?gid=0&single=true&output=csv"

    data_geo = load_geodata(file_path)
    df_eliminados = pd.read_csv(link_eliminados)

    for municipio in df_eliminados[df_eliminados.columns[-1]]:
        print(f"- {municipio.title()}" if pd.notna(municipio) else "")

    cambiador_color(data_geo, df_eliminados)
    plot_colored_map(data_geo, 3)
