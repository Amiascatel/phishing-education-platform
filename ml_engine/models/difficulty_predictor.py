"""
Difficulty Predictor

Uses gradient boosting to predict the optimal difficulty level for the
next question based on user performance patterns.
"""

import numpy as np

try:
    from sklearn.ensemble import GradientBoostingClassifier
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


class DifficultyPredictor:
    """Predicts optimal question difficulty for adaptive quizzes."""

    LEVELS = ["beginner", "intermediate", "advanced"]

    def __init__(self):
        self.model = None
        self.is_trained = False

    def train(self, training_data: list) -> bool:
        if not HAS_SKLEARN or len(training_data) < 10:
            return False

        try:
            X = np.array([
                [
                    d.get("proficiency_score", 0.5),
                    d.get("recent_accuracy", 0.5),
                    d.get("num_answers", 0),
                ]
                for d in training_data
            ])

            y = np.array([
                self.LEVELS.index(d.get("target_difficulty", "beginner"))
                for d in training_data
            ])

            self.model = GradientBoostingClassifier(
                n_estimators=50,
                max_depth=3,
                random_state=42,
            )
            self.model.fit(X, y)
            self.is_trained = True
            return True
        except Exception:
            self.is_trained = False
            return False

    def predict(self, proficiency_score: float, recent_accuracy: float, num_answers: int) -> str:
        if self.is_trained and self.model is not None:
            try:
                X = np.array([[proficiency_score, recent_accuracy, num_answers]])
                pred = self.model.predict(X)[0]
                return self.LEVELS[int(pred)]
            except Exception:
                pass

        return self._rule_based_predict(proficiency_score, recent_accuracy)

    def _rule_based_predict(self, proficiency_score: float, recent_accuracy: float) -> str:
        blended = 0.6 * proficiency_score + 0.4 * recent_accuracy
        if blended < 0.35:
            return "beginner"
        elif blended < 0.70:
            return "intermediate"
        else:
            return "advanced"
