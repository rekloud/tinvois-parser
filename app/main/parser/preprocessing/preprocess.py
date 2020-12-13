import re
from typing import List
import pandas as pd
from ..ml_approach.preprocessing import tokenize
from .rotate import rotate_df_ocr
from .utils import merge_two_strings


def pre_process_ocr_results(receipt) -> (pd.DataFrame, float):
    df_ocr = receipt.df_ocr_raw.copy()
    df_ocr['text'] = df_ocr['text'].str.lower()
    df_ocr['text'] = (df_ocr['text'].str.replace(r'\(1\)', '')
                      .str.replace(r'\(2\)', '')
                      .str.replace(r'\(3\)', ''))
    df_ocr['token'] = df_ocr['text'].apply(lambda x: tokenize(x, receipt))

    df_ocr, rotation = rotate_df_ocr(df_ocr)
    df_ocr = merge_split_values(receipt, df_ocr)
    df_ocr.sort_values('1y', inplace=True)
    df_ocr['text2'] = (df_ocr['text'].str.replace(',', '')
                       .str.replace('.', '')
                       .str.replace('€', '')
                       .str.replace('$', '')
                       .str.replace('*', '')
                       .str.strip()
                       )
    df_ocr['is_numeric'] = (df_ocr['text2'].str.isdigit()
                            & (df_ocr['text2'].apply(len) >= 3)
                            & (df_ocr['text'].str.contains('[,\.]', regex=True))
                            )
    return df_ocr, rotation


def merge_split_values(receipt, df_ocr: pd.DataFrame) -> pd.DataFrame:
    """To merge the cases which numbers are split into two words by decimal separator like 13, 45"""
    indices = indices_with_split_values(df_ocr)
    if len(indices) > 0:
        for index in indices:
            index_after = get_index_of_word_after(df_ocr, index)
            if index_after:
                word_after = df_ocr.loc[index_after, 'text']
                if word_after.isdigit():
                    df_ocr = merge_two_strings(receipt, df_ocr, [index, index_after])
    return df_ocr


def indices_with_split_values(df_ocr: pd.DataFrame) -> List[int]:
    return [r.Index
            for r in df_ocr.itertuples()
            if len(re.findall('\d+[,\.]$', r.text)) > 0]


def get_index_of_word_after(df_ocr: pd.DataFrame, idx: int) -> int:
    row = df_ocr.loc[idx]
    word_height = abs(row['3y'] - row['2y'])
    df_same_line_after = df_ocr.loc[((df_ocr['3y'] - row['3y']).abs() <= .5 * word_height)
                             & (df_ocr['3x'] > row['3x'])
                             ]
    if len(df_same_line_after) > 0:
        return df_same_line_after.sort_values('1x', ascending=True).index[0]
