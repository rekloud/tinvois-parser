import pandas as pd
from ...utils import get_logger
from ..base import _Receipt

logger = get_logger(__file__)


def parse_netto(receipt: _Receipt) -> int:
    netto_parsers = [parse_netto_from_table, parse_netto_in_front, parse_netto_from_vat]
    for netto_parser in netto_parsers:
        netto_value = netto_parser(receipt)
        if netto_value:
            receipt.netto_amount = netto_value
            return netto_value
    logger.warning('could not find netto')


def parse_netto_from_table(receipt: _Receipt) -> int:

    netto_value = receipt.df_values.loc[receipt.df_values['CLASS'] == 'NETTO_TABLE',
                                        'text2'].sum()
    if pd.notnull(netto_value):
        return int(netto_value)


def parse_netto_in_front(receipt: _Receipt) -> int:
    netto_value = receipt.df_values.loc[receipt.df_values['CLASS'] == 'NETTO_LINE',
                                        'text2'].sum()
    if pd.notnull(netto_value):
        return int(netto_value)


def parse_netto_from_vat(receipt: _Receipt):
    if hasattr(receipt, 'vat_value') and hasattr(receipt, 'sum'):
        return int(receipt.sum - receipt.vat_value)
