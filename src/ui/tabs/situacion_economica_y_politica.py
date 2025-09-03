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

from src.translate import get_translations
from src.utils import make_dict_iterable


def render_situacion_economica_y_politica_tab(df_filtered: pd.DataFrame):
    """Renderiza el tab3 situacion economica y politica"""
    # Comparación situación política
    t = get_translations()
    st.subheader(t["tab_socioeconomic_title1"])
    fig = generate_spain_basque_comparation_bar_chart(
        df=df_filtered,
        title=t["tab_socioeconomic_title1"],
        xlabel=t["tab_socioeconomic_desc1"],
        basque_question="P04",
        spain_question="P05",
        tag_map=make_dict_iterable(t["tag_maps"]["lickert_5"]),
        percent_label=t["chart_percent_label"],
        count_label=t["chart_count_label"],
    )
    st.plotly_chart(fig, use_container_width=True)

    # Comparación situación económica
    st.subheader(t["tab_socioeconomic_title2"])
    fig = generate_spain_basque_comparation_bar_chart(
        df=df_filtered,
        title=t["tab_socioeconomic_title2"],
        xlabel=t["tab_socioeconomic_desc2"],
        basque_question="P06",
        spain_question="P07",
        tag_map=make_dict_iterable(t["tag_maps"]["lickert_5"]),
        percent_label=t["chart_percent_label"],
        count_label=t["chart_count_label"],
    )
    st.plotly_chart(fig, use_container_width=True)

    # Situación laboral personal
    st.subheader(t["tab_socioeconomic_title3"])
    fig = generate_green_red_bar_chart(
        df=df_filtered,
        question="p10",
        chart_title=t["tab_socioeconomic_title3"],
        x_title=t["tab_socioeconomic_desc3"],
        tag_map=make_dict_iterable(t["tag_maps"]["lickert_5_bastante"]),
        percent_label=t["chart_percent_label"],
        count_label=t["chart_count_label"],
    )
    st.plotly_chart(fig, use_container_width=True)

    # Situación económica personal
    st.subheader(t["tab_socioeconomic_title4"])
    fig = generate_green_red_bar_chart(
        df=df_filtered,
        question="p11",
        chart_title=t["tab_socioeconomic_title4"],
        x_title=t["tab_socioeconomic_desc4"],
        tag_map=make_dict_iterable(t["tag_maps"]["lickert_5"]),
        percent_label=t["chart_percent_label"],
        count_label=t["chart_count_label"],
    )
    st.plotly_chart(fig, use_container_width=True)
