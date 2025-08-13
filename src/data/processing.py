import pandas as pd

from src.config import metadata


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
