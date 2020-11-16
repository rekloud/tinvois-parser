import pandas as pd
from .ocr import ocr_image
from .utils import read_config, get_close_matches_indexes, pre_process_ocr_results
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


def find_value_in_front(receipt: _Receipt, keys):
    matches = None
    for sum_ky in keys:
        matches = get_close_matches_indexes(sum_ky, receipt.df_ocr['text'],
                                            n=1, cutoff=receipt.cutoff)
        if matches:
            break
    if not matches:
        return None
    row = receipt.df_ocr.iloc[matches, :]

    row_with_value = pd.merge_asof(row,
                                       receipt.df_values.sort_values('3y'),
                                       on='3y', direction='nearest', suffixes=('', '_value'))
    return int(row_with_value['text2_value'].iloc[0])
