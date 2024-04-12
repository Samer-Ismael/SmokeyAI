
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

history = []

@app.route('/generate', methods=['POST'])
def generate_response():
    global history
    url = 'http://localhost:11434/api/generate'
    data = request.json

    # Set the model name
    data['model'] = 'Smokey'
    # Disable streaming
    data['stream'] = False

    # Add conversation history to the prompt
    prompt = data.get('prompt', '')
    history.append(prompt)

    # Update the prompt in the request data
    data['prompt'] = '\n'.join(history)

    # Make a POST request to the API
    response = requests.post(url, json=data)

    # Parse the response and extract the generated text
    response_data = response.json()
    generated_response = response_data.get('response', '')

    # Append the generated response to the history
    history.append(generated_response)

    # Return the generated response along with the history
    return jsonify({'generated_response': generated_response, 'history': list(history)})



if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5000, debug=True)