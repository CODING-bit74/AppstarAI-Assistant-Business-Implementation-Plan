import json
import os
import re
from rapidfuzz import process, fuzz

QA_PATH = os.path.join(os.path.dirname(__file__), "qa_data.json")

def _normalize(text: str) -> str:
    if not text:
        return ""
    t = text.lower().strip()
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"[!?.,;:]+$", "", t)
    return t

def load_qa():
    with open(QA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {_normalize(k): v for k, v in data.items()}

QA = load_qa()
QA_KEYS = list(QA.keys())

def get_answer(text: str, threshold: int = 82):
    q = _normalize(text)

    if q in QA:
        return QA[q], True, "exact"

    best = process.extractOne(
        q,
        QA_KEYS,
        scorer=fuzz.token_set_ratio
    )
    if best:
        candidate, score, _ = best
        if score >= threshold:
            return QA[candidate], True, "fuzzy"

    return "I'm not sure about that yet 🤔", False, "none"


