import math
import re
from typing import List, Tuple
from app.models.schemas import PlagiarismResult


def _tokenize(text: str) -> List[str]:
    """Lowercase, remove punctuation, split into words."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return [w for w in text.split() if len(w) > 2]


def _tf(tokens: List[str]) -> dict:
    tf = {}
    total = len(tokens) or 1
    for t in tokens:
        tf[t] = tf.get(t, 0) + 1
    return {k: v / total for k, v in tf.items()}


def _cosine_similarity(tokens1: List[str], tokens2: List[str]) -> float:
    """Compute cosine similarity between two token lists using TF vectors."""
    if not tokens1 or not tokens2:
        return 0.0

    tf1 = _tf(tokens1)
    tf2 = _tf(tokens2)

    vocab = set(tf1.keys()) | set(tf2.keys())

    dot = sum(tf1.get(w, 0) * tf2.get(w, 0) for w in vocab)
    mag1 = math.sqrt(sum(v ** 2 for v in tf1.values()))
    mag2 = math.sqrt(sum(v ** 2 for v in tf2.values()))

    if mag1 == 0 or mag2 == 0:
        return 0.0

    return round(dot / (mag1 * mag2), 4)


def _risk_level(score: float) -> str:
    if score >= 0.85:
        return "High"
    elif score >= 0.60:
        return "Medium"
    return "Low"


def _verdict(score: float) -> str:
    if score >= 0.85:
        return "Plagiarised"
    elif score >= 0.60:
        return "Suspicious"
    return "Original"


def check_similarity(text1: str, text2: str, student2_name: str = None) -> PlagiarismResult:
    """Check similarity between two texts."""
    t1 = _tokenize(text1)
    t2 = _tokenize(text2)
    score = _cosine_similarity(t1, t2)
    pct = round(score * 100, 1)

    return PlagiarismResult(
        similarity_score=score,
        similarity_percentage=pct,
        risk_level=_risk_level(score),
        matched_with=student2_name if score >= 0.60 else None,
        verdict=_verdict(score),
    )


def check_against_all(
    new_answer: str,
    existing_answers: List[Tuple[str, str]],  # list of (student_name, answer)
) -> PlagiarismResult:
    """
    Check a new answer against all existing ones.
    Returns the worst (highest similarity) result.
    """
    if not existing_answers:
        return PlagiarismResult(
            similarity_score=0.0,
            similarity_percentage=0.0,
            risk_level="Low",
            matched_with=None,
            verdict="Original",
        )

    results = [
        check_similarity(new_answer, ans, name)
        for name, ans in existing_answers
    ]

    # Return the one with highest similarity score
    return max(results, key=lambda r: r.similarity_score)
