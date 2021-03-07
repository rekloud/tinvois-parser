import re
import string

from ..utils import get_logger
from .base import BaseReceipt

logger = get_logger(__file__)


def parse_merchant(receipt: BaseReceipt) -> str:
    merchant_parsers = [regex_merchant_parser]
    for merchant_parser in merchant_parsers:
        merchant = merchant_parser(receipt)
        if merchant is not None:
            return merchant
    logger.warning('could not parse merchant')


def regex_merchant_parser(receipt: BaseReceipt) -> str or None:
    for market, spellings in receipt.config['markets'].items():
        for spelling in spellings:
            matches = re.search(spelling, receipt.df_ocr.loc[0, 'text'])
            if matches:
                return market
    return string.capwords(receipt.df_ocr.loc[0, 'text'].split('\n')[0])
