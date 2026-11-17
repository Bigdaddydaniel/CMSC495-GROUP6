"""Basic grounded AI retrieval for the Alpha release.

The Alpha uses TF-IDF similarity over approved knowledge. It demonstrates the
AI decision path without sending customer content to an external model.
"""

from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .knowledge import APPROVED_KNOWLEDGE


@dataclass
class AIResult:
    answer: str
    confidence: float
    source: str | None
    should_escalate: bool


class GroundedSupportAI:
    def __init__(self, threshold: float = 0.20) -> None:
        self.threshold = threshold
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.documents = [item["text"] for item in APPROVED_KNOWLEDGE]
        self.matrix = self.vectorizer.fit_transform(self.documents)

    def answer(self, message: str) -> AIResult:
        lowered = message.lower()
        restricted_terms = ("refund", "change my account", "delete my account", "human", "agent", "representative")
        if any(term in lowered for term in restricted_terms):
            return AIResult(
                answer="I need to send this request to a human support agent so it can be handled safely.",
                confidence=1.0,
                source="Human Support Policy",
                should_escalate=True,
            )

        query = self.vectorizer.transform([message])
        scores = cosine_similarity(query, self.matrix)[0]
        best_index = int(scores.argmax())
        confidence = float(scores[best_index])
        best = APPROVED_KNOWLEDGE[best_index]

        if confidence < self.threshold:
            return AIResult(
                answer="I could not verify an answer from the approved knowledge base, so I am escalating this request to a human agent.",
                confidence=confidence,
                source=None,
                should_escalate=True,
            )

        return AIResult(
            answer=best["text"],
            confidence=confidence,
            source=best["source"],
            should_escalate=False,
        )
