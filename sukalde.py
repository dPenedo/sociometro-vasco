# %%
# Imports
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.graph_objs import Figure
import plotly.graph_objects as go
from src.charts.helpers import add_bar_labels
from src.charts.layouts import apply_default_layout
from src.config.data import df
from src.config.questions import p32_tag_map
from src.config.colors import provincias_map
from src.data.processing import get_df_of_pct


# %%
#
# %%
#


# %%
#
def create_provinces_distribution_bar_chart2(
    df: pd.DataFrame,
    question: str,
    title: str,
    tag_map: dict,
    xlabel: str,
) -> go.Figure:
    """
    Crea un gráfico de barras agrupadas que muestra la distribución de
    respuestas por provincia.
    """
    print(f"Tipo de tag_map: {type(tag_map)}")
    print(f"Contenido de tag_map: {tag_map}")
    provinces_df = get_df_of_pct(df, "lurral", question)
    # Debug: verificar el tipo de tag_map

    # Iterar sobre el índice multi-nivel
    data = []
    for idx, row in provinces_df.iterrows():
        provincia = idx[0]  # Tomamos el primer valor que es la provincia real

        # Iterar sobre cada respuesta (columna)
        for respuesta, porcentaje in row.items():
            data.append(
                {"lurral": provincia, "Respuesta": respuesta, "Porcentaje": porcentaje}
            )

    provinces_df_long = pd.DataFrame(data)

    all_provinces = provinces_df_long["lurral"].unique()
    all_responses = list(tag_map.keys())

    # Crear un MultiIndex con todas las combinaciones
    multi_index = pd.MultiIndex.from_product(
        [all_provinces, all_responses], names=["lurral", "Respuesta"]
    )

    # Reindexar para incluir todas las combinaciones, llenando con 0 los valores faltantes
    provinces_df_long = provinces_df_long.set_index(["lurral", "Respuesta"])
    provinces_df_long = provinces_df_long.reindex(
        multi_index, fill_value=0
    ).reset_index()

    provinces_df_long["Provincia"] = provinces_df_long["lurral"].map(
        lambda x: provincias_map[x]["name"]
    )
    color_map = {prov["name"]: prov["color"] for prov in provincias_map.values()}

    provinces_df_long["Respuesta_Etiqueta"] = provinces_df_long["Respuesta"].map(
        tag_map
    )

    ordered_labels = [tag_map[i] for i in sorted(tag_map.keys())]
    category_order = [str(i) for i in sorted(tag_map.keys())]

    fig = px.bar(
        provinces_df_long,
        x="Respuesta",
        y="Porcentaje",
        color="Provincia",
        barmode="group",
        title=title,
        labels={"Porcentaje": "Porcentaje (%)"},
        color_discrete_map=color_map,
        category_orders={"Respuesta": category_order},
        hover_data={
            "Respuesta_Etiqueta": True,
            "Respuesta": False,
            "Porcentaje": ":.1f",
            "Provincia": True,
        },
    )

    fig.update_layout(
        xaxis=dict(
            title=xlabel,
            tickmode="array",
            tickvals=category_order,
            ticktext=ordered_labels,
            showline=True,
            showgrid=False,
            automargin=True,
        ),
        yaxis=dict(
            title="Porcentaje (%)",
            showline=True,
            showgrid=True,
            gridcolor="lightgray",
            zeroline=True,
            zerolinecolor="lightgray",
        ),
        legend_title_text="Provincias",
    )

    fig = apply_default_layout(fig)
    fig.update_traces(
        marker_line_color="#454545",
        marker_line_width=0.4,
        hovertemplate="<b>%{customdata[1]}</b><br>Valor: %{customdata[0]}<br>Porcentaje: %{y:.1f}%<extra></extra>",
    )

    fig.show()

    return fig


# %%
#
create_provinces_distribution_bar_chart2(
    df,
    "p32",
    "Distribución izq-derecha por provincias",
    p32_tag_map,
    "Más izquierda a más derecha",
)


# %%
#
