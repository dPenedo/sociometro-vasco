import pandas as pd
from typing import Dict, Any

from src.config.data import metadata


def get_df_of_pct(df: pd.DataFrame, col1: str, col2: str) -> pd.DataFrame:
    """
    Calcula la distribución porcentual de una variable respecto a otra y
    lo devuelve en otro DataFrame.
    """
    return (
        df.groupby([col1, col2])
        .size()
        .groupby(level=0)
        .apply(lambda x: 100 * x / x.sum())
        .unstack(fill_value=0)
    )


def get_pct_series(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Devuelve un DataFrame con la distribución porcentual de una sola columna.
    """
    return (
        df[col]
        .value_counts(normalize=True)
        .mul(100)
        .rename_axis("valores")
        .reset_index(name="porcentaje")
    )


def get_counts_and_percents(
    series: pd.Series, ordered_categories: list = None, label_col: str = "valor"
) -> pd.DataFrame:
    """
    Devuelve un DataFrame largo con conteo y porcentaje de cada valor.
    """
    counts = (
        series.value_counts().reindex(ordered_categories, fill_value=0)
        if ordered_categories
        else series.value_counts()
    )
    percents = counts / counts.sum() * 100
    df = pd.DataFrame(
        {
            label_col: counts.index,
            "conteo": counts.values,
            "porcentaje": percents.values,
        }
    )
    return df


def build_long_df(
    df: pd.DataFrame, group_col: str, value_col: str, ordered_categories: list = None
) -> pd.DataFrame:
    """
    Convierte df en formato largo para gráficas.
    Devuelve columnas: grupo (entidad), valor, conteo, porcentaje
    """
    all_data = []
    for entidad, s in df.groupby(group_col):
        df_counts = get_counts_and_percents(s[value_col], ordered_categories)
        df_counts[group_col] = entidad
        all_data.append(df_counts)
    long_df = pd.concat(all_data, ignore_index=True)
    return long_df


def get_count(df: pd.DataFrame, question: str, title: str):
    """
    Obtener el conteo de una pregunta
    """
    question_map = metadata["preguntas"][question]["opciones"]
    question_index_int = {int(k): v for k, v in question_map.items()}
    count = df[question.lower()].value_counts()
    count.index = count.index.map(question_index_int)
    count.name = title
    return count


def get_question_text(question: str):
    """
    Obtener el texto de una pregunta
    """
    return metadata["preguntas"][question]["texto"]


def get_processed_dataframe_for_streamlit(
    df: pd.DataFrame,
    p36_grouped: Dict[Any, Any],
    p36_order: list,
    p37_grouped: Dict[Any, Any],
    p37_order: list,
    p38_map: Dict[Any, Any],
    p38_order: list,
    sexo_map: Dict[Any, Any],
) -> pd.DataFrame:
    """
    Procesa el DataFrame aplicando todas las transformaciones necesarias
    """
    df_processed = df.copy()

    # Aplicar mapeos
    df_processed["nivel_de_euskera"] = df_processed["p36"].map(p36_grouped)
    df_processed["estudios"] = df_processed["p37"].map(p37_grouped)
    df_processed["clase"] = df_processed["p38"].map(p38_map)
    df_processed["sexo"] = df_processed["P01"].map(sexo_map)

    df_processed["nivel_de_euskera"] = pd.Categorical(
        df_processed["nivel_de_euskera"], categories=p36_order, ordered=True
    )
    # Reordenar
    df_processed["estudios"] = pd.Categorical(
        df_processed["estudios"], categories=p37_order, ordered=True
    )
    df_processed["clase"] = pd.Categorical(
        df_processed["clase"], categories=p38_order, ordered=True
    )

    return df_processed


def get_filter_options(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Obtiene las opciones disponibles para los filtros a partir del
    DataFrame procesado

    Args:
        df: DataFrame ya procesado con las columnas mapeadas

    Returns:
        Diccionario con todas las opciones disponibles para los filtros
    """
    # Asegurarse de que las columnas existen
    required_columns = ["nivel_de_euskera", "P02", "estudios", "clase", "sexo"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"La columna {col} no existe en el DataFrame")

    # Obtener opciones únicas, excluyendo NaN y ordenando
    euskera_options = sorted(df["nivel_de_euskera"].dropna().unique().tolist())
    estudios_options = sorted(df["estudios"].dropna().unique().tolist())
    clase_options = sorted(df["clase"].dropna().unique().tolist())
    sexo_options = sorted(df["sexo"].dropna().unique().tolist())

    # Obtener rango de edad (convertir a int para el slider)
    edad_min = int(df["P02"].min())
    edad_max = int(df["P02"].max())

    return {
        "euskera_options": euskera_options,
        "edad_range": (edad_min, edad_max),
        "estudios_options": estudios_options,
        "clase_options": clase_options,
        "sexo_options": sexo_options,
    }


def apply_filters(df: pd.DataFrame, filter_values: Dict[str, Any]) -> pd.DataFrame:
    """
    Aplica los filtros al DataFrame según los valores seleccionados

    Args:
        df: DataFrame procesado
        filter_values: Diccionario con los valores de filtro del sidebar

    Returns:
        DataFrame filtrado
    """
    df_filtered = df.copy()
    print("df_filtered =>---------------------------------- ", len(df_filtered))

    if filter_values["sexo"] != "Todos":
        print("filter_sexo => ", filter_values["sexo"])
        df_filtered = df_filtered[df_filtered["sexo"] == filter_values["sexo"]]

    print("df_filtered pre edad => ", len(df_filtered))
    df_filtered = df_filtered[
        (df_filtered["P02"] >= filter_values["edad_min"])
        & (df_filtered["P02"] <= filter_values["edad_max"])
    ]
    print("df_filtered post edad => ", len(df_filtered))

    if filter_values["euskera"]:
        df_filtered = df_filtered[
            df_filtered["nivel_de_euskera"].isin(filter_values["euskera"])
        ]
        print("filter_values['euskera']", filter_values["euskera"])
        print("df_filtered  eusk=> ", len(df_filtered))
    if filter_values["estudios"]:
        print("filter_estudios => ", filter_values["estudios"])
        df_filtered = df_filtered[
            df_filtered["estudios"].isin(filter_values["estudios"])
        ]
        print("df_filtered  est=> ", len(df_filtered))
    if filter_values["clase"]:
        print("filter_clase => ", filter_values["clase"])
        df_filtered = df_filtered[df_filtered["clase"].isin(filter_values["clase"])]
        print("df_filtered  clase=> ", len(df_filtered))

    return df_filtered
