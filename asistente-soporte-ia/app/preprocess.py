import re
import spacy
from nltk.stem.snowball import SpanishStemmer

nlp = spacy.load("es_core_news_md")
stemmer = SpanishStemmer()

def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = (
        text.replace("á", "a")
            .replace("é", "e")
            .replace("í", "i")
            .replace("ó", "o")
            .replace("ú", "u")
            .replace("ñ", "n")
    )
    text = re.sub(r"[^a-zA-Z0-9\\s]", " ", text)
    text = re.sub(r"\\s+", " ", text).strip()
    return text

def spacy_lemmatize(text: str) -> str:
    doc = nlp(normalize_text(text))
    lemmas = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(lemmas)

def nltk_stem_text(text: str) -> str:
    words = normalize_text(text).split()
    stems = [stemmer.stem(w) for w in words]
    return " ".join(stems)