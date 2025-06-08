from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

MAIN_SERVICE_URL = "http://main_service:8000"  # adres kontenera (nazwa z docker-compose)


@app.route("/api/all-properties", methods=["GET"])
def get_all_properties():
    try:
        response = requests.get("http://main_service:8000/properties/public")
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




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002, debug=True)
