import pandas as pd
import streamlit as st
from src.charts.bar_plotly import (
    generate_spain_basque_comparation_bar_chart,
    generate_green_red_bar_chart,
)


from src.config.questions import (
    lickert_tag_map_5,
    lickert_tag_map_5_bastante,
)


def render_situacion_economica_y_politica_tab(df_filtered: pd.DataFrame):
    """Renderiza el tab3 situacion economica y politica"""
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
