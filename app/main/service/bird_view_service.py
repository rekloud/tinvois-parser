import base64
from typing import List

import cv2
import numpy as np

from ..image_edit import four_point_transform
from ..utils.log import get_logger

logger = get_logger(__file__)


def bird_view(image: str, points: List[List[int]]) -> (dict, int):
    image_content = base64.b64decode(image)
    jpg_as_np = np.frombuffer(image_content, dtype=np.uint8)
    image = cv2.imdecode(jpg_as_np, flags=1)
    bird_view_image_array = four_point_transform(image, np.array(points))
    bird_view_image = cv2.imencode('.jpg', bird_view_image_array)[1]
    return dict(data=base64.b64encode(bird_view_image).decode()), 200
