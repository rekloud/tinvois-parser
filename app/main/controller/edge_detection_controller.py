from flask import request
from flask_restx import Resource

from ..authorization import sever_to_server_token_required
from ..service.edge_detector_service import detect_edges
from ..utils.dto import EdgeDetectorDto

api = EdgeDetectorDto.api
_image = EdgeDetectorDto.image
_response = EdgeDetectorDto.response
_header = EdgeDetectorDto.headers


@api.route("")
class ParseImage(Resource):
    @api.marshal_with(_response)
    @api.doc(security="SERVER_TO_SERVER_TOKEN")
    @api.expect(_image)
    @sever_to_server_token_required
    def get(self):
        """detect edges of document in image. No pdf"""
        data = request.json
        return detect_edges(data["image"])
