# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import geopandas as gpd
from src.charts.bar import (
    create_0_to_10_percentage_bar_chart,
    create_green_red_bar_chart,
    create_provinces_distribution_bar_chart,
    create_spain_basque_comparation_bar_chart,
)
from charts.bar_plotly import create_all_parties_stacked_chart
from src.data.processing import get_count, get_df_of_pct
from src.utils import is_light
from src.config import (
    df,
    gdf,
    lickert_tag_map_5,
    lickert_tag_map_5_bastante,
    metadata,
    ordered_p25_list,
    p34_tag_map,
    p35_tag_map,
    party_colors,
    p25_tag_map,
    p32_tag_map,
    p33_tag_map,
    provincias_map,
)

# %%
#

len(df["p32"].unique())
# %%
#
mini_df = df[(df["P02"] > 70) & (df["P0A"].isin([1, 2]))]
len(mini_df["p32"].unique())

# %%
#
create_all_parties_stacked_chart(df)

# %%
# Chart
create_provinces_distribution_bar_chart(
    df,
    "Ex-Iz",
    "Distribución izq-derecha por provincias",
    "p32",
    p32_tag_map,
)

# %%
#
for key in provincias_map:
    print(provincias_map[key]["name"])

# %%
# p34 sentimiento nacional
create_green_red_bar_chart(
    df,
    "p34",
    "¿Qué expresa mejor su sentimiento nacional?",
    "Ubicación en cuanto a sentimiento nacional",
    p34_tag_map,
)

# %%
# p35 acuerdo independencia
create_green_red_bar_chart(
    df,
    "p35",
    "Nivel de acuerdo con una posible independencia",
    "Acuerdo con una posible independencia",
    p35_tag_map,
)
# %%
# comparar euskadi-españa, gráfico de dos barras para cada
# Situación política
create_spain_basque_comparation_bar_chart(
    df,
    "Valoración de la situación política",
    "¿Cómo calificaría ud. la situación política de España y Euskadi? (Comparativa)",
    "P04",
    "P05",
    lickert_tag_map_5,
)

# %%
#  Situación política de Euskadi
create_green_red_bar_chart(
    df,
    "P04",
    "¿Cómo calificaría ud. la situación política de Euskadi?",
    "Valoración de la situación política de Euskadi",
    lickert_tag_map_5,
)

# %%
#  Situación política de España
create_green_red_bar_chart(
    df,
    "P05",
    "¿Cómo calificaría ud. la situación política de España?",
    "Valoración de la situación política de España",
    lickert_tag_map_5,
)

# %%
#  Situación económica de Euskadi
create_green_red_bar_chart(
    df,
    "P06",
    "¿Cómo calificaría ud. la situación económica de Euskadi?",
    "Valoración de la situación económica de Euskadi",
    lickert_tag_map_5,
)


# %%
#  Situación económica de España
create_green_red_bar_chart(
    df,
    "P07",
    "¿Cómo calificaría ud. la situación económica de España?",
    "Valoración de la situación económica de España",
    lickert_tag_map_5,
)

# %%
#  Comparación económica de Euskadi y España
#

create_spain_basque_comparation_bar_chart(
    df,
    "Valoración de la situación económica",
    "¿Cómo calificaría ud. la situación económica de España y Euskadi? (Comparativa)",
    "P06",
    "P07",
    lickert_tag_map_5,
)

# %%
#  Situación laboral personal
create_green_red_bar_chart(
    df,
    "P10",
    "¿Cómo calificaría ud. la situación laboral personal?",
    "Valoración de su situación laboral personal",
    lickert_tag_map_5_bastante,
)
# %%
#  Situación económica personal
create_green_red_bar_chart(
    df,
    "p11",
    "¿Cómo calificaría ud. la situación económica personal?",
    "Valoración de su situación económica personal",
    lickert_tag_map_5,
)

# %%
# p 33 - Nivel de sentimiento abertzale
create_0_to_10_percentage_bar_chart(
    df,
    "p33",
    "Nivel de sentimiento nacionalista/abertzale",
    "Menos a más abertzale/nacionalista",
    p33_tag_map,
)
# %%
# p 33 - Nivel de izquierda a derecha
create_0_to_10_percentage_bar_chart(
    df, "p32", "Eje izquierda-derecha", "Ubicación ideológica", p32_tag_map
)

# %%
# get_count
get_count(df, "P22", "Conteo de las elecciones pasadas")

# %%
# Grado de simpatía - Pie


p25_list = metadata["preguntas"]["P25"]["partidos"]

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

for i, (partido, ax) in enumerate(zip(p25_list, axes)):
    col_number = f"p250{i+1}"
    data = df[col_number].value_counts()

    data.index = data.index.map(p25_tag_map)
    data = data.reindex(ordered_p25_list, fill_value=0)

    # En este caso no aplica
    data = data[data > 0]

    estilo = party_colors.get(partido, {"colormap": "Oranges", "color": "orange"})

    colormap = plt.get_cmap(estilo["colormap"], 14)
    colors = [colormap(i) for i in range(11)]
    colors.insert(0, "black")
    colors.insert(11, "grey")

    # Creamos el mapeo de colores
    color_map = {label: color for label, color in zip(ordered_p25_list, colors)}
    slice_colors = [color_map[label] for label in data.index]

    text_colors = ["black" if is_light(color) else "white" for color in slice_colors]

    wedges, texts, autotexts = ax.pie(
        data,
        labels=data.index,
        colors=slice_colors,
        autopct="%1.0f%%",
        textprops={"color": "black"},
        startangle=90,  # Comenzamos en la parte superior
        counterclock=False,  # Orden en sentido horario
        wedgeprops={"linewidth": 1, "edgecolor": estilo["color"]},
    )

    # Ajustamos colores del texto
    for autotext, color in zip(autotexts, text_colors):
        autotext.set_color(color)

    ax.set_title(f"Simpatía por {partido}", color=estilo["color"])
    ax.axis("equal")

plt.tight_layout()
plt.show()


# %%
p25_list = metadata["preguntas"]["P25"]["partidos"]

fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()

for i, (partido, ax) in enumerate(zip(p25_list, axes)):
    col_number = f"p250{i+1}"
    data = df[col_number].value_counts(normalize=True) * 100  # Convertir a porcentaje

    data.index = data.index.map(p25_tag_map)
    data = data.reindex(ordered_p25_list, fill_value=0)

    # Ordenamos los datos según la lista ordenada
    data = data[ordered_p25_list]

    estilo = party_colors.get(partido, {"colormap": "Oranges", "color": "orange"})

    # Preparar colores
    cmap = plt.get_cmap("RdBu")
    color_map = {
        "0 - Ninguna simpatía": cmap(0.0),  # Rojo intenso
        "1": cmap(0.15),
        "2": cmap(0.25),
        "3": cmap(0.35),
        "4": cmap(0.45),
        "5": "#7f7f7f",  # Gris neutral
        "6": cmap(0.55),
        "7": cmap(0.65),
        "8": cmap(0.75),
        "9": cmap(0.85),
        "10": cmap(1.0),  # Azul intenso
        "Ns/Nc": "#999999",  # Gris para NS/NC
    }

    # Crear gráfico de barras apiladas
    bottom = np.zeros(1)  # Solo una barra por partido
    for j, (label, value) in enumerate(data.items()):
        print("label", label)
        ax.bar(
            0,
            value,
            bottom=bottom,
            color=color_map[label],
            label=label,
            edgecolor="black",
            linewidth=0.5,
        )
        bottom += value

    # Configuración del gráfico
    ax.set_title(f"Simpatía por {partido}", color=estilo["color"], pad=20)
    ax.set_xticks([])  # Eliminar ticks del eje x
    ax.set_ylim(0, 100)  # Eje y de 0 a 100%
    ax.set_ylabel("Porcentaje (%)")

    # Mostrar porcentajes dentro de las barras si son suficientemente grandes
    bottom = 0
    for j, (label, value) in enumerate(data.items()):
        if value > 5:  # Solo mostrar etiquetas para segmentos >5%
            ax.text(
                0,
                bottom + value / 2,
                f"{value:.0f}%",
                ha="center",
                va="center",
                color="white" if not is_light(color_map[label]) else "black",
            )
        bottom += value

# Crear leyenda común
handles, labels = ax.get_legend_handles_labels()
fig.legend(
    handles,
    labels,
    title="Nivel de simpatía",
    bbox_to_anchor=(1.05, 0.5),
    loc="center left",
)

plt.tight_layout()
plt.subplots_adjust(right=0.85)  # Hacer espacio para la leyenda
plt.show()

# %%
# Mapa provincias
provincias_map = {
    "Vizcaya": {"name": "Bizkaia", "color": "lightcoral"},
    "Guipúzcoa": {"name": "Gipuzkoa", "color": "lightsteelblue"},
    "Álava": {"name": "Araba", "color": "lightpink"},
}
fig, ax = plt.subplots(figsize=(8, 8))

for idx, row in gdf.iterrows():
    provincia = row["Texto"]
    color = provincias_map[provincia]["color"]
    row_geometry = gpd.GeoSeries([row.geometry])
    row_geometry.plot(ax=ax, color=color, edgecolor="black")

    nombre = provincias_map[provincia]["name"]
    centroid = row.geometry.centroid
    plt.annotate(
        text=nombre,
        xy=(centroid.x, centroid.y),
        horizontalalignment="center",
        fontsize=10,
    )

plt.title("Provincias de la Comunidad Autónoma Vasca")
plt.axis("off")
plt.show()


# %%
