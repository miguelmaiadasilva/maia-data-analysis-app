from html import escape

import streamlit as st


def render_global_styles():
    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 2rem;
                padding-bottom: 3rem;
                max-width: 1280px;
            }

            [data-testid="stSidebar"] {
                background: #f8fafc;
                border-right: 1px solid #e5e7eb;
            }

            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3 {
                color: #111827;
            }

            .maia-hero {
                padding: 2rem 2.25rem;
                border: 1px solid #e5e7eb;
                border-radius: 10px;
                background: linear-gradient(135deg, #ffffff 0%, #f8fafc 58%, #edf6ff 100%);
                margin-bottom: 1.4rem;
            }

            .maia-eyebrow {
                margin-bottom: .45rem;
                color: #2563eb;
                font-size: .82rem;
                font-weight: 700;
                letter-spacing: .08em;
                text-transform: uppercase;
            }

            .maia-hero h1 {
                color: #0f172a;
                font-size: 2.25rem;
                line-height: 1.15;
                margin: 0 0 .55rem 0;
            }

            .maia-hero p {
                color: #475569;
                max-width: 760px;
                font-size: 1.02rem;
                line-height: 1.65;
                margin: 0;
            }

            .section-kicker {
                color: #64748b;
                font-size: .92rem;
                margin-top: -.35rem;
                margin-bottom: 1rem;
            }

            .summary-card {
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                background: #ffffff;
                padding: 1rem 1.05rem;
                margin-bottom: .75rem;
                color: #334155;
                line-height: 1.55;
                box-shadow: 0 1px 2px rgba(15, 23, 42, .04);
            }

            .empty-panel {
                border: 1px dashed #cbd5e1;
                border-radius: 10px;
                background: #f8fafc;
                padding: 2rem;
                margin-top: 1.25rem;
            }

            .empty-panel h2 {
                color: #0f172a;
                margin-top: 0;
            }

            .empty-panel p {
                color: #475569;
                line-height: 1.6;
            }

            .stMetric {
                background: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: .85rem 1rem;
                box-shadow: 0 1px 2px rgba(15, 23, 42, .04);
            }

            div[data-testid="stTabs"] button {
                font-weight: 600;
            }
        </style>
        """,
        unsafe_allow_html=True
    )


def render_header():
    st.markdown(
        """
        <div class="maia-hero">
            <div class="maia-eyebrow">Data Analyst Portfolio Project</div>
            <h1>M.A.I.A. — Miguel Artificial Intelligence Analyst</h1>
            <p>
                Automated exploratory data analysis for CSV and Excel datasets, with
                a business-focused view of data quality, KPIs, visual patterns and
                plain-language insights.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_sidebar_intro():
    st.sidebar.title("M.A.I.A.")
    st.sidebar.caption("Miguel Artificial Intelligence Analyst")
    st.sidebar.markdown(
        "Upload a dataset to generate a structured EDA report with KPIs, quality checks, "
        "charts and column-level recommendations."
    )
    st.sidebar.divider()


def render_sidebar_details():
    st.sidebar.divider()
    st.sidebar.markdown("### Supported formats")
    st.sidebar.markdown("- CSV\n- Excel (.xlsx)")
    st.sidebar.markdown("### Analysis sections")
    st.sidebar.markdown(
        "- Executive summary\n"
        "- Dataset KPIs\n"
        "- Statistics and preview\n"
        "- Data quality alerts\n"
        "- Visualizations and insights"
    )


def render_section_caption(text):
    st.markdown(
        f'<div class="section-kicker">{escape(str(text))}</div>',
        unsafe_allow_html=True
    )


def render_kpi_overview(overview, kpis):
    st.subheader("Dataset Overview")
    render_section_caption(
        "A quick dashboard view of dataset size, completeness and structural risk."
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Rows", overview["num_linhas"])
    col2.metric("Columns", overview["num_colunas"])
    col3.metric("Missing values", kpis["total_missing"])
    col4.metric("Duplicate rows", kpis["duplicated_rows"])
    col5.metric("Outlier columns", kpis["outlier_columns"])


def render_executive_summary(executive_summary):
    st.subheader("Executive Summary")
    render_section_caption(
        "Business-readable highlights generated from the uploaded dataset."
    )

    for item in executive_summary:
        st.markdown(
            f'<div class="summary-card">{escape(str(item))}</div>',
            unsafe_allow_html=True
        )


def render_empty_state():
    st.markdown(
        """
        <div class="empty-panel">
            <h2>Upload a dataset to start the analysis</h2>
            <p>
                Use the sidebar to add a CSV or Excel file. M.A.I.A. will turn it
                into a compact analyst-style report with data quality checks,
                KPIs, statistics, visualizations and automated insights.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    empty_col1, empty_col2, empty_col3 = st.columns(3)

    with empty_col1:
        st.markdown("#### 1. Inspect")
        st.write("Preview the data, column types and numeric statistics.")

    with empty_col2:
        st.markdown("#### 2. Diagnose")
        st.write("Identify missing values, duplicates, outliers and alerts.")

    with empty_col3:
        st.markdown("#### 3. Communicate")
        st.write("Generate charts, correlations and plain-language insights.")
