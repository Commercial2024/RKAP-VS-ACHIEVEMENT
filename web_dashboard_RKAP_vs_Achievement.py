import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================
# KONFIGURASI DASHBOARD
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
    return pd.read_excel("data_rkap.xlsx")

df = load_data()

# ==========================
# BERSIHKAN & STANDARISASI DATA
# ==========================
df = df.dropna(subset=["Tahun", "Bulan", "Kategori"])  # hilangkan baris kosong

# --- Normalisasi nama bulan agar konsisten ---
bulan_order = ["JAN", "FEB", "MAR", "APR", "MEI", "JUN", "JUL", "AUGUST", "SEPT", "OCT", "NOV", "DES"]
df["Bulan"] = df["Bulan"].astype(str).str.upper().str.strip()
df["Bulan"] = pd.Categorical(df["Bulan"], categories=bulan_order, ordered=True)
df = df.sort_values("Bulan")

# --- Pastikan Capture Ratio numerik (hilangkan tanda % atau koma) ---
if "Capture Ratio" in df.columns:
    df["Capture Ratio"] = (
        df["Capture Ratio"]
        .astype(str)
        .str.strip()
        .str.replace("%", "", regex=False)
        .str.replace(",", ".", regex=False)
    )
    df["Capture Ratio"] = pd.to_numeric(df["Capture Ratio"], errors="coerce")

    # Jika semua di bawah 1, artinya datanya dalam bentuk desimal (misal 0.45) → ubah ke persen
    if df["Capture Ratio"].mean(skipna=True) < 1:
        df["Capture Ratio"] = df["Capture Ratio"] * 100

# ==========================
# VALIDASI KOLOM
# ==========================
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

tahun_options = sorted(df["Tahun"].dropna().unique())
kategori_options = sorted(df["Kategori"].dropna().unique())
bulan_options = [b for b in bulan_order if b in df["Bulan"].unique()]

tahun_terpilih = col1.multiselect("📅 Pilih Tahun", tahun_options, default=tahun_options)
kategori_terpilih = col2.multiselect("🏷️ Pilih Kategori", kategori_options, default=kategori_options)
bulan_terpilih = col3.multiselect("🗓️ Pilih Bulan", bulan_options, default=bulan_options)

df_filter = df[
    (df["Tahun"].isin(tahun_terpilih))
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
st.subheader("📈 RKAP vs Achievement per Kategori")
fig1 = px.bar(
    df_filter,
    x="Kategori",
    y=["RKAP", "Achievement"],
    barmode="group",
    color_discrete_sequence=px.colors.qualitative.Set2,
)
fig1.update_traces(texttemplate="%{y:,.0f}", textposition="outside")
fig1.update_layout(yaxis_title="Nilai (Rp)", xaxis_title="Kategori", template="plotly_white")
st.plotly_chart(fig1, use_container_width=True)

# ==========================
# GRAFIK 2: CAPTURE RATIO PER BULAN
# ==========================
st.subheader("🎯 Capture Ratio per Bulan")
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
st.subheader("🧍‍♂️ PAX vs Traffic Bandara")
fig3 = px.line(
    df_filter,
    x="Bulan",
    y=["PAX", "Traffic"],
    markers=True,
    title="Perbandingan PAX & Traffic",
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig3.update_layout(yaxis_title="Jumlah Penumpang", xaxis_title="Bulan", template="plotly_white")
st.plotly_chart(fig3, use_container_width=True)

# ==========================
# TABEL DATA
# ==========================
st.subheader("📋 Data Detail")

df_tampil = df_filter.copy()

# Format angka agar rapi
for kol in ["RKAP", "Achievement", "PAX", "Traffic"]:
    if kol in df_tampil.columns:
        df_tampil[kol] = df_tampil[kol].apply(
            lambda x: f"{x:,.0f}" if pd.notna(x) and isinstance(x, (int, float)) else "-"
        )

# Pastikan Capture Ratio tampil dengan format persen
if "Capture Ratio" in df_tampil.columns:
    df_tampil["Capture Ratio"] = df_tampil["Capture Ratio"].apply(
        lambda x: f"{x:.1f}%" if pd.notna(x) and isinstance(x, (int, float)) else "-"
    )

st.dataframe(df_tampil, use_container_width=True)

st.markdown("---")
st.caption("© 2025 IAS Hospitality – Automated Performance Dashboard")

