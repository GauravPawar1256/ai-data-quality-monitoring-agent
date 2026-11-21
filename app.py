
import streamlit as st
from pathlib import Path


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Data Quality Monitoring Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# 2. LOAD CUSTOM CSS
# ==========================================

def load_css():

    css_file = Path(__file__).parent / "assets" / "style.css"

    if css_file.exists():

        with open(css_file, "r", encoding="utf-8") as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )

    else:
        st.warning("CSS file not found: assets/style.css")


load_css()


# ==========================================
# 3. DEFINE APPLICATION PAGES
# ==========================================

dashboard = st.Page(
    "pages/1_Dashboard.py",
    title="Dashboard",
    icon="📊",
    default=True
)

upload = st.Page(
    "pages/2_Upload_Dataset.py",
    title="Upload Dataset",
    icon="📁"
)

profiling = st.Page(
    "pages/3_Data_Profiling.py",
    title="Data Profiling",
    icon="📈"
)

quality = st.Page(
    "pages/4_Quality_Checks.py",
    title="Quality Checks",
    icon="🔍"
)

ai = st.Page(
    "pages/5_AI_Recommendations.py",
    title="AI Recommendations",
    icon="🤖"
)

history = st.Page(
    "pages/6_History_Analytics.py",
    title="History Analytics",
    icon="📚"
)


# ==========================================
# 4. CREATE HIDDEN NAVIGATION
# ==========================================

navigation = st.navigation(
    [
        dashboard,
        upload,
        profiling,
        quality,
        ai,
        history
    ],
    position="hidden"
)



# ==========================================
# 5. SIDEBAR HEADER
# ==========================================

def sidebar_header():

    with st.sidebar:

        st.html("""
            <div style="
                text-align: center;
                padding: 20px 8px;
                background: transparent;
            ">

                <div style="
                    width: 60px;
                    height: 60px;
                    margin: 0 auto 12px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border-radius: 16px;
                    background: linear-gradient(135deg, #2563eb, #7c3aed);
                    font-size: 32px;
                    box-shadow: 0 5px 15px rgba(37, 99, 235, 0.3);
                ">
                    🛡️
                </div>

                <h2 style="
                    color: #ffffff;
                    font-size: 23px;
                    font-weight: 700;
                    margin: 5px 0;
                ">
                    DataGuard AI
                </h2>

                <p style="
                    color: #a9bad4;
                    font-size: 12px;
                    margin: 5px 0;
                ">
                    Data Quality Monitoring Agent
                </p>

                <div style="
                    display: inline-flex;
                    align-items: center;
                    gap: 8px;
                    margin-top: 15px;
                    padding: 8px 12px;
                    border-radius: 20px;
                    background: rgba(34, 197, 94, 0.10);
                    border: 1px solid rgba(74, 222, 128, 0.25);
                    color: #86efac;
                    font-size: 11px;
                    font-weight: 600;
                ">
                    <span style="
                        width: 8px;
                        height: 8px;
                        border-radius: 50%;
                        background: #22c55e;
                    "></span>
                    Intelligent Monitoring
                </div>

            </div>

            <hr style="
                border: none;
                height: 1px;
                background: rgba(169, 186, 212, 0.2);
                margin: 12px 0 18px;
            ">

            <p style="
                color: #a9bad4;
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1.5px;
                margin: 0 0 12px 5px;
            ">
                APPLICATION MENU
            </p>
        """)

# ==========================================
# 6. CUSTOM SIDEBAR NAVIGATION
# ==========================================

def sidebar_navigation():

    with st.sidebar:

        st.page_link(
            dashboard,
            label="Dashboard",
            icon="📊"
        )

        st.page_link(
            upload,
            label="Upload Dataset",
            icon="📁"
        )

        st.page_link(
            profiling,
            label="Data Profiling",
            icon="📈"
        )

        st.page_link(
            quality,
            label="Quality Checks",
            icon="🔍"
        )

        st.page_link(
            ai,
            label="AI Recommendations",
            icon="🤖"
        )

        st.page_link(
            history,
            label="History Analytics",
            icon="📚"
        )


# ==========================================
# 7. DISPLAY SIDEBAR
# ==========================================

sidebar_header()

sidebar_navigation()


# ==========================================
# 8. RUN SELECTED PAGE
# ==========================================

navigation.run()
