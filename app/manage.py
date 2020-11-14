from flask import Flask
from __init__ import blueprint


app = Flask(__name__)
app.register_blueprint(blueprint)


def run():
    @app.after_request
    def clean_headers(response):
        response.headers['server'] = ''
        return response
    app.run(port=5001, host="0.0.0.0")


if __name__ == '__main__':
    run()
