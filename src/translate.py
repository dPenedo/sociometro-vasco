import json
import streamlit as st

# Cargar el JSON de traducciones una vez
with open("translations.json", "r", encoding="utf-8") as f:
    _translations = json.load(f)


def get_translations():
    """Devuelve el diccionario de traducciones según idioma seleccionado"""
    # idioma por defecto
    lang = st.session_state.get("lang", "ES")
    return _translations[lang]


def set_language(lang: str):
    """Cambia el idioma en la sesión"""
    st.session_state["lang"] = lang
