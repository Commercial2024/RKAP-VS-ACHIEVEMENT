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

# Hapus baris kosong pada kolom utama (biar tidak error di multiselect)
df = df.dropna(subset=["Tahun", "Bulan", "Kategori"])

# ==========================
# VALIDASI KOLOM
# ==========================
required_cols = ["Tahun", "Bulan", "Kategori", "RKAP", "Achievement", "Capture Ratio", "PAX", "Traffic"]
missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"Kolom berikut belum ada di data: {', '.join(missing)}")
    st.stop()

# ==========================
# URUTKAN BULAN
# ==========================
bulan_order = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
df["Bulan"] = pd.Categorical(df["Bulan"], categories=bulan_order, ordered=True)
df = df.sort_values("Bulan")

# ==========================
# FILTER PILIHAN
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
total_rkap = df_filter["RKAP"].sum()
total_ach = df_filter["Achievement"].sum()
selisih = total_ach - total_rkap
persen = (selisih / total_rkap * 100) if total_rkap != 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total RKAP", f"Rp {total_rkap:,.0f}")
col2.metric("Total Achievement", f"Rp {total_ach:,.0f}")
col3.metric("Rata-rata Capture Ratio", f"{df_filter['Capture Ratio'].mean():.1f}%")
col4.metric("Pencapaian vs RKAP", f"{persen:.1f}%", delta=f"{selisih:,.0f}",
            delta_color="normal" if selisih >= 0 else "inverse")

# ==========================
# WARNA & TEMPLATE
# ==========================
px.defaults.template = "plotly_white"
px.defaults.color_discrete_sequence = ["#004080", "#0074D9", "#7FDBFF", "#39CCCC", "#3D9970"]

# ==========================
# GRAFIK 1: RKAP vs ACHIEVEMENT
# ==========================
st.subheader("📈 RKAP vs Achievement per Kategori")
fig1 = px.bar(
    df_filter,
    x="Kategori",
    y=["RKAP", "Achievement"],
    barmode="group",
    text_auto=".2s"
)
fig1.update_layout(yaxis_title="Nilai (Rp)", xaxis_title="Kategori", template="plotly_white")
st.plotly_chart(fig1, use_container_width=True)

# ==========================
# GRAFIK 2: CAPTURE RATIO
# ==========================
st.subheader("🎯 Capture Ratio per Bulan")
fig2 = px.line(
    df_filter,
    x="Bulan",
    y="Capture Ratio",
    color="Kategori",
    markers=True
)
fig2.add_hline(y=100, line_dash="dot", line_color="red", annotation_text="Target 100%")
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
)
fig3.update_layout(yaxis_title="Jumlah Penumpang", xaxis_title="Bulan", template="plotly_white")
st.plotly_chart(fig3, use_container_width=True)

# ==========================
# FORMAT ANGKA UNTUK TABEL
# ==========================
df_tampil = df_filter.copy()
num_cols = ["RKAP", "Achievement", "Capture Ratio", "PAX", "Traffic"]
for col in num_cols:
    if col in df_tampil.columns:
        if col in ["RKAP", "Achievement"]:
            df_tampil[col] = df_tampil[col].apply(lambda x: f"Rp {x:,.0f}")
        elif col == "Capture Ratio":
            df_tampil[col] = df_tampil[col].apply(lambda x: f"{x:.1f}%")
        else:
            df_tampil[col] = df_tampil[col].apply(lambda x: f"{x:,.0f}")

# ==========================
# TABEL DATA
# ==========================
st.subheader("📋 Data Detail")
st.data_editor(df_tampil, use_container_width=True, height=400)

# ==========================
# DOWNLOAD DATA
# ==========================
st.download_button(
    label="📥 Download Data (CSV)",
    data=df_filter.to_csv(index=False).encode("utf-8"),
    file_name=f"rkap_vs_achievement_{'_'.join(map(str, tahun_terpilih))}.csv",
    mime="text/csv"
)

# ==========================
# FOOTER
# ==========================
st.markdown("---")
st.caption("© 2025 IAS Hospitality – Automated Performance Dashboard")
