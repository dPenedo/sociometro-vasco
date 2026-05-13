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
from src.processing.processing import get_counts_and_percents


def generate_all_parties_stacked_chart(
    df: pd.DataFrame, chart_title: str, percent_label: str, count_label: str
) -> go.Figure:
    all_data = []
    ordered_categories = [str(v) for v in p25_tag_map.values()]

    for _, info in parties_map_and_colors_p25.items():
        counts_df: pd.DataFrame = get_counts_and_percents(
            df[info["question"]].map(p25_tag_map),
            ordered_categories,
            label_col="value",
        )

        for _, row in counts_df.iterrows():
            all_data.append(
                {
                    "party": info["name"],
                    "value": row["value"],
                    "count": row["count"],
                    "percentage": row["percentage"],
                    "party_color": info["color"],
                }
            )

    plot_df = pd.DataFrame(all_data)

    color_map = get_color_map_from_scale(ordered_categories)
    ordered_parties = [info["name"] for info in parties_map_and_colors_p25.values()]

    fig: go.Figure = px.bar(
        plot_df,
        x="percentage",
        y="party",
        title=chart_title,
        color="value",
        color_discrete_map=color_map,
        orientation="h",
        text=plot_df["percentage"].round(1).astype(str) + " %",
        labels={
            "value": "",
            "percentage": percent_label,
            "party": "Partido",
        },
        category_orders={"party": ordered_parties},
        custom_data=["value", "count", "percentage"],
    )
    fig.update_traces(
        hovertemplate=generate_hovertemplate(
            percent_label=percent_label, count_label=count_label
        )
    )

    fig.update_yaxes(title_text="", automargin=True)
    fig = apply_default_layout(fig)

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.15,
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
        df[question], ordered_categories=ALL_CATEGORIES, label_col="values"
    )

    counts_df["values_str"] = counts_df["values"].astype(str)
    counts_df["label"] = counts_df["values"].map(tag_map)

    category_order = [str(i) for i in ALL_CATEGORIES]

    fig: go.Figure = px.bar(
        data_frame=counts_df,
        x="values_str",
        y="percentage",
        color="values_str",
        title=chart_title,
        color_discrete_sequence=red_blue_color_list,
        category_orders={"values_str": category_order},
        labels={"label": "Orientación", "percentage": percent_label},
        custom_data=["label", "count", "percentage"],
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

    add_bar_labels(fig, counts_df, "values_str", "percentage")
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
    data = []

    for territory in df["territory"].unique():
        territory_df = df[df["territory"] == territory]

        counts_df = get_counts_and_percents(
            territory_df[question],
            ordered_categories=list(tag_map.keys()),
            label_col="response",
        )

        for _, row in counts_df.iterrows():
            data.append(
                {
                    "territory": territory,
                    "response": row["response"],
                    "percentage": row["percentage"],
                    "count": row["count"],
                }
            )

    provinces_df_long = pd.DataFrame(data)

    provinces_df_long["territory_name"] = provinces_df_long["territory"].map(
        lambda x: provincias_map[x]["name"]
    )
    provinces_df_long["response_label"] = provinces_df_long["response"].map(tag_map)

    color_map = {prov["name"]: prov["color"] for prov in provincias_map.values()}

    ordered_labels = [tag_map[i] for i in sorted(tag_map.keys())]
    category_order = [str(i) for i in sorted(tag_map.keys())]

    fig = px.bar(
        provinces_df_long,
        x="response",
        y="percentage",
        color="territory_name",
        barmode="group",
        title=title,
        labels={"percentage": percent_label},
        color_discrete_map=color_map,
        category_orders={"response": category_order},
        custom_data=["response_label", "count", "percentage", "territory_name"],
        hover_data={
            "response_label": True,
            "response": False,
            "percentage": ":.1f",
            "territory_name": True,
            "territory": False,
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
            orientation="h",
            yanchor="top",
            y=-0.2,
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
    categories = list(tag_map.keys())

    spain_df = get_counts_and_percents(
        df[spain_question],
        ordered_categories=categories,
        label_col="raw_category",
    )
    spain_df["region"] = "España"
    spain_df["category"] = spain_df["raw_category"].map(tag_map)

    basque_df = get_counts_and_percents(
        df[basque_question],
        ordered_categories=categories,
        label_col="raw_category",
    )
    basque_df["region"] = "Euskadi"
    basque_df["category"] = basque_df["raw_category"].map(tag_map)

    plot_df = pd.concat([spain_df, basque_df], ignore_index=True)

    fig = go.Figure()

    spain_data = plot_df[plot_df["region"] == "España"]
    fig.add_trace(
        go.Bar(
            x=spain_data["category"],
            y=spain_data["percentage"],
            name="España",
            marker_color="#F4A261",
            width=0.4,
            offset=-0.2,
            customdata=np.column_stack(
                (
                    spain_data["count"],
                    spain_data["raw_category"],
                    spain_data["percentage"],
                )
            ),
        )
    )

    basque_data = plot_df[plot_df["region"] == "Euskadi"]
    fig.add_trace(
        go.Bar(
            x=basque_data["category"],
            y=basque_data["percentage"],
            name="Euskadi",
            marker_color="#2A9D8F",
            width=0.4,
            offset=0.2,
            customdata=np.column_stack(
                (
                    basque_data["count"],
                    basque_data["raw_category"],
                    basque_data["percentage"],
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
    categories = sorted(tag_map.keys())

    counts_df = get_counts_and_percents(
        df[question], ordered_categories=categories, label_col="raw_value"
    )

    counts_df["category"] = counts_df["raw_value"].map(tag_map)

    gradient_colors = []

    for category in categories:
        if "NS/NC" in tag_map[category] or "ns-nc" in tag_map[category].lower():
            gradient_colors.insert(0, "gray")
        else:
            effective_categories = [
                cat
                for cat in categories
                if "NS/NC" not in tag_map[cat] and "ns-nc" not in tag_map[cat].lower()
            ]
            if effective_categories:
                pos = (
                    effective_categories.index(category) / (len(effective_categories) - 1)
                    if len(effective_categories) > 1
                    else 0.5
                )
                gradient_colors.append(
                    px.colors.sample_colorscale(red_green_color_list, pos)[0]
                )
            else:
                gradient_colors.append(
                    px.colors.sample_colorscale(red_green_color_list, 0.5)[0]
                )

    gradient_colors.reverse()

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=counts_df["category"],
            y=counts_df["percentage"],
            marker_color=gradient_colors,
            customdata=np.column_stack(
                (
                    counts_df["category"],
                    counts_df["count"],
                    counts_df["percentage"],
                )
            ),
            textposition="auto",
        )
    )

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

    fig = apply_default_layout(fig)
    add_bar_labels(fig, counts_df, "category", "percentage")

    return fig
