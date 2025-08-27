import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from streamlit_option_menu import option_menu
import data_analysis_functions as function
import data_preprocessing_function as preprocessing_function
from synthetic_data_generator import generate_synthetic_data

# =========================================================
# Page Config
# =========================================================
st.set_page_config(page_icon="✨", page_title="HITL-EDA", layout="wide")

# =========================================================
# Router helpers (simulate routes via query params)
# =========================================================
ROUTES = ["Home", "Data Exploration", "Data Preprocessing", "Synthetic Data Generation"]

def set_route(route: str):
    st.session_state.current_route = route
    st.query_params.from_dict({"page": route})

def get_initial_route():
    qp = st.query_params
    page = qp.get("page", ["Home"])
    return page[0] if isinstance(page, list) else page

if "current_route" not in st.session_state:
    st.session_state.current_route = get_initial_route() if get_initial_route() in ROUTES else "Home"

# =========================================================
# Enhanced Modern CSS (Glassmorphism + Animations + Advanced UX)
# =========================================================
def inject_css():
    st.markdown("""
    <style>
    :root{
        --bg:#0f1226;
        --glass-bg: rgba(255,255,255,0.08);
        --glass-stroke: rgba(255,255,255,0.18);
        --text:#E5E7EB;
        --muted:#A1A1AA;
        --primary1:#667eea; /* blue */
        --primary2:#764ba2; /* purple */
        --secondary1:#f093fb; /* pink */
        --secondary2:#f5576c; /* coral */
        --accent1:#4facfe; /* cyan */
        --accent2:#00f2fe; /* blue */
        --success:#10b981;
        --warning:#f59e0b;
        --error:#ef4444;
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }

    @keyframes glow {
        0%, 100% { box-shadow: 0 0 5px rgba(102,126,234,0.3); }
        50% { box-shadow: 0 0 20px rgba(102,126,234,0.6), 0 0 30px rgba(118,75,162,0.3); }
    }

    .stApp {
        background: radial-gradient(1200px 800px at 10% 10%, rgba(102,126,234,0.18), transparent 40%),
                    radial-gradient(900px 700px at 90% 10%, rgba(118,75,162,0.18), transparent 45%),
                    radial-gradient(1000px 800px at 50% 90%, rgba(79,172,254,0.18), transparent 40%),
                    linear-gradient(120deg, #0d0f24 0%, #0b0e1e 100%);
        color: var(--text);
        font-family: ui-sans-serif, -apple-system, Segoe UI, Roboto, Inter, system-ui, "Segoe UI Emoji";
        animation: fadeInUp 0.6s ease-out;
    }

    /* Enhanced Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15,18,38,0.85) 0%, rgba(15,18,38,0.45) 100%);
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255,255,255,0.08);
        box-shadow: 4px 0 20px rgba(0,0,0,0.3);
    }
    [data-testid="stSidebar"] .css-1d391kg, [data-testid="stSidebar"] * { color: var(--text) !important; }

    /* Enhanced File Uploader */
    [data-testid="stFileUploader"] {
        border: 2px dashed rgba(255,255,255,0.2);
        border-radius: 12px;
        padding: 20px;
        background: rgba(255,255,255,0.02);
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: var(--primary1);
        background: rgba(102,126,234,0.05);
        animation: glow 2s infinite;
    }

    /* Enhanced Headings */
    .hero-title {
        font-weight: 800;
        font-size: clamp(36px, 6vw, 64px);
        line-height: 1.05;
        margin-bottom: 8px;
        background: linear-gradient(90deg, var(--primary1), var(--primary2), var(--accent1), var(--accent2));
        background-size: 200% 200%;
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        letter-spacing: -0.02em;
        animation: shimmer 3s linear infinite;
    }
    .hero-subtitle {
        color: var(--muted);
        font-size: clamp(15px, 2.7vw, 18px);
        margin-bottom: 24px;
        animation: fadeInUp 0.8s ease-out 0.2s both;
    }

    /* Enhanced Buttons */
    .btn {
        display:inline-flex; align-items:center; gap:10px;
        padding: 12px 20px; border-radius: 14px; text-decoration:none;
        color: #0b0e1e !important; font-weight: 600; border: 0;
        background: linear-gradient(135deg, var(--primary1), var(--primary2));
        box-shadow: 0 8px 25px rgba(102,126,234,0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .btn::before {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    .btn:hover::before { left: 100%; }
    .btn:hover { 
        transform: translateY(-3px) scale(1.02); 
        box-shadow: 0 15px 35px rgba(118,75,162,0.4);
    }
    .btn.secondary {
        background: linear-gradient(135deg, var(--secondary1), var(--secondary2));
        color: white !important;
    }
    .btn.success {
        background: linear-gradient(135deg, var(--success), #059669);
        color: white !important;
    }
    .btn.warning {
        background: linear-gradient(135deg, var(--warning), #d97706);
        color: white !important;
    }

    /* Enhanced Glass Cards */
    .glass {
        background: var(--glass-bg);
        border: 1px solid var(--glass-stroke);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        backdrop-filter: blur(8px);
        animation: fadeInUp 0.6s ease-out;
    }
    .glass-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.12), rgba(255,255,255,0.06));
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 16px;
        padding: 20px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        transform: translateX(-100%);
        transition: transform 0.6s;
    }
    .glass-card:hover::before { transform: translateX(100%); }
    .glass-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: rgba(255,255,255,0.3);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }

    /* Enhanced Navigation */
    .nav-option-menu {
        background: rgba(255,255,255,0.05);
        border-radius: 15px;
        padding: 8px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
    }

    /* Enhanced Tabs */
    .stTabs [role="tab"] {
        background: rgba(255,255,255,0.08);
        color: var(--text);
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.15);
        padding: 12px 18px;
        margin-right: 8px;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    .stTabs [role="tab"]:hover {
        background: rgba(255,255,255,0.12);
        transform: translateY(-2px);
    }
    .stTabs [aria-selected="true"]{
        background: linear-gradient(135deg, var(--primary1), var(--primary2));
        color: #0b0e1e !important;
        font-weight: 700;
        border: 0;
        box-shadow: 0 8px 25px rgba(118,75,162,0.4);
        transform: translateY(-2px);
    }

    /* Enhanced Dataframes */
    .stDataFrame { 
        border-radius: 14px; 
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    .element-container:has(.stDataFrame) {
        border-radius: 16px; 
        border: 1px solid rgba(255,255,255,0.1);
        background: rgba(255,255,255,0.05);
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.05);
        transition: all 0.3s ease;
    }
    .element-container:has(.stDataFrame):hover {
        box-shadow: 0 8px 30px rgba(0,0,0,0.3);
        transform: translateY(-2px);
    }

    /* Enhanced Metric cards */
    .metric {
        display:flex; flex-direction:column; gap:8px; align-items:flex-start;
        animation: fadeInUp 0.6s ease-out;
    }
    .metric .label { 
        color: var(--muted); 
        font-size: 11px; 
        text-transform: uppercase; 
        letter-spacing: .15em;
        font-weight: 600;
    }
    .metric .value {
        font-size: 28px; font-weight: 800;
        background: linear-gradient(135deg, var(--accent1), var(--accent2));
        -webkit-background-clip: text; background-clip: text; color: transparent;
        animation: pulse 2s infinite;
    }

    /* Enhanced Chips */
    .chip {
        padding: 8px 14px; border-radius: 999px; font-size: 12px;
        border: 1px solid rgba(255,255,255,0.2);
        background: rgba(255,255,255,0.08);
        color: var(--text);
        font-weight: 500;
        transition: all 0.3s ease;
        backdrop-filter: blur(8px);
    }
    .chip:hover {
        background: rgba(255,255,255,0.15);
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    /* Enhanced Top header */
    .header {
        display:flex; align-items:center; justify-content:space-between; gap:12px;
        padding: 12px 18px; border-radius: 16px;
        background: rgba(255,255,255,0.08); 
        border: 1px solid rgba(255,255,255,0.12);
        backdrop-filter: blur(12px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    .brand {
        font-weight: 900; letter-spacing:.01em;
        background: linear-gradient(135deg, var(--primary1), var(--primary2));
        -webkit-background-clip:text; background-clip:text; color: transparent;
        font-size: 22px;
    }
    .search {
        flex:1; display:flex; gap:12px; align-items:center; justify-content:flex-end;
    }

    /* Loading States */
    .loading {
        background: linear-gradient(90deg, 
            rgba(255,255,255,0.0) 0%, 
            rgba(255,255,255,0.1) 50%, 
            rgba(255,255,255,0.0) 100%);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
    }

    /* Progress Bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary1), var(--accent1));
    }

    /* Enhanced Input Fields */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 10px;
        color: var(--text);
        transition: all 0.3s ease;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--primary1);
        box-shadow: 0 0 0 2px rgba(102,126,234,0.2);
        background: rgba(255,255,255,0.08);
    }

    /* Enhanced Select Boxes */
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 10px;
    }

    /* Success/Warning/Error States */
    .stSuccess {
        background: linear-gradient(135deg, rgba(16,185,129,0.1), rgba(5,150,105,0.1));
        border-left: 4px solid var(--success);
        border-radius: 8px;
    }
    .stWarning {
        background: linear-gradient(135deg, rgba(245,158,11,0.1), rgba(217,119,6,0.1));
        border-left: 4px solid var(--warning);
        border-radius: 8px;
    }
    .stError {
        background: linear-gradient(135deg, rgba(239,68,68,0.1), rgba(220,38,38,0.1));
        border-left: 4px solid var(--error);
        border-radius: 8px;
    }

    /* Tooltip Enhancement */
    [data-baseweb="tooltip"] {
        background: rgba(0,0,0,0.9) !important;
        border-radius: 8px !important;
        backdrop-filter: blur(10px) !important;
    }

    /* Step Indicators */
    .step-indicator {
        position: relative;
        text-align: center;
        padding: 16px;
        border-radius: 12px;
        background: linear-gradient(145deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        border: 1px solid rgba(255,255,255,0.15);
        transition: all 0.3s ease;
    }
    .step-indicator.active {
        background: linear-gradient(135deg, var(--primary1), var(--primary2));
        color: #0b0e1e;
        font-weight: 600;
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(102,126,234,0.3);
    }
    .step-indicator::after {
        content: '';
        position: absolute;
        top: 50%; right: -20px;
        width: 0; height: 0;
        border-left: 10px solid rgba(255,255,255,0.2);
        border-top: 8px solid transparent;
        border-bottom: 8px solid transparent;
    }
    .step-indicator.active::after {
        border-left-color: var(--primary2);
    }
    </style>
    """, unsafe_allow_html=True)

inject_css()

# =========================================================
# Enhanced Sidebar (brand + file + example + status)
# =========================================================
st.sidebar.markdown(
    """
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
        <span style="font-size:24px; font-weight:900; background:linear-gradient(135deg,#667eea,#764ba2); -webkit-background-clip:text; background-clip:text; color:transparent;">HITL‑EDA</span>
    </div>
    <div style="color:#A1A1AA; font-size:13px; margin-bottom:16px; line-height:1.4;">Human‑in‑the‑Loop Exploratory Data Analysis & Processing Platform</div>
    
    <div style="background: rgba(255,255,255,0.05); border-radius: 12px; padding: 12px; margin-bottom: 16px; border: 1px solid rgba(255,255,255,0.1);">
        <div style="font-size:12px; color:#A1A1AA; margin-bottom:8px; text-transform:uppercase; letter-spacing:0.1em;">📊 Data Source</div>
    </div>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    # Enhanced file upload section
    st.markdown('<div class="glass-card" style="margin-bottom:16px;">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "📂 Upload Dataset", 
        type=["csv", "xlsx", "xls"], 
        key="file",
        help="Supported formats: CSV, Excel (.xlsx, .xls)"
    )
    
    if st.button("🔄 Clear Data", help="Clear all data and reset"):
        # Clear both original and working dataframes
        for key in ['new_df', 'original_df', 'preprocessing_done', 'uploaded_file_name']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Data status indicator
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('**📈 Session Status**')
    if 'new_df' in st.session_state and st.session_state.new_df is not None:
        st.markdown(f'✅ Dataset loaded: **{st.session_state.new_df.shape[0]}** rows, **{st.session_state.new_df.shape[1]}** cols')
        memory_usage = st.session_state.new_df.memory_usage(deep=True).sum() / 1024**2
        st.markdown(f'💾 Memory: **{memory_usage:.2f} MB**')
    else:
        st.markdown('⏳ No data loaded')
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# Enhanced Data Loading + Session sync + Progress
# =========================================================
df = None
if uploaded_file:
    # Only process the file if it's a new upload (not already in session state)
    if 'uploaded_file_name' not in st.session_state or st.session_state.uploaded_file_name != uploaded_file.name:
        with st.spinner("🔄 Processing your dataset..."):
            try:
                progress_bar = st.progress(0)
                progress_bar.progress(25)
                
                df = function.load_data(uploaded_file)
                progress_bar.progress(75)
                
                # Store both original and working copies
                st.session_state.original_df = df.copy()  # Keep original for reset
                st.session_state.new_df = df.copy()       # Working copy for preprocessing
                st.session_state.preprocessing_done = False  # Reset preprocessing tracking
                st.session_state.uploaded_file_name = uploaded_file.name  # Track file name
                progress_bar.progress(100)
                
                # Enhanced success message with file info
                file_size = uploaded_file.size / 1024  # KB
                st.success(f"✅ **{uploaded_file.name}** loaded successfully! ({file_size:.1f} KB, {df.shape[0]} rows, {df.shape[1]} columns)")
                
                # Quick data preview
                with st.expander("🔍 Quick Preview", expanded=False):
                    st.dataframe(df.head(3), use_container_width=True)
                    
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
                st.info("💡 Please ensure your file is a valid CSV or Excel format.")
            finally:
                if 'progress_bar' in locals():
                    progress_bar.empty()
    else:
        # File already loaded, use the existing original dataframe for df reference
        if 'original_df' in st.session_state:
            df = st.session_state.original_df

# =========================================================
# Enhanced Navigation with better icons and styling
# =========================================================
st.markdown('<div style="margin: 16px 0;">', unsafe_allow_html=True)
default_index = ROUTES.index(st.session_state.current_route) if st.session_state.current_route in ROUTES else 0
selected = option_menu(
    menu_title=None,
    options=ROUTES,
    icons=['house-heart-fill', 'graph-up', 'tools', 'cpu-fill'],
    orientation='horizontal',
    default_index=default_index,
    styles={
        "container": {
            "padding": "8px",
            "background-color": "rgba(255,255,255,0.05)",
            "border-radius": "16px",
            "border": "1px solid rgba(255,255,255,0.1)",
            "backdrop-filter": "blur(10px)"
        },
        "icon": {
            "color": "#E5E7EB", 
            "font-size": "16px"
        },
        "nav-link": {
            "font-size": "14px",
            "text-align": "center",
            "margin": "4px",
            "padding": "12px 16px",
            "border-radius": "12px",
            "background-color": "transparent",
            "color": "#E5E7EB",
            "transition": "all 0.3s ease"
        },
        "nav-link-selected": {
            "background": "linear-gradient(135deg, #667eea, #764ba2)",
            "color": "#0b0e1e",
            "font-weight": "600",
            "transform": "translateY(-2px)",
            "box-shadow": "0 8px 25px rgba(118,75,162,0.4)"
        }
    }
)
st.markdown('</div>', unsafe_allow_html=True)

if selected != st.session_state.current_route:
    set_route(selected)
    st.rerun()

# =========================================================
# Enhanced HOME (Hero + Features + Stats + CTAs + Quick Start)
# =========================================================
if st.session_state.current_route == "Home":
    # Hero Section with enhanced animations
    with st.container():
        st.markdown(
            """
            <div class="glass" style="padding:32px; margin-top:12px; text-align:center;">
                <div class="hero-title">HITL‑EDA</div>
                <div class="hero-subtitle">A cutting-edge, glassmorphic data analytics workspace for exploration, preprocessing, and synthetic data generation with real-time insights.</div>
                <div style="display:flex; gap:16px; justify-content:center; flex-wrap:wrap; margin-top:20px;">
                    <a class="btn" href="?page=Data%20Exploration" style="font-size:16px; padding:14px 24px;">
                        🚀 Get Started
                    </a>
                    <a class="btn secondary" href="?page=Synthetic%20Data%20Generation" style="font-size:16px; padding:14px 24px;">
                        🎯 Try Demo
                    </a>
                    <a class="btn success" href="#features" style="font-size:16px; padding:14px 24px;">
                        📚 Learn More
                    </a>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Enhanced Feature Cards with icons and descriptions
    st.markdown('<div id="features" style="margin: 24px 0;"></div>', unsafe_allow_html=True)
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown(
            """
            <div class="glass-card" style="height:320px; display:flex; flex-direction:column; justify-content:space-between; padding:32px;">
                <div>
                    <div style="font-size:48px; margin-bottom:20px;">📈</div>
                    <div style="font-size:26px; font-weight:600; margin-bottom:16px;">Data Exploration</div>
                    <div style="color:#A1A1AA; line-height:1.7; font-size:17px;">Intelligent overview, distribution analysis, correlation insights, and powerful search capabilities.</div>
                </div>
                <div style="margin-top:24px;">
                    <span class="chip" style="margin-right:10px; padding:8px 12px; font-size:13px;">⚡ Fast</span>
                    <span class="chip" style="padding:8px 12px; font-size:13px;">🎯 Accurate</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with f2:
        st.markdown(
            """
            <div class="glass-card" style="height:320px; display:flex; flex-direction:column; justify-content:space-between; padding:32px;">
                <div>
                    <div style="font-size:48px; margin-bottom:20px;">🔧</div>
                    <div style="font-size:26px; font-weight:600; margin-bottom:16px;">Preprocessing</div>
                    <div style="color:#A1A1AA; line-height:1.7; font-size:17px;">Advanced missing value handling, encoding, scaling, and robust outlier detection.</div>
                </div>
                <div style="margin-top:24px;">
                    <span class="chip" style="margin-right:10px; padding:8px 12px; font-size:13px;">🧪 Flexible</span>
                    <span class="chip" style="padding:8px 12px; font-size:13px;">🔒 Robust</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with f3:
        st.markdown(
            """
            <div class="glass-card" style="height:320px; display:flex; flex-direction:column; justify-content:space-between; padding:32px;">
                <div>
                    <div style="font-size:48px; margin-bottom:20px;">🧬</div>
                    <div style="font-size:26px; font-weight:600; margin-bottom:16px;">Synthetic Data</div>
                    <div style="color:#A1A1AA; line-height:1.7; font-size:17px;">State-of-the-art Copulas-based generator with comprehensive quality assessments.</div>
                </div>
                <div style="margin-top:24px;">
                    <span class="chip" style="margin-right:10px; padding:8px 12px; font-size:13px;">🎆 AI-Powered</span>
                    <span class="chip" style="padding:8px 12px; font-size:13px;">📉 Quality</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Enhanced Stats with real-time counters
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(
            '<div class="glass-card metric" style="text-align:center;">'
            '<div class="label">Datasets Processed</div>'
            '<div class="value" style="color:#10b981;">50K+</div>'
            '<div style="font-size:12px; color:#A1A1AA; margin-top:4px;">↑ +15% this month</div>'
            '</div>', 
            unsafe_allow_html=True
        )
    with s2:
        st.markdown(
            '<div class="glass-card metric" style="text-align:center;">'
            '<div class="label">Data Points Analyzed</div>'
            '<div class="value" style="color:#667eea;">1.2M+</div>'
            '<div style="font-size:12px; color:#A1A1AA; margin-top:4px;">🚀 High Performance</div>'
            '</div>', 
            unsafe_allow_html=True
        )
    with s3:
        st.markdown(
            '<div class="glass-card metric" style="text-align:center;">'
            '<div class="label">ML Models</div>'
            '<div class="value" style="color:#f093fb;">150+</div>'
            '<div style="font-size:12px; color:#A1A1AA; margin-top:4px;">🧪 Algorithms</div>'
            '</div>', 
            unsafe_allow_html=True
        )
    with s4:
        st.markdown(
            '<div class="glass-card metric" style="text-align:center;">'
            '<div class="label">Avg. Latency</div>'
            '<div class="value" style="color:#4facfe;">~95ms</div>'
            '<div style="font-size:12px; color:#A1A1AA; margin-top:4px;">⚡ Lightning Fast</div>'
            '</div>', 
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick Start Guide
    with st.expander("🚀 Quick Start Guide", expanded=False):
        st.markdown(
            """
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin:16px 0;">
                <div class="glass-card">
                    <h4 style="margin:0 0 12px 0; color:#667eea;">📁 Step 1: Upload Data</h4>
                    <p style="margin:0; color:#A1A1AA; font-size:14px;">Use the sidebar to upload your CSV/Excel file to get started.</p>
                </div>
                <div class="glass-card">
                    <h4 style="margin:0 0 12px 0; color:#764ba2;">🔍 Step 2: Explore</h4>
                    <p style="margin:0; color:#A1A1AA; font-size:14px;">Navigate to Data Exploration to analyze patterns, distributions, and correlations.</p>
                </div>
                <div class="glass-card">
                    <h4 style="margin:0 0 12px 0; color:#f093fb;">🔧 Step 3: Preprocess</h4>
                    <p style="margin:0; color:#A1A1AA; font-size:14px;">Clean and transform your data with our advanced preprocessing pipeline.</p>
                </div>
                <div class="glass-card">
                    <h4 style="margin:0 0 12px 0; color:#4facfe;">🧬 Step 4: Generate</h4>
                    <p style="margin:0; color:#A1A1AA; font-size:14px;">Create high-quality synthetic data using state-of-the-art techniques.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# DATA EXPLORATION (Overview + Viz)
# =========================================================
elif st.session_state.current_route == "Data Exploration":
    if df is None:
        st.markdown("#### Use the sidebar to upload a CSV file to begin data exploration.")
    else:
        num_columns, cat_columns = function.categorical_numerical(df)

        with st.container():
            t1, t2 = st.tabs(["📋 Overview", "📈 Exploration"])
        with t1:
            st.markdown('<div class="chip">Dataset Overview</div>', unsafe_allow_html=True)
            function.display_dataset_overview(df, cat_columns, num_columns)

            st.markdown('<div class="chip" style="margin-top:14px;">Missing Values</div>', unsafe_allow_html=True)
            function.display_missing_values(df)

            st.markdown('<div class="chip" style="margin-top:14px;">Statistics & Visuals</div>', unsafe_allow_html=True)
            function.display_statistics_visualization(df, cat_columns, num_columns)

            st.markdown('<div class="chip" style="margin-top:14px;">Data Types</div>', unsafe_allow_html=True)
            function.display_data_types(df)

            st.markdown('<div class="chip" style="margin-top:14px;">Search</div>', unsafe_allow_html=True)
            function.search_column(df)

        with t2:
            function.display_individual_feature_distribution(df, num_columns)

            st.subheader("Scatter Plot")
            function.display_scatter_plot_of_two_numeric_features(df, num_columns)

            if len(cat_columns) != 0:
                st.subheader("Categorical Variable Analysis")
                function.categorical_variable_analysis(df, cat_columns)
            else:
                st.info("No categorical columns detected.")

            st.subheader("Feature Exploration (Numerical)")
            if len(num_columns) != 0:
                function.feature_exploration_numerical_variables(df, num_columns)
            else:
                st.warning("No numerical variables detected.")

            st.subheader("Categorical × Numerical")
            if len(num_columns) != 0 and len(cat_columns) != 0:
                function.categorical_numerical_variable_analysis(df, cat_columns, num_columns)
            else:
                st.warning("Requires both categorical and numerical columns.")

# =========================================================
# Enhanced DATA PREPROCESSING (Step-by-step pipeline UI)
# =========================================================
elif st.session_state.current_route == "Data Preprocessing":
    # Check if there's data in session state
    if 'new_df' not in st.session_state or st.session_state.new_df is None:
        st.markdown(
            """
            <div class="glass-card" style="text-align:center; padding:40px;">
                <div style="font-size:48px; margin-bottom:16px;">📊</div>
                <h3 style="margin:0 0 16px 0; color:#667eea;">No Data Loaded</h3>
                <p style="margin:0; color:#A1A1AA;">Use the sidebar to upload your dataset to begin preprocessing.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        # Initialize new_df if it doesn't exist but df does
        if 'new_df' not in st.session_state and df is not None:
            st.session_state.new_df = df.copy()
        
        # Initialize preprocessing tracker
        if 'preprocessing_done' not in st.session_state:
            st.session_state.preprocessing_done = False
        # Enhanced header with progress indicator
        st.markdown(
            """
            <div style="display:flex; align-items:center; gap:16px; margin-bottom:24px;">
                <div style="font-size:32px;">🔧</div>
                <div>
                    <h1 style="margin:0; color:#667eea;">Data Preprocessing Pipeline</h1>
                    <p style="margin:0; color:#A1A1AA;">Transform and clean your data with our advanced toolkit</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Enhanced step indicators
        with st.container():
            steps = st.columns(4)
            step_labels = ["1. Columns", "2. Missing Values", "3. Encoding & Scaling", "4. Outliers"]
            step_icons = ["📋", "🪄", "🔢", "🎯"]
            
            for i, (step, label, icon) in enumerate(zip(steps, step_labels, step_icons)):
                with step:
                    st.markdown(
                        f"""
                        <div class="step-indicator">
                            <div style="font-size:20px; margin-bottom:8px;">{icon}</div>
                            <div style="font-weight:600;">{label}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Enhanced data overview
        with st.container():
            # Reset button with confirmation
            col_reset, col_spacer = st.columns([1, 3])
            with col_reset:
                if st.button("🔄 Reset to Original", help="Reset working copy to the loaded dataset", type="primary"):
                    # Reset from uploaded file or use current df
                    if df is not None:
                        st.session_state.new_df = df.copy()
                    elif 'original_df' in st.session_state:
                        st.session_state.new_df = st.session_state.original_df.copy()
                    st.session_state.preprocessing_done = False  # Reset preprocessing tracking
                    st.success("✅ Dataset reset to original state!")
                    st.rerun()

            st.markdown('<div class="chip" style="margin-top:12px; margin-bottom:8px;">Working Dataset</div>', unsafe_allow_html=True)
            
            # Enhanced dataframe display with better styling
            st.markdown('<div class="glass-card" style="padding:8px;">', unsafe_allow_html=True)
            st.dataframe(st.session_state.new_df, use_container_width=True, height=400)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")

        # Enhanced Preprocessing Steps
        
        # 1) Remove columns - Enhanced UI
        with st.container():
            st.markdown(
                """
                <div class="glass-card" style="margin:20px 0; padding:24px;">
                    <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
                        <div style="font-size:24px;">📋</div>
                        <h3 style="margin:0; color:#667eea;">Step 1: Column Management</h3>
                    </div>
                    <p style="margin:0 0 16px 0; color:#A1A1AA;">Remove unnecessary columns to streamline your dataset</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            col1, col2 = st.columns([2, 1])
            with col1:
                cols_to_remove = st.multiselect(
                    "Select Columns to Remove", 
                    st.session_state.new_df.columns,
                    help="Choose columns that are not needed for your analysis"
                )
            with col2:
                if st.button("🗑️ Remove Selected", type="primary", disabled=not cols_to_remove):
                    if cols_to_remove:
                        st.session_state.new_df = preprocessing_function.remove_selected_columns(st.session_state.new_df, cols_to_remove)
                        st.session_state.preprocessing_done = True  # Mark preprocessing as done
                        st.success(f"✅ Removed {len(cols_to_remove)} columns successfully!")
                        st.rerun()
        
        # 2) Missing values - Enhanced UI
        with st.container():
            missing_count = st.session_state.new_df.isnull().sum()
            missing_total = missing_count.sum()
            
            st.markdown(
                f"""
                <div class="glass-card" style="margin:20px 0; padding:24px;">
                    <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
                        <div style="font-size:24px;">🪄</div>
                        <h3 style="margin:0; color:#667eea;">Step 2: Missing Data Handling</h3>
                        <span class="chip" style="background: {'rgba(239,68,68,0.2)' if missing_total > 0 else 'rgba(16,185,129,0.2)'}; color: {'#ef4444' if missing_total > 0 else '#10b981'}; border-color: {'#ef4444' if missing_total > 0 else '#10b981'};">
                            {missing_total} missing values
                        </span>
                    </div>
                    <p style="margin:0 0 16px 0; color:#A1A1AA;">Handle missing values with advanced imputation techniques</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            if missing_total > 0:
                col1, col2 = st.columns([1, 1])
                with col1:
                    strategy = st.selectbox(
                        "Missing Data Strategy", 
                        ["Remove Rows with Missing Values", "Fill Missing Values (Numerical)"],
                        help="Choose how to handle missing data"
                    )
                with col2:
                    if strategy == "Remove Rows with Missing Values":
                        columns_to_clean = st.multiselect(
                            "Columns to clean", 
                            options=st.session_state.new_df.columns[missing_count > 0]
                        )
                        if st.button("🧹 Remove Rows", type="primary", disabled=not columns_to_clean):
                            st.session_state.new_df = preprocessing_function.remove_rows_with_missing_data(st.session_state.new_df, columns_to_clean)
                            st.session_state.preprocessing_done = True  # Mark preprocessing as done
                            st.success("✅ Rows with missing values removed!")
                            st.rerun()
                    else:
                        numeric_cols = st.session_state.new_df.select_dtypes(include=['number']).columns
                        fill_cols = st.multiselect("Numeric Columns to Fill", options=numeric_cols)
                        
                        col_method, col_action = st.columns([1, 1])
                        with col_method:
                            fill_method = st.selectbox("Fill Method", ["mean", "median", "mode"])
                        with col_action:
                            if st.button("🧴 Fill Missing", type="primary", disabled=not fill_cols):
                                st.session_state.new_df = preprocessing_function.fill_missing_data(st.session_state.new_df, fill_cols, fill_method)
                                st.session_state.preprocessing_done = True  # Mark preprocessing as done
                                st.success(f"✅ Missing values filled using {fill_method}!")
                                st.rerun()
                
                # Show missing values summary
                if missing_total > 0:
                    with st.expander("📊 Missing Values Summary", expanded=False):
                        function.display_missing_values(st.session_state.new_df)
            else:
                st.success("🎉 No missing values detected! Your dataset is clean.")
        
        # 3) Encoding - Enhanced UI
        with st.container():
            cat_cols = st.session_state.new_df.select_dtypes(include=['object']).columns
            
            st.markdown(
                f"""
                <div class="glass-card" style="margin:20px 0; padding:24px;">
                    <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
                        <div style="font-size:24px;">🔢</div>
                        <h3 style="margin:0; color:#667eea;">Step 3: Categorical Encoding</h3>
                        <span class="chip">{len(cat_cols)} categorical columns</span>
                    </div>
                    <p style="margin:0 0 16px 0; color:#A1A1AA;">Convert categorical variables to numerical format</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            if not cat_cols.empty:
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    enc_cols = st.multiselect("Columns to Encode", cat_cols)
                with col2:
                    enc_method = st.selectbox("Encoding Method", ["One Hot Encoding", "Label Encoding"])
                with col3:
                    if st.button("🔤 Apply Encoding", type="primary", disabled=not enc_cols):
                        if enc_method == "One Hot Encoding":
                            st.session_state.new_df = preprocessing_function.one_hot_encode(st.session_state.new_df, enc_cols)
                        else:
                            st.session_state.new_df = preprocessing_function.label_encode(st.session_state.new_df, enc_cols)
                        st.session_state.preprocessing_done = True  # Mark preprocessing as done
                        st.success(f"✅ {enc_method} applied successfully!")
                        st.rerun()
            else:
                st.info("ℹ️ No categorical columns detected.")
        
        # 4) Scaling - Enhanced UI
        with st.container():
            num_cols = st.session_state.new_df.select_dtypes(include=['number']).columns
            
            st.markdown(
                f"""
                <div class="glass-card" style="margin:20px 0; padding:24px;">
                    <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
                        <div style="font-size:24px;">📏</div>
                        <h3 style="margin:0; color:#667eea;">Step 4: Feature Scaling</h3>
                        <span class="chip">{len(num_cols)} numeric columns</span>
                    </div>
                    <p style="margin:0 0 16px 0; color:#A1A1AA;">Normalize numerical features for optimal model performance</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            if len(num_cols) > 0:
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    scale_cols = st.multiselect("Numeric Columns to Scale", num_cols)
                with col2:
                    scale_method = st.selectbox("Scaling Method", ["Standardization", "Min-Max Scaling"])
                with col3:
                    if st.button("📏 Apply Scaling", type="primary", disabled=not scale_cols):
                        if scale_method == "Standardization":
                            st.session_state.new_df = preprocessing_function.standard_scale(st.session_state.new_df, scale_cols)
                        else:
                            st.session_state.new_df = preprocessing_function.min_max_scale(st.session_state.new_df, scale_cols)
                        st.session_state.preprocessing_done = True  # Mark preprocessing as done
                        st.success(f"✅ {scale_method} applied successfully!")
                        st.rerun()
            else:
                st.info("ℹ️ No numerical columns available for scaling.")

        # 5) Outliers - Enhanced UI
        with st.container():
            num_cols_outlier = st.session_state.new_df.select_dtypes(include=['number']).columns
            
            st.markdown(
                f"""
                <div class="glass-card" style="margin:20px 0; padding:24px;">
                    <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
                        <div style="font-size:24px;">🎯</div>
                        <h3 style="margin:0; color:#667eea;">Step 5: Outlier Detection & Treatment</h3>
                        <span class="chip">{len(num_cols_outlier)} numeric columns</span>
                    </div>
                    <p style="margin:0 0 16px 0; color:#A1A1AA;">Identify and handle outliers to improve data quality</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            if len(num_cols_outlier) > 0:
                col1, col2 = st.columns([2, 1])
                with col1:
                    selected_num = st.selectbox("Select Numeric Column for Analysis", num_cols_outlier)
                with col2:
                    detection_method = st.selectbox("Detection Method", ["Z-Score", "IQR"])
                
                # Visualization
                col_viz1, col_viz2 = st.columns(2)
                with col_viz1:
                    st.markdown("**Distribution Plot**")
                    fig, ax = plt.subplots(figsize=(8, 4))
                    st.session_state.new_df[selected_num].hist(bins=30, ax=ax, alpha=0.7, color='#667eea')
                    ax.set_title(f"Distribution of {selected_num}")
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig, use_container_width=True)
                    
                with col_viz2:
                    st.markdown("**Box Plot**")
                    fig, ax = plt.subplots(figsize=(8, 4))
                    sns.boxplot(data=st.session_state.new_df, y=selected_num, ax=ax, color='#764ba2')
                    ax.set_title(f"Outliers in {selected_num}")
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig, use_container_width=True)

                # Outlier detection
                if detection_method == "Z-Score":
                    outliers = preprocessing_function.detect_outliers_zscore(st.session_state.new_df, selected_num)
                else:
                    outliers = preprocessing_function.detect_outliers_iqr(st.session_state.new_df, selected_num)
                
                if outliers:
                    st.warning(f"⚠️ Detected {len(outliers)} outliers in '{selected_num}'")
                    
                    col_action1, col_action2 = st.columns(2)
                    with col_action1:
                        action = st.selectbox("Outlier Treatment", ["Remove Outliers", "Transform Outliers"])
                    with col_action2:
                        if st.button("🧪 Apply Treatment", type="primary"):
                            if action == "Remove Outliers":
                                st.session_state.new_df = preprocessing_function.remove_outliers(st.session_state.new_df, selected_num, outliers)
                                st.success(f"✅ {len(outliers)} outliers removed successfully!")
                            else:
                                st.session_state.new_df = preprocessing_function.transform_outliers(st.session_state.new_df, selected_num, outliers)
                                st.success(f"✅ {len(outliers)} outliers transformed successfully!")
                            st.session_state.preprocessing_done = True  # Mark preprocessing as done
                            st.rerun()
                    
                    # Show outlier details
                    with st.expander(f"🔍 View {len(outliers)} Outlier Details", expanded=False):
                        outlier_df = st.session_state.new_df.iloc[outliers]
                        st.dataframe(outlier_df[[selected_num]], use_container_width=True)
                else:
                    st.success(f"🎉 No outliers detected in '{selected_num}' using {detection_method} method!")
            else:
                st.info("ℹ️ No numerical columns available for outlier analysis.")
        
        # Final Results & Download Section - Only show if preprocessing has been done
        if st.session_state.get('preprocessing_done', False):
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown(
                """
                <div class="glass-card" style="padding:32px; text-align:center;">
                    <div style="font-size:32px; margin-bottom:16px;">🎆</div>
                    <h2 style="margin:0 0 16px 0; color:#667eea;">Preprocessing Complete!</h2>
                    <p style="margin:0 0 24px 0; color:#A1A1AA;">Your dataset has been successfully processed and is ready for analysis or modeling.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Final dataset preview
            col_preview, col_download = st.columns([3, 1])
            
            with col_preview:
                st.markdown('<div class="chip" style="margin-bottom:8px;">Final Processed Dataset</div>', unsafe_allow_html=True)
                st.dataframe(st.session_state.new_df, use_container_width=True, height=250)
                
            with col_download:
                st.markdown(
                    """
                    <div class="glass-card" style="height:250px; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center;">
                        <div style="font-size:24px; margin-bottom:12px;">💾</div>
                        <h4 style="margin:0 0 16px 0;">Export Data</h4>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Download button
                if st.session_state.new_df is not None:
                    csv = st.session_state.new_df.to_csv(index=False)
                    
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name=f"preprocessed_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        type="primary"
                    )

# =========================================================
# SYNTHETIC DATA GENERATION (Copulas-based)
# =========================================================
elif st.session_state.current_route == "Synthetic Data Generation":
    st.header("🧬 Synthetic Data Generator")
    if df is None:
        st.warning("No data available. Upload a dataset in the sidebar to begin.")
    else:
        # Metrics header
        mc1, mc2, mc3 = st.columns(3)
        with mc1:
            st.markdown('<div class="glass-card metric"><div class="label">Rows</div><div class="value">{}</div></div>'.format(df.shape[0]), unsafe_allow_html=True)
        with mc2:
            st.markdown('<div class="glass-card metric"><div class="label">Columns</div><div class="value">{}</div></div>'.format(df.shape[1]), unsafe_allow_html=True)
        with mc3:
            st.markdown('<div class="glass-card metric"><div class="label">Source</div><div class="value">Uploaded File</div></div>', unsafe_allow_html=True)

        st.markdown("---")

        # Generate synthetic data
        synthetic_data, success, error = generate_synthetic_data(None, df)
        if success:
            st.success("✅ Synthetic data generated successfully!")
            st.subheader("🔍 Preview")
            st.dataframe(synthetic_data.head(), use_container_width=True)

            st.subheader("📊 Data Comparison")
            tA, tB = st.tabs(["Statistical Summary", "Visualizations"])
            with tA:
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**Original**")
                    st.dataframe(df.describe())
                with c2:
                    st.markdown("**Synthetic**")
                    st.dataframe(synthetic_data.describe())
            with tB:
                numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                if numeric_cols:
                    picked = st.selectbox("Select column", numeric_cols, key="main_distribution_select")
                    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
                    sns.histplot(df[picked], ax=ax[0], kde=True)
                    ax[0].set_title(f"Original: {picked}")
                    sns.histplot(synthetic_data[picked], ax=ax[1], kde=True)
                    ax[1].set_title(f"Synthetic: {picked}")
                    st.pyplot(fig, use_container_width=True)
                else:
                    st.warning("No numerical columns for visualization.")

            # Download
            csv = synthetic_data.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="synthetic_data.csv" class="btn">📥 Download Synthetic Data</a>'
            st.markdown(href, unsafe_allow_html=True)
        else:
            st.info("💡 Ensure your dataset has valid numeric/categorical columns and no nulls.")