import pandas as pd
from typing import Dict, Any
from src.translate import (
    get_sex_map,
    get_basque_level_grouped,
    get_basque_level_order,
    get_education_grouped,
    get_education_order,
    get_social_class_map,
    get_social_class_order,
    get_translations,
)


def get_df_of_pct(df: pd.DataFrame, col1: str, col2: str) -> pd.DataFrame:
    return (
        df.groupby([col1, col2])
        .size()
        .groupby(level=0)
        .apply(lambda x: 100 * x / x.sum())
        .unstack(fill_value=0)
    )


def get_pct_series(df: pd.DataFrame, col: str) -> pd.DataFrame:
    return (
        df[col]
        .value_counts(normalize=True)
        .mul(100)
        .rename_axis("values")
        .reset_index(name="percentage")
    )


def get_counts_and_percents(
    series: pd.Series, ordered_categories: list = None, label_col: str = "value"
) -> pd.DataFrame:
    counts = (
        series.value_counts().reindex(ordered_categories, fill_value=0)
        if ordered_categories
        else series.value_counts()
    )
    percents = counts / counts.sum() * 100
    return pd.DataFrame(
        {
            label_col: counts.index,
            "count": counts.values,
            "percentage": percents.values,
        }
    )


def build_long_df(
    df: pd.DataFrame, group_col: str, value_col: str, ordered_categories: list = None
) -> pd.DataFrame:
    all_data = []
    for entity, s in df.groupby(group_col):
        df_counts = get_counts_and_percents(s[value_col], ordered_categories)
        df_counts[group_col] = entity
        all_data.append(df_counts)
    return pd.concat(all_data, ignore_index=True)


def get_processed_dataframe_for_streamlit(df: pd.DataFrame) -> pd.DataFrame:
    df_processed = df.copy()

    sex_map = get_sex_map()
    basque_level_grouped = get_basque_level_grouped()
    basque_level_order = get_basque_level_order()
    education_grouped = get_education_grouped()
    education_order = get_education_order()
    social_class_map = get_social_class_map()
    social_class_order = get_social_class_order()

    df_processed["basque_level"] = df_processed["basque_level"].map(basque_level_grouped)
    df_processed["education"] = df_processed["education"].map(education_grouped)
    df_processed["social_class"] = df_processed["social_class"].map(social_class_map)
    df_processed["sex"] = df_processed["P01"].map(sex_map)

    df_processed["basque_level"] = pd.Categorical(
        df_processed["basque_level"], categories=basque_level_order, ordered=True
    )
    df_processed["education"] = pd.Categorical(
        df_processed["education"], categories=education_order, ordered=True
    )
    df_processed["social_class"] = pd.Categorical(
        df_processed["social_class"], categories=social_class_order, ordered=True
    )

    return df_processed


def get_filter_options(df: pd.DataFrame) -> Dict[str, Any]:
    required_columns = ["basque_level", "P02", "education", "social_class", "sex"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Column {col} not found in DataFrame")

    return {
        "basque_level_options": sorted(df["basque_level"].dropna().unique().tolist()),
        "age_range": (int(df["P02"].min()), int(df["P02"].max())),
        "education_options": sorted(df["education"].dropna().unique().tolist()),
        "social_class_options": sorted(df["social_class"].dropna().unique().tolist()),
        "sex_options": sorted(df["sex"].dropna().unique().tolist()),
    }


def apply_filters(df: pd.DataFrame, filter_values: Dict[str, Any]) -> pd.DataFrame:
    df_filtered = df.copy()

    if filter_values["sex"] != get_translations()["filter_all"]:
        df_filtered = df_filtered[df_filtered["sex"] == filter_values["sex"]]

    df_filtered = df_filtered[
        (df_filtered["P02"] >= filter_values["age_min"])
        & (df_filtered["P02"] <= filter_values["age_max"])
    ]

    if filter_values["basque_level"]:
        df_filtered = df_filtered[
            df_filtered["basque_level"].isin(filter_values["basque_level"])
        ]
    if filter_values["education"]:
        df_filtered = df_filtered[
            df_filtered["education"].isin(filter_values["education"])
        ]
    if filter_values["social_class"]:
        df_filtered = df_filtered[
            df_filtered["social_class"].isin(filter_values["social_class"])
        ]

    return df_filtered
