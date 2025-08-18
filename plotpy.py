# %%
import plotly.express as px
from src.config import df, ordered_p25_list, p25_question_map, p25_tag_map
import plotly.colors as pc
import pandas as pd

# %%
# df


def create_0_to_10_percentage_bar_chart(
    df, question: str, chart_title: str, x_title: str, tag_map
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
    return figf


# # Uso:
# fig = create_all_parties_stacked_chart(df)
# fig.show()
# %%
#
