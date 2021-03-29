import unicodedata


def normalize(string):
    return unicodedata.normalize("NFD", string)\
        .encode("ascii", "ignore")\
        .decode()
