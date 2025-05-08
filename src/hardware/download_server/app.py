import requests
import time

URL = "http://sensor_server:5000/led"
MAX_RETRIES = 10

for attempt in range(MAX_RETRIES):
    try:
        response = requests.post(URL, json={"command": "auto"})
        print(f"Connected: {response.status_code}")
        break
    except requests.exceptions.ConnectionError as e:
        print(f"Connection failed (attempt {attempt+1}), retrying in 2s...")
        time.sleep(2)
else:
    print("Sensor server not responding after multiple attempts.")
