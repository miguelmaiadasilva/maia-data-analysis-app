import pandas as pd


def validate_dataframe(df):
    """
    Valida se o DataFrame tem estrutura mínima para análise.
    """

    if df.empty:
        raise ValueError("O ficheiro foi carregado, mas não contém dados.")

    if df.shape[1] == 0:
        raise ValueError("O dataset não contém colunas.")

    if df.shape[1] == 1:
        raise ValueError(
            "O dataset tem apenas uma coluna. Verifica se o separador do CSV está correto."
        )

    if df.shape[0] < 3:
        raise ValueError(
            "O dataset tem muito poucas linhas para uma análise exploratória útil."
        )


def load_csv_with_fallback(uploaded_file):
    """
    Tenta ler um ficheiro CSV usando diferentes encodings.
    """

    encodings = ["utf-8", "latin1", "cp1252"]

    for encoding in encodings:
        try:
            uploaded_file.seek(0)

            return pd.read_csv(
                uploaded_file,
                sep=None,
                engine="python",
                encoding=encoding
            )

        except UnicodeDecodeError:
            continue

    raise ValueError("Não foi possível ler o CSV. Verifica o encoding do ficheiro.")


def get_excel_sheets(uploaded_file):
    """
    Devolve a lista de folhas de um ficheiro Excel.
    """

    uploaded_file.seek(0)
    excel_file = pd.ExcelFile(uploaded_file)

    return excel_file.sheet_names


def load_file(uploaded_file, sheet_name=None):
    """
    Lê um ficheiro CSV ou Excel e devolve um DataFrame.
    """

    if uploaded_file.name.endswith(".csv"):
        df = load_csv_with_fallback(uploaded_file)

    elif uploaded_file.name.endswith(".xlsx"):
        uploaded_file.seek(0)
        df = pd.read_excel(uploaded_file, sheet_name=sheet_name)

    else:
        raise ValueError("Formato de ficheiro não suportado.")

    validate_dataframe(df)

    return df