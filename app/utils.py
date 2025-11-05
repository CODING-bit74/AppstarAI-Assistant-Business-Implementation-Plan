import json
import os

QA_PATH = os.path.join(os.path.dirname(__file__), "qa_data.json")

def load_qa():
    """Load predefined Q&A pairs from JSON"""
    with open(QA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

QA = load_qa()

def get_answer(text: str):
    """Return the answer if found"""
    text = text.lower().strip()
    return QA.get(text)

