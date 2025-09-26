import streamlit as st
import os

# Konfigurasi halaman
st.set_page_config(page_title="Analisis K-Means Pemakaian Listrik", layout="wide")

# Judul utama
st.title("⚡ Analisis Pemakaian Listrik dengan K-Means di Kota Sukabumi Berdasarkan Daya, Pemakaian KWH, dan Jam Nyala")

# Path logo (bisa taruh di folder 'assets')
logo_path = "logo.jpeg"  # ubah jadi "assets/logo.jpeg" kalau file di folder assets

# Cek apakah logo tersedia
if os.path.exists(logo_path):
    st.image(logo_path, caption="Analisis K-Means Listrik - Kota Sukabumi", use_container_width=True)
else:
    st.warning("⚠️ Logo tidak ditemukan. Pastikan file 'logo.jpeg' ada di folder project atau sesuaikan path-nya.")

# Deskripsi
st.write("Gunakan menu di sidebar untuk navigasi antara halaman.")
