from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.rules import extract_entities_and_rules
from app.schemas import ChatRequest, ChatResponse
from app.classifier import predict
from app.recommender import build_response

app = FastAPI(title="Asistente Virtual de Soporte Técnico")

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
INDEX_FILE = STATIC_DIR / "index.html"

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
def read_index():
    return FileResponse(str(INDEX_FILE))


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    category, score = predict(request.question)
    category = str(category)

    rule_hits = extract_entities_and_rules(request.question)
    response = build_response(category, request.question, rule_hits)

    return ChatResponse(
    category=category,
    confidence=float(score),
    answer=response.get("answer", "No he podido generar una respuesta."),
    steps=response.get("steps", []),
    recommendations=response.get("recommendations", []),
    detected_terms=rule_hits
  )