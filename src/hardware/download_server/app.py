from flask import Flask, request, Response
import requests

POST_URL = "http://sensor_server:5000/led"

app = Flask(__name__)

@app.route('/forward', methods=['POST'])
def forward_request():
    data = request.get_json()
    try:
        response = requests.post(POST_URL, json=data)
        return Response(response.content,
                        status=response.status_code,
                        content_type=response.headers.get('Content-Type', 'application/json'))
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
