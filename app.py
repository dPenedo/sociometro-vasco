import pandas as pd
import streamlit as st

from src.config.data import df
from src.config.questions import (
    p36_order,
    p37_order,
    p38_order,
)
from src.processing.processing import (
    apply_filters,
    get_filter_options,
    get_processed_dataframe_for_streamlit,
)
from src.translate import get_translations, set_language
from src.utils import sort_by_order
from src.ui.filters import render_filters_sidebar
from src.ui.tabs.orientacion_politica import render_political_orientation_tab
from src.ui.tabs.sentimiento_identidad_nacional import (
    render_sentimiento_identidad_nacional_tab,
)
from src.ui.tabs.situacion_economica_y_politica import (
    render_situacion_economica_y_politica_tab,
)

t = get_translations()

query_params = st.query_params
app_is_full_screen = query_params.get("utm_medium") == "oembed"

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

# Actualizar el idioma si cambió el radio button
if selected_lang != st.session_state.get("lang"):
    set_language(selected_lang)
    st.rerun()  # Forzar recarga para aplicar los cambios

st.set_page_config(
    page_title=t["page_title"], layout="wide", page_icon="assets/favicon.ico"
)

df_processed: pd.DataFrame = get_processed_dataframe_for_streamlit(
    df=df,
)
filter_options = get_filter_options(df_processed)

filter_options["euskera_options"] = sort_by_order(
    filter_options["euskera_options"], p36_order
)
filter_options["estudios_options"] = sort_by_order(
    filter_options["estudios_options"], p37_order
)
filter_options["clase_options"] = sort_by_order(
    filter_options["clase_options"], p38_order
)

filter_values = render_filters_sidebar(
    euskera_options=filter_options["euskera_options"],
    edad_range=filter_options["edad_range"],
    estudios_options=filter_options["estudios_options"],
    clase_options=filter_options["clase_options"],
)
df_filtered: pd.DataFrame = apply_filters(df_processed, filter_values)

min_samples = 20
warning_samples = 30
n_responses = len(df_filtered)
percent = n_responses / len(df_processed) * 100
# Mostrar información del tamaño de muestra
st.sidebar.info(t["sidebar_info"].format(n_responses=n_responses, percent=percent))

# Validar tamaño de muestra antes de mostrar contenido
if n_responses < min_samples:
    st.warning(
        t["warning_min_samples"].format(
            n_responses=n_responses, min_samples=min_samples, percent=percent
        )
    )

else:
    # Mostrar advertencia si la muestra es pequeña pero suficiente
    if n_responses < warning_samples:
        st.sidebar.warning(
            t["warning_limited"].format(n_responses=n_responses, percent=percent)
        )
        st.warning(
            t["warning_limited"].format(n_responses=n_responses, percent=percent)
        )

    # Mostrar el contenido principal solo si hay suficientes muestras
    # st.markdown(t["main_intro"])

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
