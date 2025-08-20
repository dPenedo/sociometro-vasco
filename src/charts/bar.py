import matplotlib.pyplot as plt
import pandas as pd
from src.config import ordered_p25_list, p25_question_map, p25_tag_map, provincias_map
import numpy as np

from src.data.processing import get_df_of_pct

plt.style.use("seaborn-v0_8-pastel")
default_fig_size = (10, 6)


def create_0_to_10_percentage_bar_chart(
    df: pd.DataFrame, question: str, chart_title: str, x_title: str, tag_map
):
    """
    Generar un grafico de barras de porcentaje en base a un puntaje del 0 al 10
    """
    color_gradiants = [plt.get_cmap("RdBu")(i / 10) for i in range(11)]
    fig, ax = plt.subplots(figsize=default_fig_size)
    color_gradiants[5] = (  # pyright: ignore[reportCallIssue, reportArgumentType]
        "lightgray"
    )
    color_gradiants.append("gray")  # pyright: ignore[reportArgumentType]
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
    return fig


def create_provinces_distribution_bar_chart(
    df: pd.DataFrame,
    question: str,
    title: str,
    tag_map,
    xlabel: str,
):
    provinces_df = get_df_of_pct(df, "lurral", question)
    fig, ax = plt.subplots(figsize=default_fig_size)
    positions = np.arange(len(provinces_df.iloc[0]))
    width = 0.2
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Porcentaje (%)")
    ax.set_title(title)
    for i, prov_name in enumerate(provincias_map.values()):
        prov = provincias_map[i + 1]
        ax.bar(
            positions + (i - (len(provinces_df) - 1) / 2) * width,
            provinces_df.iloc[i],
            width,
            label=prov["name"],
            color=prov["color"],
        )
    ax.set_xticks(positions)
    ax.set_xticklabels([tag_map.get(k, k) for k in provinces_df.columns])
    ax.legend()
    plt.show()
    return fig


def create_spain_basque_comparation_bar_chart(
    df: pd.DataFrame,
    xlabel: str,
    title: str,
    basque_question: str,
    spain_question: str,
    tag_map,
):
    """
    Crea un gráfico de barras comparando respuestas para España y Euskadi
    """
    fig, ax = plt.subplots(figsize=default_fig_size)
    width = 0.3
    categories = list(tag_map.keys())
    positions = np.arange(len(categories))
    spain_count = df[spain_question].value_counts(normalize=True) * 100
    spain_count = spain_count.reindex(categories, fill_value=0)
    spain_count.index = spain_count.index.map(tag_map)
    ax.bar(
        positions - (width / 2),
        spain_count,
        width,
        label="España",
        color="#F4A261",
        edgecolor="dimgray",
    )
    basque_count = df[basque_question].value_counts(normalize=True) * 100
    basque_count = basque_count.reindex(categories, fill_value=0)
    basque_count.index = basque_count.index.map(tag_map)
    ax.bar(
        positions + (width / 2),
        basque_count,
        width,
        label="Euskadi",
        color="#2A9D8F",
        edgecolor="dimgray",
    )
    ax.set_ylabel("Porcentaje (%)")
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    ax.set_xticks(positions)
    ax.set_xticklabels(list(tag_map.values()))
    plt.xticks(rotation=70)
    plt.tight_layout()
    plt.legend()
    # plt.show()
    plt.draw()
    plt.pause(0.001)
    return fig


def create_green_red_bar_chart(
    df:pd.DataFrame , question: str, chart_title: str, x_title: str, tag_map
):
    """
    Generar un grafico de barras de porcentaje en base a un puntaje del 0 al 10
    """
    fig, ax = plt.subplots(figsize=default_fig_size)
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
    return fig
