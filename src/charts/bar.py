import matplotlib.pyplot as plt
from src.config import provincias_map
import numpy as np

from src.data.processing import get_df_of_pct


def create_0_to_10_percentage_bar_chart(
    df, question: str, chart_title: str, x_title: str, tag_map
):
    """
    Generar un grafico de barras de porcentaje en base a un puntaje del 0 al 10
    """
    color_gradiants = [plt.get_cmap("RdBu")(i / 10) for i in range(11)]
    color_gradiants[5] = "lightgray"
    color_gradiants.append("gray")
    count = df[question].value_counts(normalize=True) * 100
    count = count.sort_index(ascending=True)
    count.index = count.index.map(tag_map)
    ax = count.plot(
        kind="bar",
        color=color_gradiants,
        title=chart_title,
        edgecolor="dimgray",
    )
    ax.set_ylabel("Porcentaje (%)")
    ax.set_xlabel(x_title)
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()


def create_provinces_distribution_bar_chart(
    df,
    xlabel: str,
    ylabel: str,
    title: str,
    index0label: str,
    index10label: str,
    question: str,
):
    """
    Crea un gráfico de barras comparando Araba, Bizkaia y Gipuzkoa
    """
    dataframe = get_df_of_pct(df, "lurral", question)
    fig, ax = plt.subplots()
    posiciones = np.arange(len(dataframe.iloc[0]))
    width = 0.2
    indices = list(dataframe.iloc[0].index)
    indices[0] = index0label
    indices[10] = index10label
    indices[11] = "Ns/Nc"
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.bar(
        posiciones - width,
        dataframe.iloc[0],
        width,
        label="Araba",
        color=provincias_map[1]["color"],
    )
    ax.bar(
        posiciones,
        dataframe.iloc[1],
        width,
        label="Bizkaia",
        color=provincias_map[2]["color"],
    )
    ax.bar(
        posiciones + width,
        dataframe.iloc[2],
        width,
        label="Gipuzkoa",
        color=provincias_map[3]["color"],
    )
    ax.set_xticks(posiciones)
    ax.set_xticklabels(indices)
    ax.legend()
    plt.show()


def create_green_red_bar_chart(
    df, question: str, chart_title: str, x_title: str, tag_map
) -> None:
    """
    Generar un grafico de barras de porcentaje en base a un puntaje del 0 al 10
    """
    colores_gradiente = [
        plt.get_cmap("RdYlGn_r")(i / (len(tag_map) - 2))
        for i in range((len(tag_map) - 1))
    ]
    colores_gradiente.append("gray")  # pyright: ignore[]
    count = df[question].value_counts(normalize=True) * 100
    count = count.sort_index(ascending=True)
    count.index = count.index.map(tag_map)
    ax = count.plot(
        kind="bar",
        color=colores_gradiente,
        title=chart_title,
        edgecolor="dimgray",
    )
    ax.set_ylabel("Porcentaje (%)")
    ax.set_xlabel(x_title)
    plt.xticks(rotation=70)
    plt.tight_layout()
    plt.show()
