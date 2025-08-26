import pandas as pd
import streamlit as st
from src.charts.bar_plotly import (
    generate_0_to_10_bar_chart,
    generate_provinces_distribution_bar_chart,
    generate_green_red_bar_chart,
)

from src.config.questions import (
    p33_tag_map,
    p34_tag_map,
    p35_tag_map,
)


def render_sentimiento_identidad_nacional_tab(df_filtered: pd.DataFrame):
    """Renderiza el tab2 de orientación política"""
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
