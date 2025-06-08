import os
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod
from flask import Flask, request, Response

IOTHUB_CONNECTION_STRING = os.getenv("IOTHUB_CONNECTION_STRING")
DEVICE_ID = "edge-downlink"

if not IOTHUB_CONNECTION_STRING:
    raise ValueError("Missing IOTHUB_CONNECTION_STRING environment variable")

# Create the IoT Hub client
registry_manager = IoTHubRegistryManager(IOTHUB_CONNECTION_STRING)

app = Flask(__name__)

@app.route("/command", methods=["POST"])
def send_command():
    try:
        data = request.get_json()
        if not data:
            return {"status": "error", "message": "No data provided"}, 400

        method_name = data.get("methodName", "execute")  # Default to "execute" if not provided
        payload = data.get("payload", {})

        # Create a CloudToDeviceMethod object
        direct_method = CloudToDeviceMethod(
            method_name=method_name,
            payload=payload,
            response_timeout_in_seconds=30,
        )

        # Send the command to the device
        response = registry_manager.invoke_device_method(DEVICE_ID, direct_method)

        return Response(response.payload, status=response.status, content_type='application/json')
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
