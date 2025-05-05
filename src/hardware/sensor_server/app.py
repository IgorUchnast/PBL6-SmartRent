from flask import Flask, request, jsonify
import threading
from sensors import sensor_loop

app = Flask(__name__)

# Global variable to control LED state
external_led_override = None  # None = automatic, True/False = manual control

@app.route('/led', methods=['POST'])
def control_led():
    global external_led_override
    data = request.get_json()
    cmd = data.get("command")

    if cmd == "on":
        external_led_override = True
    elif cmd == "off":
        external_led_override = False
    elif cmd == "auto":
        external_led_override = None
    else:
        return jsonify({"error": "Unknown command"}), 400

    return jsonify({"status": "OK", "mode": cmd})

# Start the sensor loop in a separate thread
threading.Thread(target=sensor_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
