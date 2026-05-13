import pandas as pd
from pathlib import Path
from geopandas import gpd
import json

ROOT = Path(__file__).resolve().parent.parent.parent

df_path = ROOT / "data/raw/86-edition/sociometro-vasco-86-prevision-voto.csv"
gdf_path = ROOT / "data/raw/euskadi.geojson"
metadata_json_path = ROOT / "data/metadata/86-edition/preguntas.json"

_ED86_COLUMN_MAP = {
    "basque_level": "p36",
    "education":    "p37",
    "social_class": "p38",
    "left_right":   "p32",
    "nationalist":  "p33",
    "identity":     "p34",
    "independence": "p35",
    "sympathy_pnv":   "p2501",
    "sympathy_bildu": "p2502",
    "sympathy_pse":   "p2503",
    "sympathy_sumar": "p2504",
    "sympathy_pp":    "p2505",
    "sympathy_vox":   "p2506",
    "territory":    "lurral",
}

df: pd.DataFrame = pd.read_csv(df_path, delimiter=";")
df = df.rename(columns={v: k for k, v in _ED86_COLUMN_MAP.items()})
gdf = gpd.read_file(gdf_path)
with open(metadata_json_path, "r", encoding="utf-8") as f:
    metadata = json.load(f)
