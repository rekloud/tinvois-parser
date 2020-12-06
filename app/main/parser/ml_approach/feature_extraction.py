import pandas as pd
from main.parser.base import _Receipt


def get_same_line_before(receipt: _Receipt, row: pd.Series, col_name: str) -> str:
    word_height = abs(row['3y'] - row['2y'])
    df_ocr = receipt.df_ocr
    df_filtered = df_ocr.loc[((df_ocr['3y'] - row['3y']).abs() <= word_height)
                             & (df_ocr['3x'] < row['3x'])
                             ]
    return '|'.join(df_filtered[col_name])


def get_same_line_after(receipt: _Receipt, row: pd.Series, col_name: str) -> str:
    word_height = abs(row['3y'] - row['2y'])
    df_ocr = receipt.df_ocr
    df_filtered = df_ocr.loc[((df_ocr['3y'] - row['3y']).abs() <= word_height)
                             & (df_ocr['3x'] > row['3x'])
                             ]
    return '|'.join(df_filtered[col_name])


def get_over(receipt: _Receipt, row: pd.Series, col_name: str) -> str:
    word_length = row['3x'] - row['4x']
    word_height = abs(row['3y'] - row['2y'])
    df_ocr = receipt.df_ocr
    df_filtered = df_ocr[((df_ocr['3x'] - row['3x']).abs() < (word_length / 1))
                         & ((row['3y'] - df_ocr['3y']).between(word_height / 2, word_height * 4))
                         ]
    return '|'.join(df_filtered[col_name])
