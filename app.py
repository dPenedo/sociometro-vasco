import pandas as pd
import streamlit as st

from src.config.data import df
from src.config.questions import (
    p36_order,
    p37_order,
    p38_order,
)
from src.data.processing import (
    apply_filters,
    get_filter_options,
    get_processed_dataframe_for_streamlit,
)
from src.translate import get_translations, set_language
from src.utils import sort_by_order
from ui.filters import render_filters_sidebar
from ui.tabs.orientacion_politica import render_political_orientation_tab
from ui.tabs.sentimiento_identidad_nacional import (
    render_sentimiento_identidad_nacional_tab,
)
from ui.tabs.situacion_economica_y_politica import (
    render_situacion_economica_y_politica_tab,
)

# Selector de idioma
t = get_translations()

col1, col2 = st.columns([12, 2])
with col2:
    # Get the current language from session state to set the radio default
    current_lang = st.session_state.get("lang", "ES")

    # Find the index of the current language for the radio button
    lang_options = ["ES", "EUS"]
    default_index = lang_options.index(current_lang)

    # Create the radio button. When it changes, it calls set_language
    lang = st.radio(
        " ",
        options=lang_options,
        index=default_index,  # This sets the default based on URL/session
        label_visibility="collapsed",
        key="lang_selector",  # Give it a key
        # REMOVE the on_change and args from here
    )

# Check if the radio button was changed and update the language
if "lang_selector" in st.session_state:
    # Only set the language if it's different from the current one
    if st.session_state.lang_selector != st.session_state.get("lang"):
        set_language(st.session_state.lang_selector)
        # Force a rerun to apply the language change immediately
        st.rerun()
st.set_page_config(page_title=t["page_title"], layout="wide")
st.title(t["main_title"])

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
    st.markdown(t["main_intro"])

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
