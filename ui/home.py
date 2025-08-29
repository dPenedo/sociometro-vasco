import streamlit as st


def show_page():
    """Muestra la página de inicio"""
    # st.header("Análisis interactivo del Sociómetro Vasco")

    st.markdown(
        """
    El [Sociometro_vasco](https://www.euskadi.eus/sociometros-vascos/web01-s1lehike/es/), es un estudio periódico oficial que realiza un cuestionario sobre una población amplia desde **1996**. En este caso los datos son de **Julio del 2025**.
    Los datos de la encuesta son compartidos en formato **CSV**, [aquí el enlace](https://www.euskadi.eus/estudios-sociologicos-ficheros-datos/web01-s1lehike/es/).
    Hay un total de 11 gráficos en total divididos en 3 secciones: orientación política, sentimiento de identidad nacional y situación económica y política. A ellos se les pueden aplicar los siguientes filtros. En el caso de que los filtros no estén abiertos, se pueden abrir en la parte superior izquierda(con el ícono `>>`):
    - Sexo
    - Edad 
    - Nivel de estudios finalizados
    - Clase social autopercibida
    - Nivel de euskera
"""
    )
