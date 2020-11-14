import json
import base64
from flask import jsonify
import unittest

import app.main.parser.parse_image as pi
from app.main.service.img_parser_service import parse_image
from app.main.parser.utils import read_config
import io

# imgae_path = r'C:\Users\shossein\Documents\personal\taxapp\sample_invoices\3.jpeg'
imgae_path = r'C:\Users\shossein\Documents\personal\taxapp\sample_invoices\alaki.jpg'
imgae_path = r'C:\Users\shossein\Documents\personal\taxapp\sample_invoices\fileName.jpg'
imgae_path = r'C:\Users\shossein\Documents\personal\taxapp\sample_invoices\fritten.jpg'
# imgae_path = r'C:\Users\shossein\Documents\personal\taxapp\sample_invoices\2.jpeg'
# imgae_path = r'C:\Users\shossein\Documents\personal\taxapp\sample_invoices\invoice1.jpeg'
imgae_path = r'C:\Users\shossein\Documents\personal\taxapp\sample_invoices\3.jpeg'
# imgae_path = r'C:\Users\shossein\Documents\personal\taxapp\sample_invoices\kaufland_horiz.jpg'
# imgae_path = r'C:\Users\shossein\Documents\personal\taxapp\sample_invoices\kaufland_vertical.jpg'
# imgae_path = r'C:\Users\shossein\Documents\personal\taxapp\sample_invoices\rossmann.jpg'
# imgae_path = r'C:\Users\shossein\Documents\personal\taxapp\sample_invoices\tank-oil.jpg'
# imgae_path = r'C:\Users\shossein\OneDrive\house\hoerde Stiftkamp 18\Rechnung\hornbach-26.03.2019.jpg'
with io.open(imgae_path, 'rb') as f:
    image_content = f.read()

print(imgae_path)
# res = parse_image(base64.b64encode(image_content).decode())
# print(json.dumps(res))


def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    test()