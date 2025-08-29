from typing import Any, List, Dict
import streamlit as st


def render_filters_sidebar(
    euskera_options: List[str],
    edad_range: tuple,
    estudios_options: List[str],
    clase_options: List[str],
) -> Dict[str, Any]:
    """Muestra los filtros de la barra lateral y retorna los valores seleccionados"""

    st.sidebar.header("Filtros Demográficos")

    selected_sex = st.sidebar.selectbox(
        "Sexo",
        [
            "Todos",
            "Hombre",
            "Mujer",
        ],
        index=0,
    )

    # Filtro por edad
    selected_edad_min, selected_edad_max = st.sidebar.slider(
        "Rango de edad",
        min_value=edad_range[0],
        max_value=edad_range[1],
        value=edad_range,
    )

    # Filtro por estudios
    selected_estudios = st.sidebar.multiselect(
        "Nivel de estudios finalizados",
        options=estudios_options,
        default=estudios_options,
    )

    # Filtro por clase social
    selected_clase = st.sidebar.multiselect(
        "Clase social autopercibida",
        options=clase_options,
        default=clase_options,
    )

    selected_euskera = st.sidebar.multiselect(
        "Nivel de euskera",
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
