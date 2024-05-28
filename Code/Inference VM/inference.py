from flask import Flask, request, jsonify
import numpy as np
import h5py
import tensorflow as tf
import pickle

app = Flask(__name__)
i = 0
def windowing(flat, window_size=60):
    X = []
    row = [[x] for x in flat[0:0+window_size]]
    X.append(row)
    return np.array(X)

@app.route('/predict_pv', methods=['POST'])
def predict_pv():
    data = request.json
    light = data['light']
    voltage = data['voltage']
    current = best_pv_model.predict(np.array([light, voltage]).reshape(1, 2))
    solar_power = abs(voltage) * abs(current) * 0.001  # Amperes
    return jsonify({'solar_power': float(solar_power[0])})

@app.route('/predict_load', methods=['POST'])
def predict_load():
    records = X_test.shape[0]
    global i
    i = i+1 if i<records else 0
    estimate = abs(best_load_model.predict(X_test[i].reshape(1,60,1))[0][0])
    estimated_demand = scaler.inverse_transform(estimate.reshape(-1, 1))
    #with h5py.File('load_array.h5', 'r') as hf:
    #    load_array = np.array(hf['load_array'])
    #estimated_demand = abs(best_load_model.predict(windowing(load_array))[0][0])
    #estimated_demand = scaler.inverse_transform(estimated_demand.reshape(-1, 1))
    #print(estimated_demand.shape)
    #load_array = load_array[1:]
    #load_array = np.append(load_array, estimated_demand[0], axis=0)
    #print(load_array)
    #with h5py.File('load_array.h5', 'w') as hf:
    #    hf.create_dataset('load_array', data=load_array)
    return jsonify({'estimated_demand': float(estimated_demand)})

if __name__ == '__main__':
    best_pv_model = tf.keras.models.load_model('best_pv_readings_2.h5')
    best_load_model = tf.keras.models.load_model('lstm_load.keras')
    with open('minmax_scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    i = 0
    X_test = np.load('X_test.npy')
    app.run(host='0.0.0.0',debug=True)
