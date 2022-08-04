import pandas as pd

from ..base import BaseReceipt
from ...utils import get_logger

logger = get_logger(__file__)


def parse_netto_from_table(receipt: BaseReceipt) -> int:

    netto_value = receipt.df_values.loc[receipt.df_values["CLASS"] == "NETTO_TABLE", "text2"].sum()
    if pd.notnull(netto_value):
        return int(netto_value)


def parse_netto_in_front(receipt: BaseReceipt) -> int:
    netto_value = receipt.df_values.loc[receipt.df_values["CLASS"] == "NETTO_LINE", "text2"].sum()
    if pd.notnull(netto_value):
        return int(netto_value)


def parse_netto_from_vat(receipt: BaseReceipt):
    if hasattr(receipt, "vat_value") and hasattr(receipt, "sum"):
        return int(receipt.sum - receipt.vat_value)
