import yaml
from difflib import SequenceMatcher
from heapq import nlargest as _nlargest
from ..config import PARSER_CONFIG_FILE


def read_config(config=PARSER_CONFIG_FILE):
    with open(config, 'r') as stream:
        try:
            docs = yaml.safe_load(stream)
            return docs
        except yaml.YAMLError as e:
            print(e)


def get_close_matches_indexes(word, possibilities, n=3, cutoff=0.6):
    """Use SequenceMatcher to return a list of the indexes of the best
    "good enough" matches. word is a sequence for which close matches
    are desired (typically a string).
    possibilities is a list of sequences against which to match word
    (typically a list of strings).
    Optional arg n (default 3) is the maximum number of close matches to
    return.  n must be > 0.
    Optional arg cutoff (default 0.6) is a float in [0, 1].  Possibilities
    that don't score at least that similar to word are ignored.
    """

    if not n > 0:
        raise ValueError("n must be > 0: %r" % (n,))
    if not 0.0 <= cutoff <= 1.0:
        raise ValueError("cutoff must be in [0.0, 1.0]: %r" % (cutoff,))
    result = []
    s = SequenceMatcher()
    s.set_seq2(word)
    # To ensure getting first match when it is a total match
    for idx, x in enumerate(possibilities):
        s.set_seq1(x)
        if n == 1 and \
           s.real_quick_ratio() >= .99 and \
           s.quick_ratio() >= .99 and \
           s.ratio() >= .99:
            return [idx]

        if s.real_quick_ratio() >= cutoff and \
           s.quick_ratio() >= cutoff and \
           s.ratio() >= cutoff:
            result.append((s.ratio(), idx))

    # Move the best scorers to head of list
    result = _nlargest(n, result)

    # Strip scores for the best n matches
    return [x for score, x in result]
