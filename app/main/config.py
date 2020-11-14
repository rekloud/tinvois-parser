import os

basedir = os.path.abspath(os.path.dirname(__file__))
LOGGING_LEVEL = 'DEBUG'
SERVER_TO_SERVER_TOKEN = 'abcd1234'
PARSER_CONFIG_FILE = os.path.join(
    os.path.split(__file__)[0], 'config.yml'
)
