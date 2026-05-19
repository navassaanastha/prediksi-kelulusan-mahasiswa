import streamlit as st
import pandas as pd
import joblib

# load model
model = joblib.load('model_kelulusan.pkl')

st.set_page_config(page_title="Prediksi Kelulusan", layout="centered")

st.set_page_config(
    page_title="Prediksi Kelulusan Mahasiswa",
    layout="centered"
)

st.markdown("""
<h1 style='
text-align: center;
font-size: 55px;
font-weight: 800;
background: linear-gradient(90deg, #8B5CF6, #EC4899);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
margin-bottom: 10px;
'>
Dashboard Prediksi Kelulusan Mahasiswa
</h1>

<p style='
text-align: center;
font-size:18px;
color:#9CA3AF;
margin-top:0px;
'>
Sistem Early Warning Prediksi Kelulusan Mahasiswa Tepat Waktu
</p>

""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    tahun_masuk = st.number_input("Tahun Masuk", 2018, 2025, 2023)
    ipk = st.number_input("IPK", 0.0, 4.0, 3.0)
    jumlah_mk_gagal = st.number_input("Jumlah MK Gagal", 0, 20, 0)

with col2:
    sks_lulus = st.number_input("SKS Lulus", 0, 160, 120)

    status_skripsi = st.selectbox(
    "Status Skripsi",
    [
        "0 - Belum Mulai",
        "1 - Judul ACC",
        "2 - Sempro",
        "3 - Semhas",
        "4 - Skripsi"
    ]
)

    mapping_status = {
    "0 - Belum Mulai": 0,
    "1 - Judul ACC": 1,
    "2 - Sempro": 2,
    "3 - Semhas": 3,
    "4 - Skripsi": 4
}

    status_skripsi = mapping_status[status_skripsi]

    jumlah_bimbingan = st.number_input("Jumlah Bimbingan", 0, 30, 5)
    
st.markdown("<br>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 1, 1])

with c2:
    prediksi_btn = st.button("Prediksi", use_container_width=True)

if prediksi_btn:
    
    data_baru = pd.DataFrame({
        'tahun_masuk': [tahun_masuk],
        'ipk': [ipk],
        'jumlah_mk_gagal': [jumlah_mk_gagal],
        'sks_lulus': [sks_lulus],
        'status_skripsi': [status_skripsi],
        'jumlah_bimbingan': [jumlah_bimbingan]
    })

    hasil = model.predict(data_baru)

    st.markdown("<br>", unsafe_allow_html=True)

    if hasil[0] == 1:
        st.success("Mahasiswa diprediksi LULUS TEPAT WAKTU")
        st.info("Pertahankan performa akademik dan progres skripsi.")
    else:
        st.error("Mahasiswa BERESIKO TIDAK LULUS TEPAT WAKTU")
        st.warning("Perlu monitoring akademik, peningkatan bimbingan, dan evaluasi mata kuliah gagal.")

    data_baru = pd.DataFrame({
        'tahun_masuk': [tahun_masuk],
        'ipk': [ipk],
        'jumlah_mk_gagal': [jumlah_mk_gagal],
        'sks_lulus': [sks_lulus],
        'status_skripsi': [status_skripsi],
        'jumlah_bimbingan': [jumlah_bimbingan]
    })