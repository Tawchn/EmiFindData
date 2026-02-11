import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

# --- PAGE CONFIG ---
st.set_page_config(page_title="EmiFindData Web", layout="wide")

# --- LOGO & SIDEBAR ---
try:
    logo = Image.open("IMG_8009.jpeg")
    st.sidebar.image(logo, use_container_width=True)
except:
    st.sidebar.title("EmiFindData")

st.sidebar.write("### Created by Tawanda Mucheriwa")

# --- DATA PROFILING LOGIC ---
def get_profile(df):
    stats = []
    for col in df.columns:
        nulls = df[col].isnull().sum()
        dtype = str(df[col].dtype)
        is_unique = "✅" if df[col].is_unique else "❌"
        stats.append({"Column": col, "Type": dtype, "Missing": nulls, "Unique": is_unique})
    return pd.DataFrame(stats)

# --- WEB INTERFACE ---
st.title("🔬 EmiFindData: Professional Profiler")

uploaded_files = st.sidebar.file_uploader("Choose CSV or Excel files", accept_multiple_files=True)

if uploaded_files:
    # Use a dropdown to select which file to analyze
    filenames = [file.name for file in uploaded_files]
    selected_file = st.selectbox("Select dataset to analyze", filenames)
    
    # Load the selected file
    for file in uploaded_files:
        if file.name == selected_file:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
            
            # --- TABS ---
            tab1, tab2, tab3 = st.tabs(["📊 Profile Report", "🗂️ Data Preview", "🔗 Correlation"])
            
            with tab1:
                st.subheader("Data Health Report")
                profile_df = get_profile(df)
                st.dataframe(profile_df, use_container_width=True)
                
                # Content Discovery: Missing Values Chart
                st.subheader("Missing Value Discovery")
                fig, ax = plt.subplots()
                df.isnull().sum().plot(kind='bar', ax=ax, color='magenta')
                st.pyplot(fig)
                            
            with tab2:
                st.subheader("Raw Data Preview")
                st.write(df.head(100))
                
            with tab3:
                st.subheader("Relationship Discovery")
                # Only correlate numeric data
                numeric_df = df.select_dtypes(include=['number'])
                if not numeric_df.empty:
                    fig, ax = plt.subplots()
                    sns.heatmap(numeric_df.corr(), annot=True, cmap="mako", ax=ax)
                    st.pyplot(fig)
                                    else:
                    st.write("No numeric data found for correlation.")
else:
    st.info("Please upload a file in the sidebar to begin profiling.")
