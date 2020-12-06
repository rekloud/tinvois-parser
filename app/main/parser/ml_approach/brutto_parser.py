import pandas as pd
from ...utils import get_logger
from ..base import _Receipt

logger = get_logger(__file__)


def parse_brutto(receipt: _Receipt) -> int:
    brutto_parsers = [parse_brutto_direct, parse_brutto_with_vat]
    for brutto_parser in brutto_parsers:
        brutto_value = brutto_parser(receipt)
        if brutto_value:
            return brutto_value
    logger.warning('could not find brutto at all')


# TODO split this in two functions
def parse_brutto_direct(receipt: _Receipt) -> int:
    brutto_value = receipt.df_values.loc[receipt.df_values['CLASS'] == 'BRUTTO_TABLE',
                                         'text2'].sum()
    if pd.notnull(brutto_value) and (brutto_value > 0):
        return int(brutto_value)
    brutto_value = receipt.df_values.loc[receipt.df_values['CLASS'] == 'BRUTTO_LINE',
                                         'text2'].sum()
    if pd.notnull(brutto_value) and (brutto_value > 0):
        return int(brutto_value)
    logger.warning('could not find brutto from table')


# TODO split this in two functions
def parse_brutto_with_vat(receipt: _Receipt):
    vat_value = receipt.df_values.loc[receipt.df_values['CLASS'] == 'VAT_TABLE',
                                      'text2'].sum()
    if pd.notnull(vat_value) and (vat_value > 0):
        return int(vat_value) + receipt.netto_amount
    vat_value = receipt.df_values.loc[receipt.df_values['CLASS'] == 'VAT_LINE',
                                      'text2'].sum()
    if pd.notnull(vat_value) and (vat_value > 0):
        return int(vat_value) + receipt.netto_amount
    logger.warning('could not find brutto from vat')
