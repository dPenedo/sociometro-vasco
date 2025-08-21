import pandas as pd
from pathlib import Path
from geopandas import gpd
import json

ROOT = Path(__file__).resolve().parent.parent.parent

df_path = ROOT / "data/raw/sociometro-vasco-86-prevision-voto.csv"
gdf_path = ROOT / "data/raw/euskadi.geojson"
metadata_json_path = ROOT / "data/metadata/preguntas.json"

df: pd.DataFrame = pd.read_csv(df_path, delimiter=";")
gdf = gpd.read_file(gdf_path)
with open(metadata_json_path, "r", encoding="utf-8") as f:
    metadata = json.load(f)
