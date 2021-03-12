from flask import Flask
from __init__ import blueprint


app = Flask(__name__)
app.register_blueprint(blueprint)


@app.after_request
def clean_headers(response):
    response.headers['server'] = ''
    return response


if __name__ == '__main__':
    app.run(port=5001, host="0.0.0.0")
