# %%
import plotly.express as px
from src.config import df, ordered_p25_list, p25_question_map, p25_tag_map
import plotly.colors as pc
import pandas as pd

# %%

# Funcion Calcular porcentajes por etiqueta y reordenar


def create_sympathy_stacked_bar_chart(
    df: pd.DataFrame, question: str, party_name: str, party_color: str | None = None
):
    percent_series: pd.Series = (
        df[question].map(p25_tag_map).value_counts(normalize=True) * 100
    )
    percent_series = percent_series.reindex(ordered_p25_list, fill_value=0)
    plot_df = percent_series.reset_index()
    plot_df.columns = ["valor", "porcentaje"]
    plot_df["categoria"] = "Simpatía por partido"  # una sola barra
    numeric_values = [v for v in ordered_p25_list if v != "Ns/Nc"]
    colors = pc.sample_colorscale("RdYlGn", len(numeric_values))
    color_map = {v: colors[i] for i, v in enumerate(numeric_values)}
    color_map["Ns/Nc"] = "lightgrey"

    # Gráfico apilado en una sola barra
    fig = px.bar(
        plot_df,
        x="porcentaje",
        y="categoria",
        color="valor",
        color_discrete_map=color_map,
        orientation="h",
        text=plot_df["porcentaje"].round(1).astype(str) + " %",
        title=f"Distribución de simpatía de {party_name}",
        labels={"valor": "Puntaje", "porcentaje": "Porcentaje"},
    )

    fig.update_layout(
        barmode="stack",
        xaxis=dict(range=[0, 100]),
        yaxis_title=None,
        legend_title="Simpatía",
        title_font_color=party_color,
    )

    fig.show()


# %%
# Gráfico en barras

for _, name in p25_question_map.items():
    create_sympathy_stacked_bar_chart(df, name["question"], name["name"], name["color"])

# Uso:
fig = create_all_parties_stacked_chart(df)
fig.show()
# %%
#
