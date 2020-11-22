# import unittest
#
# def test():
#     """Runs the unit tests."""
#     tests = unittest.TestLoader().discover('test', pattern='test*.py')
#     result = unittest.TextTestRunner(verbosity=2).run(tests)
#     if result.wasSuccessful():
#         return 0
#     return 1
#
#
# if __name__ == '__main__':
#     test()
#
# import pandas as pd
# from app.main.parser.preprocessing.rotate import get_rotation
# df_ocr = pd.read_csv(r'C:\Users\shossein\Documents\personal\taxapp\backend\notebook\kaufland_horiz.csv')
# p = get_rotation(df_ocr)
# print(p)

import json
j = json.loads('{"data": {"rotation": 0, "amount": 3791, "amountexvat": 3599, "brutto": null, "merchant_name": "Kuzey", "date": "2020-11-13T00:00:00", "hash": "2d7ac1db-6add-4410-8219-1bbf24604f63"}, "parser": "tinvois"}')
