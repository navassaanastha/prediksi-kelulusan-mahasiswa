from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

model = joblib.load('model_kelulusan.pkl')

@app.route('/')
def home():
    return render_template('index.html')

# PREDIKSI DARI FORM HTML
@app.route('/predict', methods=['POST'])
def predict():

    data_baru = pd.DataFrame({
        'tahun_masuk': [int(request.form['tahun_masuk'])],
        'bulan_lulus': [int(request.form['bulan_lulus'])],
        'ipk': [float(request.form['ipk'])],
        'jumlah_mk_gagal': [int(request.form['jumlah_mk_gagal'])],
        'sks_lulus': [int(request.form['sks_lulus'])],
        'status_skripsi': [int(request.form['status_skripsi'])],
        'jumlah_bimbingan': [int(request.form['jumlah_bimbingan'])]
    })

    hasil = model.predict(data_baru)
    
    if hasil[0] == 1:
        prediksi = "Mahasiswa diprediksi LULUS TEPAT WAKTU"
        rekomendasi = "Pertahankan performa akademik dan progres skripsi."
    else:
        prediksi = "Mahasiswa BERESIKO TIDAK LULUS TEPAT WAKTU"
        rekomendasi = "Perlu monitoring akademik, peningkatan bimbingan, dan evaluasi mata kuliah gagal."

    return render_template(
        'hasil.html',
        hasil_prediksi=prediksi,
        rekomendasi=rekomendasi
    )

# PREDIKSI DARI JSON / API
@app.route('/api/predict', methods=['GET', 'POST'])
def api_predict():

    # jika dibuka dari browser
    if request.method == 'GET':

        data = {
            'tahun_masuk': 2019,
            'bulan_lulus': 7,
            'ipk': 3.8,
            'jumlah_mk_gagal': 0,
            'sks_lulus': 145,
            'status_skripsi': 4,
            'jumlah_bimbingan': 14
        }

    # jika dari POST JSON
    else:

        data = request.get_json()

    data_baru = pd.DataFrame({
        'tahun_masuk': [int(data['tahun_masuk'])],
        'bulan_lulus': [int(data['bulan_lulus'])],
        'ipk': [float(data['ipk'])],
        'jumlah_mk_gagal': [int(data['jumlah_mk_gagal'])],
        'sks_lulus': [int(data['sks_lulus'])],
        'status_skripsi': [int(data['status_skripsi'])],
        'jumlah_bimbingan': [int(data['jumlah_bimbingan'])]
    })

    hasil = model.predict(data_baru)

    if hasil[0] == 1:
        prediksi = "LULUS TEPAT WAKTU"
        rekomendasi = "Pertahankan performa akademik dan progres skripsi."
    else:
        prediksi = "BERESIKO TIDAK LULUS TEPAT WAKTU"
        rekomendasi = "Perlu monitoring akademik, peningkatan bimbingan, dan evaluasi mata kuliah gagal."

    return jsonify({
        "input_data": data,
        "hasil_prediksi": prediksi,
        "nilai_prediksi": int(hasil[0]),
        "rekomendasi": rekomendasi
    })

if __name__ == '__main__':
    app.run(debug=True)