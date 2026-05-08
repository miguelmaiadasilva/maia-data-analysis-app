import pandas as pd


def validate_dataframe(df):
    """
    Valida se o DataFrame tem estrutura mínima para análise.
    """

    if df.empty:
        raise ValueError("The file was loaded, but it does not contain any data.")

    if df.shape[1] == 0:
        raise ValueError("The dataset does not contain any columns.")

    if df.shape[1] == 1:
        raise ValueError(
            "The dataset has only one column. Check whether the CSV delimiter is correct."
        )

    if df.shape[0] < 3:
        raise ValueError(
            "The dataset has too few rows for a useful exploratory analysis."
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

    raise ValueError("The CSV could not be read. Check the file encoding.")


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
        raise ValueError("Unsupported file format.")

    validate_dataframe(df)

    return df
