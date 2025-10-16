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
    .stMetricLabel {
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================
# HEADER
# ==========================
st.title("📊 Dashboard RKAP vs Achievement IASH")
st.markdown("### Data Perbandingan RKAP, Achievement, Capture Ratio, PAX, dan Traffic Tahun 2024–2025")

# ==========================
# UPLOAD FILE
# ==========================
uploaded_file = st.file_uploader("📂 Upload file Excel data RKAP", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Validasi kolom wajib
    required_cols = ["Tahun", "Kategori", "RKAP", "Achievement", "Capture Ratio", "PAX", "Traffic"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        st.error(f"Kolom berikut belum ada di data: {', '.join(missing)}")
        st.stop()

    # ==========================
    # FILTER TAHUN
    # ==========================
    tahun_terpilih = st.selectbox("Pilih Tahun", sorted(df["Tahun"].unique()))

    df_tahun = df[df["Tahun"] == tahun_terpilih]

    # ==========================
    # METRIK UTAMA
    # ==========================
    col1, col2, col3 = st.columns(3)
    total_rkap = df_tahun["RKAP"].sum()
    total_ach = df_tahun["Achievement"].sum()
    avg_ratio = df_tahun["Capture Ratio"].mean()

    col1.metric("Total RKAP", f"Rp {total_rkap:,.0f}")
    col2.metric("Total Achievement", f"Rp {total_ach:,.0f}")
    col3.metric("Rata-rata Capture Ratio", f"{avg_ratio:.1f}%")

    # ==========================
    # GRAFIK 1 - RKAP vs ACHIEVEMENT
    # ==========================
    st.subheader(f"📈 RKAP vs Achievement per Kategori - {tahun_terpilih}")
    fig1 = px.bar(
        df_tahun,
        x="Kategori",
        y=["RKAP", "Achievement"],
        barmode="group",
        color_discrete_sequence=px.colors.qualitative.Set2,
        text="Kategori"  # Label kategori di atas batang
    )
    fig1.update_traces(
        textposition="outside",
        textfont=dict(size=12, color="#1C2833")
    )
    fig1.update_layout(
        yaxis_title="Nilai (Rp)",
        xaxis_title="Kategori",
        template="plotly_white"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # ==========================
    # GRAFIK 2 - CAPTURE RATIO
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
    fig2.update_traces(
        textposition="outside",
        textfont=dict(size=12, color="#1C2833")
    )
    fig2.update_layout(
        yaxis_title="Capture Ratio (%)",
        xaxis_title="Kategori",
        template="plotly_white"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # ==========================
    # GRAFIK 3 - PAX vs TRAFFIC
    # ==========================
    st.subheader(f"🧍‍♂️ PAX vs Traffic Bandara - {tahun_terpilih}")
    fig3 = px.line(
        df_tahun,
        x="Kategori",
        y=["PAX", "Traffic"],
        markers=True,
        title=f"Perbandingan Data PAX dan Traffic {tahun_terpilih}",
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    fig3.update_layout(
        yaxis_title="Jumlah Penumpang",
        xaxis_title="Kategori",
        template="plotly_white"
    )
    st.plotly_chart(fig3, use_container_width=True)

    # ==========================
    # TABEL DATA
    # ==========================
    st.subheader("📋 Data Detail")
    st.dataframe(df_tahun, use_container_width=True)

else:
    st.info("Silakan upload file Excel terlebih dahulu untuk melihat dashboard.")

st.markdown("---")
st.caption("© 2025 IAS Hospitality – Automated Performance Dashboard")
