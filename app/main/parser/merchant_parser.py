from ..utils import get_logger
from .utils import get_close_matches_indexes
from .base import _Receipt

logger = get_logger(__file__)


def parse_merchant(receipt: _Receipt) -> str:
    merchant_parsers = [regex_merchant_parser]
    for merchant_parser in merchant_parsers:
        merchant = merchant_parser(receipt)
        if merchant is not None:
            return merchant
    logger.warning('could not parse merchant')


def regex_merchant_parser(receipt: _Receipt) -> str or None:
    for market, spellings in receipt.config['markets'].items():
        for spelling in spellings:
            matches = get_close_matches_indexes(spelling, receipt.df_ocr['text'],
                                                n=1, cutoff=receipt.cutoff)
            if matches:
                return market
    return receipt.df_ocr.loc[1, 'text'].capitalize()
