import base64
from uuid import uuid4
from .base import _Receipt
from .sum_parser import parse_sum
from .date_parser import parse_date
from .netto_parser import parse_netto
from .brutto_parser import parse_brutto
from .merchant_parser import parse_merchant
from ..utils import get_logger

logger = get_logger(__file__)


class Receipt(_Receipt):

    def parse_all(self) -> dict:
        return dict(
            rotation=self.rotation,
            amount=self.get_sum(),
            amountexvat=self.get_netto(),
            brutto=self.get_brutto(),
            merchant_name=self.get_merchant(),
            date=self.get_date(),
            hash=get_image_hash(self.image_content),
            raw_text=base64.b64encode(self.df_ocr_raw.to_json(orient='index').encode()).decode()
        )

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
