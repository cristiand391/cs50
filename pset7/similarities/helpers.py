def lines(a, b):
    """Return lines in both a and b"""

    lines_a = a.split('\n')
    lines_b = b.split('\n')

    matches = {line for line in lines_a if line in lines_b}

    return matches


def sentences(a, b):
    """Return sentences in both a and b"""

    from nltk.tokenize import sent_tokenize

    sents_a = sent_tokenize(a)
    sents_b = sent_tokenize(b)

    matches = {sent for sent in sents_a if sent in sents_b}

    return matches


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    def substring(s, n):
        subs = set()

        for i in range(len(s) - 1):
            if n > len(s):
                break
            subs.add(s[i:n])
            n += 1

        return subs

    subs_a = substring(a, n)
    subs_b = substring(b, n)

    matches = subs_a.intersection(subs_b)

    return matches
