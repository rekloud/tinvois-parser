import re
import string

from .base import BaseReceipt
from ..utils import get_logger

logger = get_logger(__file__)


def regex_merchant_parser(receipt: BaseReceipt) -> str or None:
    for market, spellings in receipt.config["markets"].items():
        for spelling in spellings:
            matches = re.search(spelling, receipt.df_ocr.loc[0, "text"])
            if matches:
                receipt.merchant_from_list = True
                return market
    return string.capwords(
        receipt.df_ocr.loc[0, "text"]
        .split("\n")[0]
        .strip()
        .strip("-")
        .strip("_")
        .strip("/")
        .strip("\\")
        .strip("*")
        .strip("#")
        .strip()
    )
