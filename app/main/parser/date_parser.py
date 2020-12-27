import re
import dateutil
from ..utils import get_logger
from .base import _Receipt

logger = get_logger(__file__)


def parse_date(receipt: _Receipt) -> str:
    date_parsers = [regex_date_parser, regex_date_parser_from_full_text]
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
                logger.debug(f'date_str: {date_str}')
                date_str = date_str.replace(" ", "")
                logger.info(f'date parsed using individual rows {date_str}')
                return dateutil.parser.parse(date_str, dayfirst=True).isoformat()
            except Exception as e:
                logger.warning(f'Failed to parse a date {str(e)}')
                continue


def regex_date_parser_from_full_text(receipt: _Receipt) -> str or None:
    matches = re.findall(receipt.config['date_format2'], receipt.df_ocr.iloc[0, :].text)
    for date_str in matches:
        try:
            date_str = date_str.replace(" ", "")
            logger.debug(f'date_str: {date_str}')
            parsed_date = dateutil.parser.parse(date_str, dayfirst=True)
            if parsed_date.year > 1990:
                logger.info(f'date parsed using full rows {date_str}')
                return parsed_date.isoformat()
            else:
                continue
        except:
            pass
