Requests Module
The Requests module is a popular Python library for making HTTP requests in Python. It simplifies sending HTTP requests, handling responses, and working with REST APIs.

Key features of the Requests module include:

HTTP Methods: Sending GET, POST, PUT, DELETE, PATCH, etc.
Headers: Adding custom headers to requests.
Cookies: Sending and receiving cookies.
Data Payloads: Sending form data and JSON payloads.
Response Objects: Accessing status codes, headers, content, and more from the server's response.

HTTP Status Codes
HTTP Status Codes indicate the status of a client's request to the server. They are categorized as follows:

1xx (Informational): Request received, continuing process.
2xx (Success): Request successfully received, understood, and accepted.
200 OK: The request was successful.
201 Created: The request was successful, and a new resource was created.
204 No Content: The request was successful, but there is no content to send in the response.
3xx (Redirection): Further action must be taken to complete the request.
301 Moved Permanently: The resource has been moved permanently to a new URL.
302 Found: The resource has been temporarily moved to a different URL.
4xx (Client Error): The request contains bad syntax or cannot be fulfilled.
400 Bad Request: The request cannot be processed due to client error.
401 Unauthorized: Authentication is required and has failed or has not yet been provided.
403 Forbidden: The server understood the request but refuses to authorize it.
404 Not Found: The requested resource could not be found.
5xx (Server Error): The server failed to fulfill a valid request.
500 Internal Server Error: The server encountered an unexpected condition that prevented it from fulfilling the request.
503 Service Unavailable: The server is currently unable to handle the request.

How to Declare API Routes in a Flask App
In Flask, API routes are defined using the @app.route() decorator. For example:
from flask import Flask

app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    return {'data': 'Here is some data'}

You can specify the HTTP methods allowed by passing the methods parameter (e.g., methods=['GET', 'POST']).

How to Get and Set Cookies
Get Cookies: Access cookies using request.cookies.
Set Cookies: Use response.set_cookie() to set cookies in the response.
Example:
from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/')
def index():
    # Get a cookie
    username = request.cookies.get('username')
    
    # Set a cookie
    response = make_response(f'Hello, {username}')
    response.set_cookie('username', 'John Doe')
    return response

How to Retrieve Request Form Data
Use request.form to access form data sent with a POST request:
Example:
from flask import Flask, request

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit_form():
    username = request.form['username']
    return f'Hello, {username}'

How to Return Various HTTP Status Codes
Use the return statement with a tuple to specify content and status code:
Example:
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/success')
def success():
    return jsonify(message="Success!"), 200

@app.route('/not-found')
def not_found():
    return jsonify(error="Resource not found"), 404

@app.route('/server-error')
def server_error():
    return jsonify(error="Internal Server Error"), 500