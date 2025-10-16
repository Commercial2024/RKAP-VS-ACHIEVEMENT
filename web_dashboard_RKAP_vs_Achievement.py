import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================
# CONFIGURASI DASHBOARD
# ==========================
st.set_page_config(page_title="Dashboard RKAP vs Achievement IASH", layout="wide")

st.markdown(
    """
    <style>
    .main {
        background-color: #F7F9FC;
    }
    h1, h2, h3 {
        color: #004080;
        font-family: 'Helvetica Neue', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================
# LOAD DATA
# ==========================
@st.cache_data
def load_data():
    return pd.read_excel("data_rkap_final.xlsx")

df = load_data()

# Validasi kolom wajib
required_cols = ["Tahun", "Bulan", "Kategori", "RKAP", "Achievement", "Capture Ratio", "PAX", "Traffic"]
missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"Kolom berikut belum ada di data: {', '.join(missing)}")
    st.stop()

# ==========================
# FILTER (TAHUN, KATEGORI, BULAN)
# ==========================
st.title("📊 Dashboard RKAP vs Achievement IASH")
st.markdown("### Perbandingan RKAP, Achievement, Capture Ratio, PAX, dan Traffic per Bulan & Kategori")

col1, col

