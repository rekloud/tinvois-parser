from flask_restplus import Resource
from flask import request

from ..authorization.decorator import sever_to_server_token_required
from ..service.img_parser_service import parse_image
from ..utils.dto import ParseDto

api = ParseDto.api
_response = ParseDto.response
_header = ParseDto.headers


@api.route('/')
class ParseImage(Resource):
    @api.marshal_with(_response)
    @api.doc(security='SERVER_TO_SERVER_TOKEN')
    @sever_to_server_token_required
    def post(self):
        """parse a receipt in image format. No pdf"""
        data = request.json
        return parse_image(data)
