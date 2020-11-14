from flask_restplus import Namespace, fields

authorizations = {
    'SERVER_TO_SERVER_TOKEN': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}


class ParseDto:
    api = Namespace('parse', description='parse invoice',
                    authorizations=authorizations)
    response = api.model('parse_response',
                         {'message': fields.String(required=True,
                                                   description='json with parse results')})
    headers = api.parser(). \
        add_argument('Authorization', location='headers', help='server to server token')
