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
    t = get_translations()

    st.subheader(t["tab_national_title1"])
    fig = generate_0_to_10_bar_chart(
        df=df_filtered,
        question="nationalist",
        chart_title=t["tab_national_title1"],
        x_title=t["tab_national_desc1"],
        tag_map=make_dict_iterable(t["tag_maps"]["nationalist"]),
        percent_label=t["chart_percent_label"],
        count_label=t["chart_count_label"],
    )
    st.plotly_chart(fig, width="stretch")

    st.subheader(t["tab_national_title2"])
    fig = generate_provinces_distribution_bar_chart(
        df=df_filtered,
        question="nationalist",
        title=t["tab_national_title2"],
        xlabel=t["tab_national_desc2"],
        tag_map=make_dict_iterable(t["tag_maps"]["nationalist"]),
        percent_label=t["chart_percent_label"],
        count_label=t["chart_count_label"],
        provinces_label=t["chart_province"],
    )
    st.plotly_chart(fig, width="stretch")

    st.subheader(t["tab_national_title3"])
    fig = generate_green_red_bar_chart(
        df=df_filtered,
        question="identity",
        chart_title=t["tab_national_title3"],
        x_title=t["tab_national_desc3"],
        tag_map=make_dict_iterable(t["tag_maps"]["identity"]),
        percent_label=t["chart_percent_label"],
        count_label=t["chart_count_label"],
    )
    st.plotly_chart(fig, width="stretch")

    st.subheader(t["tab_national_title4"])
    fig = generate_green_red_bar_chart(
        df=df_filtered,
        question="independence",
        chart_title=t["tab_national_title4"],
        x_title=t["tab_national_desc4"],
        tag_map=make_dict_iterable(t["tag_maps"]["independence"]),
        percent_label=t["chart_percent_label"],
        count_label=t["chart_count_label"],
    )
    st.plotly_chart(fig, width="stretch")
