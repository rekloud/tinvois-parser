import base64
import numpy as np
from uuid import uuid4
from flask_restplus import abort
from .base import BaseReceipt
from .preprocessing import pre_process_ocr_results
from .ml_approach import extract_features_token, classify, parse_vat, parse_sum, parse_netto, \
    parse_brutto
from .date_parser import parse_date
from .merchant_parser import parse_merchant
from ..utils import get_logger

logger = get_logger(__file__)


class Receipt(BaseReceipt):

    def preprocess(self):
        self.df_ocr, self.rotation = pre_process_ocr_results(self)
        self.df_values = self.df_ocr.loc[self.df_ocr['is_numeric'], :].copy()
        if len(self.df_values) == 0:
            msg = 'Image contains no amount'
            logger.warning(msg)
            abort(400, msg)
        self.df_values['text2'] = self.df_values['text2'].astype(float)

    def _get_height_of_line_in_receipt(self):
        self.line_height = np.median(self.df_ocr['3y'] - self.df_ocr['2y'])

    def fit(self) -> BaseReceipt:
        self._get_height_of_line_in_receipt()
        extract_features_token(self)
        classify(self)
        parse_vat(self)
        return self

    def parse_all(self) -> dict:
        self.preprocess()
        self.fit()
        output = dict(
            rotation=self.rotation,
            amount=self.get_sum(),
            amountexvat=self.get_netto(),
            merchant_name=self.get_merchant(),
            date=self.get_date(),
            hash=get_image_hash(self.image_content),
            raw_text=base64.b64encode(self.df_ocr_raw.to_json(orient='index').encode()).decode()
        )
        if output['amount'] is None:
            output['amount'] = self.get_brutto()
        return output

    def get_date(self):
        return parse_date(self)

    def get_merchant(self):
        return parse_merchant(self)

    def get_sum(self):
        return parse_sum(self)

    def get_netto(self):
        return parse_netto(self)

    def get_brutto(self):
        return parse_brutto(self)


def get_image_hash(image_content):
    # TODO do real image hashing
    return str(uuid4())
