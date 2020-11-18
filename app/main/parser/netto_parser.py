from ..utils import get_logger
from .base import _Receipt, find_one_value_in_front
from .netto_brutto_parser import _get_df_netto_brutto_table
logger = get_logger(__file__)


def parse_netto(receipt: _Receipt) -> int:
    netto_parsers = [parse_netto_table, parse_netto_in_front]
    for netto_parser in netto_parsers:
        netto_value = netto_parser(receipt)
        if netto_value:
            if (hasattr(receipt, 'sum')) and (netto_value > receipt.sum):
                netto_value = int(netto_value / 2)
            return netto_value
    logger.warning('could not find netto')


def parse_netto_table(receipt: _Receipt) -> int:
    df_netto = _get_df_netto_brutto_table(receipt, receipt.config['netto_keys'])
    if df_netto is not None:
        receipt.number_of_netto_values = len(df_netto)
        receipt.netto_amount = int(df_netto['text2'].sum())
        return receipt.netto_amount


def parse_netto_in_front(receipt: _Receipt) -> int:
    netto_value = 0
    df_ocr = receipt.df_ocr.copy()
    while True:
        _netto_value, match_index = find_one_value_in_front(df_ocr, receipt.df_values,
                                                            receipt.config['netto_keys'],
                                                            receipt.cutoff)
        if _netto_value is None:
            return netto_value if netto_value > 0 else None
        df_ocr.drop(df_ocr.index[match_index], inplace=True)
        netto_value += _netto_value
