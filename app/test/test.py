import base64
import io
import json
import os
import unittest

import pandas as pd
import werkzeug

from app.main.service.img_parser_service import parse_image

expected_results = pd.read_csv('./resource/sample_results.csv')


class TestParser(unittest.TestCase):
    def test_parser_on_sample_images(self):
        failed_cases = []
        for i, image, expected in expected_results.itertuples():
            actual, code = parse_image(get_image_content(image), False, True)
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
                _actual = json.loads(_actual)
                _actual['data'].pop('raw_text')
                _expected = json.loads(_expected)
                _expected['data'].pop('raw_text')
                print('actual  ', _actual)
                print('expected', _expected)
            assert False

    def test_fail_when_no_text_in_image(self):
        image_with_no_text = './resource/sample_receipts/alaki.jpg'
        self.assertRaises(werkzeug.exceptions.BadRequest,
                          parse_image, get_image_content(image_with_no_text), False, True)

    def test_fail_when_no_value_in_image(self):
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
# def rel_path(path):
#     return os.path.join('.', 'resource/sample_receipts', os.path.split(path)[1])
# files = glob.glob(os.path.join(os.path.dirname(__file__), './resource/sample_receipts/*.*'))
# files = [rel_path(file) for file in files]
# files_result = []
# # for file in files:
# for i, file, expected in expected_results.itertuples():
#     if 'alaki' not in file:
#         res, code = parse_image(get_image_content(file), False, True)
#         # res['data']['hash'] = 'a_hash'
#         # print("(", file, json.dumps(res), ')')
#         files_result.append((file, json.dumps(res)))
# import pandas as pd
# res_df = pd.DataFrame(files_result, columns=['file', 'result'])
# res_df.to_csv('./resource/sample_results2.csv', index=False)
# print(res_df)
