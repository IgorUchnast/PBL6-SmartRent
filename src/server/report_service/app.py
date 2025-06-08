from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

MAIN_SERVICE_URL = "http://main_service:8000"  # adres kontenera (nazwa z docker-compose)


@app.route("/api/all-properties", methods=["GET"])
def get_all_properties():
    try:
        response = requests.get(f"{MAIN_SERVICE_URL}/properties/public")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def forward_request(path, token):
    """Pomocnicza funkcja do wysyłania żądań z JWT"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{MAIN_SERVICE_URL}{path}", headers=headers)

    try:
        return jsonify(response.json()), response.status_code
    except Exception:
        return jsonify({"error": "Invalid response from main service"}), 500


@app.route("/api/properties", methods=["GET"])
def proxy_properties():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return jsonify({"error": "Missing token"}), 401

    return forward_request("/properties", token)


@app.route("/api/reservations", methods=["GET"])
def proxy_reservations():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return jsonify({"error": "Missing token"}), 401

    return forward_request("/reservations", token)


@app.route("/api/properties", methods=["POST"])
def proxy_add_property():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return jsonify({"error": "Missing token"}), 401

    try:
        payload = request.get_json()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.post(
            f"{MAIN_SERVICE_URL}/properties",
            headers=headers,
            json=payload
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/outlets/<int:outlet_id>/status", methods=["GET"])
def proxy_outlet_status(outlet_id):
    try:
        response = requests.get(f"{MAIN_SERVICE_URL}/outlets/{outlet_id}/status")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/outlets/<int:outlet_id>/toggle", methods=["POST"])
def proxy_toggle_outlet(outlet_id):
    try:
        response = requests.post(f"{MAIN_SERVICE_URL}/outlets/{outlet_id}/toggle")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/reserve", methods=["POST"])
def reserve_property():
    try:
        data = request.get_json()
        response = requests.post(f"{MAIN_SERVICE_URL}/reserve", json=data)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/properties/<int:property_id>/release", methods=["PATCH"])
def proxy_release_property(property_id):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return jsonify({"error": "Missing token"}), 401

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.patch(
            f"{MAIN_SERVICE_URL}/properties/{property_id}/release",
            headers=headers
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/lightbulbs/<int:lightbulb_id>", methods=["GET"])
def proxy_lightbulb_get(lightbulb_id):
    try:
        response = requests.get(f"{MAIN_SERVICE_URL}/lightbulbs/{lightbulb_id}")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/lightbulbs/<int:lightbulb_id>", methods=["PATCH"])
def proxy_lightbulb_patch(lightbulb_id):
    try:
        data = request.get_json()
        response = requests.patch(
            f"{MAIN_SERVICE_URL}/lightbulbs/{lightbulb_id}",
            headers={"Content-Type": "application/json"},
            json=data
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/sensors/<string:sensor_type>/history", methods=["GET"])
def proxy_sensor_history(sensor_type):
    try:
        response = requests.get(f"{MAIN_SERVICE_URL}/sensors/{sensor_type}/history")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/sensors/<sensor_type>/latest', methods=['GET'])
def proxy_sensor_latest(sensor_type):
    try:
        res = requests.get(f'{MAIN_SERVICE_URL}/sensors/{sensor_type}/latest')
        return (res.content, res.status_code, res.headers.items())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002, debug=True)
