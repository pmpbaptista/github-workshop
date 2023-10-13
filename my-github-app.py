# Flask app to get smee content and print in console

from flask import Flask, request, jsonify
import json

import modules.github_app_auth as auth

app = Flask(__name__)

@app.route('/', methods=['POST'])
def my_github_app():
    if request.headers['Content-Type'] != 'application/json':
        return "415 Unsupported Media Type ;)"
    data = request.json
    print(json.dumps(data, indent=4))
    return jsonify(data)

    
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=3000)
