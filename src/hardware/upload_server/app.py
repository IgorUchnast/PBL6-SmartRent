import os
import json
from azure.iot.device import IoTHubDeviceClient, Message  # type: ignore
from flask import Flask, request, jsonify

CONNECTION_STRING = os.getenv("CONNECTION_STRING")

if not CONNECTION_STRING:
    raise ValueError("Missing CONNECTION_STRING in environment variables")

client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
client.connect()

app = Flask(__name__)

@app.route("/forward", methods=["POST"])
def forward_request():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400

        json_data = json.dumps(data)
        message = Message(json_data)

        client.send_message(message)

        print("Message sent to IoTHub:", json_data)
        return jsonify({"status": "success", "sent": data}), 200
        
    except Exception as e:
        print("Error processing request:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
