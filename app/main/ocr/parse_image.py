import re
import dateutil
from google.cloud import vision
import numpy as np
import pandas as pd
from .utils import read_config, get_close_matches_indexes
from ..utils import get_logger

client = vision.ImageAnnotatorClient()
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

    def get_date(self):
        for row in self.df_ocr.iloc[1:, :].itertuples():
            match = re.match(self.config['date_format'], row.text)
            if match:
                date_str = match.group(0)
                date_str = date_str.replace(" ", "")
                return dateutil.parser.parse(date_str, dayfirst=True).isoformat()

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
        self.number_of_netto_values = len(df_netto)
        return int(df_netto['text2'].sum())

    def get_brutto(self):
        df_brutto = self._get_df_netto_brutto(self.config['brutto_keys'])
        if len(df_brutto) > self.number_of_netto_values:
            df_brutto = df_brutto.sort_values('3y').head(self.number_of_netto_values)
        return int(df_brutto['text2'].sum())

    def _get_df_netto_brutto(self, keys):
        matches = None
        for key in keys:
            matches = get_close_matches_indexes(key, self.df_ocr['text'],
                                                n=1, cutoff=self.cutoff)
            if matches:
                break
        if not matches:
            logger.warning('could not find netto')
            return None
        row = self.df_ocr.iloc[matches, :].iloc[0, :]

        df_below = self.df_values[(self.df_values['3y'] - row['3y'])
                                  .between(0, self.image_y_range / 19)].copy()
        df = df_below[((df_below['3x'] - row['3x']).abs()
                       < self.image_x_range / 100)
                      & ((df_below['1x'] - row['1x']).abs()
                         < self.image_x_range / 10)]
        return df


def pre_process_ocr_results(df_ocr: pd.DataFrame):
    df_ocr['text'] = df_ocr['text'].str.lower()
    df_ocr['text2'] = df_ocr['text'].str.replace(',', '').str.replace('.', '')
    df_ocr['is_numeric'] = df_ocr['text2'].str.isdigit()
    return df_ocr


def ocr_image(image_content):
    image = vision.Image(content=image_content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    l_texts = []
    l_vertices = []
    for text in texts:
        l_texts.append(text.description)
        vertices = np.ravel([[vertex.x, vertex.y]
                             for vertex in text.bounding_poly.vertices])
        l_vertices.append(vertices)
    df_text = pd.DataFrame(l_vertices, columns=['1x', '1y', '2x', '2y', '3x', '3y', '4x', '4y'])
    df_text['text'] = l_texts
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return df_text
