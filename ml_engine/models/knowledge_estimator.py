"""
Bayesian Knowledge Estimator

Uses item response theory (IRT) principles to estimate user proficiency
per category based on their quiz answers.
"""

import numpy as np


class KnowledgeEstimator:
    """Estimates user knowledge level using Bayesian updating."""

    DIFFICULTY_WEIGHTS = {
        "beginner": 0.3,
        "intermediate": 0.6,
        "advanced": 1.0,
    }

    def estimate_proficiency(self, answers: list, current_score: float = 0.5) -> dict:
        """
        Estimate proficiency from a set of answers.

        Args:
            answers: List of {is_correct, difficulty, category_id, time_seconds}
            current_score: Prior proficiency score (0-1)

        Returns:
            {proficiency_score, estimated_level, confidence}
        """
        if not answers:
            return {
                "proficiency_score": current_score,
                "estimated_level": self._score_to_level(current_score),
                "confidence": 0.3,
            }

        weighted_correct = 0.0
        total_weight = 0.0

        for answer in answers:
            difficulty = answer.get("difficulty", "beginner")
            weight = self.DIFFICULTY_WEIGHTS.get(difficulty, 0.5)
            total_weight += weight

            if answer.get("is_correct", False):
                weighted_correct += weight
                time_s = answer.get("time_seconds")
                if time_s and time_s < 15:
                    weighted_correct += weight * 0.1

        if total_weight == 0:
            observed_score = 0.5
        else:
            observed_score = weighted_correct / total_weight

        num_answers = len(answers)
        prior_weight = max(0.2, 1.0 / (1.0 + num_answers * 0.3))
        updated_score = prior_weight * current_score + (1 - prior_weight) * observed_score
        updated_score = float(np.clip(updated_score, 0.0, 1.0))

        confidence = float(np.clip(0.3 + num_answers * 0.07, 0.3, 0.95))

        return {
            "proficiency_score": round(updated_score, 4),
            "estimated_level": self._score_to_level(updated_score),
            "confidence": round(confidence, 4),
        }

    def _score_to_level(self, score: float) -> str:
        if score < 0.35:
            return "beginner"
        elif score < 0.70:
            return "intermediate"
        else:
            return "advanced"
