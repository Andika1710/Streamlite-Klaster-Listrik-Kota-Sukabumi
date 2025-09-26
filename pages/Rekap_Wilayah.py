import streamlit as st
import pandas as pd

st.title("🌍 Rekap Wilayah per Kategori")

if "clustered_data" not in st.session_state:
    st.warning("⚠️ Jalankan clustering dulu di halaman Hasil Cluster.")
else:
    df = st.session_state["clustered_data"]

    # --- Bagian Rekap Wilayah ---
    st.markdown("""
    ### Hasil Rekapitulasi Wilayah per Kategori
    Tabel di bawah ini merangkum jumlah data yang masuk ke dalam setiap kategori klaster (tingkat pemakaian listrik) di setiap kecamatan. 
    Anda dapat melihat dan menganalisis sebaran pelanggan di setiap wilayah.
    """)
    rekap_wilayah = df.groupby(["Kategori", "KECAMATAN"]).size().reset_index(name="Jumlah_Data")

    # Tambahkan kolom No mulai dari 1, hapus index bawaan
    rekap_display = rekap_wilayah.copy()
    rekap_display.insert(0, "No", range(1, len(rekap_display) + 1))

    st.subheader("Tabel Rekap Wilayah per Kategori")
    st.dataframe(rekap_display, hide_index=True)

    st.download_button("⬇️ Download Rekap Wilayah",
                      rekap_display.to_csv(index=False).encode("utf-8"),
                      file_name="Rekap_Wilayah.csv",
                      mime="text/csv")
    
    # --- Bagian Penjelasan Hasil ---
    st.markdown("---")
    st.subheader("Analisis Hasil")
    st.markdown("""
    Berdasarkan data yang diolah, berikut adalah penjelasan dari setiap kategori klaster yang terbentuk:
    """)
    
    # Hitung total data per kategori untuk penjelasan
    total_data_per_kategori = df.groupby("Kategori").size().sort_values(ascending=False).reset_index(name='Jumlah')
    total_data_per_kategori.insert(0, "No", range(1, len(total_data_per_kategori) + 1))

    st.dataframe(total_data_per_kategori, hide_index=True)

    for index, row in total_data_per_kategori.iterrows():
        st.markdown(f"""
        **{row['Kategori']}**:  
        Kategori ini memiliki jumlah data sebanyak **{row['Jumlah']:,}** pelanggan. Ini adalah kelompok yang paling dominan/minoritas dalam data Anda.
        """)
