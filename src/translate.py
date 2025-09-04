import json
import streamlit as st

# Cargar el JSON de traducciones una vez
with open("src/config/translations.json", "r", encoding="utf-8") as f:
    _translations = json.load(f)


def get_translations() -> dict[str, str]:
    """Devuelve el diccionario de traducciones según idioma seleccionado"""

    # Inicializar el idioma en session_state si no existe
    if "lang" not in st.session_state:
        # Intentar obtener de la URL de Streamlit (para carga inicial)
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
    """Cambia el idioma en la sesión"""
    if lang in _translations:
        st.session_state["lang"] = lang


def get_translated_map(map_name: str) -> dict:
    """Devuelve un mapa traducido según el idioma seleccionado"""
    lang: str = st.session_state.get("lang", "ES")
    t = _translations[lang]
    return t.get(map_name, {})


def get_translated_sexo_map() -> dict:
    """Devuelve el mapa de sexo traducido"""
    t = get_translations()
    return {1: t["sexo_map"]["1"], 2: t["sexo_map"]["2"]}


def get_translated_p36_grouped() -> dict:
    """Devuelve el mapa de euskera traducido"""
    t = get_translations()
    return {
        1: t["p36_grouped"]["1"],
        2: t["p36_grouped"]["2"],
        3: t["p36_grouped"]["3"],
        4: t["p36_grouped"]["4"],
        5: t["p36_grouped"]["5"],
        6: t["p36_grouped"]["6"],
    }


def get_translated_p37_grouped() -> dict:
    """Devuelve el mapa de estudios traducido"""
    t = get_translations()
    return {
        1: t["p37_grouped"]["1"],
        2: t["p37_grouped"]["2"],
        3: t["p37_grouped"]["3"],
        4: t["p37_grouped"]["4"],
        5: t["p37_grouped"]["5"],
        6: t["p37_grouped"]["6"],
    }


def get_translated_p38_map() -> dict:
    """Devuelve el mapa de clase social traducido"""
    t = get_translations()
    return {
        1: t["p38_map"]["1"],
        2: t["p38_map"]["2"],
        3: t["p38_map"]["3"],
        4: t["p38_map"]["4"],
    }


def get_translated_p36_order() -> list:
    """Devuelve el orden de euskera traducido"""
    t = get_translations()
    return t["p36_order"]


def get_translated_p37_order() -> list:
    """Devuelve el orden de estudios traducido"""
    t = get_translations()
    return t["p37_order"]


def get_translated_p38_order() -> list:
    """Devuelve el orden de clase social traducido"""
    t = get_translations()
    return t["p38_order"]
