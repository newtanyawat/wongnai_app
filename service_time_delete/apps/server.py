from flask import Flask 
from flask_cors import CORS
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__, template_folder='../templates')

app.secret_key = 'super secret key'

@app.after_request
def after_request(response):
    response.headers.add(
    'Access-Control-Allow-Origin',
    '*',
    )
    response.headers.add(
    'Access-Control-Allow-Credentials',
    'true'
    )
    response.headers.add(
    'Access-Control-Allow-Headers',
    'X-Requested-With,Content-type,withCredentials,authorization'
    )
    response.headers.add(
    'Access-Control-Allow-Methods',
    'GET,PUT,POST,DELETE,OPTIONS'
    )
    return response



