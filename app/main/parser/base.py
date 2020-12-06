from typing import List
import numpy as np
import pandas as pd
from .ocr import ocr_image
from .utils import read_config, get_close_matches_indexes
from .preprocessing import pre_process_ocr_results, get_rotation
from ..utils import get_logger

logger = get_logger(__file__)


class _Receipt:
    def __init__(self, image_content, cutoff=.8):
        self.cutoff = cutoff
        self.config = read_config()
        self.image_content = image_content
        self.df_ocr_raw = ocr_image(image_content)
        self.number_of_netto_values = 4
        self.netto_amount = 0
        self.rotation = get_rotation(self.df_ocr_raw)
        self.df_ocr = pre_process_ocr_results(self)
        self.image_x_range = self.df_ocr['2x'].max() - self.df_ocr['1x'].min()
        self.image_y_range = self.df_ocr['3y'].max() - self.df_ocr['1y'].min()
        self.df_values = self.df_ocr.loc[self.df_ocr['is_numeric'], :].copy()
        self.df_values['text2'] = self.df_values['text2'].astype(float)
        self.line_height = np.median(self.df_ocr['3y'] - self.df_ocr['2y'])


def find_value_in_front(receipt: _Receipt, keys: List[int]) -> (int or None, int):
    return find_one_value_in_front(receipt.df_ocr, receipt.df_values, keys, receipt.cutoff)


def find_one_value_in_front(df_ocr: pd.DataFrame, df_values: pd.DataFrame,
                            keys: List[int], cutoff: float) -> (int or None, int):
    match = None
    for sum_ky in keys:
        match = get_close_matches_indexes(sum_ky, df_ocr['text'].values,
                                          n=1, cutoff=cutoff)
        if match:
            break
    if not match:
        return None, match
    row = df_ocr.iloc[match, :]
    assert len(row) == 1, 'only one row is accepted'
    logger.debug(f'value in front based on text: {row["text"].iloc[0]}')
    word_height = (row['3y'] - row['2y']).mean()
    close_numbers = df_values[(df_values['3y'] -
                               row['3y'].iloc[0]).abs() <= (word_height * 1.2)].copy()
    close_numbers['distance_y'] = (close_numbers['3y'] - row['3y'].iloc[0]).abs()
    close_numbers['distance_x'] = (close_numbers['3x'] - row['3x'].iloc[0]).abs()
    value_in_front = close_numbers.sort_values(['distance_y', 'distance_x']).head(1)
    if len(value_in_front) > 0:
        try:
            return int(value_in_front['text2'].iloc[0]), match
        except ValueError as e:
            logger.debug(f'{str(e)}')
            return None, match
    return None, match
