import nltk


def _nltk_downloader():
    try:
        nltk.download("vader_lexicon", quiet=True)
        nltk.download("subjectivity", quiet=True)
        nltk.download("stopwords", quiet=True)
        nltk.download("punkt", quiet=True)
    except LookupError as e:
        print(e)


_nltk_downloader()

from .analyser import *
