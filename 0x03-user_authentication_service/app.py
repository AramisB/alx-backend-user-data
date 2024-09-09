#!/usr/bin/env python3
"""
App module
"""
from flask import app, jsonify, Flask, request
from auth import Auth
import flask


app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def index():
    """
    return a JSON payload of the form:
    """
    return jsonify({
        "message": "Bievenue"
    })


@app.route('/users', methods=['POST'])
def users() -> None:
    """
    Register a new user with the given email and password.
    Args:
     email - the email of the user
     password - the password of the user
    Raises:
     ValueError - if the user does not exist,
     return a json payload:
     {"email": "<registered email>", "message": "user created"}
     If it exist, return json payload of the form:
     {"message": "email already registered"} with a 400 status code
    """
    data = request.form
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({
            "message": "email and password are required"
        }), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({
            "email": user.email,
            "message": "user created"
        })
    except ValueError:
        return jsonify({
            "message": "email already registered"
        }), 400

@app.route('/sessions', methods=['POST'])
def login() -> None:
    """
    a function to respond to the POST /sessions route.
    The request is expected to contain form data
    with "email" and a "password" fields.
    If the login information is incorrect,
    use flask.abort to respond with a 401 HTTP status.
    Otherwise, create a new session for the user,
    store it the session ID as a cookie with key "session_id"
    on the response and return a JSON payload of the form:
    {"email": "<user email>", "message": "logged in"}
    """
    data = request.form
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({
            "message": "email and password are required"
            }), 400

    try:
        user = AUTH.valid_login(email, password)
        if user:
            session_id = AUTH.create_session(user.email)
        else:
            flask.abort(401)
        response = jsonify({
            "email": user.email,
            "message": "logged in"
        })
        response.set_cookie("session_id", session_id)
        return response
    except ValueError:
        flask.abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
