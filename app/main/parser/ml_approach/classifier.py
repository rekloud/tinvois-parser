from main.parser.base import _Receipt


def classify(receipt: _Receipt):
    assert 'same_line_before_token' in receipt.df_values.columns, 'do the feature extraction first'
    classes = ['SUM', 'NETTO_TABLE', 'BRUTTO_TABLE', 'VAT_TABLE', 'NETTO_LINE',
               'BRUTTO_LINE', 'VAT_LINE']
    receipt.df_values['SUM'] = (receipt.df_values['same_line_before_token'].str.contains('SUM')
                                & (receipt.df_values['same_line_after_token'] == ''))

    receipt.df_values['NETTO_TABLE'] = (
            receipt.df_values['over_token'].str.contains('NETTO')
            & (~receipt.df_values['same_line_before_token'].str.contains('SUM'))
    )

    receipt.df_values['BRUTTO_TABLE'] = (
            receipt.df_values['over_token'].str.contains('BRUTTO')
            & (~receipt.df_values['same_line_before_token'].str.contains('SUM'))
    )

    receipt.df_values['VAT_TABLE'] = (
            receipt.df_values['over_token'].str.contains('VAT')
            & (~receipt.df_values['same_line_before_token'].str.contains('SUM'))
    )

    receipt.df_values['NETTO_LINE'] = (
            receipt.df_values['same_line_before_token'].str.contains('NETTO')
            & (~receipt.df_values['same_line_after_token'].str.contains('BRUTTO'))
    )

    receipt.df_values['BRUTTO_LINE'] = (
        receipt.df_values['same_line_before_token'].str.contains('BRUTTO')
    )

    receipt.df_values['VAT_LINE'] = (
        receipt.df_values['same_line_before_token'].str.contains('VAT')
    )
    receipt.df_values['CLASS'] = receipt.df_values[classes].idxmax(1)
    receipt.df_values.loc[receipt.df_values[classes].sum(1) == 0, 'CLASS'] = 'OTHER'
