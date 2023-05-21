import time
import json
import requests


with open("./test_payload.json", "r") as f:
    json_payload = json.load(f)

start = time.time()
r = requests.post('http://127.0.0.1:8890/predict',
                  json={"data":json_payload})
inference_time = time.time() - start


response = r.content.decode("utf-8") 

print("Transaction(s) status:", response)
print("Inference time:", inference_time)
