import pandas as pd
from .rotate import rotate_df_ocr


def pre_process_ocr_results(df_ocr_raw: pd.DataFrame, rotation: int) -> pd.DataFrame:
    df_ocr = df_ocr_raw.copy()
    df_ocr = rotate_df_ocr(df_ocr, degrees=rotation)
    df_ocr.sort_values('1y', inplace=True)
    df_ocr['text'] = df_ocr['text'].str.lower()
    df_ocr['text'] = (df_ocr['text'].str.replace('\(1\)', '')
                      .str.replace('\(2\)', '')
                      .str.replace('\(3\)', ''))
    df_ocr['text2'] = (df_ocr['text'].str.replace(',', '')
                       .str.replace('.', '')
                       .str.replace('€', '')
                       .str.replace('$', '')
                       .str.replace('*', '')
                       .str.strip()
                       )
    df_ocr['is_numeric'] = df_ocr['text2'].str.isdigit() & (df_ocr['text2'].apply(len) >= 3)
    return df_ocr
