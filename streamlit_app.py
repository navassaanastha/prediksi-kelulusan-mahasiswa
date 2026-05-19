import streamlit as st
import pandas as pd
import joblib

# load model
model = joblib.load('model_kelulusan.pkl')

st.set_page_config(page_title="Prediksi Kelulusan", layout="centered")

st.title("Dashboard Prediksi Kelulusan Mahasiswa")

tahun_masuk = st.number_input("Tahun Masuk", 2015, 2030, 2019)
ipk = st.number_input("IPK", 0.0, 4.0, 3.5)
jumlah_mk_gagal = st.number_input("Jumlah MK Gagal", 0, 20, 1)
sks_lulus = st.number_input("SKS Lulus", 0, 200, 140)
status_skripsi = st.number_input("Status Skripsi (0-4)", 0, 4, 4)
jumlah_bimbingan = st.number_input("Jumlah Bimbingan", 0, 50, 12)

if st.button("Prediksi"):

    data_baru = pd.DataFrame({
        'tahun_masuk': [tahun_masuk],
        'ipk': [ipk],
        'jumlah_mk_gagal': [jumlah_mk_gagal],
        'sks_lulus': [sks_lulus],
        'status_skripsi': [status_skripsi],
        'jumlah_bimbingan': [jumlah_bimbingan]
    })

    hasil = model.predict(data_baru)

    if hasil[0] == 1:
        st.success("Mahasiswa diprediksi LULUS TEPAT WAKTU")
        st.info("Pertahankan performa akademik dan progres skripsi.")
    else:
        st.error("Mahasiswa BERESIKO TIDAK LULUS TEPAT WAKTU")
        st.warning("Perlu monitoring akademik dan peningkatan bimbingan.")