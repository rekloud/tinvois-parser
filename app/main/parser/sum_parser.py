from ..utils import get_logger
from .base import _Receipt
from .base import find_value_in_front

logger = get_logger(__file__)


def parse_sum(receipt: _Receipt) -> int:
    sum_parsers = [parse_sum_in_front]
    for sum_parser in sum_parsers:
        sum_value = sum_parser(receipt)
        if sum_value is not None:
            receipt.sum = sum_value
            return sum_value
    logger.warning('could not parse sum')


def parse_sum_in_front(receipt: _Receipt):
    sum_value = find_value_in_front(receipt, receipt.config['sum_keys'])
    if sum_value is None:
        logger.info('could not find sum in front')
    return sum_value
