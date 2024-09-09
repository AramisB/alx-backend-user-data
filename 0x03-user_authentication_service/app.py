#!/usr/bin/env python3
"""
App module
"""
from flask import app, jsonify, Flask, request
from auth import Auth


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
