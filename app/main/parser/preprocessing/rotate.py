import numpy as np
import pandas as pd
from math import isclose


def get_rotation(df_ocr: pd.DataFrame) -> int:
    _df_ocr = df_ocr.drop(0)[
        df_ocr.drop(0)['token'].isin(['NETTO', 'BRUTTO', 'VAT', 'SUM', 'VALUE'])]
    row = _df_ocr.assign(length=_df_ocr['text'].apply(len)
                         ).sort_values('length', ascending=False
                                       ).select_dtypes(np.number).iloc[0].astype(float)
    word_height_vertical = .25 * abs(row['3y'] - row['2y'])
    word_height_horizontal = .25 * abs(row['3x'] - row['2x'])
    if isclose(row['4x'], row['3x'], abs_tol=word_height_horizontal):
        denominator = 1
    else:
        denominator = row['3x'] - row['4x']
    if isclose(row['4y'], row['3y'], abs_tol=word_height_vertical):
        if row['2y'] > row['3y']:
            return 180
        else:
            return 0
    slope = (row['4y'] - row['3y']) / denominator
    return int(np.round(np.degrees(np.arctan(slope))))


def rotate_df_ocr(df_ocr: pd.DataFrame) -> (pd.DataFrame, int):
    rotation = get_rotation(df_ocr)
    for i in range(1, 5):
        df_ocr[f'{i}y'] = - df_ocr[f'{i}y']
        df_ocr[[f'{i}x', f'{i}y']] = \
            rotate(df_ocr[[f'{i}x', f'{i}y']].values, degrees=-rotation)
        df_ocr[f'{i}y'] = - df_ocr[f'{i}y']
    return df_ocr, rotation


def rotate(p: np.ndarray, degrees: float) -> np.ndarray:
    angle = np.deg2rad(degrees)
    R = np.array([[np.cos(angle), -np.sin(angle)],
                  [np.sin(angle), np.cos(angle)]])
    p = np.atleast_2d(p)
    return np.squeeze((R @ p.T).T)
