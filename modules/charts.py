import matplotlib.pyplot as plt
import seaborn as sns


# Estilo global
sns.set_style("whitegrid")


def create_histogram(df, column):
    """
    Cria um histograma para uma coluna numérica.
    """

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.hist(
        df[column].dropna(),
        bins=15,
        edgecolor="black"
    )

    ax.set_title(
        f"Distribution of {column}",
        fontsize=18,
        fontweight="bold"
    )

    ax.set_xlabel(column, fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)

    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()

    return fig


def create_bar_chart(df, column):
    """
    Cria gráfico de barras para coluna categórica.
    """

    counts = df[column].dropna().astype(str).value_counts().head(10)

    fig, ax = plt.subplots(figsize=(10, 5))

    counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title(
        f"Top categories for {column}",
        fontsize=18,
        fontweight="bold"
    )

    ax.set_xlabel(column, fontsize=12)
    ax.set_ylabel("Count", fontsize=12)

    ax.grid(True, axis="y", linestyle="--", alpha=0.5)

    plt.xticks(rotation=45)

    plt.tight_layout()

    return fig


def create_correlation_heatmap(df):
    """
    Cria heatmap de correlação para colunas numéricas.
    """

    numeric_df = df.select_dtypes(include="number")

    correlation_matrix = numeric_df.corr()

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.heatmap(
        correlation_matrix,
        annot=True,
        cmap="coolwarm",
        linewidths=0.5,
        fmt=".2f",
        ax=ax
    )

    ax.set_title(
        "Correlation Heatmap",
        fontsize=18,
        fontweight="bold"
    )

    plt.tight_layout()

    return fig


def create_boxplot(df, column):
    """
    Cria boxplot para coluna numérica.
    """

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.boxplot(
        df[column].dropna(),
        patch_artist=True
    )

    ax.set_title(
        f"Boxplot of {column}",
        fontsize=18,
        fontweight="bold"
    )

    ax.set_ylabel(column, fontsize=12)

    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()

    return fig
