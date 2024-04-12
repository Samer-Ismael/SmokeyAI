import threading
import time
from collections import deque
from flask_cors import CORS
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

history = deque(maxlen=3)  # Set maximum length of history to 3

def clear_history():
    global history
    while True:
        time.sleep(120)  # Sleep for 2 minutes
        history.clear()

# Start a separate thread to clear history periodically
history_cleaner_thread = threading.Thread(target=clear_history)
history_cleaner_thread.daemon = True
history_cleaner_thread.start()

@app.route('/generate', methods=['POST'])
def generate_response():
    global history
    url = 'http://localhost:11434/api/generate'
    data = request.json

    # Set the model name
    data['model'] = 'mistral'
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