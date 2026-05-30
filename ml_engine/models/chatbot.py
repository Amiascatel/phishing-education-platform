"""
Retrieval-based Chatbot Model

Uses TF-IDF vectorization + cosine similarity to match user questions
to a pre-built knowledge base of phishing education Q&A pairs.
No GPU needed, instant responses, works fully offline.
"""

import os
import re
import numpy as np
import joblib

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

from ml_engine.data.chatbot_knowledge import PHISHING_QA_KNOWLEDGE
from ml_engine.config import settings


class ChatbotModel:
    """TF-IDF retrieval-based chatbot for phishing education."""

    SIMILARITY_THRESHOLD = 0.10
    DIRECT_MATCH_THRESHOLD = 0.55
    MODEL_FILENAME = "chatbot_model.pkl"

    def __init__(self):
        self.vectorizer = None
        self.tfidf_matrix = None
        self.qa_pairs = []
        self.is_trained = False

        if not self.load():
            self.train(PHISHING_QA_KNOWLEDGE)

    # ── helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def _normalise(text: str) -> str:
        """Lower-case and strip punctuation."""
        return re.sub(r'[^\w\s]', '', text.lower()).strip()

    def _build_corpus_entry(self, pair: dict) -> str:
        """
        Build a rich text representation of each Q&A pair for TF-IDF.
        Include question + keywords (repeated for weight).
        We deliberately do NOT include the full answer so the index stays
        question-focused, but we do repeat keywords 2× for boosting.
        """
        parts = [pair["question"]]
        keywords = pair.get("keywords", [])
        if keywords:
            parts.append(" ".join(keywords))
            parts.append(" ".join(keywords))   # repeat for TF-IDF weight
        return " ".join(parts).lower()

    # ── training ──────────────────────────────────────────────────────────────

    def train(self, qa_pairs: list) -> bool:
        if not HAS_SKLEARN or not qa_pairs:
            return False

        self.qa_pairs = qa_pairs
        corpus = [self._build_corpus_entry(p) for p in qa_pairs]

        # Do NOT strip stop words — "what", "how", "types" distinguish questions
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),
            max_features=8000,
            sublinear_tf=True,          # dampen very frequent terms
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)
        self.is_trained = True
        self.save()
        return True

    def add_qa_pairs(self, new_pairs: list) -> bool:
        existing = {p["question"].lower() for p in self.qa_pairs}
        for pair in new_pairs:
            if pair["question"].lower() not in existing:
                self.qa_pairs.append(pair)
                existing.add(pair["question"].lower())
        return self.train(self.qa_pairs)

    # ── inference ─────────────────────────────────────────────────────────────

    def _direct_keyword_match(self, message: str):
        """
        Before TF-IDF, check for a near-exact or high keyword-overlap match.
        Returns (index, score) or (None, 0).
        """
        msg_words = set(self._normalise(message).split())
        if not msg_words:
            return None, 0

        best_idx, best_score = None, 0.0

        for i, pair in enumerate(self.qa_pairs):
            # 1. Exact question match
            if self._normalise(pair["question"]) == self._normalise(message):
                return i, 1.0

            # 2. Word overlap between query and (question + keywords)
            q_words = set(self._normalise(pair["question"]).split())
            kw_words = set(self._normalise(" ".join(pair.get("keywords", []))).split())
            candidate_words = q_words | kw_words

            common = msg_words & candidate_words
            if not common:
                continue

            # Jaccard-like score, boosted by fraction of query covered
            query_coverage = len(common) / len(msg_words)
            jaccard = len(common) / len(msg_words | candidate_words)
            score = 0.6 * query_coverage + 0.4 * jaccard

            if score > best_score:
                best_score = score
                best_idx = i

        return best_idx, best_score

    def get_response(self, message: str, history: list = None) -> dict:
        if not self.is_trained or not HAS_SKLEARN:
            return {
                "reply": "I'm still learning! Please try again shortly.",
                "confidence": 0.0,
                "matched_question": None,
            }

        # ── Step 1: direct keyword match ──────────────────────────────────────
        kw_idx, kw_score = self._direct_keyword_match(message)
        if kw_idx is not None and kw_score >= self.DIRECT_MATCH_THRESHOLD:
            matched = self.qa_pairs[kw_idx]
            return {
                "reply": matched["answer"],
                "confidence": kw_score,
                "matched_question": matched["question"],
            }

        # ── Step 2: TF-IDF cosine similarity ──────────────────────────────────
        query_vector = self.vectorizer.transform([message.lower()])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()

        best_idx = int(np.argmax(similarities))
        best_score = float(similarities[best_idx])

        # If TF-IDF beats keyword match, use it
        if best_score >= self.SIMILARITY_THRESHOLD:
            # Prefer keyword match if scores are close
            if kw_idx is not None and kw_score >= best_score * 0.8:
                best_idx = kw_idx
                best_score = kw_score

            matched = self.qa_pairs[best_idx]
            return {
                "reply": matched["answer"],
                "confidence": best_score,
                "matched_question": matched["question"],
            }

        return {
            "reply": (
                "I'm focused on phishing and cybersecurity education. "
                "Could you rephrase your question? For example, you can ask: "
                "\"What is phishing?\", \"How do I spot a phishing email?\", "
                "or \"What are the types of phishing attacks?\""
            ),
            "confidence": best_score,
            "matched_question": None,
        }

    # ── persistence ───────────────────────────────────────────────────────────

    def save(self) -> bool:
        model_path = os.path.join(settings.model_dir, self.MODEL_FILENAME)
        os.makedirs(settings.model_dir, exist_ok=True)
        try:
            joblib.dump({
                "vectorizer": self.vectorizer,
                "tfidf_matrix": self.tfidf_matrix,
                "qa_pairs": self.qa_pairs,
            }, model_path)
            return True
        except Exception:
            return False

    def load(self) -> bool:
        model_path = os.path.join(settings.model_dir, self.MODEL_FILENAME)
        if not os.path.exists(model_path):
            return False
        try:
            data = joblib.load(model_path)
            self.vectorizer = data["vectorizer"]
            self.tfidf_matrix = data["tfidf_matrix"]
            self.qa_pairs = data["qa_pairs"]
            self.is_trained = True
            return True
        except Exception:
            return False


# Singleton instance
chatbot = ChatbotModel()
