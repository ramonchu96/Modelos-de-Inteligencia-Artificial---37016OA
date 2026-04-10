import json
import joblib
from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from app.preprocess import spacy_lemmatize

BASE_DIR = Path(__file__).resolve().parent
TRAIN_FILE = BASE_DIR / "data" / "training_data.json"
MODEL_DIR = BASE_DIR / "model"
MODEL_DIR.mkdir(exist_ok=True)

with open(TRAIN_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

X = [spacy_lemmatize(item["text"]) for item in data]
y = [item["label"] for item in data]

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
    ("clf", LinearSVC())
])

pipeline.fit(X, y)

joblib.dump(pipeline, MODEL_DIR / "classifier.pkl")
print("Modelo entrenado correctamente.")