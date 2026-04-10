# Asistente de Soporte IA

Proyecto de asistente virtual de soporte técnico desarrollado con **FastAPI**, capaz de clasificar incidencias, aplicar reglas básicas y devolver respuestas guiadas a partir de una base de conocimiento en formato JSON.

## Descripción

Este proyecto permite construir un asistente de soporte técnico que recibe preguntas de usuarios, identifica la categoría de la incidencia y devuelve:

- una respuesta principal,
- pasos recomendados,
- recomendaciones adicionales según palabras clave detectadas.

El sistema está pensado para consultas de soporte técnico comunes, como problemas de acceso, red, impresoras, correo, audio, cámara, rendimiento, teclado, ratón o pantalla.

---

## Tecnologías utilizadas

- Python 3.10 o superior
- FastAPI
- Uvicorn
- NLTK
- spaCy
- JSON como base de conocimiento
- Scikit-learn para el clasificador entrenado

---

## Estructura del proyecto

```bash
asistente-soporte-ia/
│
├── app/
│   ├── __init__.py
│   ├── classifier.py
│   ├── main.py
│   ├── predictor.py
│   ├── preprocess.py
│   ├── recommender.py
│   ├── rules.py
│   ├── schemas.py
│   └── static/
│
├── data/
│   └── knowledge_base.json
│
├── models/
│   └── classifier.pkl
│
├── requirements.txt
├── train_model.py
└── README.md