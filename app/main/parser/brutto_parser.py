from ..utils import get_logger
from .base import _Receipt, find_one_value_in_front
from .netto_parser import _get_df_netto_brutto_table

logger = get_logger(__file__)


def parse_brutto(receipt: _Receipt) -> int:
    brutto_parsers = [parse_brutto_table, parse_brutto_table_with_steuer, parse_brutto_in_front]
    for brutto_parser in brutto_parsers:
        brutto_value = brutto_parser(receipt)
        if brutto_value:
            return brutto_value
    logger.warning('could not find brutto at all')


def parse_brutto_table(receipt: _Receipt):
    df_brutto = _get_df_netto_brutto_table(receipt, receipt.config['brutto_keys'])
    if df_brutto is not None:
        if len(df_brutto) > receipt.number_of_netto_values:
            df_brutto = df_brutto.sort_values('3y').head(receipt.number_of_netto_values)
        return int(df_brutto['text2'].sum())
    logger.info('could not find brutto from table')


def parse_brutto_table_with_steuer(self: _Receipt):
    df_steuer = _get_df_netto_brutto_table(self, self.config['steure_keys'])
    if df_steuer is None:
        logger.info('could not find steuer from table')
        return
    if len(df_steuer) > self.number_of_netto_values:
        df_steuer = df_steuer.sort_values('3y').head(self.number_of_netto_values)
    steuer_value = int(df_steuer['text2'].sum())
    return self.netto_amount + steuer_value


def parse_brutto_in_front(receipt: _Receipt) -> int:
    brutto_value = 0
    df_ocr = receipt.df_ocr.copy()
    while True:
        _brutto_value, match_index = find_one_value_in_front(df_ocr, receipt.df_values,
                                                             receipt.config['brutto_keys'],
                                                             receipt.cutoff)
        if _brutto_value is None:
            return brutto_value if brutto_value > 0 else None
        df_ocr.drop(df_ocr.index[match_index], inplace=True)
        brutto_value += _brutto_value
