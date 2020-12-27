import numpy as np
import pandas as pd
from math import isclose


def rotate_df_ocr(df_ocr: pd.DataFrame) -> (pd.DataFrame, int):
    rotation = get_rotation(df_ocr)
    for i in range(1, 5):
        df_ocr[f'{i}y'] = - df_ocr[f'{i}y']
        df_ocr[[f'{i}x', f'{i}y']] = \
            rotate(df_ocr[[f'{i}x', f'{i}y']].values, degrees=-rotation)
        df_ocr[f'{i}y'] = - df_ocr[f'{i}y']
    return df_ocr, rotation


def get_rotation(df_ocr: pd.DataFrame) -> int:
    row = get_row_with_longest_word(df_ocr)
    slope = get_slope(row)
    rotation = int(np.round(np.degrees(np.arctan(slope))))
    return round_rotation(rotation, row, 1)


def get_row_with_longest_word(df_ocr: pd.DataFrame) -> pd.Series:
    _df_ocr = df_ocr.drop(0)[
        df_ocr.drop(0)['token'].isin(['NETTO', 'BRUTTO', 'VAT', 'SUM', 'VALUE'])]
    if len(_df_ocr) == 0:
        _df_ocr = df_ocr.drop(0)
    row = _df_ocr.assign(length=_df_ocr['text'].apply(len)
                         ).sort_values('length', ascending=False
                                       ).select_dtypes(np.number).iloc[0].astype(float)
    return row


def get_slope(row: pd.Series) -> float:
    denominator = row['3x'] - row['4x']
    if isclose(abs(denominator), 0, abs_tol=.01):
        slope = row['4y'] - row['3y']
    else:
        slope = (row['4y'] - row['3y']) / denominator
    return slope


def round_rotation(rotation: int, row: pd.Series, max_rotation: int) -> int:
    """
    ignore rotations less than 5 degrees
    """
    if isclose(abs(rotation), 90, abs_tol=max_rotation):
        if row['2x'] > row['3x']:
            return -90
        else:
            return 90
    if isclose(abs(rotation), 0, abs_tol=max_rotation):
        if row['2y'] > row['3y']:
            return 180
        else:
            return 0
    return rotation


def rotate(p: np.ndarray, degrees: float) -> np.ndarray:
    angle = np.deg2rad(degrees)
    R = np.array([[np.cos(angle), -np.sin(angle)],
                  [np.sin(angle), np.cos(angle)]])
    p = np.atleast_2d(p)
    return np.squeeze((R @ p.T).T)
