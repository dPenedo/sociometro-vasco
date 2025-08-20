# %%
# Imports
import pandas as pd
import plotly.express as px
from plotly.graph_objs import Figure
import plotly.graph_objects as go
from src.charts.bar_plotly import create_0_to_10_percentage_bar_chart2
from src.config import df, p32_tag_map
from src.data.processing import get_pct_series


# %%
#

import plotly.io as pio

pio.renderers.default = "png"
# %%
#


def create_0_to_10_percentage_bar_chart2(
    df: pd.DataFrame, question: str, chart_title: str, x_title: str, tag_map: dict
) -> go.Figure:

    # dfcount con manejo de categorías faltantes
    ALL_CATEGORIES = list(range(12))

    # Crear dataframe base con todas las categorías
    base_df: pd.DataFrame = pd.DataFrame({"valores": ALL_CATEGORIES})

    # Calcular porcentajes
    dfcount: pd.DataFrame = get_pct_series(df, question)

    # Merge con todas las categorías (asegura las 12)
    dfcount = base_df.merge(dfcount, on="valores", how="left").fillna(0)

    dfcount["valores_str"] = dfcount["valores"].astype(str)
    dfcount["etiqueta"] = dfcount["valores"].map(tag_map)

    # Lista de 12 colores
    red_blue_color_list = [
        "#A50026",  # 0 - Ext. Izquierda (rojo intenso)
        "#D73027",  # 1
        "#F46D43",  # 2
        "#FDAE61",  # 3
        "#FEE090",  # 4
        "#FFFFBF",  # 5 - Centro (amarillo muy claro)
        "#E0F3F8",  # 6
        "#ABD9E9",  # 7
        "#74ADD1",  # 8
        "#4575B4",  # 9
        "#313695",  # 10 - Ext. Derecha (azul intenso)
        "#808080",  # 11 - NS/NC (gris neutral)
    ]

    # Orden de las categorías
    category_order = [str(i) for i in ALL_CATEGORIES]

    fig = px.bar(
        dfcount,
        x="valores_str",
        y="porcentaje",
        color="valores_str",
        title=chart_title,
        color_discrete_sequence=red_blue_color_list,
        category_orders={"valores_str": category_order},
        hover_data={"etiqueta": True, "valores_str": False, "porcentaje": ":.1f"},
        labels={"etiqueta": "Orientación", "porcentaje": "Porcentaje (%)"},
    )

    # Personalizar ejes
    fig.update_layout(
        xaxis=dict(
            title=x_title,
            tickmode="array",
            tickvals=category_order,
            ticktext=[tag_map[i] for i in ALL_CATEGORIES],
            showline=True,
            showgrid=False,
            # linecolor="#434343",
            # linewidth=2,
        ),
        yaxis=dict(
            title="Porcentaje (%)",
            showline=True,
            showgrid=True,
            gridcolor="lightgray",
            zeroline=True,
            zerolinecolor="lightgray",
            # linecolor="#434343",
            # linewidth=2,
        ),
        font=dict(size=14),
        showlegend=False,
        height=500,
        hoverlabel=dict(font_size=14),
    )

    # Mejorar las barras
    fig.update_traces(
        marker_line_color="#454545",
        marker_line_width=0.4,
        hovertemplate="<b>%{customdata[0]}</b><br>Porcentaje: %{y:.1f}%<extra></extra>",
    )

    # Añadir anotaciones de porcentaje solo si > 0
    for i, row in dfcount.iterrows():
        fig.add_annotation(
            x=row["valores_str"],
            y=row["porcentaje"] + 0.5,
            text=f"{row['porcentaje']:.1f}%",
            showarrow=False,
            font=dict(size=10),
            yshift=10,
        )
    return fig


# %%
#
fig = create_0_to_10_percentage_bar_chart2(
    df,
    "p32",
    "Eje izquierda-derecha",
    "Ubicación ideológica en el eje izquierda-derecha",
    p32_tag_map,
)
fig.write_html("grafico_debug.html", auto_open=True)

# %%
#
