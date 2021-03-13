from typing import List
import base64
import numpy as np
import cv2
from ..image_edit import PaperEdgeDetector
from ..utils.log import get_logger

logger = get_logger(__file__)


def detect_edges(image: str) -> (dict, int):
    image_content = base64.b64decode(image)
    edges = get_edges(image_content)
    return dict(data=edges), 200


def get_edges(image_content: bytes) -> List[List[int]]:
    jpg_as_np = np.frombuffer(image_content, dtype=np.uint8)
    image = cv2.imdecode(jpg_as_np, flags=1)
    edges = PaperEdgeDetector(image=image).get_image_edges()
    return edges
