from flask import Flask, request, Response
import requests

LED_URL = "http://localhost:5000/led"
OUTLET_URL = "http://localhost:5000/outlet"

app = Flask(__name__)

@app.route('/led', methods=['POST'])
def forward_led():
    data = request.get_json()
    try:
        response = requests.post(LED_URL, json=data)
        return Response(response.content,
                        status=response.status_code,
                        content_type=response.headers.get('Content-Type', 'application/json'))
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

@app.route('/outlet', methods=['POST'])
def forward_outlet():
    data = request.get_json()
    try:
        response = requests.post(OUTLET_URL, json=data)
        return Response(response.content,
                        status=response.status_code,
                        content_type=response.headers.get('Content-Type', 'application/json'))
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
