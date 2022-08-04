import pandas as pd

from ..base import BaseReceipt
from ...utils import get_logger

logger = get_logger(__file__)


def parse_vat(receipt: BaseReceipt):
    vat_parsers = [parse_vat_from_table, parse_vat_in_front]
    for vat_parser in vat_parsers:
        vat_value = vat_parser(receipt)
        if vat_value:
            receipt.vat_value = vat_value
            return vat_value
    logger.warning("could not find vat")


def parse_vat_from_table(receipt: BaseReceipt):
    vat_value = receipt.df_values.loc[receipt.df_values["CLASS"] == "VAT_TABLE", "text2"].sum()
    if pd.notnull(vat_value) and (vat_value > 0):
        return int(vat_value)


def parse_vat_in_front(receipt: BaseReceipt):
    vat_value = receipt.df_values.loc[receipt.df_values["CLASS"] == "VAT_LINE", "text2"].sum()
    if pd.notnull(vat_value) and (vat_value > 0):
        return int(vat_value)
