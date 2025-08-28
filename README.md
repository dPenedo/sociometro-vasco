# Sociómetro Vasco

## Descripción

El **Sociómetro Vasco** es una aplicación de análisis de datos basada en los estudios periódicos oficiales realizados sobre la población vasca desde 1996. La encuesta, recopila información sobre actitudes políticas, valoración de la situación social y otros temas diversos sobre una muestra de más de 3000 encuestados.

Los datos se comparten en formato CSV, disponibles [aquí](https://www.euskadi.eus/estudios-sociologicos-ficheros-datos/web01-s1lehike/es/).

## Características

- Filtrado interactivo por edad, sexo, clase social, nivel de estudios y conocimiento del euskera.
- Visualizaciones de los resultados de la encuesta.
- Fácil análisis comparativo entre distintas categorías.
- Desarrollo técnico en Python usando **Pandas** y **Plotly**, implementado en **Streamlit**.
- Inicialmente hice los gráficos con Matplotlib, pero los migré a Plotly para mayor interactividad. El código de Matplotlib se mantiene en el repositorio, por si alguien desea usarlo.

## Licencia

Este proyecto está bajo una doble licencia:

- **Código fuente**: Licencia MIT - Ver [LICENSE](LICENSE) para detalles
- **Contenido estático**: Creative Commons Attribution-NonCommercial 4.0 (CC BY-NC 4.0)

Los gráficos y visualizaciones generados por la aplicación se consideran salida del código y están cubiertos por la licencia MIT.
