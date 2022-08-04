import pandas as pd

from ..base import BaseReceipt
from ...utils import get_logger

logger = get_logger(__file__)


def parse_brutto_from_table(receipt: BaseReceipt) -> int:
    brutto_value = receipt.df_values.loc[
        receipt.df_values["CLASS"] == "BRUTTO_TABLE", "text2"
    ].sum()
    if pd.notnull(brutto_value) and (brutto_value > 0):
        return int(brutto_value)


def parse_brutto_in_front(receipt: BaseReceipt) -> int:
    brutto_value = receipt.df_values.loc[receipt.df_values["CLASS"] == "BRUTTO_LINE", "text2"].sum()
    if pd.notnull(brutto_value) and (brutto_value > 0):
        return int(brutto_value)


def parse_brutto_with_vat(receipt: BaseReceipt):
    if hasattr(receipt, "vat_value") and hasattr(receipt, "netto_amount"):
        return int(receipt.vat_value + receipt.netto_amount)
