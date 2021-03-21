import re

import dateutil
import datetime

from .base import BaseReceipt
from ..utils import get_logger

logger = get_logger(__file__)
default_date = datetime.datetime.now().replace(year=1900, hour=0, minute=0,
                                               second=0, microsecond=0)


def parse_date(receipt: BaseReceipt) -> str:
    date_parsers = [
        regex_date_parser_direct_dateutils,
        # regex_date_parser,
        regex_date_parser_from_full_text,
    ]
    for date_parser in date_parsers:
        date_string = date_parser(receipt)
        if date_string is not None:
            return date_string.replace(hour=0, minute=0,
                                       second=0, microsecond=0).isoformat()
    logger.warning('could not parse date')


def regex_date_parser(receipt: BaseReceipt) -> datetime.datetime or None:
    for row in receipt.df_ocr.iloc[1:, :].itertuples():
        match = re.match(receipt.config['date_format'], row.text)
        if match:
            try:
                date_str = match.group(0)
                date_str = date_str.replace(" ", "").replace("\n", "")
                if len(date_str) < 6:
                    logger.debug(f'date_str dateutil: {date_str} too short')
                logger.debug(f'date_str: {date_str}')
                detected_date = dateutil.parser.parse(date_str, dayfirst=True, default=default_date)
                validate_detected_date(detected_date)
                logger.info(f'date parsed using individual rows {date_str}')
                return detected_date
            except Exception as e:
                logger.warning(f'Failed to parse a date {str(e)}')
                continue


def regex_date_parser_from_full_text(receipt: BaseReceipt) -> datetime.datetime or None:
    matches = re.findall(receipt.config['date_format2'], receipt.df_ocr.iloc[0, :].text)
    for date_str in matches:
        try:
            date_str = date_str.replace(" ", "")
            logger.debug(f'date_str: {date_str}')
            parsed_date = dateutil.parser.parse(date_str, dayfirst=True, default=default_date)
            validate_detected_date(parsed_date)
            logger.info(f'date parsed using full rows {date_str}')
            return parsed_date
        except Exception as e:
            logger.warning(f'sth went wrong in date parser {e}')
            pass


def regex_date_parser_direct_dateutils(receipt: BaseReceipt) -> datetime.datetime or None:
    for row in receipt.df_ocr.iloc[1:, :].itertuples():
        try:
            date_str = row.text
            date_str = date_str.replace(" ", "")
            if len(date_str) < 6:
                logger.debug(f'date_str dateutil: {date_str} too short')
                continue
            logger.debug(f'date_str dateutil: {date_str}')
            detected_date = dateutil.parser.parse(date_str, dayfirst=True, default=default_date)
            validate_detected_date(detected_date)
            logger.info(f'date parsed using individual rows dateutils {date_str}')
            return detected_date
        except Exception as e:
            logger.warning(f'Failed to parse a date dateutils {str(e)}')
            continue


def validate_detected_date(detected_date):
    detected_year = detected_date.year
    if detected_year < 1990 or detected_year > (datetime.date.today().year + 2):
        raise Exception(f'invalid year {detected_date.year}')
