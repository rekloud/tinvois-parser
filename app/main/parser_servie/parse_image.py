from .base import _Receipt
from .sum_parser import parse_sum
from .date_parser import parse_date
from .netto_parser import parse_netto
from .brutto_parser import parse_brutto
from .merchant_parser import parse_merchant
from ..utils import get_logger

logger = get_logger(__file__)


class Receipt(_Receipt):

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
