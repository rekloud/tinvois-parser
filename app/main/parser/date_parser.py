import re
import dateutil
from ..utils import get_logger
from .base import BaseReceipt

logger = get_logger(__file__)


def parse_date(receipt: BaseReceipt) -> str:
    date_parsers = [
        regex_date_parser,
        regex_date_parser_from_full_text,
        regex_date_parser_direct_dateutils
    ]
    for date_parser in date_parsers:
        date_string = date_parser(receipt)
        if date_string is not None:
            return date_string
    logger.warning('could not parse date')


def regex_date_parser(receipt: BaseReceipt) -> str or None:
    for row in receipt.df_ocr.iloc[1:, :].itertuples():
        match = re.match(receipt.config['date_format'], row.text)
        if match:
            try:
                date_str = match.group(0)
                date_str = date_str.replace(" ", "").replace("\n", "")
                if len(date_str) < 6:
                    logger.debug(f'date_str dateutil: {date_str} too short')
                logger.debug(f'date_str: {date_str}')
                logger.info(f'date parsed using individual rows {date_str}')
                return dateutil.parser.parse(date_str, dayfirst=True).isoformat()
            except Exception as e:
                logger.warning(f'Failed to parse a date {str(e)}')
                continue


def regex_date_parser_from_full_text(receipt: BaseReceipt) -> str or None:
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
        except Exception as e:
            logger.warning(f'sth went wrong in date parser {e}')
            pass


def regex_date_parser_direct_dateutils(receipt: BaseReceipt) -> str or None:
    for row in receipt.df_ocr.iloc[1:, :].itertuples():
        try:
            date_str = row.text
            date_str = date_str.replace(" ", "")
            if len(date_str) < 6:
                logger.debug(f'date_str dateutil: {date_str} too short')
                continue
            logger.debug(f'date_str dateutil: {date_str}')
            d = dateutil.parser.parse(date_str, dayfirst=True).isoformat()
            logger.info(f'date parsed using individual rows dateutils {date_str}')
            return d
        except Exception as e:
            logger.warning(f'Failed to parse a date dateutils {str(e)}')
            continue
