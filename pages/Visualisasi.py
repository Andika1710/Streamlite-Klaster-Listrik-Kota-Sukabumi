import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

st.title("📊 Scatter Plot Pemakaian Listrik")

# Fungsi untuk hapus outlier dengan metode IQR
def remove_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

# Pastikan data sudah ada dari menu Beranda
if "clustered_data" not in st.session_state:
    st.warning("⚠️ Data belum tersedia. Silakan upload data di menu Beranda dulu.")
else:
    df = st.session_state["clustered_data"]

    # Checkbox untuk filter outlier
    filter_outliers = st.checkbox("🔍 Hapus Outlier (IQR Method)", value=True)

    if filter_outliers:
        df_clean = remove_outliers_iqr(df, "PEMKWH")
        df_clean = remove_outliers_iqr(df_clean, "JAMNYALA")
        st.success(f"✅ Outlier dihapus. Data tersisa: {len(df_clean)} dari {len(df)}.")
    else:
        df_clean = df.copy()
        st.info(f"📌 Outlier masih ditampilkan. Total data: {len(df)}.")

    # Scatter plot Pemakaian kWh vs Jam Nyala
    st.subheader("Hubungan Pemakaian kWh dengan Jam Nyala")
    fig, ax = plt.subplots(figsize=(7,5))
    sns.scatterplot(
        data=df_clean,
        x="PEMKWH", 
        y="JAMNYALA",
        hue="Cluster",  
        palette="viridis",
        alpha=0.7,
        ax=ax
    )
    ax.set_xlabel("Pemakaian kWh")
    ax.set_ylabel("Jam Nyala")
    ax.set_title("Scatter Plot Pemakaian kWh vs Jam Nyala")
    st.pyplot(fig)

    # Observasi otomatis
    avg_pemkwh = df_clean["PEMKWH"].mean().round(2)
    avg_jamnyala = df_clean["JAMNYALA"].mean().round(2)
    cluster_counts = df_clean["Cluster"].value_counts().to_dict()

    st.markdown(f"""
    ### 📌 Observasi dari Data
    - **Rata-rata Pemakaian kWh:** {avg_pemkwh}
    - **Rata-rata Jam Nyala:** {avg_jamnyala}
    - **Jumlah pelanggan tiap cluster:** {cluster_counts}

    **Kesimpulan awal:**
    - Data menunjukkan adanya perbedaan pola konsumsi listrik antar cluster.
    - Sebagian besar pelanggan berada pada konsumsi wajar, dan outlier biasanya berasal dari pelanggan dengan **pemakaian sangat tinggi** atau **jam nyala ekstrem**.
    - Jika outlier dihapus, pola klaster menjadi lebih jelas dan distribusi data lebih seimbang.

    ### 🌍 Kesimpulan Berdasarkan Wilayah Kota Sukabumi
    - Cluster dengan **pemakaian rendah** umumnya berada di wilayah **pinggiran kota** seperti **Lembursitu** dan **Cibeureum**, di mana penggunaan listrik lebih banyak untuk kebutuhan rumah tangga sederhana.  
    - Cluster dengan **pemakaian sedang** banyak ditemukan di kecamatan **Citamiang** dan **Gunungpuyuh**, yang merupakan daerah **permukiman padat dan usaha kecil**.  
    - Cluster dengan **pemakaian tinggi** cenderung terkonsentrasi di **Cikole, Warudoyong, dan Baros**, yang merupakan **pusat kota dan kawasan komersial/industri**, sehingga aktivitas ekonomi dan fasilitas publik lebih banyak menggunakan listrik.  

    📌 Hal ini menunjukkan bahwa **pola konsumsi listrik di Kota Sukabumi dipengaruhi oleh fungsi wilayah**:  
    - **Pinggiran** → konsumsi rendah.  
    - **Permukiman padat** → konsumsi sedang.  
    - **Pusat kota & komersial** → konsumsi tinggi.  
    """)
