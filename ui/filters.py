from typing import Any, List, Dict
import streamlit as st
from src.translate import get_translations, get_translated_sexo_map


def render_filters_sidebar(
    euskera_options: List[str],
    edad_range: tuple,
    estudios_options: List[str],
    clase_options: List[str],
) -> Dict[str, Any]:
    """Muestra los filtros de la barra lateral y retorna los valores seleccionados"""

    t = get_translations()
    st.sidebar.header(t["sidebar_header"])

    sexo_map = get_translated_sexo_map()
    print("sexo_map => ", sexo_map)
    sex_options = [t["filter_all"], sexo_map[1], sexo_map[2]]
    selected_sex = st.sidebar.selectbox(
        t["sidebar_sex_label"],
        sex_options,
        index=0,
    )

    # Filtro por edad
    selected_edad_min, selected_edad_max = st.sidebar.slider(
        t["sidebar_age_label"],
        min_value=edad_range[0],
        max_value=edad_range[1],
        value=edad_range,
    )

    # Filtro por estudios
    selected_estudios = st.sidebar.multiselect(
        t["sidebar_studies_label"],
        options=estudios_options,
        default=estudios_options,
    )

    # Filtro por clase social
    selected_clase = st.sidebar.multiselect(
        t["sidebar_class_label"],
        options=clase_options,
        default=clase_options,
    )

    selected_euskera = st.sidebar.multiselect(
        t["sidebar_basque_label"],
        options=euskera_options,
        default=euskera_options,
    )
    return {
        "sexo": selected_sex,
        "euskera": selected_euskera,
        "edad_min": selected_edad_min,
        "edad_max": selected_edad_max,
        "estudios": selected_estudios,
        "clase": selected_clase,
    }
