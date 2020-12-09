import pandas as pd
from ...utils import get_logger
from ..base import _Receipt

logger = get_logger(__file__)


# TODO when netto could not be find try reducing VAT from SUM
def parse_netto(receipt: _Receipt) -> int:
    netto_parsers = [parse_netto_from_table, parse_netto_in_front]
    for netto_parser in netto_parsers:
        netto_value = netto_parser(receipt)
        if netto_value:
            return netto_value
    logger.warning('could not find netto')


def parse_netto_from_table(receipt: _Receipt) -> int:
    netto_value = receipt.df_values.loc[receipt.df_values['CLASS'] == 'NETTO_TABLE',
                                        'text2'].sum()
    if pd.notnull(netto_value):
        receipt.netto_amount = int(netto_value)
        return receipt.netto_amount


def parse_netto_in_front(receipt: _Receipt) -> int:
    netto_value = receipt.df_values.loc[receipt.df_values['CLASS'] == 'NETTO_LINE',
                                        'text2'].sum()
    if pd.notnull(netto_value):
        receipt.netto_amount = int(netto_value)
        return receipt.netto_amount
