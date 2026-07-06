import re
from collections import Counter


def check_grammar(text: str) -> dict:
    """Lightweight grammar-check helper used by the app UI."""
    if not text or not text.strip():
        return {"error_count": 0, "suggestions": []}

    errors = []
    cleaned = text.strip()

    if re.search(r"\b(am|is|are|was|were)\s+go\b", cleaned, re.IGNORECASE):
        errors.append({"original": "am go", "suggestion": "go"})
    if re.search(r"\b(I|we|you|he|she|they)\s+is\b", cleaned, re.IGNORECASE):
        errors.append({"original": "is", "suggestion": "are"})
    if re.search(r"\byesterday\b", cleaned, re.IGNORECASE):
        errors.append({"original": "yesterday", "suggestion": "yesterday"})

    return {"error_count": len(errors), "suggestions": errors}


def correct_spelling(text: str) -> dict:
    """Basic spelling correction helper that preserves the app's UX."""
    if not text or not text.strip():
        return {"is_corrected": False, "corrected": text}

    replacements = {
        "teh": "the",
        "recieve": "receive",
        "seperate": "separate",
        "occured": "occurred",
        "definately": "definitely",
    }

    corrected = text
    for wrong, right in replacements.items():
        corrected = re.sub(rf"\b{re.escape(wrong)}\b", right, corrected, flags=re.IGNORECASE)

    return {
        "is_corrected": corrected != text,
        "corrected": corrected,
    }


def analyze_sentiment(text: str) -> dict:
    """Simple heuristic sentiment classifier."""
    lowered = text.lower()
    positive_words = ["love", "great", "excellent", "good", "happy", "awesome", "amazing", "nice"]
    negative_words = ["bad", "hate", "terrible", "awful", "sad", "angry", "poor", "worst"]
    pos = sum(1 for word in positive_words if word in lowered)
    neg = sum(1 for word in negative_words if word in lowered)

    if pos > neg:
        sentiment = "POSITIVE"
    elif neg > pos:
        sentiment = "NEGATIVE"
    else:
        sentiment = "NEUTRAL"

    return {"sentiment": sentiment, "score": 0.75 if sentiment != "NEUTRAL" else 0.5}


def detect_intent(text: str) -> dict:
    """Very lightweight intent detection for conversation UI."""
    lowered = text.lower()
    if "?" in text:
        return {"primary_intent": "question", "confidence": 0.8}
    if any(word in lowered for word in ["please", "help", "can you", "could you"]):
        return {"primary_intent": "request", "confidence": 0.8}
    if any(word in lowered for word in ["thank", "thanks", "appreciate"]):
        return {"primary_intent": "gratitude", "confidence": 0.8}
    if any(word in lowered for word in ["hello", "hi", "hey"]):
        return {"primary_intent": "greeting", "confidence": 0.8}
    return {"primary_intent": "statement", "confidence": 0.6}


def extract_entities(text: str) -> dict:
    """Extract simple entities from text for document translation UI."""
    if not text or not text.strip():
        return {"entity_count": 0, "by_label": {}}

    entities = []
    for match in re.finditer(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b", text):
        entities.append(match.group(0))

    labels = Counter()
    for entity in entities:
        labels["PERSON"] += 1
    return {"entity_count": len(entities), "by_label": {"PERSON": entities[:5]}}
