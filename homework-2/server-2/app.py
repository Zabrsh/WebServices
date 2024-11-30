import json
from flask import Flask, request, render_template, redirect, url_for, flash
import subprocess

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def curl_request(method, url, data=None):
    command = ['curl','-s', '-X',  method, '-H', 'Content-Type: application/json']
    if data:
        command.extend(['-d', data])
    command.append(url)
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout, result.stderr

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        age = request.form['age']
        password = request.form['password']
        data = json.dumps({'email': email, 'age': age, 'password': password})
        response, error = curl_request('POST', 'http://127.0.0.1:5000/api/user', data)
        if error:
            flash('Error: ' + error)
        else:
            flash('User registered successfully')
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        response, error = curl_request('GET', f'http://127.0.0.1:5000/api/user/{email}')
        if error:
            flash('Error: ' + error)
        else:
            user = json.loads(response)
            if user['password'] == password:
                flash('Login successful')
                return redirect(url_for('profile', email=email))
            else:
                flash('Invalid credentials')
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/profile/<email>', methods=['GET', 'POST'])
def profile(email):
    if request.method == 'POST':
        age = request.form['age']
        data = json.dumps({'age': age})
        response, error = curl_request('PUT', f'http://127.0.0.1:5000/api/user/{email}', data)
        if error:
            flash('Error: ' + error)
        else:
            flash('Profile updated successfully')
        return redirect(url_for('profile', email=email))
    response, error = curl_request('GET', f'http://127.0.0.1:5000/api/user/{email}')
    if error:
        flash('Error: ' + error)
        return redirect(url_for('index'))
    user = json.loads(response)
    return render_template('profile.html', user=user)

@app.route('/delete/<email>', methods=['POST'])
def delete_account(email):
    response, error = curl_request('DELETE', f'http://127.0.0.1:5000/api/user/{email}')
    if error:
        flash('Error: ' + error)
    else:
        flash('Account deleted successfully')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5001, debug=True)