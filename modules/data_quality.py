import pandas as pd

def get_missing_values(df):
    """
    Devolve a quantidade e percentagem de valores em falta por coluna.
    """

    missing_count = df.isnull().sum()
    missing_percentage = (missing_count / len(df)) * 100

    missing_info = {
        "valores_em_falta": missing_count,
        "percentagem_em_falta": missing_percentage
    }

    return missing_info


def get_zero_values(df):
    """
    Devolve a quantidade e percentagem de valores zero por coluna numérica.
    """

    numeric_df = df.select_dtypes(include="number")

    zero_count = (numeric_df == 0).sum()
    zero_percentage = (zero_count / len(df)) * 100

    zero_info = {
        "valores_zero": zero_count,
        "percentagem_zero": zero_percentage
    }

    return zero_info


def get_duplicated_rows(df):
    """
    Devolve informação sobre linhas duplicadas.
    """

    duplicated_mask = df.duplicated(keep=False)
    duplicated_rows = df[duplicated_mask]

    total_duplicated_rows = len(duplicated_rows)
    duplicate_records = df.duplicated().sum()

    return {
        "total_linhas_duplicadas": total_duplicated_rows,
        "registos_duplicados": duplicate_records
    }

def generate_data_quality_alerts(df):
    """
    Gera alertas automáticos com níveis de gravidade.
    """

    alerts = []

    # Valores em falta
    missing_count = df.isnull().sum()
    missing_percentage = (missing_count / len(df)) * 100

    for col in df.columns:
        count = missing_count[col]
        perc = missing_percentage[col]

        if count > 0:
            if perc > 50:
                alerts.append({
                    "level": "critical",
                    "message": f"A coluna '{col}' tem {count} valores em falta ({perc:.2f}%). Situação crítica."
                })
            elif perc > 20:
                alerts.append({
                    "level": "warning",
                    "message": f"A coluna '{col}' tem {count} valores em falta ({perc:.2f}%). Requer atenção."
                })
            else:
                alerts.append({
                    "level": "info",
                    "message": f"A coluna '{col}' tem {count} valores em falta ({perc:.2f}%). Impacto aparentemente baixo."
                })

    # Valores zero
    numeric_df = df.select_dtypes(include="number")
    zero_count = (numeric_df == 0).sum()
    zero_percentage = (zero_count / len(df)) * 100

    for col in numeric_df.columns:
        count = zero_count[col]
        perc = zero_percentage[col]

        if count > 0:
            if perc > 50:
                alerts.append({
                    "level": "critical",
                    "message": f"A coluna '{col}' tem {count} valores iguais a 0 ({perc:.2f}%). Situação crítica."
                })
            elif perc > 20:
                alerts.append({
                    "level": "warning",
                    "message": f"A coluna '{col}' tem {count} valores iguais a 0 ({perc:.2f}%). Requer atenção."
                })
            else:
                alerts.append({
                    "level": "info",
                    "message": f"A coluna '{col}' tem {count} valores iguais a 0 ({perc:.2f}%). Pode ser normal ou requer validação."
                })

    # Duplicados
    duplicated_rows = len(df[df.duplicated(keep=False)])

    if duplicated_rows > 0:
        alerts.append({
            "level": "warning",
            "message": f"Existem {duplicated_rows} linhas envolvidas em duplicados no dataset."
        })

    return alerts

def create_data_quality_table(df):
    """
    Cria uma tabela resumo da qualidade dos dados por coluna.
    """

    missing_count = df.isnull().sum()
    missing_percentage = (missing_count / len(df)) * 100

    numeric_df = df.select_dtypes(include="number")
    zero_count = (numeric_df == 0).sum()
    zero_percentage = (zero_count / len(df)) * 100

    quality_data = []

    for column in df.columns:

        quality_data.append({
            "Coluna": column,
            "Valores em falta": int(missing_count[column]),
            "% em falta": round(missing_percentage[column], 2),
            "Valores zero": int(zero_count[column]) if column in zero_count else 0,
            "% zero": round(zero_percentage[column], 2) if column in zero_percentage else 0
        })

    return pd.DataFrame(quality_data)