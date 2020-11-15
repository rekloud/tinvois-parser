import base64
from ..parser.parse_image import Receipt


def parse_image(image: str) -> (dict, int):
    image_content = base64.b64decode(image)
    data = Receipt(image_content=image_content).parse_all()
    return dict(data=data), 200