import pandas as pd
import streamlit as st

from ui.home import show_page
from ui.filters import render_filters_sidebar
from ui.tabs.orientacion_politica import render_political_orientation_tab
from ui.tabs.sentimiento_identidad_nacional import (
    render_sentimiento_identidad_nacional_tab,
)
from ui.tabs.situacion_economica_y_politica import (
    render_situacion_economica_y_politica_tab,
)
from src.config.data import df


from src.data.processing import (
    apply_filters,
    get_filter_options,
    get_processed_dataframe_for_streamlit,
)

from src.utils import sort_by_order

from src.config.questions import (
    sexo_map,
    p36_grouped,
    p36_order,
    p37_grouped,
    p37_order,
    p38_map,
    p38_order,
)

st.set_page_config(layout="wide")
st.title("Análisis del Sociómetro Vasco")

df_processed: pd.DataFrame = get_processed_dataframe_for_streamlit(
    df=df,
    p36_grouped=p36_grouped,
    p36_order=p36_order,
    p37_grouped=p37_grouped,
    p37_order=p37_order,
    p38_map=p38_map,
    p38_order=p38_order,
    sexo_map=sexo_map,
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
# Mostrar información del tamaño de muestra
st.sidebar.info(
    f"Filtro actual: {n_responses} respuestas\n\n"
    f"Porcentaje del total: {n_responses / len(df_processed) * 100:.1f}%"
)

# Validar tamaño de muestra antes de mostrar contenido
if n_responses < min_samples:
    st.warning(
        f"⚠️ Muestra insuficiente: {n_responses} respuestas\n\n"
        f"Se requieren al menos {min_samples} respuestas para mostrar el análisis. "
        f"La muestra actual, tras aplicar los filtros seleccionados, solo constituye un "
        f"{n_responses / len(df_processed) * 100:.1f}% de la muestra total.\n\n"
        "Por favor, ajuste los filtros para incluir más datos."
    )

else:
    # Mostrar advertencia si la muestra es pequeña pero suficiente
    if n_responses < warning_samples:
        st.sidebar.warning(
            f"⚠️ Muestra limitada: {n_responses} respuestas\n"
            f"({n_responses / len(df_processed) * 100:.1f}% del total)\n"
            "Los resultados pueden tener baja representatividad estadística."
        )
        st.warning(
            f"⚠️ Muestra limitada: {n_responses} respuestas\n"
            f"({n_responses / len(df_processed) * 100:.1f}% del total)\n"
            "Los resultados pueden tener baja representatividad estadística."
        )

    # Mostrar el contenido principal solo si hay suficientes muestras
    show_page()

    (
        tab1,
        tab2,
        tab3,
    ) = st.tabs(
        [
            "Orientación política",
            "Sentimiento de identidad nacional",
            "Situación económica y política",
        ]
    )

    with tab1:
        render_political_orientation_tab(df_filtered)

    with tab2:
        render_sentimiento_identidad_nacional_tab(df_filtered)

    with tab3:
        render_situacion_economica_y_politica_tab(df_filtered)
