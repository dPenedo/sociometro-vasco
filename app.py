import pandas as pd
import streamlit as st

from src.config.data import df
from src.processing.processing import (
    apply_filters,
    get_filter_options,
    get_processed_dataframe_for_streamlit,
)
from src.translate import (
    get_basque_level_order,
    get_education_order,
    get_social_class_order,
    get_translations,
    set_language,
)
from src.ui.filters import render_filters_sidebar
from src.ui.tabs.orientacion_politica import render_political_orientation_tab
from src.ui.tabs.sentimiento_identidad_nacional import (
    render_sentimiento_identidad_nacional_tab,
)
from src.ui.tabs.situacion_economica_y_politica import (
    render_situacion_economica_y_politica_tab,
)
from src.utils import sort_by_order

t = get_translations()

query_params = st.query_params
app_is_full_screen = query_params.get("utm_medium") == "oembed"

# Version selector
col1, col2 = st.columns([10, 3])
with col2:
    version_options = ["86 - julio del 2025", "88 - marzo de 2026"]

    selected_version = st.menu_button(
        label="Azken bertsioa",
        options=version_options,
        key="version_selector",
    )


col1, col2 = st.columns([12, 2])
with col1:
    if app_is_full_screen:
        st.link_button(t["go_back_button"], t["dpenedo_url"], type="primary")
with col2:
    current_lang = st.session_state.get("lang", "ES")
    lang_options = ["ES", "EUS"]
    default_index = lang_options.index(current_lang)

    selected_lang = st.radio(
        " ",
        options=lang_options,
        index=default_index,
        label_visibility="collapsed",
        key="lang_selector",
    )

if selected_lang != st.session_state.get("lang"):
    set_language(selected_lang)
    st.rerun()

st.set_page_config(
    page_title=t["page_title"], layout="wide", page_icon="assets/favicon.ico"
)

df_processed: pd.DataFrame = get_processed_dataframe_for_streamlit(df=df)
filter_options = get_filter_options(df_processed)

filter_options["basque_level_options"] = sort_by_order(
    filter_options["basque_level_options"], get_basque_level_order()
)
filter_options["education_options"] = sort_by_order(
    filter_options["education_options"], get_education_order()
)
filter_options["social_class_options"] = sort_by_order(
    filter_options["social_class_options"], get_social_class_order()
)

filter_values = render_filters_sidebar(
    basque_level_options=filter_options["basque_level_options"],
    age_range=filter_options["age_range"],
    education_options=filter_options["education_options"],
    social_class_options=filter_options["social_class_options"],
)
df_filtered: pd.DataFrame = apply_filters(df_processed, filter_values)

min_samples = 20
warning_samples = 30
n_responses = len(df_filtered)
percent = n_responses / len(df_processed) * 100

st.sidebar.info(t["sidebar_info"].format(n_responses=n_responses, percent=percent))

if n_responses < min_samples:
    st.warning(
        t["warning_min_samples"].format(
            n_responses=n_responses, min_samples=min_samples, percent=percent
        )
    )

else:
    if n_responses < warning_samples:
        st.sidebar.warning(
            t["warning_limited"].format(n_responses=n_responses, percent=percent)
        )
        st.warning(
            t["warning_limited"].format(n_responses=n_responses, percent=percent)
        )

    (
        tab1,
        tab2,
        tab3,
    ) = st.tabs(
        [
            t["tab1_title"],
            t["tab2_title"],
            t["tab3_title"],
        ]
    )

    with tab1:
        render_political_orientation_tab(df_filtered)

    with tab2:
        render_sentimiento_identidad_nacional_tab(df_filtered)

    with tab3:
        render_situacion_economica_y_politica_tab(df_filtered)

    css = """
    <style>
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size:1.3rem;
        }
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)
