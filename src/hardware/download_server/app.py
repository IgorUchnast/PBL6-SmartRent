import os
import time
import requests
from azure.iot.device import IoTHubDeviceClient, MethodResponse  # type: ignore

LED_URL = "http://localhost:5000/led"
OUTLET_URL = "http://localhost:5000/outlet"

CONNECTION_STRING = os.getenv("CONNECTION_STRING")

if not CONNECTION_STRING:
    raise ValueError("Missing CONNECTION_STRING in environment variables")

client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
client.connect()

def handle_method(request):
    print("== RECEIVED COMMAND ==")
    print(f"Name: {request.name}")
    print(f"Payload: {request.payload}")

    status = 200
    response_payload = {"result": "Command executed"}

    try:
        if request.name == "execute":
            cmd = request.payload.get("command")

            if cmd == "turn_off_led":
                requests.post(LED_URL, json={"command": "off"})
            elif cmd == "turn_on_led":
                requests.post(LED_URL, json={"command": "on"})
            elif cmd == "set_led_auto":
                requests.post(LED_URL, json={"command": "auto"})
            elif cmd == "turn_off_outlet":
                requests.post(OUTLET_URL, json={"command": "off"})
            elif cmd == "turn_on_outlet":
                requests.post(OUTLET_URL, json={"command": "on"})
            else:
                status = 400
                response_payload = {"error": f"Unknown command: {cmd}"}
        else:
            status = 404
            response_payload = {"error": "Unknown request name"}
    except Exception as e:
        print("Error while executing command:", e)
        status = 500
        response_payload = {"error": str(e)}

    # Respond to IoTHub
    method_response = MethodResponse.create_from_method_request(request, status, response_payload)
    try:
        client.send_method_response(method_response)
        print(f"Response sent to cloud (status: {status})\n")
    except Exception as e:
        print("Error while responding to cloud:", e)

client.on_method_request_received = handle_method

# Main loop
print("Listening for commands from IoTHub...")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Closing connection...")
    client.shutdown()
