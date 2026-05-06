def generate_numeric_insight(df, column):
    """
    Gera um insight simples para uma coluna numérica.
    """

    data = df[column].dropna()

    if data.empty:
        return f"A coluna '{column}' não tem dados suficientes para análise."

    mean_value = data.mean()
    median_value = data.median()
    min_value = data.min()
    max_value = data.max()
    outlier_count = detect_outliers(df, column)

    insight = (
        f"A coluna '{column}' apresenta uma média de {mean_value:.2f} "
        f"e uma mediana de {median_value:.2f}. "
        f"Os valores variam entre {min_value:.2f} e {max_value:.2f}."
    )

    if mean_value > median_value:
        insight += " A média é superior à mediana, o que pode indicar valores altos a puxar a média para cima."
    elif mean_value < median_value:
        insight += " A média é inferior à mediana, o que pode indicar valores baixos a influenciar a distribuição."
    else:
        insight += " A média e a mediana são iguais, sugerindo uma distribuição mais equilibrada."
    
    if outlier_count > 0:
        insight += (
        f" Foram encontrados {outlier_count} possíveis outliers nesta coluna."
    )

    return insight


def generate_categorical_insight(df, column):
    """
    Gera um insight simples para uma coluna categórica.
    """

    data = df[column].dropna()

    if data.empty:
        return f"A coluna '{column}' não tem dados suficientes para análise."

    counts = data.value_counts()
    top_category = counts.index[0]
    top_count = counts.iloc[0]
    total = len(data)
    top_percentage = (top_count / total) * 100
    unique_values = data.nunique()

    insight = (
        f"A coluna '{column}' tem {unique_values} categorias diferentes. "
        f"A categoria mais frequente é '{top_category}', com {top_count} ocorrências, "
        f"representando {top_percentage:.2f}% dos registos válidos."
    )

    if top_percentage > 70:
        insight += " Esta coluna está muito concentrada numa única categoria."
    elif top_percentage > 40:
        insight += " Existe alguma concentração na categoria principal."
    else:
        insight += " A distribuição parece relativamente mais equilibrada entre categorias."

    return insight

def detect_outliers(df, column):
    """
    Deteta possíveis outliers usando o método IQR.
    """

    data = df[column].dropna()

    if data.empty:
        return 0

    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)

    iqr = q3 - q1

    lower_limit = q1 - 1.5 * iqr
    upper_limit = q3 + 1.5 * iqr

    outliers = data[
        (data < lower_limit) |
        (data > upper_limit)
    ]

    return len(outliers)

def generate_executive_summary(df):
    """
    Gera um resumo executivo interpretativo do dataset.
    """

    summary = []

    num_rows = df.shape[0]
    num_columns = df.shape[1]

    numeric_columns = df.select_dtypes(include="number").columns
    categorical_columns = df.select_dtypes(include="object").columns

    # Visão geral
    summary.append(
        f"O dataset contém {num_rows} registos e {num_columns} variáveis, "
        f"permitindo uma análise exploratória inicial da informação disponível."
    )

    # Perfil do dataset
    if len(numeric_columns) > len(categorical_columns):
        summary.append(
            "O dataset tem predominância de variáveis numéricas, o que favorece análises estatísticas, "
            "distribuições, dispersão e identificação de possíveis outliers."
        )
    elif len(categorical_columns) > len(numeric_columns):
        summary.append(
            "O dataset tem predominância de variáveis categóricas, sendo mais adequado para análises de frequência, "
            "segmentação e comparação entre grupos."
        )
    else:
        summary.append(
            "O dataset apresenta equilíbrio entre variáveis numéricas e categóricas, permitindo combinar análise estatística "
            "com análise de segmentos."
        )

    # Qualidade geral
    missing_total = df.isnull().sum().sum()
    duplicated_rows = len(df[df.duplicated(keep=False)])

    if missing_total == 0 and duplicated_rows == 0:
        summary.append(
            "A qualidade geral dos dados parece positiva, sem valores em falta ou duplicados evidentes."
        )
    else:
        summary.append(
            "A qualidade dos dados requer validação antes de uma análise final, pois foram detetados sinais de possíveis inconsistências."
        )

    # Potencial analítico
    if len(numeric_columns) > 0 and len(categorical_columns) > 0:
        summary.append(
            "Existe potencial para cruzar variáveis numéricas com categorias, permitindo identificar padrões por grupo, localização ou perfil."
        )
    elif len(numeric_columns) > 0:
        summary.append(
            "O dataset permite sobretudo análise quantitativa, como estatísticas descritivas, dispersão e comparação de valores."
        )
    elif len(categorical_columns) > 0:
        summary.append(
            "O dataset permite sobretudo análise qualitativa ou de segmentação, baseada na frequência das categorias."
        )

    # Próximo passo recomendado
    summary.append(
        "Antes de retirar conclusões definitivas, recomenda-se validar valores em falta, zeros suspeitos, duplicados e possíveis outliers."
    )

    return summary

def generate_correlation_insights(df):
    """
    Gera insights automáticos sobre correlações numéricas.
    """

    insights = []

    numeric_df = df.select_dtypes(include="number")

    # Verificar se existem pelo menos 2 colunas numéricas
    if numeric_df.shape[1] < 2:
        return ["Não existem colunas numéricas suficientes para análise de correlação."]

    correlation_matrix = numeric_df.corr()

    processed_pairs = set()

    for col1 in correlation_matrix.columns:
        for col2 in correlation_matrix.columns:

            if col1 != col2:

                pair = tuple(sorted([col1, col2]))

                if pair not in processed_pairs:

                    processed_pairs.add(pair)

                    corr_value = correlation_matrix.loc[col1, col2]

                    abs_corr = abs(corr_value)

                    if abs_corr >= 0.7:

                        if corr_value > 0:
                            insights.append(
                                f"Foi encontrada forte correlação positiva entre '{col1}' e '{col2}' ({corr_value:.2f})."
                            )

                        else:
                            insights.append(
                                f"Foi encontrada forte correlação negativa entre '{col1}' e '{col2}' ({corr_value:.2f})."
                            )

                    elif abs_corr >= 0.4:

                        insights.append(
                            f"As variáveis '{col1}' e '{col2}' apresentam correlação moderada ({corr_value:.2f})."
                        )

    if not insights:
        insights.append(
            "Não foram encontradas correlações fortes ou moderadas entre as variáveis numéricas."
        )

    return insights

def generate_dataset_kpis(df):
    """
    Gera KPIs principais do dataset.
    """

    total_missing = int(df.isnull().sum().sum())

    duplicated_rows = int(
        len(df[df.duplicated(keep=False)])
    )

    numeric_columns = df.select_dtypes(include="number").columns

    outlier_columns = 0

    for column in numeric_columns:

        outlier_count = detect_outliers(df, column)

        if outlier_count > 0:
            outlier_columns += 1

    return {
        "total_missing": total_missing,
        "duplicated_rows": duplicated_rows,
        "outlier_columns": outlier_columns
    }