import os
from dotenv import load_dotenv

load_dotenv(verbose=True, override=False)

basedir = os.path.abspath(os.path.dirname(__file__))
LOGGING_LEVEL = 'DEBUG'
SERVER_TO_SERVER_TOKEN = os.environ.get('SERVER_TO_SERVER_TOKEN')
PARSER_CONFIG_FILE = os.path.join(
    os.path.split(__file__)[0], 'config.yml'
)
