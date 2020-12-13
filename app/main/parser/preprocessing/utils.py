from typing import List
import numpy as np
import pandas as pd
from ..ml_approach.preprocessing import tokenize


def merge_two_strings(receipt, df_ocr: pd.DataFrame, indices: List[int]) -> pd.DataFrame:
    rows = [df_ocr.loc[i] for i in indices]
    merged_row = df_ocr.loc[indices[0]].copy()
    merged_row['1x'] = np.min([row['1x'] for row in rows])
    merged_row['1y'] = np.min([row['1y'] for row in rows])
    merged_row['2x'] = np.max([row['2x'] for row in rows])
    merged_row['2y'] = np.min([row['2y'] for row in rows])
    merged_row['3x'] = np.max([row['3x'] for row in rows])
    merged_row['3y'] = np.max([row['3y'] for row in rows])
    merged_row['4x'] = np.min([row['4x'] for row in rows])
    merged_row['4y'] = np.max([row['4y'] for row in rows])
    merged_text = ''.join([row['text'] for row in rows])
    merged_row['text'] = merged_text
    merged_row['token'] = tokenize(merged_text, receipt)
    df_ocr.loc[df_ocr.index.max() + 1] = merged_row
    return df_ocr
