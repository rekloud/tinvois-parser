import pandas as pd


def pre_process_ocr_results(df_ocr_raw: pd.DataFrame):
    df_ocr = df_ocr_raw.copy()
    df_ocr.sort_values('1y', inplace=True)
    df_ocr['text'] = df_ocr['text'].str.lower()
    df_ocr['text2'] = (df_ocr['text'].str.replace(',', '')
                       .str.replace('.', '')
                       .str.replace('€', '')
                       .str.replace('$', '')
                       .str.replace('*', '')
                       )
    df_ocr['is_numeric'] = df_ocr['text2'].str.isdigit() & (df_ocr['text2'].apply(len) >= 3)
    return df_ocr
