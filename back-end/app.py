from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/login', methods=['POST'])
def api_login():
    user_data = request.get_json()
    print(user_data)
    return jsonify({'status': 200})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)