from flask_restplus import Resource
from flask import request

from ..authorization import sever_to_server_token_required
from ..service.img_parser_service import parse_image
from ..utils.dto import ParseDto

api = ParseDto.api
_image = ParseDto.image
_response = ParseDto.response
_header = ParseDto.headers


@api.route('')
class ParseImage(Resource):
    @api.marshal_with(_response)
    @api.doc(security='SERVER_TO_SERVER_TOKEN')
    @api.expect(_image)
    @sever_to_server_token_required
    def get(self):
        """parse a receipt in image format. No pdf"""
        data = request.json
        return parse_image(data['image'])
