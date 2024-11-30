import json
from flask import Flask, request, jsonify
from cryptography.fernet import Fernet

app = Flask(__name__)

key = Fernet.generate_key()
cipher_suite = Fernet(key)
file_path = 'messages.json'

def save_message(encrypted_message):
    try:
        with open(file_path, 'r') as file:
            messages = json.load(file)
    except FileNotFoundError:
        messages = []

    messages.append({'encrypted_message': encrypted_message})

    with open(file_path, 'w') as file:
        json.dump(messages, file)

def load_messages():
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

@app.route('/send', methods=['POST'])
def send_message():
    message = request.json.get('message')
    encrypted_message = cipher_suite.encrypt(message.encode()).decode()
    save_message(encrypted_message)
    return jsonify({'encrypted_message': encrypted_message})

@app.route('/retrieve', methods=['POST'])
def retrieve_message():
    encrypted_message = request.json.get('encrypted_message')
    messages = load_messages()
    for msg in messages:
        if msg['encrypted_message'] == encrypted_message:
            decrypted_message = cipher_suite.decrypt(encrypted_message.encode()).decode()
            return jsonify({'decrypted_message': decrypted_message})
    return jsonify({'error': 'Message not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)