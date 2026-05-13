from typing import Any, List, Dict
import streamlit as st
from src.translate import get_translations, get_sex_map


def render_filters_sidebar(
    basque_level_options: List[str],
    age_range: tuple,
    education_options: List[str],
    social_class_options: List[str],
) -> Dict[str, Any]:
    t = get_translations()
    st.sidebar.header(t["sidebar_header"])

    sex_map = get_sex_map()
    sex_options = [t["filter_all"], sex_map[1], sex_map[2]]
    selected_sex = st.sidebar.selectbox(
        t["sidebar_sex_label"],
        sex_options,
        index=0,
    )

    selected_age_min, selected_age_max = st.sidebar.slider(
        t["sidebar_age_label"],
        min_value=age_range[0],
        max_value=age_range[1],
        value=age_range,
    )

    selected_education = st.sidebar.multiselect(
        t["sidebar_studies_label"],
        options=education_options,
        default=education_options,
    )

    selected_social_class = st.sidebar.multiselect(
        t["sidebar_class_label"],
        options=social_class_options,
        default=social_class_options,
    )

    selected_basque_level = st.sidebar.multiselect(
        t["sidebar_basque_label"],
        options=basque_level_options,
        default=basque_level_options,
    )

    return {
        "sex": selected_sex,
        "basque_level": selected_basque_level,
        "age_min": selected_age_min,
        "age_max": selected_age_max,
        "education": selected_education,
        "social_class": selected_social_class,
    }
