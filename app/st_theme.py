# st_theme.py
import streamlit as st
import base64

LOGO_PATH = "./assets/logo.png"  # adjust if different

def set_page_theme(title="Segmenta Pro", icon="🧩", spin_logo=False):
    """Apply custom theme, branding, and CSS for the Segmenta app."""
    st.set_page_config(page_title=title, page_icon=icon, layout="wide")

    # --- Load logo ---
    try:
        logo_b64 = base64.b64encode(open(LOGO_PATH, "rb").read()).decode()
    except Exception:
        logo_b64 = ""

    st.markdown("""
    <link rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
    <style>
    .material-symbol {
      font-family: 'Material Symbols Rounded';
      font-weight: 400;
      font-style: normal;
      font-size: 24px; /* Adjust size */
      line-height: 1;
      display: inline-block;
      vertical-align: middle;
      color: #FF9E6B; /* Orange accent or your custom color */
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Branding block ---
    st.markdown(f"""
    <style>
    .brand {{
      display:flex;align-items:center;gap:8px;line-height:1;
    }}
    .brand img.logo {{
      height:116px;width:auto;display:block;margin:0;
      transform-origin:50% 50%;
      filter: drop-shadow(0 6px 12px rgba(0,0,0,0.25));
    }}          
    .brand img.logo.spin {{
      animation:spin 1s linear infinite;
    }}
    @keyframes spin {{from{{transform:rotate(0)}}to{{transform:rotate(360deg)}}}}
    .brand h1{{
      margin:0;
      font-family:'Calibre Light','Calibre',ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
      font-weight:300;
      font-size:clamp(28px,5vw,56px);
      color:#0F172A;
      text-shadow:0 1px 0 rgba(255,255,255,.6),0 8px 24px rgba(15,23,42,.15);
    }}
    </style>
    <div class="brand">
      <img class="logo {'spin' if spin_logo else ''}" src="data:image/png;base64,{logo_b64}" />
      <h1>{title}</h1>
    </div>
    """, unsafe_allow_html=True)

    # --- Global card-like shadow for blocks (tables, charts, figures) ---
    st.markdown("""
    <style>
    /* Tables */
    .stDataFrame, .stTable {
        box-shadow: 0 6px 18px rgba(0,0,0,0.12);
        border-radius: 12px;
        padding: 10px;
        background: white;
    }

    /* Matplotlib/Plotly figures */
    [data-testid="stPlotlyChart"], [data-testid="stVegaLiteChart"], [data-testid="stAltairChart"], [data-testid="stDeckGlJsonChart"], .stImage {
        box-shadow: 0 8px 22px rgba(0,0,0,0.15);
        border-radius: 12px;
        background: white;
        padding: 8px;
    }

    /* Expander + Metrics (already styled but add consistency) */
    div[data-testid="stMetric"], div[data-testid="stExpander"] {
        box-shadow: 0 6px 16px rgba(0,0,0,0.12);
        border-radius: 12px;
        background: white;
    }

    /* Callout (info box) */
    .callout {
      font-family: 'Calibre Light','Calibre',
                   ui-sans-serif, system-ui, -apple-system,
                   'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      font-weight: 300;
      background: #f0f6f7;
      border: 1px solid #f0f6f7;
      color: #082F49;
      border-radius: 12px;
      padding: 14px 16px;
      margin: 12px 0;
      box-shadow: 0 10px 28px rgba(8, 47, 73, 0.16);
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Gradient button (as before) ---
    st.markdown("""
    <style>
    .stButton > button {
        background: linear-gradient(90deg, #6366F1, #3B82F6);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 15px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #4F46E5, #2563EB);
        box-shadow: 0 6px 16px rgba(0,0,0,0.25);
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Background & sidebar (frosted glass aesthetic) ---
    st.markdown("""
    <style>
/* 🌅 Frosty orange–blue gradient background */
.stApp {
  background:
    radial-gradient(50rem 35rem at 10% 20%, rgba(255, 175, 100, 0.45) 0%, transparent 70%),
    radial-gradient(45rem 30rem at 85% 15%, rgba(90, 180, 255, 0.40) 0%, transparent 70%),
    radial-gradient(55rem 40rem at 50% 80%, rgba(255, 230, 180, 0.35) 0%, transparent 75%),
    linear-gradient(120deg, #fdf6f0 0%, #eaf4ff 50%, #f8f9ff 100%);
  background-attachment: fixed;
  color: #1a1a1a;
}

    /* 🧊 Sidebar frosted panel */
    [data-testid="stSidebar"] > div:first-child {
      background: rgba(255, 255, 255, 0.45);
      backdrop-filter: blur(14px) saturate(180%);
      -webkit-backdrop-filter: blur(14px) saturate(180%);
      border-right: 1px solid rgba(255, 255, 255, 0.25);
      box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
    }

    /* 🪟 General glass card container */
    .glass {
      background: rgba(255, 255, 255, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.3);
      border-radius: 18px;
      padding: 20px 24px;
      box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
      backdrop-filter: blur(10px) saturate(180%);
      -webkit-backdrop-filter: blur(10px) saturate(180%);
      transition: all 0.3s ease-in-out;
    }

    /* ✨ Hover lift for cards */
    .glass:hover {
      transform: translateY(-2px);
      box-shadow: 0 10px 36px rgba(31, 38, 135, 0.15);
    }

    /* 📊 Optional: blur for dataframe containers */
    [data-testid="stDataFrame"] {
      background: rgba(255, 255, 255, 0.65);
      backdrop-filter: blur(8px);
      border-radius: 10px;
      padding: 6px;
    }
    </style>
    """, unsafe_allow_html=True)


def show_callout(message: str):
    """Render a message inside a styled callout box."""
    st.markdown(f"<div class='callout'>{message}</div>", unsafe_allow_html=True)


def apply_crypto_theme():
    """Apply the crypto dashboard theme with glass effects"""
    st.markdown("""
    <style>
    /* Beautiful background */
    .stApp {
      background:
        radial-gradient(50rem 35rem at 10% 20%, rgba(255, 175, 100, 0.45) 0%, transparent 70%),
        radial-gradient(45rem 30rem at 85% 15%, rgba(90, 180, 255, 0.40) 0%, transparent 70%),
        radial-gradient(55rem 40rem at 50% 80%, rgba(255, 230, 180, 0.35) 0%, transparent 75%),
        linear-gradient(120deg, #fdf6f0 0%, #eaf4ff 50%, #f8f9ff 100%);
      background-attachment: fixed;
      color: #1a1a1a;
    }

    /* 🧊 Sidebar frosted panel */
    [data-testid="stSidebar"] > div:first-child {
      background: rgba(255, 255, 255, 0.45);
      backdrop-filter: blur(14px) saturate(180%);
      -webkit-backdrop-filter: blur(14px) saturate(180%);
      border-right: 1px solid rgba(255, 255, 255, 0.25);
      box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
    }

    /* Glass effects for components */
    [data-testid="stMetric"], div[data-testid="stExpander"] {
        box-shadow: 0 6px 16px rgba(0,0,0,0.12);
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.8);
        padding: 8px;
    }

    [data-testid="stPlotlyChart"] {
        box-shadow: 0 8px 22px rgba(0,0,0,0.15);
        border-radius: 12px;
        background: white;
        padding: 8px;
    }

    /* Tables */
    .stDataFrame, .stTable {
        box-shadow: 0 6px 18px rgba(0,0,0,0.12);
        border-radius: 12px;
        padding: 10px;
        background: white;
    }

    /* Buttons with gradient */
    .stButton > button {
        background: linear-gradient(90deg, #6366F1, #3B82F6);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 15px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #4F46E5, #2563EB);
        box-shadow: 0 6px 16px rgba(0,0,0,0.25);
        transform: translateY(-2px);
    }

    /* Main header styling */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #FF6B35, #F7931E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* Callout (info box) */
    .callout {
      font-family: 'Calibre Light','Calibre',
                   ui-sans-serif, system-ui, -apple-system,
                   'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      font-weight: 300;
      background: rgba(255, 255, 255, 0.9);
      border: 1px solid rgba(255, 255, 255, 0.3);
      color: #082F49;
      border-radius: 12px;
      padding: 14px 16px;
      margin: 12px 0;
      box-shadow: 0 10px 28px rgba(8, 47, 73, 0.16);
      backdrop-filter: blur(10px);
    }
    </style>
    """, unsafe_allow_html=True)

