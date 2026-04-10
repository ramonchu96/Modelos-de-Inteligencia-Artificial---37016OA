import json
import joblib
import re
import unicodedata
from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "knowledge_base.json"
MODEL_FILE = BASE_DIR / "models" / "classifier.pkl"


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = unicodedata.normalize("NFD", text)
    text = "".join(char for char in text if unicodedata.category(char) != "Mn")
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def train_model():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = [normalize_text(item["text"]) for item in data]
    labels = [item["label"] for item in data]

    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
        ("clf", LogisticRegression(max_iter=3000))
    ])

    model.fit(texts, labels)
    MODEL_FILE.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_FILE)

    return model


def load_model():
    if MODEL_FILE.exists():
        return joblib.load(MODEL_FILE)
    return train_model()


def predict(text: str):
    model = load_model()
    clean_text = normalize_text(text)
    predicted_label = model.predict([clean_text])[0]
    probabilities = model.predict_proba([clean_text])[0]
    max_probability = max(probabilities)
    return predicted_label, float(max_probability)