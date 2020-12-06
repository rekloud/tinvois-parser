import pandas as pd
from ...utils import get_logger
from ..base import _Receipt

logger = get_logger(__file__)


def parse_sum(receipt: _Receipt) -> int:
    sum_value = receipt.df_values.loc[receipt.df_values['CLASS'] == 'SUM', 'text2'].max()
    if not pd.isnull(sum_value):
        receipt.sum = sum_value
        return int(sum_value)
    logger.warning('could not parse sum')
