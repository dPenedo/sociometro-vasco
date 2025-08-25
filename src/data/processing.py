import pandas as pd

from src.config.data import metadata


def get_df_of_pct(df: pd.DataFrame, col1: str, col2: str) -> pd.DataFrame:
    """
    Calcula la distribución porcentual de una variable respecto a otra y lo devuelve en otro DataFrame.
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
