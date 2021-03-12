import base64
import io
import json
import os
import unittest
import werkzeug

import pandas as pd
from unittest import mock
from app.main.service.img_parser_service import parse_image


def get_image_content(image_path):
    with io.open(image_path, 'rb') as f:
        image_content = f.read()
    return base64.b64encode(image_content).decode()


image = r'C:\Users\shossein\Downloads\Telegram Desktop\salamander2.jpg'
image = r'C:\Users\shossein\Downloads\Telegram Desktop\2021\mostafa2.jpg'
# image = r'C:\Users\shossein\Downloads\Telegram Desktop\20210107\rossman.jpg'
# image = r'C:\Users\shossein\Downloads\Telegram Desktop\20210107\dm2.jpg'
# image = r'.\resource/sample_receipts\park.jpg'
# image = r'.\resource/sample_receipts\no_value.jpg'
# image = r'.\resource/sample_receipts\tedi2.jpg'
# image = r'.\resource/sample_receipts\invoice1.jpeg'
# image = r'C:\Users\shossein\Downloads\Telegram Desktop\saturn.jpg'
# image = r'C:\Users\shossein\Downloads\Telegram Desktop\pick.jpg'
# image = r'C:\Users\shossein\Downloads\Telegram Desktop\tschibo.jpg'
# image = r'C:\Users\shossein\Downloads\Telegram Desktop\action2.jpg'
# image = r'C:\Users\shossein\Downloads\Telegram Desktop\penny4.jpgROTATED.jpg'
# image = r'C:\Users\shossein\Downloads\Telegram Desktop\20201225\notebooks.jpg'
# image = r'C:\Users\shossein\Downloads\Telegram Desktop\20201214\3.jpg'
# image = r'C:\Users\shossein\Downloads\Telegram Desktop\20201225\feri.jpg'
# image = r'C:\Users\shossein\Pictures\2020\2\2020-02-29-1.jpeg'
# image = r'C:\Users\shossein\Pictures\2020\8\2020-08-28-1.jpeg'
# image = r'C:\Users\shossein\Pictures\2020\9\2020-09-07-1.jpeg'
image = r'C:\Users\shossein\Documents\personal\taxapp\parser\app\test\resource\sample_receipts\kaufland_vertical.jpg'
image_content = get_image_content(image)
# print(image_content)
actual, code = parse_image(image_content)
actual['data'].pop('raw_text')
actual_str = json.dumps(actual)
print(image, flush=True)
print(actual_str, flush=True)
