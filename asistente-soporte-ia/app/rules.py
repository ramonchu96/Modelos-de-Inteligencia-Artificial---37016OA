import spacy
from spacy.matcher import Matcher

nlp = spacy.load("es_core_news_md")
matcher = Matcher(nlp.vocab)

matcher.add("VPN", [[{"LOWER": "vpn"}]])
matcher.add("OUTLOOK", [[{"LOWER": "outlook"}]])
matcher.add("TEAMS", [[{"LOWER": "teams"}]])
matcher.add("IMPRESORA", [[{"LOWER": "impresora"}]])
matcher.add("CONTRASENA", [[{"LOWER": {"IN": ["contrasena", "clave", "password"]}}]])

def extract_entities_and_rules(text: str):
    doc = nlp(text.lower())
    matches = matcher(doc)
    found = []

    for match_id, start, end in matches:
        found.append(nlp.vocab.strings[match_id])

    return list(set(found))