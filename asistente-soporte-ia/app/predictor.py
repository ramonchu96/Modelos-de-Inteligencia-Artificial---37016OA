import joblib
from pathlib import Path
from app.preprocess import spacy_lemmatize

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_FILE = BASE_DIR / "model" / "classifier.pkl"

classifier = joblib.load(MODEL_FILE)

def predict(text: str):
    processed = spacy_lemmatize(text)
    category = classifier.predict([processed])[0]
    return category