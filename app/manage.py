from flask import Flask
from __init__ import blueprint


app = Flask(__name__)
app.register_blueprint(blueprint)


@app.after_request
def clean_headers(response):
    response.headers['server'] = ''
    return response