import numpy as np
import pandas as pd
from flask_restx import abort
from google.cloud import vision

from ..utils.log import get_logger

client = vision.ImageAnnotatorClient()
logger = get_logger(__file__)


def ocr_image(image_content):
    image = vision.Image(content=image_content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    l_texts = []
    l_vertices = []
    for text in texts:
        l_texts.append(text.description)
        vertices = np.ravel([[vertex.x, vertex.y] for vertex in text.bounding_poly.vertices])
        l_vertices.append(vertices)
    df_text = pd.DataFrame(l_vertices, columns=["1x", "1y", "2x", "2y", "3x", "3y", "4x", "4y"])
    df_text["text"] = l_texts
    if len(df_text) == 0:
        msg = "Image contains no text"
        logger.warning(msg)
        abort(400, msg)
    if response.error.message:
        logger.warning("parser failed")
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    return df_text
