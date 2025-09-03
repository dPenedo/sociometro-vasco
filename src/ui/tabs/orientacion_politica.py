import pandas as pd
import streamlit as st

from src.charts.bar_plotly import (
    generate_0_to_10_bar_chart,
    generate_all_parties_stacked_chart,
    generate_provinces_distribution_bar_chart,
)
from src.translate import get_translations
from src.utils import make_dict_iterable


def render_political_orientation_tab(df_filtered: pd.DataFrame):
    """Renderiza el tab1 de orientación política"""

    t = get_translations()
    st.subheader(t["tab_political_orientation_title1"])
    fig = generate_all_parties_stacked_chart(
        df=df_filtered,
        chart_title=t["tab_political_orientation_title1"],
        percent_label=t["chart_percent_label"],
        count_label=t["chart_count_label"],
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(t["tab_political_orientation_title2"])
    fig = generate_0_to_10_bar_chart(
        df=df_filtered,
        question="p32",
        chart_title=t["tab_political_orientation_title2"],
        x_title=t["tab_political_orientation_desc2"],
        tag_map=make_dict_iterable((t["tag_maps"]["p32"])),
        percent_label=t["chart_percent_label"],
        count_label=t["chart_count_label"],
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(t["tab_political_orientation_title3"])
    fig = generate_provinces_distribution_bar_chart(
        df=df_filtered,
        question="p32",
        title=t["tab_political_orientation_chart3"],
        tag_map=make_dict_iterable((t["tag_maps"]["p32"])),
        xlabel=t["tab_political_orientation_axis3"],
        percent_label=t["chart_percent_label"],
        count_label=t["chart_count_label"],
        provinces_label=t["chart_province"],
    )
    st.plotly_chart(fig, use_container_width=True)
