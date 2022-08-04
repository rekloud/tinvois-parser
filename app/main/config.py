import base64
import os

from dotenv import load_dotenv

load_dotenv(verbose=True, override=False)


def create_google_auth_json_from_env(json_in_b64, path):
    with open(path, "w") as f:
        f.write(base64.b64decode(json_in_b64).decode())


google_auth_path = os.path.join(
    os.path.split(os.path.abspath(os.path.dirname(__file__)))[0], "google_auth", "google_auth.json"
)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_auth_path

if os.environ.get("GOOGLE_AUTH") is not None:
    create_google_auth_json_from_env(os.environ.get("GOOGLE_AUTH"), google_auth_path)
else:
    print("no google auth in env variables")

basedir = os.path.abspath(os.path.dirname(__file__))
SERVER_TO_SERVER_TOKEN = os.environ.get("SERVER_TO_SERVER_TOKEN")
PARSER_CONFIG_FILE = os.path.join(os.path.split(__file__)[0], "config.yml")


MAX_ROWS_OF_TAX_TABLE = 2

LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL", "DEBUG")
