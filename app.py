from flask import Flask, jsonify, request, render_template
import logging
import requests
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os
import joblib
import time 

app = Flask(__name__)

# URL API untuk mendapatkan data sensor dengan metode GET
api_url_get = 'https://bqek2kufrh.execute-api.us-east-1.amazonaws.com/coba/smartsoil'

# Definisikan fitur yang digunakan secara global
features = ['Nitrogen', 'Phosphor', 'Kalium', 'Temperature', 'Humidity', 'ph', 'Conductivity']

# Load model saat aplikasi dimulai
model_filename = 'crop_recommendation_model.joblib'
if os.path.exists(model_filename):
    model = joblib.load(model_filename)
else:
    model = None

# Cache data API
cached_sensor_data = None

def get_data_from_api():
    global cached_sensor_data
    if cached_sensor_data is not None:
        return cached_sensor_data

    try:
        response = requests.get(api_url_get)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        df = pd.DataFrame(data)
        df = df[['Nitrogen', 'Phosphor', 'Kalium', 'Temperature', 'Moisture', 'pH', 'Conductivity']]
        df.rename(columns={'pH': 'ph', 'Moisture': 'Humidity'}, inplace=True)
        cached_sensor_data = df
        return df
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch data from API: {str(e)}")
        return None
    except ValueError as e:
        logging.error(f"Failed to parse JSON response: {str(e)}")
        return None

def predict_crop(data):
    try:
        input_df = pd.DataFrame([data])
        prediction = model.predict(input_df[features].values)
        return prediction.tolist()
    except Exception as e:
        logging.error(f"Failed to predict crop: {str(e)}")
        return None

@app.route('/')
def home():
    sensor_data = get_data_from_api()
    if sensor_data is None:
        sensor_data = []  # Jika gagal mengambil data, atur menjadi list kosong
    elif isinstance(sensor_data, pd.DataFrame):
        sensor_data = sensor_data.to_dict(orient='records')

    return render_template('index.html', sensor_data=sensor_data)

@app.route('/Rekomendasi')
def rekomendasi():
    return render_template('Rekomendasi.html')

@app.route('/GPS')
def gps():
    return render_template('GPS.html')

@app.route('/data', methods=['GET'])
def get_data():
    sensor_data = get_data_from_api()
    if sensor_data is None:
        return jsonify({'message': 'Failed to fetch data from API'}), 400
    return jsonify(sensor_data.to_dict(orient='records'))

@app.route('/train', methods=['GET'])
def train_model():
    start_time = time.time()  # Mulai menghitung waktu
    sensor_data = get_data_from_api()
    if sensor_data is None or sensor_data.empty:
        return jsonify({'message': 'Failed to fetch data from API or no data available'}), 400

    dataset_path = 'Crop_recommendation.csv'
    dataset = pd.read_csv(dataset_path)
    features = ['Nitrogen', 'Phosphor', 'Kalium', 'Temperature', 'Humidity', 'ph']
    target = 'Label'
    
    combined_data = pd.concat([sensor_data[features], dataset[features + [target]]], ignore_index=True)
    combined_data.dropna(inplace=True)
    
    X = combined_data[features].values
    y = combined_data[target].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Simpan model yang telah dilatih ke dalam file
    model_filename = 'crop_recommendation_model.joblib'
    joblib.dump(model, model_filename)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    end_time = time.time()
    training_time = end_time - start_time  # Hitung waktu total pelatihan

    logging.info(f"Model trained successfully in {training_time:.2f} seconds")

    return jsonify({'accuracy': accuracy, 'training_time': training_time, 'message': 'Model trained successfully'})

@app.route('/predict', methods=['GET'])
def predict():
    sensor_data = get_data_from_api()
    if sensor_data is None or sensor_data.empty:
        return jsonify({'message': 'Failed to fetch data from API or no data available'}), 400

    # Load model dari file
    model_filename = 'crop_recommendation_model.joblib'
    if not os.path.exists(model_filename):
        return jsonify({'message': 'Model not found'}), 500

    model = joblib.load(model_filename)

    # Hanya menggunakan data terakhir untuk prediksi
    last_data = sensor_data.iloc[-1:]

    dataset_path = 'Crop_recommendation.csv'
    dataset = pd.read_csv(dataset_path)
    features = ['Nitrogen', 'Phosphor', 'Kalium', 'Temperature', 'Humidity', 'ph']
    target = 'Label'

    combined_data = pd.concat([sensor_data[features], dataset[features + [target]]], ignore_index=True)
    combined_data.dropna(inplace=True)

    prediction = model.predict(last_data[features].values)

    return jsonify({'prediction': prediction.tolist()})

@app.route('/manual_predict', methods=['POST'])
def manual_predict():
    try:
        # Ambil data dari formulir HTML
        input_data = {
            'Nitrogen': float(request.form['inputNitrogen']),
            'Phosphor': float(request.form['inputPhosphor']),
            'Kalium': float(request.form['inputKalium']),
            'Temperature': float(request.form['inputTemperature']),
            'Humidity': float(request.form['inputHumidity']),
            'ph': float(request.form['inputPh']),
            'Conductivity': float(request.form['inputConductivity'])
        }
        
        # Ubah data menjadi DataFrame untuk prediksi
        input_df = pd.DataFrame([input_data])
        
        # Lakukan prediksi menggunakan model yang sudah ada
        if model is None:
            return jsonify({'message': 'Model not found'}), 500

        prediction = model.predict(input_df[features].values)

        return jsonify({'prediction': prediction.tolist()})
    
    except Exception as e:
        return jsonify({'message': str(e)}), 400

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
