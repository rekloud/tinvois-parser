import re
import dateutil
from ..utils import get_logger
from .base import _Receipt

logger = get_logger(__file__)


def parse_date(receipt: _Receipt) -> str:
    date_parsers = [regex_date_parser]
    for date_parser in date_parsers:
        date_string = date_parser(receipt)
        if date_string is not None:
            return date_string
    logger.warning('could not parse date')


def regex_date_parser(receipt: _Receipt) -> str or None:
    for row in receipt.df_ocr.iloc[1:, :].itertuples():
        match = re.match(receipt.config['date_format'], row.text)
        if match:
            try:
                date_str = match.group(0)
                logger.debug(date_str)
                date_str = date_str.replace(" ", "")
                return dateutil.parser.parse(date_str, dayfirst=True).isoformat()
            except Exception as e:
                logger.warning(f'Failed to parse a date {str(e)}')
                continue
