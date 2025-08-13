# %%
import pandas as pd

from src.charts.bar import create_provinces_distribution_bar_chart
from src.config import idioma_map, provincias_map, sexo_map
from src.data.processing import get_df_of_pct


# %%

df = pd.read_csv("./data/raw/sociometro-vasco-86-prevision-voto.csv", delimiter=";")

# %%


df["lurralde"] = df["lurral"].map(lambda k: provincias_map[k]["name"])
df["idioma"] = df["P0A"].map(idioma_map)
df["sexo"] = df["P01"].map(sexo_map)


conteo_lurral = df.groupby("lurral").lurral.count()
lurral_porcentajes = df["lurralde"].value_counts(normalize=True) * 100
idioma_porcentajes = df["idioma"].value_counts(normalize=True) * 100
print("idioma_porcentajes => ", idioma_porcentajes)
# %%
# Media de Edad
# La Media de edad de la CAV es 45.9 y la de la encuesta es 53.6

media_de_edad = round(float(df["P02"].mean()), 1)
print("media_de_edad => ", media_de_edad)


datos_edad = df["P02"].agg(["min", "max", "mean", "median"])
print(datos_edad)


# %%
# Municipio más contestado

municipio_mas_contestado = int(
    df["P0B"].value_counts().sort_values(ascending=False).iloc[0]
)
print("municipio_mas_contestado => ", municipio_mas_contestado)
# %%
# Headers
df.columns.to_list()

# %%
# Lurraldeak
araba = df[df["lurral"] == 1]
bizkaia = df[df["lurral"] == 2]
gipuzkoa = df[df["lurral"] == 3]
araba["idioma"].value_counts()
bizkaia["idioma"].value_counts()
gipuzkoa["idioma"].value_counts()


# %%
# Porcentaje idioma por lurralde


idioma_por_lurralde = get_df_of_pct(df, "lurralde", "idioma")
print("idioma_por_lurralde => ", idioma_por_lurralde)
# %%
# Porcentaje sexo por provincia

sexo_por_provincia = get_df_of_pct(df, "lurralde", "sexo")
sexo_por_provincia  # pyright: ignore[reportUnusedExpression]

# %%
# lista headers
df.columns
# %%
# Porcentaje cada puntuacion izq/derecha

izq_dcha_por_provincia = get_df_of_pct(df, "lurralde", "p32")
araba_izq_derecha = izq_dcha_por_provincia.iloc[0]
bizkaia_izq_derecha = izq_dcha_por_provincia.iloc[1]
gipuzkoa_izq_derecha = izq_dcha_por_provincia.iloc[2]
araba_izq_derecha  # pyright: ignore[reportUnusedExpression]
# %%
# Plot


create_provinces_distribution_bar_chart(
    df,
    "Eje izquierda-derecha",
    "Porcentaje",
    "Distribución izq-derecha por provincias",
    "Ex-Iz",
    "Ex-Dr",
    "p32",
)

# %%
# Distribucion nacionalista por provincias
create_provinces_distribution_bar_chart(
    df,
    "Eje nacionalismo/abertzalismo",
    "Porcentaje",
    "Distribución no abertzale-abertzale por provincias",
    "No abertz",
    "Abertz",
    "p33",
)
# %%
# %%
