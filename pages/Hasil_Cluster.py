import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

st.title("📊 Hasil Clustering")

if "data" not in st.session_state:
    st.warning("⚠️ Silakan upload data di halaman Data Awal terlebih dahulu.")
else:
    df = st.session_state["data"].copy()

    required_cols = ["DAYA", "PEMKWH", "JAMNYALA", "KECAMATAN"]
    if not all(col in df.columns for col in required_cols):
        st.error(f"Kolom wajib {required_cols} tidak ditemukan di file!")
    else:
        # Fitur numerik
        features = ["DAYA", "PEMKWH", "JAMNYALA"]
        X = df[features]

        # Normalisasi
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # K-Means
        kmeans = KMeans(n_clusters=3, random_state=42)
        df["Cluster"] = kmeans.fit_predict(X_scaled) + 1

        # --- LANGKAH PENGURUTAN KLASTER BARU ---
        cluster_means_pemkwh = df.groupby("Cluster")["PEMKWH"].mean()
        sorted_clusters = cluster_means_pemkwh.sort_values().index.tolist()
        cluster_remapping = {old_id: new_id for new_id, old_id in enumerate(sorted_clusters, 1)}
        df["Cluster"] = df["Cluster"].map(cluster_remapping)

        # Kategori sesuai urutan baru
        kategori_map = {
             1: "Pemakaian Rendah",
             2: "Pemakaian Sedang",
             3: "Pemakaian Tinggi"
        }
        df["Kategori"] = df["Cluster"].map(kategori_map)

        st.session_state["clustered_data"] = df

        # --- REKAP CLUSTER DENGAN KECAMATAN (sudah terurut) ---
        rekap_cluster = df.groupby("Cluster").agg(
            DAYA_rata2=("DAYA", "mean"),
            PEMKWH_rata2=("PEMKWH", "mean"),
            JAMNYALA_rata2=("JAMNYALA", "mean"),
            Jumlah_Data=("Cluster", "count")
        ).round(2)
        rekap_cluster["Kategori"] = rekap_cluster.index.map(kategori_map)
        most_frequent_kecamatan = df.groupby("Cluster")["KECAMATAN"].agg(lambda x: x.mode()[0])
        rekap_cluster["Kecamatan_Dominan"] = most_frequent_kecamatan

        st.subheader("📌 Ringkasan Setiap Klaster (Terurut Berdasarkan Pemakaian KWh)")
        st.markdown("Tabel ini menunjukkan karakteristik klaster yang sudah diurutkan dari pemakaian **KWh terendah (Klaster 1)** hingga **tertinggi (Klaster 3)**.")

        # Tambahkan kolom No agar mulai dari 1, sembunyikan index Pandas
        rekap_display = rekap_cluster.reset_index()
        rekap_display.insert(0, "No", range(1, len(rekap_display) + 1))
        st.dataframe(rekap_display, hide_index=True)

        # Keterangan tiap klaster
        st.subheader("📝 Keterangan Per Klaster (Terurut)")
        for i, row in rekap_cluster.iterrows():
            st.markdown(f"""
            **Klaster {i} ({row['Kategori']})** - Jumlah Data: {row['Jumlah_Data']}  
            - Rata-rata Daya: {row['DAYA_rata2']}  
            - Rata-rata Pemakaian KWh: {row['PEMKWH_rata2']}  
            - Rata-rata Jam Nyala: {row['JAMNYALA_rata2']}  
            - **Kecamatan Dominan:** {row['Kecamatan_Dominan']}
            """)

        # --- FITUR PENCARIAN KECAMATAN ---
        st.markdown("---")
        st.subheader("🔍 Cari Informasi Kecamatan")
        
        nama_kecamatan = st.text_input("Masukkan nama kecamatan:", "").strip().title()

        if nama_kecamatan:
            kecamatan_data = df[df["KECAMATAN"].str.title() == nama_kecamatan]
            
            if not kecamatan_data.empty:
                avg_data = kecamatan_data.groupby("KECAMATAN").agg(
                    Cluster=('Cluster', lambda x: x.mode()[0]),
                    PEMKWH_rata2=("PEMKWH", "mean"),
                    JAMNYALA_rata2=("JAMNYALA", "mean")
                ).round(2).reset_index()

                avg_data.insert(0, "No", range(1, len(avg_data) + 1))
                st.markdown(f"**Hasil untuk Kecamatan {nama_kecamatan}:**")
                st.dataframe(avg_data, hide_index=True)
            else:
                st.warning(f"Kecamatan '{nama_kecamatan}' tidak ditemukan dalam data.")
        else:
            st.info("Silakan masukkan nama kecamatan untuk memulai pencarian.")

        # --- DAFTAR KECAMATAN PER KLASTER ---
        st.markdown("---")
        st.subheader("🗺️ Daftar Klaster Setiap Kecamatan")
        st.markdown("Tabel ini menunjukkan klaster rata-rata (klaster yang paling sering muncul) untuk setiap kecamatan, sesuai dengan urutan yang sudah diperbarui.")

        kecamatan_klaster = df.groupby('KECAMATAN')['Cluster'].mean().round(0).astype(int).reset_index()
        kecamatan_klaster.insert(0, "No", range(1, len(kecamatan_klaster) + 1))
        st.dataframe(kecamatan_klaster, hide_index=True)
        
        st.subheader("Daftar Kecamatan per Klaster (Grup)")
        for cluster_id, group in kecamatan_klaster.groupby('Cluster'):
            st.markdown(f"**Klaster {cluster_id}** ({kategori_map.get(cluster_id, 'Tidak Dikenal')})")
            st.markdown(", ".join(group['KECAMATAN'].tolist()))
            st.markdown("---")
