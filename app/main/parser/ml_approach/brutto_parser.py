import pandas as pd
from ...utils import get_logger
from ..base import BaseReceipt

logger = get_logger(__file__)


def parse_brutto(receipt: BaseReceipt) -> int:
    brutto_parsers = [parse_brutto_from_table, parse_brutto_in_front, parse_brutto_with_vat]
    for brutto_parser in brutto_parsers:
        brutto_value = brutto_parser(receipt)
        if brutto_value:
            return brutto_value
    logger.warning('could not find brutto at all')


def parse_brutto_from_table(receipt: BaseReceipt) -> int:
    brutto_value = receipt.df_values.loc[receipt.df_values['CLASS'] == 'BRUTTO_TABLE',
                                         'text2'].sum()
    if pd.notnull(brutto_value) and (brutto_value > 0):
        return int(brutto_value)


def parse_brutto_in_front(receipt: BaseReceipt) -> int:
    brutto_value = receipt.df_values.loc[receipt.df_values['CLASS'] == 'BRUTTO_LINE',
                                         'text2'].sum()
    if pd.notnull(brutto_value) and (brutto_value > 0):
        return int(brutto_value)


def parse_brutto_with_vat(receipt: BaseReceipt):
    if hasattr(receipt, 'vat_value') and hasattr(receipt, 'netto_amount'):
        return int(receipt.vat_value + receipt.netto_amount)
