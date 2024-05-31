from flask import Flask, request, jsonify

app = Flask(__name__)
logs = {}

@app.route('/log', methods=['POST'])
def log_message():
    data = request.json
    unique_id = data.get('id')
    msg = data.get('msg')
    if not unique_id or not msg:
        return jsonify({'error': 'Invalid data'}), 400
    logs[unique_id] = msg
    print(f"Logged: {unique_id} -> {msg}")
    return jsonify({'status': 'success'}), 200

@app.route('/log', methods=['GET'])
def get_logs():
    return '\n'.join(logs.values()), 200

if __name__ == '__main__':
    app.run(port=5001)
