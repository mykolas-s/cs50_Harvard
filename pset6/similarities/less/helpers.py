from nltk.tokenize import sent_tokenize

def lines(a, b):
    """Return lines in both a and b"""
    # split a and b in lines
    splitted_a = a.splitlines()
    splitted_b = b.splitlines()
    
    # compute set of lines in both a and b (duplicate matches excluded)
    set_ab = set(splitted_a) & set(splitted_b)
    return (set_ab)


def sentences(a, b):
    """Return sentences in both a and b"""
    # split a and b in sentences
    splitted_a = sent_tokenize(a, language='english')
    splitted_b = sent_tokenize(b, language='english')
    
    # compute set of sentences in both a and b (duplicate matches excluded)
    set_ab = set(splitted_a) & set(splitted_b)
    return (set_ab)


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    # compute lists of substrings in a and b
    list_a = []
    list_b = []
    for i in range(len(a) - n + 1):
        list_a.append(a[i:i+n]) # append list with substrings of lenght n
    for j in range(len(b) - n + 1):
        list_b.append(b[j:j+n]) # append list with substrings of lenght n
    
    # make set (which excludes duplicate matches)
    set_ab = set(list_a) & set(list_b)
    return (set_ab)