from flask import Flask, request, jsonify
import requests
import uuid

app = Flask(__name__)

LOGGING_SERVICE_URL = 'http://localhost:5001/log'
MESSAGES_SERVICE_URL = 'http://localhost:5002/message'

@app.route("/", methods=['POST'])
def post_message():
    msg = request.json.get('msg')
    if not msg:
        return jsonify({'error': 'Message content is required'}), 400
    unique_id = str(uuid.uuid4())
    data = {'id': unique_id, 'msg': msg}
    response = requests.post(LOGGING_SERVICE_URL, json=data)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to log message'}), response.status_code
    return jsonify({'id': unique_id}), response.status_code

@app.route("/", methods=['GET'])
def get_messages():
    # Get messages from logging-service
    log_response = requests.get(LOGGING_SERVICE_URL)
    if log_response.status_code != 200:
        return jsonify({'error': 'Failed to get logs'}), log_response.status_code 
    logs = log_response.text
    msg_response = requests.get(MESSAGES_SERVICE_URL)
    if msg_response.status_code != 200:
        return jsonify({'error': 'Failed to get static message'}), msg_response.status_code

    static_msg = msg_response.text
    full_response = f"{logs}\n{static_msg}"
    return full_response, 200

if __name__ == '__main__':
    app.run(port=5000)
