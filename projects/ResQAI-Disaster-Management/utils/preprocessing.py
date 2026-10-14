"""
ResQAI - text preprocessing pipeline.

Implements exactly the preprocessing chain named in the project abstract:
text cleaning -> tokenization -> stop-word removal -> stemming, ready for
TF-IDF vectorisation.

Shared by model/train_models.py (training) and utils/resqai_engine.py
(inference), so a tweet is processed identically in both paths.
"""

import re

from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer

# RegexpTokenizer avoids the punkt/punkt_tab download dance and gives the same
# word-level split we need for stemming. PorterStemmer is algorithmic, so
# neither needs a downloaded corpus.
_TOKENIZER = RegexpTokenizer(r"[a-z]+")
_STEMMER = PorterStemmer()

# NLTK's standard English stop-word list, embedded rather than loaded via
# nltk.corpus. On Windows Store Python, NLTK's path-security check rejects the
# virtualised nltk_data directory ("Security Violation ... escapes root"), which
# would make the app fail at import on the target machine. The list is a fixed
# constant, so inlining it removes that runtime dependency entirely.
_NLTK_ENGLISH_STOPWORDS = """
i me my myself we our ours ourselves you you're you've you'll you'd your yours
yourself yourselves he him his himself she she's her hers herself it it's its
itself they them their theirs themselves what which who whom this that that'll
these those am is are was were be been being have has had having do does did
doing a an the and but if or because as until while of at by for with about
against between into through during before after above below to from up down in
out on off over under again further then once here there when where why how all
any both each few more most other some such no nor not only own same so than too
very s t can will just don don't should should've now d ll m o re ve y ain aren
aren't couldn couldn't didn didn't doesn doesn't hadn hadn't hasn hasn't haven
haven't isn isn't ma mightn mightn't mustn mustn't needn needn't shan shan't
shouldn shouldn't wasn wasn't weren weren't won won't wouldn wouldn't
""".split()

_STOPWORDS = set(_NLTK_ENGLISH_STOPWORDS)
# "not"/"no" flip the meaning of an emergency report - keep them.
_STOPWORDS -= {"not", "no", "nor", "against", "down", "off", "under", "over"}

URL_RE = re.compile(r"https?://\S+|www\.\S+")
MENTION_RE = re.compile(r"@\w+")
HTML_RE = re.compile(r"&[a-z]+;")
NONALPHA_RE = re.compile(r"[^a-z\s]")
SPACE_RE = re.compile(r"\s+")


def clean_text(text):
    """Step 1 - text cleaning: lowercase, strip URLs, @mentions, HTML entities,
    digits and punctuation."""
    text = str(text).lower()
    text = URL_RE.sub(" ", text)
    text = MENTION_RE.sub(" ", text)
    text = HTML_RE.sub(" ", text)
    text = text.replace("#", " ")            # keep the hashtag word, drop the '#'
    text = NONALPHA_RE.sub(" ", text)
    return SPACE_RE.sub(" ", text).strip()


def preprocess(text):
    """Full chain: clean -> tokenize -> remove stop-words -> stem."""
    cleaned = clean_text(text)
    tokens = _TOKENIZER.tokenize(cleaned)
    tokens = [t for t in tokens if t not in _STOPWORDS and len(t) > 2]
    tokens = [_STEMMER.stem(t) for t in tokens]
    return " ".join(tokens)


def build_corpus(df, text_col="text", keyword_col="keyword"):
    """Preprocess a dataframe's tweets. The `keyword` column is a real signal
    in this dataset (it is the disaster term the tweet was collected under),
    so it is appended to the text before vectorising."""
    texts = df[text_col].fillna("")
    if keyword_col in df.columns:
        kw = df[keyword_col].fillna("").astype(str).str.replace("%20", " ", regex=False)
        texts = texts + " " + kw
    return texts.map(preprocess)
