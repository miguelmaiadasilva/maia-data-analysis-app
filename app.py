import streamlit as st
from modules.file_loader import load_file, get_excel_sheets
from modules.eda import get_dataset_overview, get_numeric_statistics
from modules.data_quality import  get_duplicated_rows, generate_data_quality_alerts, create_data_quality_table
from modules.charts import create_histogram, create_bar_chart, create_correlation_heatmap, create_boxplot
from modules.insights import generate_numeric_insight, generate_categorical_insight, generate_executive_summary, generate_correlation_insights, generate_dataset_kpis
from modules.column_intelligence import get_visualization_recommendation, create_column_profile_table
from modules.ui_components import (
    render_empty_state,
    render_executive_summary,
    render_global_styles,
    render_header,
    render_kpi_overview,
    render_sidebar_details,
    render_sidebar_intro,
)

st.set_page_config(
    page_title="M.A.I.A.",
    page_icon="📊",
    layout="wide"
)

render_global_styles()
render_header()
render_sidebar_intro()

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

render_sidebar_details()

# Se o utilizador carregar um ficheiro
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".xlsx"):
            sheet_names = get_excel_sheets(uploaded_file)
            selected_sheet = st.sidebar.selectbox("Select worksheet", sheet_names)
            df = load_file(uploaded_file, sheet_name=selected_sheet)
        else:
            df = load_file(uploaded_file)
        st.sidebar.success("File loaded successfully.")

        overview = get_dataset_overview(df)
        kpis = generate_dataset_kpis(df)

        render_kpi_overview(overview, kpis)

        st.divider()

        executive_summary = generate_executive_summary(df)
        render_executive_summary(executive_summary)

        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📄 Data Preview",
            "📈 Statistics",
            "🧭 Data Quality",
            "🚦 Alerts",
            "📊 Visual Insights",
            "🧠 Column Intelligence"
        ])

        with tab1:
            st.subheader("Data Preview")
            st.caption("First rows of the uploaded dataset for a fast structural check.")
            st.dataframe(df.head(), use_container_width=True)

            st.subheader("Data Types")
            st.caption("Detected column types used by the analysis and chart recommendations.")
            st.dataframe(
                df.dtypes.astype(str).rename("Data type"),
                use_container_width=True
            )
        
        with tab2:
            st.subheader("Numeric Statistics")
            st.caption("Descriptive statistics for numeric columns, including central tendency and spread.")
            numeric_statistics = get_numeric_statistics(df)

            if numeric_statistics is not None:
                st.dataframe(numeric_statistics, use_container_width=True)
            else:
                st.info("No numeric columns are available for statistical profiling.")

        with tab3:
            st.subheader("Data Quality")
            st.caption("Column-level completeness, uniqueness and potential quality issues.")

            quality_table = create_data_quality_table(df)

            st.dataframe(
                quality_table,
                use_container_width=True,
                hide_index=True
            )

            duplicated_info = get_duplicated_rows(df)

            dup_col1, dup_col2 = st.columns(2)

            dup_col1.metric(
                "Rows involved in duplicates",
                duplicated_info['total_linhas_duplicadas']
            )

            dup_col2.metric(
                "Duplicate records found",
                duplicated_info['registos_duplicados']
            )
        
        with tab4:
            st.subheader("Quality Alerts")
            st.caption("Severity-based checks highlighting the most relevant data quality concerns.")

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
                st.success("No relevant data quality issues were detected.")
        with tab5:
            st.subheader("Column Visualization")
            st.caption("Select a column to receive the recommended chart and an automated insight.")

            selected_column = st.selectbox(
                "Select column",
                df.columns
            )

            recommendation = get_visualization_recommendation(df, selected_column)

            st.info(recommendation["reason"])

            if recommendation["can_plot"]:

                if recommendation["chart_type"] == "numeric":

                    st.markdown("#### Distribution")
                    fig = create_histogram(df, selected_column)
                    st.pyplot(fig)

                    st.markdown("#### Outlier View")
                    boxplot_fig = create_boxplot(df, selected_column)
                    st.pyplot(boxplot_fig)

                    st.subheader("Automated Insight")
                    st.info(generate_numeric_insight(df, selected_column))

                elif recommendation["chart_type"] == "categorical":

                    fig = create_bar_chart(df, selected_column)
                    st.pyplot(fig)

                    st.subheader("Automated Insight")
                    st.info(generate_categorical_insight(df, selected_column))

            st.divider()

            st.subheader("Correlation Between Numeric Variables")
            st.caption("Correlation heatmap and plain-language findings for numeric relationships.")

            numeric_columns = df.select_dtypes(include="number").columns

            if len(numeric_columns) >= 2:
                heatmap_fig = create_correlation_heatmap(df)
                st.pyplot(heatmap_fig)

                st.subheader("Correlation Insights")

                correlation_insights = generate_correlation_insights(df)

                for insight in correlation_insights:
                    st.info(insight)

            else:
                st.info("The dataset needs at least 2 numeric columns to calculate correlation.")

        with tab6:
            st.subheader("Column Intelligence")
            st.caption("A practical profile of each column, including analytical role and visualization guidance.")

            profile_table = create_column_profile_table(df)

            st.dataframe(
                profile_table,
                use_container_width=True,
                hide_index=True
            )
                
    except Exception as e:
        st.error(f"Error loading file: {e}")
    
else:
    render_empty_state()
