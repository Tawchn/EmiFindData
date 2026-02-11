import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

# --- PAGE SETTINGS ---
st.set_page_config(page_title="EmiFindData Web", layout="wide")

# --- CUSTOM CSS FOR THE NEON THEME ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR LOGO & BRANDING ---
try:
    logo = Image.open("IMG_8009.jpeg")
    st.sidebar.image(logo, use_container_width=True)
except:
    st.sidebar.title("EmiFindData")

st.sidebar.write("### Created by Tawanda Mucheriwa")
st.sidebar.divider()

# --- ANALYSIS FUNCTIONS ---
def get_data_profile(df):
    """Industry standard column profiling."""
    stats = []
    for col in df.columns:
        nulls = df[col].isnull().sum()
        dtype = str(df[col].dtype)
        unique_val = df[col].nunique()
        # Suggesting column status
        status = "🔑 Potential Key" if (df[col].is_unique and nulls == 0) else "Data Field"
        stats.append({
            "Column": col, 
            "Type": dtype, 
            "Missing": nulls, 
            "Unique Count": unique_val,
            "Analysis": status
        })
    return pd.DataFrame(stats)

# --- MAIN INTERFACE ---
st.title("🔬 EmiFindData Web Profiler")

# Replaces your manual buttons with a professional file uploader
uploaded_files = st.sidebar.file_uploader("Upload CSV or Excel", accept_multiple_files=True)

if uploaded_files:
    # 1. Select the Dataset
    filenames = [file.name for file in uploaded
