import pandas as pd

def analyze_column(df, column):
    """
    Analisa características de uma coluna.
    """

    data = df[column]

    analysis = {
        "column_name": column,
        "dtype": str(data.dtype),
        "unique_values": data.nunique(),
        "missing_values": data.isnull().sum(),
        "is_numeric": pd.api.types.is_numeric_dtype(data),
        "is_datetime": pd.api.types.is_datetime64_any_dtype(data),
        "is_constant": False,
        "is_probable_id": False,
        "high_cardinality": False
    }

    # Coluna constante
    if data.nunique() <= 1:
        analysis["is_constant"] = True

    # Alta cardinalidade
    if data.nunique() > 20:
        analysis["high_cardinality"] = True

    # Verificar possível ID
    unique_ratio = data.nunique() / len(data)

    suspicious_id_names = [
        "id",
        "codigo",
        "code",
        "cliente_id",
        "user_id"
    ]

    column_lower = column.lower()

    # Verificar possível ID
    suspicious_id_names = [
        "id",
        "codigo",
        "code",
        "cliente_id",
        "user_id"
    ]

    column_lower = column.lower()

    for keyword in suspicious_id_names:

        if keyword == column_lower or column_lower.endswith(keyword):

            analysis["is_probable_id"] = True
            break

    # Verificar datas apenas para texto
    if data.dtype == "object":

        try:
            pd.to_datetime(data.dropna(), errors="raise")
            analysis["is_datetime"] = True

        except:
            pass

    return analysis

def analyze_dataset_columns(df):
    """
    Analisa todas as colunas do dataset.
    """

    results = []

    for column in df.columns:
        results.append(analyze_column(df, column))

    return results

def get_visualization_recommendation(df, column):
    """
    Decide se uma coluna é adequada para visualização e recomenda o tipo de gráfico.
    """

    analysis = analyze_column(df, column)

    if analysis["is_datetime"]:
        return {
            "can_plot": False,
            "reason": "This column represents dates. Time-based analysis will be added in a future version.",
            "chart_type": None
        }

    if analysis["is_probable_id"]:
        return {
            "can_plot": False,
            "reason": "This column appears to represent unique identifiers and is not suitable for statistical visualization.",
            "chart_type": None
        }

    if analysis["is_constant"]:
        return {
            "can_plot": False,
            "reason": "This column always has the same value, so it does not provide variability for chart analysis.",
            "chart_type": None
        }

    if analysis["high_cardinality"] and not analysis["is_numeric"]:
        return {
            "can_plot": False,
            "reason": "This column has too many categories for a useful bar chart.",
            "chart_type": None
        }

    if analysis["is_numeric"]:
        return {
            "can_plot": True,
            "reason": "Numeric column suitable for a histogram and boxplot.",
            "chart_type": "numeric"
        }

    return {
        "can_plot": True,
        "reason": "Categorical column suitable for a bar chart.",
        "chart_type": "categorical"
    }

def create_column_profile_table(df):
    """
    Cria uma tabela resumo com a análise inteligente das colunas.
    """

    column_analysis = analyze_dataset_columns(df)

    profile_data = []

    for analysis in column_analysis:
        profile_data.append({
            "Column": analysis["column_name"],
            "Type": analysis["dtype"],
            "Unique values": analysis["unique_values"],
            "Missing values": analysis["missing_values"],
            "Numeric": "Yes" if analysis["is_numeric"] else "No",
            "Date": "Yes" if analysis["is_datetime"] else "No",
            "Probable ID": "Yes" if analysis["is_probable_id"] else "No",
            "High cardinality": "Yes" if analysis["high_cardinality"] else "No",
            "Constant": "Yes" if analysis["is_constant"] else "No"
        })

    return pd.DataFrame(profile_data)
