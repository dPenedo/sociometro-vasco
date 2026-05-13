import json
import streamlit as st

with open("src/config/translations.json", "r", encoding="utf-8") as f:
    _translations = json.load(f)


def get_translations() -> dict:
    if "lang" not in st.session_state:
        params = st.query_params
        if "lang" in params:
            lang_from_url = params["lang"].upper()
            if lang_from_url in _translations:
                st.session_state["lang"] = lang_from_url
            else:
                st.session_state["lang"] = "ES"
        else:
            st.session_state["lang"] = "ES"

    return _translations[st.session_state["lang"]]


def set_language(lang: str) -> None:
    if lang in _translations:
        st.session_state["lang"] = lang


def get_map(map_name: str) -> dict:
    lang: str = st.session_state.get("lang", "ES")
    t = _translations[lang]
    return t.get(map_name, {})


def get_sex_map() -> dict:
    t = get_translations()
    return {1: t["sex_map"]["1"], 2: t["sex_map"]["2"]}


def get_basque_level_grouped() -> dict:
    t = get_translations()
    return {int(k): v for k, v in t["basque_level_grouped"].items()}


def get_education_grouped() -> dict:
    t = get_translations()
    return {int(k): v for k, v in t["education_grouped"].items()}


def get_social_class_map() -> dict:
    t = get_translations()
    return {int(k): v for k, v in t["social_class_map"].items()}


def get_basque_level_order() -> list:
    t = get_translations()
    return t["basque_level_order"]


def get_education_order() -> list:
    t = get_translations()
    return t["education_order"]


def get_social_class_order() -> list:
    t = get_translations()
    return t["social_class_order"]
