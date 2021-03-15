import base64
import io
import json
import os
import unittest
import werkzeug

import pandas as pd
from unittest import mock
from app.main.service.img_parser_service import parse_image

expected_results = pd.read_csv('./resource/sample_results.csv')


@mock.patch('app.main.parser.parse_image.get_image_hash')
class TestParser(unittest.TestCase):
    def test_parser_on_sample_images(self, mock_hash):
        mock_hash.return_value = 'a_hash'
        failed_cases = []
        for i, image, expected in expected_results.itertuples():
            actual, code = parse_image(get_image_content(image), False, True)
            actual['data'].pop('raw_text')
            actual_str = json.dumps(actual)
            file_name = os.path.split(image)[1]
            print(file_name, end=' ')
            if actual_str != expected:
                print('FAILED')
                print('actual  ', actual_str)
                print('expected', expected)
                failed_cases.append((file_name,  actual_str, expected))
            else:
                print('succeed')

        if len(failed_cases) > 0:
            print(len(failed_cases), 'has been failed')
            for file_name, _actual, _expected in failed_cases:
                print(file_name)
                print('actual  ', _actual)
                print('expected', _expected)
            assert False

    def test_fail_when_no_text_in_image(self, mock_hash):
        image_with_no_text = './resource/sample_receipts/alaki.jpg'
        self.assertRaises(werkzeug.exceptions.BadRequest,
                          parse_image, get_image_content(image_with_no_text), False, True)

    def test_fail_when_no_value_in_image(self, mock_hash):
        image_with_no_text = './resource/sample_receipts/no_value.jpg'
        self.assertRaises(werkzeug.exceptions.BadRequest,
                          parse_image, get_image_content(image_with_no_text), False, True)


def get_image_content(image_path):
    with io.open(image_path, 'rb') as f:
        image_content = f.read()
    return base64.b64encode(image_content).decode()


TestParser().test_parser_on_sample_images()
TestParser().test_fail_when_no_text_in_image()
TestParser().test_fail_when_no_value_in_image()

# To produce test material
# import glob
# def rel_path(path):
#     return os.path.join('.', 'resource/sample_receipts', os.path.split(path)[1])
# files = glob.glob(os.path.join(os.path.dirname(__file__), './resource/sample_receipts/*.*'))
# files = [rel_path(file) for file in files]
# files_result = []
# for file in files:
#     if 'alaki' not in file:
#         res, code = parse_image(get_image_content(file))
#         res['data']['hash'] = 'a_hash'
#         # print("(", file, json.dumps(res), ')')
#         files_result.append((file, json.dumps(res)))
# import pandas as pd
# res_df = pd.DataFrame(files_result, columns=['file', 'result'])
# res_df.to_csv('./resource/sample_results.csv', index=False)
# print(res_df)
