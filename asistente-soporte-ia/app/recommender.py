import json
from pathlib import Path
import random

BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_FILE = BASE_DIR / "data" / "knowledge_base.json"


def load_knowledge_base():
    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_text(text: str) -> str:
    return (
        text.lower()
        .strip()
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ñ", "n")
    )


def extract_keywords(text: str):
    text = normalize_text(text)

    possible_keywords = [
        "wifi", "internet", "router", "portatil", "cable",
        "contrasena", "clave", "correo", "bloqueada", "usuario",
        "atasco", "papel", "tinta", "hp", "cola",
        "error", "aplicacion", "programa", "bloquea", "cierra",
        "lento", "arrancar", "memoria", "disco",
        "microfono", "micro", "auriculares", "teams", "volumen",
        "webcam", "zoom", "permiso", "negro",
        "outlook", "enviar", "recibir", "sincroniza", "email",
        "teclas", "bloqueado", "escribe", "usb",
        "cursor", "inalambrico", "touchpad", "clic",
        "negra", "monitor","pantalla", "externa", "parpadea", "imagen",
        "vpn", "word", "excel"
    ]

    found = []
    for keyword in possible_keywords:
        if keyword in text:
            found.append(keyword)

    return found


def pick_base_answer(category_info: dict) -> str:
    variants = category_info.get("variants", [])
    if variants:
        return random.choice(variants)
    return category_info.get("base_answer", "No he podido generar una respuesta.")


def build_response(category: str, question: str, rule_hits=None):
    if rule_hits is None:
        rule_hits = []

    knowledge_base = load_knowledge_base()

    normalized_knowledge_base = {
        normalize_text(k): v for k, v in knowledge_base.items()
    }

    normalized_category = normalize_text(category)

    if normalized_category not in normalized_knowledge_base:
        return {
            "answer": "No he podido identificar exactamente la incidencia, pero solo puedo ayudarte con consultas de soporte técnico contempladas en la base de conocimiento.",
            "steps": [],
            "recommendations": []
        }

    category_info = normalized_knowledge_base[normalized_category]

    found_keywords = extract_keywords(question)
    normalized_rule_hits = [normalize_text(x) for x in rule_hits]

    rec_map = category_info.get("recommendations", {})

    # Filtrar solo rule_hits que existan en recommendations
    valid_rule_hits = [term for term in normalized_rule_hits if term in rec_map]

    # Si no hay palabras clave ni rule_hits válidos, devolver mensaje de no soportado
    if not found_keywords and not valid_rule_hits:
        return {
            "answer": "No puedo consultar ese tipo de información. Solo puedo ayudarte con incidencias de soporte técnico contempladas en la base de conocimiento.",
            "steps": [],
            "recommendations": []
        }

    recommendations = []

    for keyword in found_keywords:
        if keyword in rec_map and rec_map[keyword] not in recommendations:
            recommendations.append(rec_map[keyword])

    for term in valid_rule_hits:
        if rec_map[term] not in recommendations:
            recommendations.append(rec_map[term])

    return {
        "answer": pick_base_answer(category_info),
        "steps": category_info.get("steps", []),
        "recommendations": recommendations
    }