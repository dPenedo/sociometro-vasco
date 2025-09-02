import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from src.charts.helpers import add_bar_labels, generate_hovertemplate
from src.config.colors import red_green_color_list
from src.charts.layouts import apply_default_layout, get_color_map_from_scale
from src.config.questions import (
    p25_tag_map,
)

from src.config.colors import (
    parties_map_and_colors_p25,
    provincias_map,
    red_blue_color_list,
)
from src.data.processing import get_counts_and_percents


def generate_all_parties_stacked_chart(
    df: pd.DataFrame, chart_title: str, percent_label: str, count_label: str
) -> go.Figure:
    all_data = []
    ordered_categories = []
    for v in p25_tag_map.values():
        ordered_categories.append(str(v))

    for _, info in parties_map_and_colors_p25.items():
        counts_df: pd.DataFrame = get_counts_and_percents(
            df[info["question"]].map(p25_tag_map),
            ordered_categories,
            label_col="valor",
        )

        for _, row in counts_df.iterrows():
            all_data.append(
                {
                    "partido": info["name"],
                    "valor": row["valor"],
                    "conteo": row["conteo"],
                    "porcentaje": row["porcentaje"],
                    "party_color": info["color"],
                }
            )

    plot_df = pd.DataFrame(all_data)

    color_map = get_color_map_from_scale(ordered_categories)
    ordered_parties = [info["name"] for info in parties_map_and_colors_p25.values()]

    fig: go.Figure = px.bar(
        plot_df,
        x="porcentaje",
        y="partido",
        title=chart_title,
        color="valor",
        color_discrete_map=color_map,
        orientation="h",
        text=plot_df["porcentaje"].round(1).astype(str) + " %",
        labels={
            "valor": "",
            "porcentaje": percent_label,
            "partido": "Partido",
        },
        category_orders={"partido": ordered_parties},
        custom_data=["valor", "conteo", "porcentaje"],
    )
    fig.update_traces(
        hovertemplate=generate_hovertemplate(
            percent_label=percent_label, count_label=count_label
        )
    )

    fig.update_yaxes(title_text="", automargin=True)  # quita el título del eje y
    fig = apply_default_layout(fig)

    fig.update_layout(
        legend=dict(
            orientation="h",  # horizontal
            yanchor="top",
            y=-0.15,  # un poco debajo del gráfico
            xanchor="center",
            x=0.5,
            font=dict(size=10),
        )
    )
    return fig


def generate_0_to_10_bar_chart(
    df: pd.DataFrame,
    question: str,
    chart_title: str,
    x_title: str,
    tag_map: dict,
    percent_label: str,
    count_label: str,
) -> go.Figure:
    ALL_CATEGORIES: list[int] = list(range(12))
    counts_df = get_counts_and_percents(
        df[question], ordered_categories=ALL_CATEGORIES, label_col="valores"
    )

    counts_df["valores_str"] = counts_df["valores"].astype(str)
    counts_df["etiqueta"] = counts_df["valores"].map(tag_map)

    category_order = [str(i) for i in ALL_CATEGORIES]

    fig: go.Figure = px.bar(
        data_frame=counts_df,
        x="valores_str",
        y="porcentaje",
        color="valores_str",
        title=chart_title,
        color_discrete_sequence=red_blue_color_list,
        category_orders={"valores_str": category_order},
        labels={"etiqueta": "Orientación", "porcentaje": percent_label},
        custom_data=["etiqueta", "conteo", "porcentaje"],
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
            title=percent_label,
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
        hovertemplate=generate_hovertemplate(
            percent_label=percent_label, count_label=count_label
        )
    )

    add_bar_labels(fig, counts_df, "valores_str", "porcentaje")
    return fig


def generate_provinces_distribution_bar_chart(
    df: pd.DataFrame,
    question: str,
    title: str,
    tag_map: dict,
    xlabel: str,
    percent_label: str,
    count_label: str,
    provinces_label: str,
) -> go.Figure:
    """
    Crea un gráfico de barras agrupadas que muestra la distribución de
    respuestas por provincia.
    """
    data = []

    for provincia in df["lurral"].unique():
        provincia_df = df[df["lurral"] == provincia]

        # Usar get_counts_and_percents para cada provincia
        counts_df = get_counts_and_percents(
            provincia_df[question],
            ordered_categories=list(tag_map.keys()),
            label_col="Respuesta",
        )

        for _, row in counts_df.iterrows():
            data.append(
                {
                    "lurral": provincia,
                    "Respuesta": row["Respuesta"],
                    "Porcentaje": row["porcentaje"],
                    "conteo": row["conteo"],
                }
            )

    provinces_df_long = pd.DataFrame(data)

    provinces_df_long["Provincia"] = provinces_df_long["lurral"].map(
        lambda x: provincias_map[x]["name"]
    )
    provinces_df_long["Respuesta_Etiqueta"] = provinces_df_long["Respuesta"].map(
        tag_map
    )

    color_map = {prov["name"]: prov["color"] for prov in provincias_map.values()}

    ordered_labels = [tag_map[i] for i in sorted(tag_map.keys())]
    category_order = [str(i) for i in sorted(tag_map.keys())]

    fig = px.bar(
        provinces_df_long,
        x="Respuesta",
        y="Porcentaje",
        color="Provincia",
        barmode="group",
        title=title,
        labels={"Porcentaje": percent_label},
        color_discrete_map=color_map,
        category_orders={"Respuesta": category_order},
        custom_data=["Respuesta_Etiqueta", "conteo", "Porcentaje", "Provincia"],
        hover_data={
            "Respuesta_Etiqueta": True,
            "Respuesta": False,
            "Porcentaje": ":.1f",
            "Provincia": True,
            "lurral": False,
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
            title=percent_label,
            showline=True,
            showgrid=True,
            gridcolor="lightgray",
            zeroline=True,
            zerolinecolor="lightgray",
        ),
        legend_title_text=provinces_label,
    )

    fig = apply_default_layout(fig)
    fig.update_traces(
        hovertemplate=generate_hovertemplate(
            percent_label=percent_label, count_label=count_label
        )
    )

    fig.update_layout(
        legend=dict(
            orientation="h",  # horizontal
            yanchor="top",
            y=-0.2,  # un poco debajo del gráfico
            xanchor="center",
            x=0.5,
            font=dict(size=10),
        )
    )
    return fig


def generate_spain_basque_comparation_bar_chart(
    df: pd.DataFrame,
    xlabel: str,
    title: str,
    basque_question: str,
    spain_question: str,
    tag_map: dict,
    percent_label: str,
    count_label: str,
) -> go.Figure:
    """
    Crea un gráfico de barras comparando respuestas para España y Euskadi
    """
    categories = list(tag_map.keys())

    # Usar get_counts_and_percents para ambas preguntas
    spain_df = get_counts_and_percents(
        df[spain_question],
        ordered_categories=categories,
        label_col="Categoría_original",
    )
    spain_df["Región"] = "España"
    spain_df["Categoría"] = spain_df["Categoría_original"].map(tag_map)

    basque_df = get_counts_and_percents(
        df[basque_question],
        ordered_categories=categories,
        label_col="Categoría_original",
    )
    basque_df["Región"] = "Euskadi"
    basque_df["Categoría"] = basque_df["Categoría_original"].map(tag_map)

    # Combinar ambos DataFrames
    plot_df = pd.concat([spain_df, basque_df], ignore_index=True)

    fig = go.Figure()

    # Traza para España
    spain_data = plot_df[plot_df["Región"] == "España"]
    fig.add_trace(
        go.Bar(
            x=spain_data["Categoría"],
            y=spain_data["porcentaje"],
            name="España",
            marker_color="#F4A261",
            width=0.4,
            offset=-0.2,
            customdata=np.column_stack(
                (
                    spain_data["conteo"],
                    spain_data["Categoría_original"],
                    spain_data["porcentaje"],
                )
            ),
        )
    )

    # Traza para Euskadi
    basque_data = plot_df[plot_df["Región"] == "Euskadi"]
    fig.add_trace(
        go.Bar(
            x=basque_data["Categoría"],
            y=basque_data["porcentaje"],
            name="Euskadi",
            marker_color="#2A9D8F",
            width=0.4,
            offset=0.2,
            customdata=np.column_stack(
                (
                    basque_data["conteo"],
                    basque_data["Categoría_original"],
                    basque_data["porcentaje"],
                )
            ),
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title=percent_label,
        barmode="group",
        bargap=0.15,
        bargroupgap=0.1,
        legend_title_text="Región",
        showlegend=True,
    )

    fig.update_traces(
        hovertemplate=generate_hovertemplate(
            percent_label=percent_label, count_label=count_label, show_x_as_name=True
        )
    )
    fig = apply_default_layout(fig)
    # fig.update_xaxes(tickangle=70)

    return fig


def generate_green_red_bar_chart(
    df: pd.DataFrame,
    question: str,
    chart_title: str,
    x_title: str,
    tag_map: dict,
    percent_label: str,
    count_label: str,
) -> go.Figure:
    """
    Generar un gráfico de barras de porcentaje con gradiente de colores de rojo a verde
    Incluye todas las categorías incluso si faltan en los datos, y colorea NS/NC en gris
    """
    # Obtener todas las categorías del tag_map
    categories = sorted(tag_map.keys())

    # Usar get_counts_and_percents
    counts_df = get_counts_and_percents(
        df[question], ordered_categories=categories, label_col="valor_original"
    )

    # Crear etiquetas para el eje X
    counts_df["categoria"] = counts_df["valor_original"].map(tag_map)

    colores_gradiente = []

    for category in categories:
        # Verificar si es la categoría NS/NC
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
                    px.colors.sample_colorscale(red_green_color_list, pos_in_gradient)[
                        0
                    ]
                )
            else:
                colores_gradiente.append(
                    px.colors.sample_colorscale(red_green_color_list, 0.5)[0]
                )

    colores_gradiente.reverse()

    # Crear el gráfico
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=counts_df["categoria"],
            y=counts_df["porcentaje"],
            marker_color=colores_gradiente,
            customdata=np.column_stack(
                (
                    counts_df["categoria"],
                    counts_df["conteo"],
                    counts_df["porcentaje"],
                )
            ),
            textposition="auto",
        )
    )

    # Configurar layout
    fig.update_layout(
        title=chart_title,
        xaxis_title=x_title,
        yaxis_title=percent_label,
        showlegend=False,
    )

    fig.update_traces(
        hovertemplate=generate_hovertemplate(
            percent_label=percent_label, count_label=count_label
        )
    )

    # Aplicar el layout por defecto
    fig = apply_default_layout(fig)

    # Añadir etiquetas en las barras
    add_bar_labels(fig, counts_df, "categoria", "porcentaje")

    return fig
