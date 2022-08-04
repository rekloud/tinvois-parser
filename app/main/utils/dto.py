from flask_restx import Namespace, fields

authorizations = {
    "SERVER_TO_SERVER_TOKEN": {"type": "apiKey", "in": "header", "name": "Authorization"}
}


class ParseDto:
    api = Namespace("parse", description="parse invoice", authorizations=authorizations)
    image = api.model(
        "image",
        {
            "image": fields.String(required=True, description="base64 encode content of the image"),
            "edit_image": fields.Boolean(
                required=False,
                description="Return the automatically edited" "to bird view of image",
            ),
            "try_auto_edit": fields.Boolean(
                required=False,
                description="Should the parser try to "
                "aut detect the edges and retry"
                "parsing if failed",
            ),
        },
    )
    response = api.model(
        "parse_response",
        {
            "data": fields.Raw(required=True, description="json with parse results"),
            "image": fields.String(
                required=False, description="base64 encode content of the edited " "image"
            ),
        },
    )
    headers = api.parser().add_argument(
        "Authorization", location="headers", help="server to server token"
    )


class EdgeDetectorDto:
    api = Namespace(
        "detect_edges", description="detect edges in image", authorizations=authorizations
    )
    image = api.model(
        "image",
        {"image": fields.String(required=True, description="base64 encode content of the image")},
    )
    # TODO should be possible to specify exact output type via fields.List
    response = api.model(
        "edge_detector_response",
        {
            "data": fields.Raw(
                required=True, description="coordinate of edges as a 4x2 list " "of integers "
            )
        },
    )
    headers = api.parser().add_argument(
        "Authorization", location="headers", help="server to server token"
    )


class BirdViewDto:
    api = Namespace(
        "bird_view",
        description="make an bird view of the image using edges",
        authorizations=authorizations,
    )
    # TODO should be possible to specify exact output type via fields.List in both
    image = api.model(
        "image_and_points",
        {
            "image": fields.String(required=True, description="base64 encode content of the image"),
            "points": fields.Raw(
                required=True, description="coordinate of edges as a 4x2 list " "of integers "
            ),
        },
    )
    response = api.model(
        "bird_view_response",
        {
            "data": fields.String(
                required=True, description="base64 encode content of the " "transformed image"
            )
        },
    )
    headers = api.parser().add_argument(
        "Authorization", location="headers", help="server to server token"
    )
