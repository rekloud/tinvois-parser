from ..config import MAX_ROWS_OF_TAX_TABLE
from ..utils import get_logger
from .base import _Receipt
from .utils import get_close_matches_indexes

logger = get_logger(__file__)


def _get_df_netto_brutto_table(receipt: _Receipt, keys):
    matches = None
    for key in keys:
        matches = get_close_matches_indexes(key, receipt.df_ocr['text'],
                                            n=1, cutoff=receipt.cutoff)
        if matches and (key != 'total'):
            break
    if not matches:
        return None
    row = receipt.df_ocr.iloc[matches, :].iloc[0, :]
    word_height = row['3y'] - row['2y']
    word_length = row['2x'] - row['1x']
    df_below = receipt.df_values[(receipt.df_values['3y'] - row['3y'])
                                 .between(0, word_height * 4)].copy()
    df = df_below[((df_below['3x'] - row['3x']).abs()
                   < word_length / 2)
                  & ((df_below['1x'] - row['1x']).abs()
                     < receipt.image_x_range / 10)]
    return df.head(MAX_ROWS_OF_TAX_TABLE)
