import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from src.charts.helpers import add_bar_labels
from src.charts.layouts import apply_default_layout, get_color_map_from_scale
from src.config.questions import (
    p25_tag_map,
    ordered_p25_list,
)

from src.config.colors import (
    parties_map_and_colors_p25,
    provincias_map,
    red_blue_color_list,
)
from src.data.processing import get_df_of_pct, get_pct_series


def create_all_parties_stacked_chart(df: pd.DataFrame) -> go.Figure:
    all_data = []

    for _, info in parties_map_and_colors_p25.items():
        percent_series = (
            df[info["question"]].map(p25_tag_map).value_counts(normalize=True) * 100
        ).reindex(ordered_p25_list, fill_value=0)

        for valor, porcentaje in percent_series.items():
            all_data.append(
                {
                    "partido": info["name"],
                    "valor": valor,
                    "porcentaje": porcentaje,
                    "party_color": info["color"],
                }
            )

    plot_df = pd.DataFrame(all_data)

    color_map = get_color_map_from_scale(ordered_p25_list)
    ordered_parties = [info["name"] for info in parties_map_and_colors_p25.values()]
    fig: go.Figure = px.bar(
        plot_df,
        x="porcentaje",
        y="partido",
        title="Distribución de simpatía por partido",
        color="valor",
        color_discrete_map=color_map,
        orientation="h",
        text=plot_df["porcentaje"].round(1).astype(str) + " %",
        labels={"valor": "Puntaje", "porcentaje": "Menor a mayor simpatía"},
        category_orders={"partido": ordered_parties},
    )

    fig = apply_default_layout(fig, {"barmode": "stack"})

    return fig


def create_0_to_10_percentage_bar_chart2(
    df: pd.DataFrame, question: str, chart_title: str, x_title: str, tag_map: dict
) -> go.Figure:

    ALL_CATEGORIES: list[int] = list(range(12))
    base_df: pd.DataFrame = pd.DataFrame({"valores": ALL_CATEGORIES})
    dfcount: pd.DataFrame = get_pct_series(df, question)
    dfcount = base_df.merge(dfcount, on="valores", how="left").fillna(0)
    dfcount["valores_str"] = dfcount["valores"].astype(str)
    dfcount["etiqueta"] = dfcount["valores"].map(tag_map)

    category_order = [str(i) for i in ALL_CATEGORIES]

    fig: go.Figure = px.bar(
        data_frame=dfcount,
        x="valores_str",
        y="porcentaje",
        color="valores_str",
        title=chart_title,
        color_discrete_sequence=red_blue_color_list,
        category_orders={"valores_str": category_order},
        hover_data={"etiqueta": True, "valores_str": False, "porcentaje": ":.1f"},
        labels={"etiqueta": "Orientación", "porcentaje": "Porcentaje (%)"},
    )

    fig.update_layout(
        xaxis=dict(
            title=x_title,
            tickmode="array",
            tickvals=category_order,
            ticktext=[tag_map[i] for i in ALL_CATEGORIES],
            showline=True,
            showgrid=False,
        ),
        yaxis=dict(
            title="Porcentaje (%)",
            showline=True,
            showgrid=True,
            gridcolor="lightgray",
            zeroline=True,
            zerolinecolor="lightgray",
        ),
        showlegend=False,
    )

    fig = apply_default_layout(fig)
    fig.update_traces(
        marker_line_color="#454545",
        marker_line_width=0.4,
        hovertemplate="<b>%{customdata[0]}</b><br>Porcentaje: %{y:.1f}%<extra></extra>",
    )

    add_bar_labels(fig, dfcount, "valores_str", "porcentaje")
    return fig


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
    # Verificación robusta para Streamlit
    if hasattr(tag_map, "keys"):
        # Es un diccionario, proceder normalmente
        all_responses = list(tag_map.keys())
    else:
        # No es un diccionario, intentar recuperar el verdadero tag_map
        try:
            from src.config.questions import p32_tag_map as real_tag_map

            tag_map = real_tag_map
            all_responses = list(tag_map.keys())
        except ImportError:
            raise ValueError("No se pudo obtener el tag_map correcto")
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
