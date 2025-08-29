import pandas as pd
import streamlit as st
from src.charts.bar_plotly import (
    generate_all_parties_stacked_chart,
    generate_0_to_10_bar_chart,
    generate_provinces_distribution_bar_chart,
)
from src.config.questions import (
    p32_tag_map,
)


def render_political_orientation_tab(df_filtered: pd.DataFrame):
    """Renderiza el tab1 de orientación política"""
    st.subheader("Nivel de simpatía por partido político")
    fig = generate_all_parties_stacked_chart(
        df_filtered,
    )
    st.plotly_chart(fig, use_container_width=True)

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
