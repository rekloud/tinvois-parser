from functools import wraps
from flask import request
from flask_restplus import abort

from ..config import SERVER_TO_SERVER_TOKEN
from ..utils.log import get_logger

logger = get_logger(__file__)


def sever_to_server_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_token = request.headers.get('Authorization')
        if auth_token:
            if auth_token.strip() == SERVER_TO_SERVER_TOKEN:
                return f(*args, **kwargs)
            msg = 'Invalid token'
        else:
            msg = 'No token is provided'
        logger.warning(msg)
        abort(401, msg)
    return decorated
