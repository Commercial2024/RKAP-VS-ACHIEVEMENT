import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard RKAP vs Achievement", layout="wide")

st.title("📊 Dashboard RKAP vs Achievement IASH")

# Tombol untuk bersihkan cache data
st.cache_data.clear()

# Upload file Excel
uploaded_file = st.file_uploader("📂 Upload file Excel RKAP (format .xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()  # hapus spasi tersembunyi
        st.success("✅ Data berhasil dimuat!")

        # Kolom wajib minimal
        required_cols = ["Tahun", "Kategori", "RKAP", "Achievement"]
        missing_cols = [c for c in required_cols if c not in df.columns]

        if missing_cols:
            st.error(f"Kolom berikut belum ada di data: {', '.join(missing_cols)}")
        else:
            # Tampilkan data
            st.dataframe(df)

            # Filter dinamis
            tahun_opsi = df["Tahun"].unique().tolist() if "Tahun" in df.columns else []
            kategori_opsi = df["Kategori"].unique().tolist() if "Kategori" in df.columns else []
            bulan_opsi = df["Bulan"].unique().tolist() if "Bulan" in df.columns else []

            col1, col2, col3 = st.columns(3)
            with col1:
                tahun_filter = st.selectbox("📅 Pilih Tahun", ["Semua"] + list(map(str, tahun_opsi))) if tahun_opsi else "Semua"
            with col2:
                kategori_filter = st.selectbox("🏷️ Pilih Kategori", ["Semua"] + kategori_opsi) if kategori_opsi else "Semua"
            with col3:
                bulan_filter = st.selectbox("🗓️ Pilih Bulan", ["Semua"] + bulan_opsi) if bulan_opsi else "Semua"

            df_filtered = df.copy()
            if tahun_filter != "Semua":
                df_filtered = df_filtered[df_filtered["Tahun"].astype(str) == str(tahun_filter)]
            if kategori_filter != "Semua":
                df_filtered = df_filtered[df_filtered["Kategori"] == kategori_filter]
            if bulan_filter != "Semua" and "Bulan" in df_filtered.columns:
                df_filtered = df_filtered[df_filtered["Bulan"] == bulan_filter]

            # Hitung persentase pencapaian
            df_filtered["Persentase"] = (df_filtered["Achievement"] / df_filtered["RKAP"]) * 100

            # Grafik utama RKAP vs Achievement
            st.subheader("📈 Grafik RKAP vs Achievement")
            fig = px.bar(
                df_filtered,
                x="Kategori" if "Kategori" in df_filtered.columns else "Tahun",
                y=["RKAP", "Achievement"],
                barmode="group",
                title="Perbandingan RKAP dan Achievement",
                text_auto=".2s"
            )
            fig.update_traces(textfont_size=12)
            st.plotly_chart(fig, use_container_width=True)

            # Grafik tambahan Capture Ratio, PAX, Traffic
            optional_charts = ["Capture Ratio", "PAX", "Traffic"]
            for col in optional_charts:
                if col in df_filtered.columns:
                    st.subheader(f"📊 Grafik {col}")
                    fig2 = px.line(
                        df_filtered,
                        x="Kategori" if "Kategori" in df_filtered.columns else "Tahun",
                        y=col,
                        markers=True,
                        title=f"Tren {col} per Kategori"
                    )
                    st.plotly_chart(fig2, use_container_width=True)

    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")

else:
    st.info("⬆️ Silakan upload file Excel terlebih dahulu untuk melihat dashboard.")
