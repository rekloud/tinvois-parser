from flask import request
from flask_restx import Resource

from ..authorization import sever_to_server_token_required
from ..service.img_parser_service import parse_image
from ..utils.dto import ParseDto

api = ParseDto.api
_image = ParseDto.image
_response = ParseDto.response
_header = ParseDto.headers


@api.route("")
class ParseImage(Resource):
    @api.marshal_with(_response)
    @api.doc(security="SERVER_TO_SERVER_TOKEN")
    @api.expect(_image)
    @sever_to_server_token_required
    def post(self):
        """parse a receipt in image format. No pdf"""
        data = request.json
        output_edited_image = data.get("edit_image", False)
        try_auto_edit = data.get("try_auto_edit", True)
        return parse_image(data["image"], output_edited_image, try_auto_edit)
