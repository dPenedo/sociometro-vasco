import pandas as pd
import streamlit as st

from src.charts.bar_plotly import (
    generate_0_to_10_bar_chart,
    generate_green_red_bar_chart,
    generate_provinces_distribution_bar_chart,
)
from src.translate import get_translations
from src.utils import make_dict_iterable


def render_sentimiento_identidad_nacional_tab(df_filtered: pd.DataFrame):
    """Renderiza el tab2 de orientación política"""

    t = get_translations()
    st.subheader(t["tab_national_title1"])
    # Gráfico principal eje nacionalista/abertzale
    fig = generate_0_to_10_bar_chart(
        df=df_filtered,
        question="p33",
        chart_title=t["tab_national_title1"],
        x_title=t["tab_national_desc1"],
        tag_map=make_dict_iterable((t["tag_maps"]["p33"])),
        percent_label=t["chart_percent_label"],
        count_label=t["chart_count_label"],
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(t["tab_national_title2"])

    fig = generate_provinces_distribution_bar_chart(
        df=df_filtered,
        question="p33",
        title=t["tab_national_title2"],
        xlabel=t["tab_national_desc2"],
        tag_map=make_dict_iterable((t["tag_maps"]["p33"])),
        percent_label=t["chart_percent_label"],
        count_label=t["chart_count_label"],
        provinces_label=t["chart_province"],
    )
    st.plotly_chart(fig, use_container_width=True)

    # Sentimiento nacional
    st.subheader(t["tab_national_title3"])
    fig = generate_green_red_bar_chart(
        df=df_filtered,
        question="p34",
        chart_title=t["tab_national_title3"],
        x_title=t["tab_national_desc3"],
        tag_map=make_dict_iterable((t["tag_maps"]["p34"])),
        percent_label=t["chart_percent_label"],
        count_label=t["chart_count_label"],
    )
    st.plotly_chart(fig, use_container_width=True)

    # Acuerdo con independencia
    st.subheader(t["tab_national_title4"])
    fig = generate_green_red_bar_chart(
        df=df_filtered,
        question="p35",
        chart_title="Nivel de acuerdo con una posible independencia",
        x_title="Acuerdo con una posible independencia",
        tag_map=make_dict_iterable((t["tag_maps"]["p35"])),
        percent_label=t["chart_percent_label"],
        count_label=t["chart_count_label"],
    )
    st.plotly_chart(fig, use_container_width=True)
