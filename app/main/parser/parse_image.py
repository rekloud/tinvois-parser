import base64
from uuid import uuid4
from .base import _Receipt
from .ml_approach.feature_extraction import extract_features_token
from .ml_approach.classifier import classify
from .ml_approach.vat_parser import parse_vat
from .ml_approach.sum_parser import parse_sum
from .ml_approach.netto_parser import parse_netto
from .ml_approach.brutto_parser import parse_brutto
from .date_parser import parse_date
from .merchant_parser import parse_merchant
from ..utils import get_logger

logger = get_logger(__file__)


class Receipt(_Receipt):

    def fit(self):
        self.df_ocr.loc[self.df_ocr['is_numeric'], 'token'] = 'VALUE'
        extract_features_token(self)
        classify(self)
        parse_vat(self)

    def parse_all(self) -> dict:
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
