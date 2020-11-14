import base64
import unittest
import io
import json
from app.test.base import BaseTestCase

imgae3 = r'C:\Users\shossein\Documents\personal\taxapp\sample_invoices\3.jpeg'

def path_to_base64(image_path):
    with io.open(image_path, 'rb') as f:
        image_content = f.read()
    return base64.b64encode(image_content).decode()


class TestImageParser(BaseTestCase):
    # TODO finish it using here https://flask.palletsprojects.com/en/1.1.x/testing/#the-first-test
    def test_image_3(self):
        # result = self.app.parse.
        pass
