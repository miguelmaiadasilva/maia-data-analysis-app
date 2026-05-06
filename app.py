import streamlit as st
import pandas as pd
from modules.file_loader import load_file, get_excel_sheets
from modules.eda import get_dataset_overview, get_numeric_statistics
from modules.data_quality import  get_duplicated_rows, generate_data_quality_alerts, create_data_quality_table
from modules.charts import create_histogram, create_bar_chart, create_correlation_heatmap, create_boxplot
from modules.insights import generate_numeric_insight, generate_categorical_insight, generate_executive_summary, generate_correlation_insights, generate_dataset_kpis
from modules.column_intelligence import get_visualization_recommendation, create_column_profile_table

st.set_page_config(
    page_title="M.A.I.A.",
    page_icon="📊",
    layout="wide"
)

st.title("M.A.I.A. — Miguel Artificial Intelligence Analyst")
st.markdown(
    "Ferramenta de análise exploratória automática para datasets CSV e Excel, "
    "com foco em qualidade dos dados, visualizações e insights em linguagem natural."
)

st.sidebar.title("M.A.I.A.")
st.sidebar.caption("Miguel Artificial Intelligence Analyst")
st.sidebar.write("Carrega um ficheiro CSV ou Excel para iniciar a análise.")

uploaded_file = st.sidebar.file_uploader(
    "Escolhe um ficheiro CSV ou Excel",
    type=["csv", "xlsx"]
)

st.sidebar.divider()
st.sidebar.markdown("### Formatos suportados")
st.sidebar.write("CSV")
st.sidebar.write("Excel (.xlsx)")

# Se o utilizador carregar um ficheiro
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".xlsx"):
            sheet_names = get_excel_sheets(uploaded_file)
            selected_sheet = st.sidebar.selectbox("Escolhe uma folha", sheet_names)
            df = load_file(uploaded_file, sheet_name=selected_sheet)
        else:
            df = load_file(uploaded_file)
        st.success("Ficheiro carregado com sucesso!")

        overview = get_dataset_overview(df)
        st.subheader("Resumo geral")

        kpis = generate_dataset_kpis(df)

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("Linhas", overview["num_linhas"])

        col2.metric("Colunas", overview["num_colunas"])

        col3.metric(
            "Valores em falta",
            kpis["total_missing"]
        )

        col4.metric(
            "Duplicados",
            kpis["duplicated_rows"]
        )

        col5.metric(
            "Colunas com outliers",
            kpis["outlier_columns"]
        )

        st.subheader("Resumo executivo")

        executive_summary = generate_executive_summary(df)

        for item in executive_summary:
            st.info(item)

        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Pré-visualização",
        "Estatísticas",
        "Qualidade dos dados",
        "Alertas",
        "Gráficos e insights",
        "Inteligência das colunas"
    ])
        with tab1:
            st.subheader("Pré-visualização dos dados")
            st.dataframe(df.head())

            st.subheader("Tipos de dados")
            st.write(df.dtypes)
        
        with tab2:
            st.subheader("Estatísticas numéricas")
            numeric_statistics = get_numeric_statistics(df)

            if numeric_statistics is not None:
                st.dataframe(numeric_statistics)
            else:
                st.info("Não existem colunas numéricas para apresentar estatísticas.")

        with tab3:
                st.subheader("Qualidade dos dados")

                quality_table = create_data_quality_table(df)

                st.dataframe(
                    quality_table,
                    use_container_width=True,
                    hide_index=True
                )

                duplicated_info = get_duplicated_rows(df)

                st.write(
                    f"Linhas envolvidas em duplicados: "
                    f"{duplicated_info['total_linhas_duplicadas']}"
                )

                st.write(
                    f"Registos duplicados encontrados: "
                    f"{duplicated_info['registos_duplicados']}"
                )
        
        with tab4:
            st.subheader("Alertas")

            alerts = generate_data_quality_alerts(df)

            if alerts:
                for alert in alerts:

                    if alert["level"] == "critical":
                        st.error(alert["message"])

                    elif alert["level"] == "warning":
                        st.warning(alert["message"])

                    else:
                        st.info(alert["message"])

            else:
                st.success("Não foram detetados problemas relevantes na qualidade dos dados.")
        with tab5:
            st.subheader("Visualização por coluna")

            selected_column = st.selectbox(
                "Escolhe uma coluna para visualizar",
                df.columns
            )

            recommendation = get_visualization_recommendation(df, selected_column)

            st.info(recommendation["reason"])

            if recommendation["can_plot"]:

                if recommendation["chart_type"] == "numeric":

                    st.write("Histograma")
                    fig = create_histogram(df, selected_column)
                    st.pyplot(fig)

                    st.write("Boxplot")
                    boxplot_fig = create_boxplot(df, selected_column)
                    st.pyplot(boxplot_fig)

                    st.subheader("Insight automático")
                    st.info(generate_numeric_insight(df, selected_column))

                elif recommendation["chart_type"] == "categorical":

                    fig = create_bar_chart(df, selected_column)
                    st.pyplot(fig)

                    st.subheader("Insight automático")
                    st.info(generate_categorical_insight(df, selected_column))

            st.divider()

            st.subheader("Correlação entre variáveis numéricas")

            numeric_columns = df.select_dtypes(include="number").columns

            if len(numeric_columns) >= 2:
                heatmap_fig = create_correlation_heatmap(df)
                st.pyplot(heatmap_fig)

                st.subheader("Insights de correlação")

                correlation_insights = generate_correlation_insights(df)

                for insight in correlation_insights:
                    st.info(insight)

            else:
                st.info("O dataset precisa de pelo menos 2 colunas numéricas para calcular correlação.")

        with tab6:

                st.subheader("Inteligência das colunas")

                profile_table = create_column_profile_table(df)

                st.dataframe(
                    profile_table,
                    use_container_width=True,
                    hide_index=True
                )
                
    except Exception as e:
        st.error(f"Erro ao carregar ficheiro: {e}")
    
else:
    st.info("Carrega um ficheiro CSV ou Excel na barra lateral para iniciar a análise.")

    st.markdown("""
    ### O que o M.A.I.A. faz

    - Analisa automaticamente datasets CSV e Excel
    - Deteta valores em falta, zeros, duplicados e possíveis outliers
    - Gera estatísticas, gráficos e insights automáticos
    - Avalia a qualidade dos dados
    - Recomenda visualizações adequadas para cada coluna
    """)