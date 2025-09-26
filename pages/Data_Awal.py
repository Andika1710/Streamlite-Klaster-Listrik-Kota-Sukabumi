import streamlit as st
import pandas as pd

st.title("📄 Data Awal")

# Baca file CSV langsung dari folder project
# Pastikan file 'data.csv' ada di direktori yang sama dengan script ini
df = pd.read_csv("data.csv")

# Simpan di session agar bisa dipakai di halaman lain
st.session_state["data"] = df

st.success(f"✅ Data berhasil dimuat ({len(df)} baris)")

# Tambahkan kolom No mulai dari 1
df_display = df.head().copy()
df_display.insert(0, "No", range(1, len(df_display) + 1))

st.dataframe(df_display, use_container_width=True, hide_index=True)
