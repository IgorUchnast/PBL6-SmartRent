from flask import Flask, request, jsonify
from azure.iot.device import IoTHubDeviceClient, Message # type: ignore
import os
import requests

POST_URL = os.getenv("POST_URL", False)
CONNECTION_STRING = os.getenv("CONNECTION_STRING", None)

client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
client.connect()

msg = Message('{"temperature": 24.5}')
client.send_message(msg)

app = Flask(__name__)

@app.route("/forward", methods=["POST"])
def forward_request():
    data = request.get_json()
    # Only forward if POST_URL is set
    if POST_URL:
        try:
            response = requests.post(POST_URL, json=data)
            return jsonify({"status": "success", "data": response.json()}), response.status_code
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        print("Received data:", data)
    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
