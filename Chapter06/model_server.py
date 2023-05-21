import os
import json
import numpy as np
from flask import Flask, request
import joblib
import json

model_artifact = joblib.load("./model.joblib")
scaler = model_artifact["scaler"]
logreg_model = model_artifact["logreg_model"]
model_threshold = model_artifact["logreg_model_threshold"]

def pre_process(data):
    raw_input = [data[feature_name] for feature_name in sorted(data.keys())]
    scaled_input = scaler.transform([raw_input])
    return scaled_input

def make_prediction(input_payload):
    prediction_probabilities = logreg_model.predict_proba(input_payload)
    predictions = [1 if p[1] > model_threshold else 0 for p in prediction_probabilities]
    return predictions

def post_process(output):
    label_dict = {0: "Genuine", 1: "Fraud"}
    final_output = [label_dict[o] for o in output]
    return str(final_output)

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json["data"]
    input_array = pre_process(data)
    output = make_prediction(input_array)
    final_output = post_process(output)
    return final_output

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8890)