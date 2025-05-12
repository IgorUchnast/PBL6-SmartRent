from flask import Flask, request, Response
import os
import requests

POST_URL = os.getenv("POST_URL", False)

app = Flask(__name__)

@app.route("/command", methods=["POST"])
def send_command():
    data = request.get_json()
    # Only forward if POST_URL is set
    if POST_URL:
        try:
            response = requests.post(POST_URL, json=data)
            return Response(response.content,
                            status=response.status_code,
                            content_type=response.headers.get('Content-Type', 'application/json'))
        except Exception as e:
            return {"status": "error", "message": str(e)}, 500
    else:
        print("Received data:", data)
        return {"status": "received"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
