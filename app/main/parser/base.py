from typing import List
import pandas as pd
from .ocr import ocr_image
from .utils import read_config, get_close_matches_indexes
from .preprocessing import pre_process_ocr_results
from ..utils import get_logger

logger = get_logger(__file__)


class _Receipt:
    def __init__(self, image_content, cutoff=.8):
        self.config = read_config()
        # TODO rotate if the image is horizontal
        self.image_content = image_content
        self.df_ocr_raw = ocr_image(image_content)
        self.df_ocr = pre_process_ocr_results(self.df_ocr_raw)
        self.image_x_range = self.df_ocr['2x'].max() - self.df_ocr['1x'].min()
        self.image_y_range = self.df_ocr['3y'].max() - self.df_ocr['1y'].min()
        self.df_values = self.df_ocr.loc[self.df_ocr['is_numeric'], :].copy()
        self.df_values['text2'] = self.df_values['text2'].astype(float)
        self.cutoff = cutoff
        self.number_of_netto_values = 4
        self.netto_amount = 0


def find_value_in_front(receipt: _Receipt, keys: List[int]) -> int or None:
    matches = None
    for sum_ky in keys:
        matches = get_close_matches_indexes(sum_ky, receipt.df_ocr['text'].values,
                                            n=1, cutoff=receipt.cutoff)
        if matches:
            break
    if not matches:
        return None
    row = receipt.df_ocr.iloc[matches, :]
    assert len(row) == 1, 'only one row is accepted'
    logger.debug(f'value in front based on text: {row["text"].iloc[0]}')
    word_height = (row['3y'] - row['2y']).mean()
    close_numbers = receipt.df_values[(receipt.df_values['3y'] -
                                       row['3y'].iloc[0]).abs() <= (word_height * 2)].copy()
    close_numbers['distance'] = (close_numbers['3y'] - row['3y'].iloc[0]).abs()
    values_in_front = close_numbers.sort_values('distance').head(1)
    if len(values_in_front) > 0:
        try:
            return int(values_in_front['text2'].iloc[0])
        except ValueError as e:
            logger.debug(f'{str(e)}')
            return None
