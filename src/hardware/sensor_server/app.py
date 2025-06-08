from flask import Flask, request, jsonify
import threading
import sensors

app = Flask(__name__)

@app.route('/led', methods=['POST'])
def control_led():
    data = request.get_json()
    cmd = data.get("command")

    if cmd == "on":
        sensors.external_led_override = True
    elif cmd == "off":
        sensors.external_led_override = False
    elif cmd == "auto":
        sensors.external_led_override = None
    else:
        return jsonify({"error": "Unknown command"}), 400

    return jsonify({"status": "OK", "mode": cmd})

@app.route('/outlet', methods=['POST'])
def control_outlet():
    data = request.get_json()
    cmd = data.get("command")

    if cmd == "on":
        sensors.outlet.turn_on()
    elif cmd == "off":
        sensors.outlet.turn_off()
    else:
        return jsonify({"error": "Unknown command"}), 400

    return jsonify({"status": "OK", "mode": cmd})

# Start sensor loop in a background thread
threading.Thread(target=sensors.sensor_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
