#!/usr/bin/env python3
"""
Main file
"""

import requests


def register_user(email: str, password: str) -> None:
    """Register a new user."""
    url = "http://localhost:5000/users"
    response = requests.post(url, data={"email": email, "password": password})

    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}
    print("register_user passed")


def log_in_wrong_password(email: str, password: str) -> None:
    """Attempt to log in with a wrong password."""
    url = "http://localhost:5000/sessions"
    response = requests.post(url, data={"email": email, "password": password})

    assert response.status_code == 401
    print("log_in_wrong_password passed")


def log_in(email: str, password: str) -> str:
    """Log in with the correct password."""
    url = "http://localhost:5000/sessions"
    response = requests.post(url, data={"email": email, "password": password})

    assert response.status_code == 200
    assert response.json().get("email") == email
    print("log_in passed")

    # Return the session_id from the cookies
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """Try to access the profile without being logged in."""
    url = "http://localhost:5000/profile"
    response = requests.get(url)

    assert response.status_code == 403
    print("profile_unlogged passed")


def profile_logged(session_id: str) -> None:
    """Access the profile while logged in."""
    url = "http://localhost:5000/profile"
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)

    assert response.status_code == 200
    assert "email" in response.json()
    print("profile_logged passed")


def log_out(session_id: str) -> None:
    """Log out of the current session."""
    url = "http://localhost:5000/sessions"
    cookies = {"session_id": session_id}
    response = requests.delete(url, cookies=cookies)

    assert response.status_code == 200
    print("log_out passed")


def reset_password_token(email: str) -> str:
    """Request a password reset token."""
    url = "http://localhost:5000/reset_password"
    response = requests.post(url, data={"email": email})

    assert response.status_code == 200
    reset_token = response.json().get("reset_token")
    assert reset_token is not None
    print("reset_password_token passed")

    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update the password using a reset token."""
    url = "http://localhost:5000/reset_password"
    response = requests.put(url, data={
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
        }
        )

    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}
    print("update_password passed")


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)

    print("All tests passed")
