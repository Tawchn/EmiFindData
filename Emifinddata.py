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
    filenames = [file.name for file in uploaded_files]
    selected_name = st.selectbox("Select a dataset to explore:", filenames)
    
    # 2. Load Data
    for file in uploaded_files:
        if file.name == selected_name:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)

            # 3. Create Dashboard Tabs
            tab1, tab2, tab3 = st.tabs(["📊 Quality Profile", "🗂️ Data Browser", "🔗 Correlations"])

            with tab1:
                st.subheader(f"Data Health: {selected_name}")
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Column-level profile
                    profile_df = get_data_profile(df)
                    st.dataframe(profile_df, use_container_width=True)
                
                with col2:
                    # Visual Missing Value Summary
                    st.write("**Missing Values Discovery**")
                    null_counts = df.isnull().sum()
                    if null_counts.sum() > 0:
                        fig, ax = plt.subplots()
                        null_counts[null_counts > 0].plot(kind='barh', ax=ax, color='#ff00ff')
                        st.pyplot(fig)
                    else:
                        st.success("Clean Data! No missing values found.")

            with tab2:
                st.subheader("Interactive Table")
                st.dataframe(df, use_container_width=True)

            with tab3:
                st.subheader("Relationship Discovery")
                # Professional correlation heatmap (like your IMG_c545fe.png)
                numeric_df = df.select_dtypes(include=['number'])
                if not numeric_df.empty:
                    fig, ax = plt.subplots(figsize=(10, 8))
                    sns.heatmap(numeric_df.corr(), annot=True, cmap="mako", ax=ax, fmt=".2f")
                    st.pyplot(fig)
                else:
                    st.warning("No numeric columns found for correlation analysis.")
else:
    # Instructions if nothing is uploaded
    st.info("👋 Welcome to EmiFindData! Please upload a file in the sidebar to start profiling.")
