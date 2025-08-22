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


def generate_all_parties_stacked_chart(df: pd.DataFrame) -> go.Figure:
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


def generate_0_to_10_bar_chart(
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


def generate_provinces_distribution_bar_chart(
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

    return fig


def generate_spain_basque_comparation_bar_chart(
    df: pd.DataFrame,
    xlabel: str,
    title: str,
    basque_question: str,
    spain_question: str,
    tag_map: dict,
) -> go.Figure:
    """
    Crea un gráfico de barras comparando respuestas para España y Euskadi
    """
    categories = list(tag_map.keys())

    spain_count = df[spain_question].value_counts(normalize=True) * 100
    spain_count = spain_count.reindex(categories, fill_value=0)
    basque_count = df[basque_question].value_counts(normalize=True) * 100
    basque_count = basque_count.reindex(categories, fill_value=0)

    data = []
    for i, category in enumerate(categories):
        data.append(
            {
                "Categoría": tag_map[category],
                "Porcentaje": spain_count[category],
                "Región": "España",
                "Posición": i - 0.2,
            }
        )
        data.append(
            {
                "Categoría": tag_map[category],
                "Porcentaje": basque_count[category],
                "Región": "Euskadi",
                "Posición": i + 0.2,  # Desplazamiento para agrupar barras
            }
        )

    plot_df = pd.DataFrame(data)

    fig = go.Figure()

    spain_df = plot_df[plot_df["Región"] == "España"]
    fig.add_trace(
        go.Bar(
            x=spain_df["Categoría"],
            y=spain_df["Porcentaje"],
            name="España",
            marker_color="#F4A261",
            marker_line_color="dimgray",
            marker_line_width=1,
            width=0.4,
            offset=-0.2,
            hovertemplate="<b>España - %{x}</b><br>Porcentaje: %{y:.1f}%<extra></extra>",
        )
    )

    basque_df = plot_df[plot_df["Región"] == "Euskadi"]
    fig.add_trace(
        go.Bar(
            x=basque_df["Categoría"],
            y=basque_df["Porcentaje"],
            name="Euskadi",
            marker_color="#2A9D8F",
            marker_line_color="dimgray",
            marker_line_width=1,
            width=0.4,
            offset=0.2,
            hovertemplate="<b>Euskadi - %{x}</b><br>Porcentaje: %{y:.1f}%<extra></extra>",
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title="Porcentaje (%)",
        barmode="group",
        bargap=0.15,
        bargroupgap=0.1,
        legend_title_text="Región",
        showlegend=True,
    )

    fig = apply_default_layout(fig)

    fig.update_xaxes(tickangle=70)

    return fig


def generate_green_red_bar_chart(
    df: pd.DataFrame, question: str, chart_title: str, x_title: str, tag_map: dict
) -> go.Figure:
    """
    Generar un gráfico de barras de porcentaje con gradiente de colores de rojo a verde
    Incluye todas las categorías incluso si faltan en los datos, y colorea NS/NC en gris
    """
    # Obtener todas las categorías del tag_map
    categories = sorted(tag_map.keys())

    # Obtener los datos y reindexar para incluir todas las categorías
    count = df[question].value_counts(normalize=True) * 100
    count = count.reindex(categories, fill_value=0).sort_index(ascending=True)

    # Crear gradiente de colores (RdYlGn)
    n_categories = len(categories)
    colores_gradiente = []

    for i, category in enumerate(categories):
        # Verificar si es la categoría NS/NC (normalmente la última)
        if "NS/NC" in tag_map[category] or "ns-nc" in tag_map[category].lower():
            colores_gradiente.insert(0, "gray")
        else:
            # Para el gradiente, usamos posición relativa excluyendo NS/NC
            effective_categories = [
                cat
                for cat in categories
                if "NS/NC" not in tag_map[cat] and "ns-nc" not in tag_map[cat].lower()
            ]
            if effective_categories:
                pos_in_gradient = (
                    effective_categories.index(category)
                    / (len(effective_categories) - 1)
                    if len(effective_categories) > 1
                    else 0.5
                )
                colores_gradiente.append(
                    px.colors.sample_colorscale("RdYlGn", pos_in_gradient)[0]
                )
            else:
                colores_gradiente.append(px.colors.sample_colorscale("RdYlGn", 0.5)[0])

    colores_gradiente.reverse()
    # Crear etiquetas para el eje X
    x_labels = [tag_map[cat] for cat in categories]

    # Crear DataFrame para las etiquetas
    plot_df = pd.DataFrame(
        {
            "categoria": x_labels,
            "porcentaje": count.values,
            "valor_original": categories,
        }
    )

    # Crear el gráfico
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=x_labels,
            y=count.values,
            marker_color=colores_gradiente,
            marker_line_color="dimgray",
            marker_line_width=1,
            hovertemplate="<b>%{x}</b><br>Porcentaje: %{y:.1f}%<extra></extra>",
            # text=count.round(1).astype(str) + " %",
            textposition="auto",
        )
    )

    # Configurar layout
    fig.update_layout(
        title=chart_title,
        xaxis_title=x_title,
        yaxis_title="Porcentaje (%)",
        showlegend=False,
    )

    # Aplicar el layout por defecto
    fig = apply_default_layout(fig)

    # # Añadir etiquetas en las barras
    add_bar_labels(fig, plot_df, "categoria", "porcentaje")

    return fig
