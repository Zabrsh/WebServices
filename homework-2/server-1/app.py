from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Load users from a JSON file
def load_users():
    if not os.path.exists('users.json'):
        return {}
    try:
        with open('users.json', 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}

# Save users to a JSON file
def save_users(users):
    with open('users.json', 'w') as file:
        json.dump(users, file)

users = load_users()

@app.route('/api/user', methods=['POST'])
def add_user():
    data = request.get_json()
    email = data.get('email')
    if email in users:
        return jsonify({'message': 'User already exists'}), 400
    users[email] = {'email': email, 'age': data.get('age'), 'password': data.get('password')}
    save_users(users)
    return jsonify({'message': 'User added successfully'}), 201

@app.route('/api/user/<email>', methods=['GET'])
def get_user(email):
    user = users.get(email)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user), 200

@app.route('/api/user/<email>', methods=['PUT'])
def update_user(email):
    user = users.get(email)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    data = request.get_json()
    user['age'] = data.get('age', user['age'])
    save_users(users)
    return jsonify({'message': 'User updated successfully'}), 200

@app.route('/api/user/<email>', methods=['DELETE'])
def delete_user(email):
    if email in users:
        del users[email]
        save_users(users)
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)