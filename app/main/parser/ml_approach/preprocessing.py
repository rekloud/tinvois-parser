from difflib import get_close_matches


def tokenize(text: str, receipt) -> str:
    for key_label, token in [('netto_keys', 'NETTO'),
                             ('brutto_keys', 'BRUTTO'),
                             ('steure_keys', 'VAT'),
                             ('sum_keys', 'SUM')]:
        for key in receipt.config[key_label]:
            matches = get_close_matches(key, [text], cutoff=receipt.cutoff)
            if len(matches) > 0:
                return token
    return 'OTHER'
