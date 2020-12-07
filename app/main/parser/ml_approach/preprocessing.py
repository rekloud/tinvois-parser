from difflib import get_close_matches


def tokenize(text: str, receipt) -> str:
    for key_label, token in [('sum_keys', 'SUM'), ('netto_keys', 'NETTO'),
                             ('brutto_keys', 'BRUTTO'), ('steure_keys', 'VAT')]:
        for key in receipt.config[key_label]:
            matches = get_close_matches(key, [text], cutoff=receipt.cutoff)
            if (len(matches) > 0) or (key in text):
                return token
    return 'OTHER'
