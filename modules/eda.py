def get_dataset_overview(df):
    """
    Devolve informação geral sobre o dataset.
    """

    overview = {
        "num_linhas": df.shape[0],
        "num_colunas": df.shape[1],
        "colunas": list(df.columns),
        "colunas_numericas": list(df.select_dtypes(include="number").columns),
        "colunas_categoricas": list(df.select_dtypes(include="object").columns)
    }

    return overview


def get_numeric_statistics(df):
    """
    Devolve estatísticas apenas das colunas numéricas.
    """

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        return None

    return numeric_df.describe()