import pandas as pd
import plotly.colors as pc
import plotly.express as px

from src.config import p25_question_map, p25_tag_map, ordered_p25_list


def create_all_parties_stacked_chart(df: pd.DataFrame):
    all_data = []

    for _, info in p25_question_map.items():
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

    # Colores para niveles 0–10
    numeric_values = [v for v in ordered_p25_list if v != "Ns/Nc"]
    colors = pc.sample_colorscale("RdYlGn", len(numeric_values))
    color_map = {v: colors[i] for i, v in enumerate(numeric_values)}
    color_map["Ns/Nc"] = "grey"

    fig = px.bar(
        plot_df,
        x="porcentaje",
        y="partido",
        color="valor",
        color_discrete_map=color_map,
        orientation="h",
        text=plot_df["porcentaje"].round(1).astype(str) + " %",
        title="Distribución de simpatía por partido",
        labels={"valor": "Puntaje", "porcentaje": "Menor a mayor simpatía"},
    )

    fig.update_layout(
        barmode="stack",
        xaxis=dict(range=[0, 100]),
        legend_title="Nivel de simpatía",
        yaxis=dict(autorange="reversed"),
    )

    return fig


def create_0_to_10_percentage_bar_chart2(
    df: pd.DataFrame, question: str, chart_title: str, x_title: str, tag_map: dict
):
    # Calcular el porcentaje y normalizar los datos
    count = df[question].value_counts(normalize=True) * 100
    count.index = count.index.map(tag_map)
    count = count.sort_index(ascending=True).reset_index()
    count.columns = [x_title, "Porcentaje (%)"]

    # Crear el gráfico con Plotly Express
    fig = px.bar(
        count,
        x=x_title,
        y="Porcentaje (%)",
        title=chart_title,
        labels={"y": "Porcentaje (%)", "x": x_title},
        color=x_title,  # Para colorear cada barra
        color_discrete_sequence=px.colors.diverging.RdBu,
        height=700,
    )
    fig.update_traces(
        marker_line_width=0.5,
        marker_line_color="#232323",
    )
    # max_y = df_plot["Porcentaje (%)"].max()
    # fig.update_yaxes(
    #     range=[0, max_y * 1.1]
    # )  # Multiplicamos por 1.1 para dar un pequeño margen
    fig.update_layout(
        xaxis_tickangle=-45,
        title_font_size=20,  # Tamaño del título principal
        font=dict(
            size=14,  # Tamaño de la fuente para todo el gráfico
        ),
    )

    return fig
