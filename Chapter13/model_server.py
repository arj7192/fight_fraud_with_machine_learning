import os
import json
import numpy as np
from flask import Flask, request
import joblib
import json

model_artifact = joblib.load("./model.joblib")
features = model_artifact["ordered_columns"]
rf_model = model_artifact["rf_model"]
model_threshold = model_artifact["rf_model_threshold"]


def pre_process(data, features):
    data["amountOrig"] = data["oldbalanceOrg"] - data["newbalanceOrig"]
    data["amountDest"] = data["oldbalanceDest"] - data["newbalanceDest"]
    data["errorBalanceOrig"] = data["amount"] - data["amountOrig"]
    data["errorBalanceDest"] = data["amount"] - data["amountDest"]
    for cat_f in ["CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"]:
        data[cat_f] = 1 if data["type"] == cat_f else 0
    data = [data[f] for f in features]
    return [data]

def make_prediction(input_payload, model, threshold):
    prediction_probabilities = rf_model.predict_proba(input_payload)
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
    input_array = pre_process(data, features)
    output = make_prediction(input_array, rf_model, model_threshold)
    final_output = post_process(output)
    return final_output

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8890)