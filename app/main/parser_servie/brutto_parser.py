from ..utils import get_logger
from .base import _Receipt
from .netto_parser import _get_df_netto_brutto_table
logger = get_logger(__file__)


def parse_brutto(receipt: _Receipt) -> int:
    brutto_parsers = [parse_brutto_table, parse_brutto_table_with_steuer]
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

