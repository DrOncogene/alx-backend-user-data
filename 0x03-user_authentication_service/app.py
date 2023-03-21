#!/usr/bin/env python3
"""
basic flask app
"""
from flask import Flask, jsonify, request, abort

from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    email = request.form.get('email')
    passwd = request.form.get('password')
    if not email or not passwd:
        return jsonify({'message': 'missing email or password'}), 400
    try:
        user = AUTH.register_user(email=email, password=passwd)
        payload = {'email': email, 'message': 'user created'}
        return jsonify(payload)
    except ValueError:
        return jsonify({'message': 'email already registered'}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
