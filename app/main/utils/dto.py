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
    image = api.model('image',
                         {'image': fields.String(required=True,
                                                 description='base64 encode content of the image')
                          })
    response = api.model('parse_response',
                         {'data': fields.Raw(required=True,
                                                description='json with parse results')})
    headers = api.parser(). \
        add_argument('Authorization', location='headers', help='server to server token')
