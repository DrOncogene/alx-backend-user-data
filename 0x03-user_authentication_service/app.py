#!/usr/bin/env python3
"""
basic flask app
"""
from flask import Flask, jsonify, request, abort, redirect, url_for

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


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """logs a user in"""
    email = request.form.get('email')
    passwd = request.form.get('password')
    is_valid = AUTH.valid_login(email, passwd)
    if not is_valid:
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({'email': email, 'message': 'logged in'})
    response.set_cookie('session_id', session_id)

    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """logs a user in"""
    sid = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(sid)
    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """return a user email for a given session id"""
    sid = request.cookies.get('session_id')
    if sid is None:
        abort(403)

    user = AUTH.get_user_from_session_id(sid)
    if user is None:
        abort(403)

    return jsonify({'email': user.email})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
