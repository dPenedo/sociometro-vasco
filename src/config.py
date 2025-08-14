import json
from pathlib import Path
from geopandas import gpd
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

df_path = ROOT / "data/raw/sociometro-vasco-86-prevision-voto.csv"
gdf_path = ROOT / "data/raw/euskadi.geojson"
metadata_json_path = ROOT / "data/metadata/preguntas.json"

df = pd.read_csv(df_path, delimiter=";")
gdf = gpd.read_file(gdf_path)
with open(metadata_json_path, "r", encoding="utf-8") as f:
    metadata = json.load(f)

with open(metadata_json_path, "r", encoding="utf-8") as f:
    metadata = json.load(f)

p25_tag_map = {
    0: "0 - Ninguna simpatía",
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "10",
    11: "Ns/Nc",
}

provincias_map = {
    1: {"name": "Araba", "color": "#A31182"},
    2: {"name": "Bizkaia", "color": "#A71E23"},
    3: {"name": "Gipuzkoa", "color": "#1772B3"},
}


idioma_map = {
    1: 1,
    2: 1,
    3: 2,
}

idioma_text_map = {"Todos": [1, 2, 3], "Euskera": [1, 2], "Castellano": [3]}

sexo_map = {
    1: "Hombre",
    2: "Mujer",
}

ordered_p25_list = [
    "0 - Ninguna simpatía",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "6",
    "8",
    "9",
    "10",
    "Ns/Nc",
]


lickert_tag_map_5 = {
    1: "Muy buena",
    2: "Buena",
    3: "Mala",
    4: "Muy mala",
    5: "NS-NC",
}
lickert_tag_map_5_bastante = {
    1: "Muy buena",
    2: "Bastante buena",
    3: "Bastante mala",
    4: "Muy mala",
    5: "NS-NC",
}
lickert_tag_map_6 = {
    1: "Muy buena",
    2: "Buena",
    3: "Regular",
    4: "Mala",
    5: "Muy mala",
    6: "NS-NC",
}

p32_tag_map = {
    0: "0\nExt. Izquierda",
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5\nCentro",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "10\nExt. Derecha",
    11: "NS/NC",
}

p33_tag_map = {
    0: "0\nNada abertzale",
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "10\nMuy abertzale",
    11: "NS/NC",
}

p34_tag_map = {
    1: "ÚNICAMENTE\nVASCO/A",
    2: "MÁS VASCO/A\nQUE ESPAÑOL/A",
    3: "TANTO VASCO/A\nCOMO ESPAÑOL/A",
    4: "MÁS ESPAÑOL/A\nQUE VASCO/A",
    5: "ÚNICAMENTE\nESPAÑOL/A",
    6: "NS/NC",
}

p35_tag_map = {
    1: "DE ACUERDO",
    2: "SEGÚN LAS\n CIRCUNSTANCIAS",
    3: "EN DESACUERDO",
    4: "NS-NC",
}

party_colors = {
    "PNV/EAJ": {"colormap": "Greens", "color": "green", "textcolor": "black"},
    "EH BILDU": {"colormap": "PuBuGn", "color": "darkcyan", "textcolor": "black"},
    "PARTIDO SOCIALISTA DE EUSKADI": {
        "colormap": "Reds",
        "color": "red",
        "textcolor": "black",
    },
    "SUMAR": {"colormap": "RdPu", "color": "crimson", "textcolor": "black"},
    "PP": {"colormap": "Blues", "color": "dodgerblue", "textcolor": "black"},
    "VOX": {"colormap": "Greens", "color": "limegreen", "textcolor": "black"},
}
