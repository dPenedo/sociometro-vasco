import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from src.charts.bar_plotly import (
    generate_all_parties_stacked_chart,
    generate_0_to_10_bar_chart,
    generate_provinces_distribution_bar_chart,
    generate_spain_basque_comparation_bar_chart,
    generate_green_red_bar_chart,
)
from src.config.data import df
from src.config.questions import (
    lickert_tag_map_5,
    lickert_tag_map_5_bastante,
    sexo_map,
    p32_tag_map,
    p33_tag_map,
    p34_tag_map,
    p35_tag_map,
    p36_grouped,
    p37_grouped,
    p38_map,
    p38_order,
)


# Configuración de la página
st.set_page_config(layout="wide")
st.title("Análisis del Sociómetro Vasco")

st.header("Pruebas interactivas")

st.sidebar.header("Filtros Demográficos")

# Filtrado
# WARN: Arreglar
df["nivel_de_euskera"] = df["p36"].map(p36_grouped)
df["estudios"] = df["p37"].map(p37_grouped)
df["clase"] = pd.Categorical(df["p38"], categories=p38_order, ordered=True)
df["clase"] = df["p38"].map(p38_map)  # Reordenado
df["sexo"] = df["P01"].map(sexo_map)
st.sidebar.header("Filtros Demográficos")

# # Filtro por idioma de la encuesta
# selected_idioma = st.sidebar.selectbox(
#     "Idioma de la encuesta", ["Todos", "Euskera", "Castellano"], index=0
# )

# Filtro por sexo
#
selected_sex = st.sidebar.selectbox(
    "Sexo",
    [
        "Todos",
        "Hombre",
        "Mujer",
    ],
    index=0,
)

print("selected_sex => ", selected_sex)

# Filtro por estudios
nivel_de_euskera = st.sidebar.multiselect(
    "Nivel de euskera",
    options=df["nivel_de_euskera"].dropna().unique(),
    default=df["nivel_de_euskera"].dropna().unique().tolist(),
)

# Filtro por edad
edad_min, edad_max = st.sidebar.slider(
    "Rango de edad",
    min_value=int(df["P02"].min()),
    max_value=int(df["P02"].max()),
    value=(18, 97),
)

# Filtro por estudios
# TODO: añadir Ninguno
selected_estudios = st.sidebar.multiselect(
    "Nivel de estudios finalizados",
    options=df["estudios"].dropna().unique(),
    default=df["estudios"].dropna().unique().tolist(),
)

# Filtro por clase social
selected_clase = st.sidebar.multiselect(
    "Clase social autopercibida",
    options=df["clase"].dropna().unique(),
    default=df["clase"].dropna().unique().tolist(),
)

# Aplicar filtros
df_filtered = df[
    (df["P02"] >= edad_min)
    & (df["P02"] <= edad_max)
    & (df["nivel_de_euskera"].isin(nivel_de_euskera))
    & (df["estudios"].isin(selected_estudios))
    & (df["clase"].isin(selected_clase))
]

# Filtrar por idioma solo si no es "Todos"
# if selected_idioma != "Todos":
#     df_filtered = df_filtered[df_filtered["P0A"].isin(idioma_text_map[selected_idioma])]

# TODO: arreglar
if selected_sex != "Todos":
    df_filtered = df_filtered[df_filtered["P01"].isin(sexo_map[selected_sex])]

# TODO: añadir filtros de:
# - Género 0 p42 / sexo P01
#  - Euskera p36
#  - Nivel de estudios: p37
#  - En qué clase social se situaría p38
#


def show_chart(fig, n_responses, min_samples=30, min_warning=20):
    """
    Muestra un gráfico con advertencias si el tamaño de muestra es pequeño

    Args:
        fig: Figura de matplotlib
        n_responses: Número de respuestas en el filtro actual
        min_samples: Mínimo absoluto para mostrar el gráfico
        min_warning: Mínimo para mostrar advertencia pero aún mostrar gráfico
    """
    if n_responses < min_warning:
        st.error(
            f"🚫 Solo hay {n_responses} respuestas para estos filtros. "
            f"El gráfico no se muestra por baja representatividad (mínimo {
                min_warning
            })."
        )
        plt.close(fig)
        return

    if n_responses < min_samples:
        st.warning(
            f"⚠️ Advertencia: Este gráfico se basa en solo {n_responses} respuestas. "
            "Los gráficos que se generen tienen una baja representatividad."
        )

    st.pyplot(fig)
    plt.close(fig)


min_samples = 20
n_responses = len(df_filtered)


st.markdown(
    """
El [Sociometro_vasco](https://www.euskadi.eus/sociometros-vascos/web01-s1lehike/es/), es un estudio periódico oficial que realiza un cuestionario sobre una población amplia desde **1996**. 
Los datos de la encuesta son compartidos en formato **CSV**, [aquí el enlace](https://www.euskadi.eus/estudios-sociologicos-ficheros-datos/web01-s1lehike/es/).

La encuesta se lleva a cabo por la lehendakaritza. Esta es su descripción en el sitio web:

> Serie de estudios que comenzó en 1996 y que intenta ofrecer un retrato de la realidad social vasca. 
> Consta de un cuerpo común (actitudes políticas y valoración de la situación) y una o más partes con temas diversos. 
> Su enfoque es descriptivo, evolutivo y comparativo. El objetivo no es sólo conocer cómo somos las vascas y los vascos, 
> sino también cómo vamos cambiando, y en qué nos parecemos o nos diferenciamos de las y los habitantes de la totalidad 
> del Estado y de los países de la Unión Europea.
"""
)

# TODO: aplicarlas con `with tab1:...`
(
    tab1,
    tab2,
    tab3,
) = st.tabs(
    [
        "Orientación política",
        "Sentimiento de identidad nacional",
        "Situación económica y política",
    ]
)

# Mostrar advertencia general si la muestra es pequeña
if n_responses < 30:
    st.sidebar.warning(
        f"Filtro actual: {n_responses} respuestas."
        "\nLos gráficos que se generen tienen una baja representatividad.\n"
        f"Solo un ({n_responses / len(df) * 100:.1f}% del total)"
    )

# TAB1: Orientación política
with tab1:
    st.subheader("Nivel de simpatía por partido político")
    fig = generate_all_parties_stacked_chart(
        df_filtered,
    )
    st.plotly_chart(fig)

    st.subheader("Eje izquierda-derecha del 0 al 10")
    fig = generate_0_to_10_bar_chart(
        df_filtered,
        "p32",
        "Eje izquierda-derecha",
        "Ubicación ideológica en el eje izquierda-derecha",
        p32_tag_map,
    )
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("Eje de izquierda-derecha - Comparación entre provincias")

    fig = generate_provinces_distribution_bar_chart(
        df_filtered,
        "p32",
        "Distribución izq-derecha por provincias",
        p32_tag_map,
        "Más izquierda a más derecha",
    )
    st.plotly_chart(fig, use_container_width=True)


# TAB2: Sentimiento de identidad nacional
with tab2:
    st.subheader("Eje nivel de sentimiento nacionalista/abertzale del 0 al 10")
    # Gráfico principal eje nacionalista/abertzale
    fig = generate_0_to_10_bar_chart(
        df_filtered,
        "p33",
        "Nivel de sentimiento nacionalista/abertzale",
        "Menos a más sentimiento nacionalista/abertzale",
        p33_tag_map,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Sentimiento nacionalista/abertzale - Comparación entre provincias")

    fig = generate_provinces_distribution_bar_chart(
        df_filtered,
        "p33",
        "Distribución sentimiento abertzale/nacionalista por provincias",
        p33_tag_map,
        "Menos abertzale a más abertzale",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Sentimiento nacional
    st.subheader("¿Qué expresa mejor su sentimiento nacional?")
    fig = generate_green_red_bar_chart(
        df_filtered,
        "p34",
        "¿Qué expresa mejor su sentimiento nacional?",
        "Ubicación en cuanto a sentimiento nacional",
        p34_tag_map,
    )
    st.plotly_chart(fig, use_container_width=True)

    # Acuerdo con independencia
    st.subheader("Nivel de acuerdo con una posible independencia")
    fig = generate_green_red_bar_chart(
        df_filtered,
        "p35",
        "Nivel de acuerdo con una posible independencia",
        "Acuerdo con una posible independencia",
        p35_tag_map,
    )
    st.plotly_chart(fig, use_container_width=True)

# TAB3: Situación económica y política
with tab3:
    # Comparación situación política
    st.subheader("Comparación situación política Euskadi-España")
    fig = generate_spain_basque_comparation_bar_chart(
        df_filtered,
        "Valoración de la situación política",
        "¿Cómo calificaría ud. la situación política de España y Euskadi? (Comparativa)",
        "P04",
        "P05",
        lickert_tag_map_5,
    )
    st.plotly_chart(fig, use_container_width=True)

    # Comparación situación económica
    st.subheader("Comparación situación económica Euskadi-España")
    fig = generate_spain_basque_comparation_bar_chart(
        df_filtered,
        "Valoración de la situación económica",
        "¿Cómo calificaría ud. la situación económica de España y Euskadi? (Comparativa)",
        "P06",
        "P07",
        lickert_tag_map_5,
    )
    st.plotly_chart(fig, use_container_width=True)

    # Situación laboral personal
    st.subheader("¿Cómo califacaría su situación laboral personal?")
    fig = generate_green_red_bar_chart(
        df_filtered,
        "p10",
        "¿Cómo calificaría ud. la situación laboral personal?",
        "Valoración de su situación laboral personal",
        lickert_tag_map_5_bastante,
    )
    st.plotly_chart(fig, use_container_width=True)

    # Situación económica personal
    st.subheader("¿Cómo califacaría su situación económica personal?")
    fig = generate_green_red_bar_chart(
        df_filtered,
        "p11",
        "¿Cómo calificaría ud. la situación económica personal?",
        "Valoración de su situación económica personal",
        lickert_tag_map_5,
    )
    st.plotly_chart(fig, use_container_width=True)
