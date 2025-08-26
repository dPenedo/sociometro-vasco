import streamlit as st

def show_page():
    """Muestra la página de inicio"""
    # st.header("Análisis interactivo del Sociómetro Vasco")

    st.markdown(
        """
    El [Sociometro_vasco](https://www.euskadi.eus/sociometros-vascos/web01-s1lehike/es/), es un estudio periódico oficial que realiza un cuestionario sobre una población amplia desde **1996**. 
    Los datos de la encuesta son compartidos en formato **CSV**, [aquí el enlace](https://www.euskadi.eus/estudios-sociologicos-ficheros-datos/web01-s1lehike/es/).

    La encuesta se lleva a cabo por la lehendakaritza. Esta es su descripción en el sitio web:

    > Serie de estudios que comenzó en 1996 y que intenta ofrecer un retrato de la realidad social vasca. 
    > Consta de un cuerpo común (actitudes políticas y valoración de la situación) y una o más partes con temas diversos. 
    > Su enfoque es descriptivo, evolutivo y comparativo. El objetivo no es sólo conocer cómo somos las vascas y los vascos, 
    > sino también cómo vamos cambiando, y en qué nos parecemos o nos diferenciamos de las y los habitantes de la totalidad 
    > del Estado y de los países de la Unión Europea.
    """
    )
