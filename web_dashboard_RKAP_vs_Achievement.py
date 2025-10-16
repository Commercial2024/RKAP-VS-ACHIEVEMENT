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

col1, col2, col3 = st.columns(3)
tahun_terpilih = col1.selectbox("Pilih Tahun", sorted(df["Tahun"].unique()))
kategori_terpilih = col2.multiselect("Pilih Kategori", df["Kategori"].unique(), default=list(df["Kategori"].unique()))
bulan_terpilih = col3.multiselect("Pilih Bulan", df["Bulan"].unique(), default=list(df["Bulan"].unique()))

df_filter = df[
    (df["Tahun"] == tahun_terpilih)
    & (df["Kategori"].isin(kategori_terpilih))
    & (df["Bulan"].isin(bulan_terpilih))
]

# ==========================
# METRIK UTAMA
# ==========================
col1, col2, col3 = st.columns(3)
col1.metric("Total RKAP", f"Rp {df_filter['RKAP'].sum():,.0f}")
col2.metric("Total Achievement", f"Rp {df_filter['Achievement'].sum():,.0f}")
col3.metric("Rata-rata Capture Ratio", f"{df_filter['Capture Ratio'].mean():.1f}%")

# ==========================
# GRAFIK 1: RKAP vs ACHIEVEMENT
# ==========================
st.subheader(f"📈 RKAP vs Achievement per Kategori - {tahun_terpilih}")
fig1 = px.bar(
    df_filter,
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
# GRAFIK 2: CAPTURE RATIO PER BULAN
# ==========================
st.subheader(f"🎯 Capture Ratio per Bulan - {tahun_terpilih}")
fig2 = px.line(
    df_filter,
    x="Bulan",
    y="Capture Ratio",
    color="Kategori",
    markers=True,
    color_discrete_sequence=px.colors.qualitative.Prism
)
fig2.update_layout(yaxis_title="Capture Ratio (%)", xaxis_title="Bulan", template="plotly_white")
st.plotly_chart(fig2, use_container_width=True)

# ==========================
# GRAFIK 3: PAX VS TRAFFIC
# ==========================
st.subheader(f"🧍‍♂️ PAX vs Traffic Bandara - {tahun_terpilih}")
fig3 = px.line(
    df_filter,
    x="Bulan",
    y=["PAX", "Traffic"],
    markers=True,
    title=f"Perbandingan PAX & Traffic {tahun_terpilih}",
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig3.update_layout(yaxis_title="Jumlah Penumpang", xaxis_title="Bulan", template="plotly_white")
st.plotly_chart(fig3, use_container_width=True)

# ==========================
# TABEL DATA
# ==========================
st.subheader("📋 Data Detail")
st.dataframe(df_filter, use_container_width=True)

st.markdown("---")
st.caption("© 2025 IAS Hospitality – Automated Performance Dashboard")
