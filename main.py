from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/generate', methods=['POST'])
def generate_response():
    url = 'http://localhost:11434/api/generate'
    data = request.json

    # Set the model name to "Smokey"
    data['model'] = 'Smokey'

    # Set streaming to false
    data['stream'] = False

    # Make a POST request to the API
    response = requests.post(url, json=data)

    # Parse the response and extract the generated text
    response_data = response.json()
    generated_response = response_data.get('response', '')

    # Return the generated response
    return jsonify({'generated_response': generated_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
