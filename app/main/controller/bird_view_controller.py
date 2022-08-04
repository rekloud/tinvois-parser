from flask import request
from flask_restx import Resource

from ..authorization import sever_to_server_token_required
from ..service.bird_view_service import bird_view
from ..utils.dto import BirdViewDto

api = BirdViewDto.api
_image = BirdViewDto.image
_response = BirdViewDto.response
_header = BirdViewDto.headers


@api.route("")
class ParseImage(Resource):
    @api.marshal_with(_response)
    @api.doc(security="SERVER_TO_SERVER_TOKEN")
    @api.expect(_image)
    @sever_to_server_token_required
    def post(self):
        """detect edges of document in image. No pdf"""
        data = request.json
        return bird_view(data["image"], data["points"])
