import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================
# CONFIGURASI DASHBOARD
# ==========================
st.set_page_config(page_title="Dashboard RKAP vs Achievement", layout="wide")

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
# LOAD DATA OTOMATIS (TANPA UPLOAD)
# ==========================
@st.cache_data
def load_data():
    return pd.read_excel("data_rkap.xlsx")

df = load_data()

# ==========================
# FILTER TAHUN
# ==========================
st.title("📊 Dashboard RKAP vs Achievement IASH")
st.markdown("### Perbandingan RKAP, Achievement, Capture Ratio, PAX, dan Traffic 2024–2025")

tahun_terpilih = st.selectbox("Pilih Tahun", sorted(df["Tahun"].unique()))
df_tahun = df[df["Tahun"] == tahun_terpilih]

# ==========================
# METRIK UTAMA
# ==========================
col1, col2, col3 = st.columns(3)
col1.metric("Total RKAP", f"Rp {df_tahun['RKAP'].sum():,.0f}")
col2.metric("Total Achievement", f"Rp {df_tahun['Achievement'].sum():,.0f}")
col3.metric("Rata-rata Capture Ratio", f"{df_tahun['Capture Ratio'].mean():.1f}%")

# ==========================
# GRAFIK 1: RKAP VS ACHIEVEMENT
# ==========================
st.subheader(f"📈 RKAP vs Achievement per Kategori - {tahun_terpilih}")
fig1 = px.bar(
    df_tahun,
    x="Kategori",
    y=["RKAP", "Achievement"],
    barmode="group",
    color_discrete_sequence=px.colors.qualitative.Set2,
    text="Kategori"
)
fig1.update_traces(textposition="outside", textfont=dict(size=12, color="#1C2833"))
fig1.update_layout(yaxis_title="Nilai (Rp)", xaxis_title="Kategori", template="plotly_white")
st.plotly_chart(fig1, use_container_width=True)

# ==========================
# GRAFIK 2: CAPTURE RATIO
# ==========================
st.subheader(f"🎯 Capture Ratio per Kategori - {tahun_terpilih}")
df_tahun["Label"] = df_tahun["Kategori"] + " - " + df_tahun["Capture Ratio"].astype(str) + "%"
fig2 = px.bar(
    df_tahun,
    x="Kategori",
    y="Capture Ratio",
    color="Capture Ratio",
    color_continuous_scale="Blues",
    text="Label"
)
fig2.update_traces(textposition="outside", textfont=dict(size=12, color="#1C2833"))
fig2.update_layout(yaxis_title="Capture Ratio (%)", xaxis_title="Kategori", template="plotly_white")
st.plotly_chart(fig2, use_container_width=True)

# ==========================
# GRAFIK 3: PAX VS TRAFFIC
# ==========================
st.subheader(f"🧍‍♂️ PAX vs Traffic Bandara - {tahun_terpilih}")
fig3 = px.line(
    df_tahun,
    x="Kategori",
    y=["PAX", "Traffic"],
    markers=True,
    color_discrete_sequence=px.colors.qualitative.Prism
)
fig3.update_layout(yaxis_title="Jumlah Penumpang", xaxis_title="Kategori", template="plotly_white")
st.plotly_chart(fig3, use_container_width=True)

# ==========================
# TABEL DATA
# ==========================
st.subheader("📋 Data Detail")
st.dataframe(df_tahun, use_container_width=True)

st.markdown("---")
st.caption("© 2025 IAS Hospitality – Automated Performance Dashboard")

