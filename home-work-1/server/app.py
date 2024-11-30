from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.secret_key = 'your_secret_key'

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        age = request.form['age']
        password = generate_password_hash(request.form['password'])
        if email in users:
            return jsonify({'message': 'User already exists'}), 400
        users[email] = {'email': email, 'age': age, 'password': password}
        save_users(users)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users.get(email)
        if user and check_password_hash(user['password'], password):
            session['user'] = email
            return redirect(url_for('profile'))
        return jsonify({'message': 'Invalid credentials'}), 401
    return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    email = session['user']
    user = users.get(email)
    if request.method == 'POST':
        user['age'] = request.form['age']
        save_users(users)
    return render_template('profile.html', user=user)

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user' not in session:
        return redirect(url_for('login'))
    email = session['user']
    users.pop(email, None)
    save_users(users)
    session.pop('user', None)
    return redirect(url_for('register'))

@app.route('/api/add_user', methods=['POST'])
def api_add_user():
    data = request.get_json()
    email = data.get('email')
    if email in users:
        return jsonify({'message': 'User already exists'}), 400
    users[email] = {'email': email, 'age': data.get('age'), 'password': generate_password_hash(data.get('password'))}
    save_users(users)
    return jsonify({'message': 'User added successfully'}), 201

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = users.get(email)
    if user and check_password_hash(user['password'], password):
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/user/<email>', methods=['GET', 'PUT', 'DELETE'])
def api_user(email):
    user = users.get(email)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    if request.method == 'GET':
        return jsonify(user), 200
    elif request.method == 'PUT':
        data = request.get_json()
        user['age'] = data.get('age', user['age'])
        save_users(users)
        return jsonify({'message': 'User updated successfully'}), 200
    elif request.method == 'DELETE':
        users.pop(email, None)
        save_users(users)
        return jsonify({'message': 'User deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)