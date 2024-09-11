#!/usr/bin/env python3
"""
App module
"""
from flask import app, jsonify, Flask, request, redirect
from auth import Auth
import flask


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def hello():
    """
    return a JSON payload of the form:
    """
    return jsonify({
        "message": "Bienvenue"
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

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({
            "email": email,
            "message": "logged in"
        })
        response.set_cookie("session_id", session_id)
        return response
    else:
        flask.abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout() -> None:
    """
    respond to the DELETE /sessions route.
    The request is expected to contain the session ID
    as a cookie with key "session_id".
    Find the user with the requested session ID.
    If the user exists destroy the session
    and redirect the user to GET /.
    If the user does not exist, respond with a 403 HTTP status.
    """
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect('/')
        else:
            flask.abort(403)
    else:
        flask.abort(403)


@app.route('/profile', methods=['GET'])
def profile() -> None:
    """
    The request is expected to contain a session_id cookie.
    Use it to find the user. If the user exist,
    respond with a 200 HTTP status and the following JSON payload:
    {"email": "<user email>"}
    If the session ID is invalid or the user does not exist,
    respond with a 403 HTTP status.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({
            "email": user.email
        }), 200
    else:
        flask.abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """
    Responds to the POST /reset_password route.
    The request is expected to contain form data
    with the "email" field.
    If the email is not registered, respond with a 403 status code.
    Otherwise, generate a token and respond
    with a 200 HTTP status and the following JSON payload:
    {"email": "<user email>", "reset_token": "<reset token>"}
    """
    data = request.form
    email = data.get('email')
    if not email:
        return jsonify({
            "message": "email is required"
        }), 400

    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({
            "email": email,
            "reset_token": token
        }), 200
    except ValueError:
        return jsonify({
            "message": "email not registered"
        }), 403


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """
    responds to the PUT /reset_password route.
    The request is expected to contain form data with fields:
    "email", "reset_token" and "new_password".
    Update the password.
    If the token is invalid, catch the exception
    and respond with a 403 HTTP code.
    If the token is valid, respond with a 200 HTTP
    code and the following JSON payload:
    {"email": "<user email>", "message": "Password updated"}
    """
    data = request.form
    email = data.get('email')
    reset_token = data.get('reset_token')
    new_password = data.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({
            "email": email,
            "message": "Password updated"
        }), 200
    except Exception:
        flask.abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
