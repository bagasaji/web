from flask import Flask, jsonify, request, render_template
import logging
import requests
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

app = Flask(__name__)

# URL API untuk mendapatkan data sensor dengan metode GET
api_url_get = 'https://bqek2kufrh.execute-api.us-east-1.amazonaws.com/coba/smartsoil'

# Fungsi untuk mengambil data dari API sensor dengan metode GET
def get_data_from_api():
    response = requests.get(api_url_get)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        df = df[['Nitrogen', 'Phosphor', 'Kalium', 'Temperature', 'Moisture', 'pH']]
        df.rename(columns={'pH': 'ph', 'Moisture': 'Humidity'}, inplace=True)
        return df
    else:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def get_data():
    sensor_data = get_data_from_api()
    if sensor_data is None:
        return jsonify({'message': 'Failed to fetch data from API'}), 400
    return sensor_data.to_json(orient='records')

@app.route('/train', methods=['GET'])
def train_model():
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

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    return jsonify({'accuracy': accuracy, 'message': 'Model trained successfully'})


@app.route('/predict', methods=['GET'])
def predict():
    sensor_data = get_data_from_api()
    if sensor_data is None or sensor_data.empty:
        return jsonify({'message': 'Failed to fetch data from API or no data available'}), 400

    dataset_path = 'Crop_recommendation.csv'
    dataset = pd.read_csv(dataset_path)
    features = ['Nitrogen', 'Phosphor', 'Kalium', 'Temperature', 'Humidity', 'ph']
    target = 'Label'

    combined_data = pd.concat([sensor_data[features], dataset[features + [target]]], ignore_index=True)
    combined_data.dropna(inplace=True)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(combined_data[features], combined_data[target])

    prediction = model.predict(sensor_data[features].values)

    return jsonify({'prediction': prediction.tolist()})

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
