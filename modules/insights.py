def generate_numeric_insight(df, column):
    """
    Gera um insight simples para uma coluna numérica.
    """

    data = df[column].dropna()

    if data.empty:
        return f"The column '{column}' does not have enough data for analysis."

    mean_value = data.mean()
    median_value = data.median()
    min_value = data.min()
    max_value = data.max()
    outlier_count = detect_outliers(df, column)

    insight = (
        f"The column '{column}' has a mean of {mean_value:.2f} "
        f"and a median of {median_value:.2f}. "
        f"Values range from {min_value:.2f} to {max_value:.2f}."
    )

    if mean_value > median_value:
        insight += " The mean is higher than the median, which may indicate high values pulling the average upward."
    elif mean_value < median_value:
        insight += " The mean is lower than the median, which may indicate low values influencing the distribution."
    else:
        insight += " The mean and median are equal, suggesting a more balanced distribution."
    
    if outlier_count > 0:
        insight += (
        f" {outlier_count} potential outliers were found in this column."
    )

    return insight


def generate_categorical_insight(df, column):
    """
    Gera um insight simples para uma coluna categórica.
    """

    data = df[column].dropna()

    if data.empty:
        return f"The column '{column}' does not have enough data for analysis."

    counts = data.value_counts()
    top_category = counts.index[0]
    top_count = counts.iloc[0]
    total = len(data)
    top_percentage = (top_count / total) * 100
    unique_values = data.nunique()

    insight = (
        f"The column '{column}' has {unique_values} distinct categories. "
        f"The most frequent category is '{top_category}', with {top_count} occurrences, "
        f"representing {top_percentage:.2f}% of valid records."
    )

    if top_percentage > 70:
        insight += " This column is highly concentrated in a single category."
    elif top_percentage > 40:
        insight += " There is some concentration in the leading category."
    else:
        insight += " The distribution appears relatively balanced across categories."

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
        f"The dataset contains {num_rows} records and {num_columns} variables, "
        f"supporting an initial exploratory analysis of the available information."
    )

    # Perfil do dataset
    if len(numeric_columns) > len(categorical_columns):
        summary.append(
            "The dataset is mostly composed of numeric variables, which supports statistical analysis, "
            "distribution review, dispersion analysis and potential outlier detection."
        )
    elif len(categorical_columns) > len(numeric_columns):
        summary.append(
            "The dataset is mostly composed of categorical variables, making it suitable for frequency analysis, "
            "segmentation and comparisons between groups."
        )
    else:
        summary.append(
            "The dataset has a balanced mix of numeric and categorical variables, allowing statistical analysis "
            "to be combined with segment-level analysis."
        )

    # Qualidade geral
    missing_total = df.isnull().sum().sum()
    duplicated_rows = len(df[df.duplicated(keep=False)])

    if missing_total == 0 and duplicated_rows == 0:
        summary.append(
            "Overall data quality appears positive, with no evident missing values or duplicate records."
        )
    else:
        summary.append(
            "Data quality should be validated before final analysis, as potential consistency issues were detected."
        )

    # Potencial analítico
    if len(numeric_columns) > 0 and len(categorical_columns) > 0:
        summary.append(
            "There is potential to cross numeric variables with categories, helping identify patterns by group, location or profile."
        )
    elif len(numeric_columns) > 0:
        summary.append(
            "The dataset primarily supports quantitative analysis, such as descriptive statistics, dispersion and value comparison."
        )
    elif len(categorical_columns) > 0:
        summary.append(
            "The dataset primarily supports qualitative or segmentation analysis based on category frequencies."
        )

    # Próximo passo recomendado
    summary.append(
        "Before drawing final conclusions, missing values, suspicious zeros, duplicates and potential outliers should be validated."
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
        return ["There are not enough numeric columns for correlation analysis."]

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
                                f"A strong positive correlation was found between '{col1}' and '{col2}' ({corr_value:.2f})."
                            )

                        else:
                            insights.append(
                                f"A strong negative correlation was found between '{col1}' and '{col2}' ({corr_value:.2f})."
                            )

                    elif abs_corr >= 0.4:

                        insights.append(
                            f"The variables '{col1}' and '{col2}' show a moderate correlation ({corr_value:.2f})."
                        )

    if not insights:
        insights.append(
            "No strong or moderate correlations were found between the numeric variables."
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
