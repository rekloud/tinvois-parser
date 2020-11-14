import re
import dateutil

import pandas as pd
from .ocr import ocr_image
from .utils import read_config, get_close_matches_indexes, pre_process_ocr_results
from ..utils import get_logger

logger = get_logger(__file__)


class Receipt:
    def __init__(self, image_content, cutoff=.8):
        self.config = read_config()
        self.df_ocr = pre_process_ocr_results(ocr_image(image_content))
        self.image_x_range = self.df_ocr['2x'].max() - self.df_ocr['1x'].min()
        self.image_y_range = self.df_ocr['3y'].max() - self.df_ocr['1y'].min()
        self.df_values = self.df_ocr.loc[self.df_ocr['is_numeric'], :].copy()
        self.df_values['text2'] = self.df_values['text2'].astype(float)
        self.cutoff = cutoff
        self.number_of_netto_values = 4
        self.netto_amount = 0

    def get_date(self):
        for row in self.df_ocr.iloc[1:, :].itertuples():
            match = re.match(self.config['date_format'], row.text)
            if match:
                date_str = match.group(0)
                date_str = date_str.replace(" ", "")
                return dateutil.parser.parse(date_str, dayfirst=True).isoformat()

    def get_merchant(self):
        for market, spellings in self.config['markets'].items():
            for spelling in spellings:
                matches = get_close_matches_indexes(spelling, self.df_ocr['text'],
                                                    n=1, cutoff=self.cutoff)
                if matches:
                    return market
        return self.df_ocr.loc[1, 'text']

    def get_sum(self):
        matches = None
        for sum_ky in self.config['sum_keys']:
            matches = get_close_matches_indexes(sum_ky, self.df_ocr['text'],
                                                n=1, cutoff=self.cutoff)
            if matches:
                break
        if not matches:
            logger.warning('could not find total')
            return None
        sum_row = self.df_ocr.iloc[matches, :]

        sum_row_with_value = pd.merge_asof(sum_row,
                                           self.df_values.sort_values('3y'),
                                           on='3y', direction='nearest', suffixes=('', '_value'))
        return int(sum_row_with_value['text2_value'].iloc[0])

    def get_netto(self):
        df_netto = self._get_df_netto_brutto(self.config['netto_keys'])
        if df_netto is not None:
            self.number_of_netto_values = len(df_netto)
            self.netto_amount = int(df_netto['text2'].sum())
            return self.netto_amount
        else:
            logger.warning('could not find netto')

    def get_brutto(self):
        df_brutto = self._get_df_netto_brutto(self.config['brutto_keys'])
        if df_brutto is None:
            logger.warning('could not find brutto')
            return self.netto_amount + self.get_steuer()
        if len(df_brutto) > self.number_of_netto_values:
            df_brutto = df_brutto.sort_values('3y').head(self.number_of_netto_values)
        return int(df_brutto['text2'].sum())

    def get_steuer(self):
        df_steuer = self._get_df_netto_brutto(self.config['steure_keys'])
        if df_steuer is None:
            logger.warning('could not find steuer')
            return 0
        if len(df_steuer) > self.number_of_netto_values:
            df_steuer = df_steuer.sort_values('3y').head(self.number_of_netto_values)
        return int(df_steuer['text2'].sum())

    def _get_df_netto_brutto(self, keys):
        matches = None
        for key in keys:
            matches = get_close_matches_indexes(key, self.df_ocr['text'],
                                                n=1, cutoff=self.cutoff)
            if matches and (key != 'total'):
                break
        if not matches:
            return None
        row = self.df_ocr.iloc[matches, :].iloc[0, :]
        word_height = row['3y'] - row['2y']
        word_length = row['2x'] - row['1x']
        df_below = self.df_values[(self.df_values['3y'] - row['3y'])
                                  .between(0, word_height * 4)].copy()
        df = df_below[((df_below['3x'] - row['3x']).abs()
                       < word_length / 3)
                      & ((df_below['1x'] - row['1x']).abs()
                         < self.image_x_range / 10)]
        return df
