"""
Collaborative Filter

Uses K-Nearest Neighbors to find users with similar knowledge profiles
and recommend study areas based on what helped similar users improve.
"""

import numpy as np

try:
    from sklearn.neighbors import NearestNeighbors
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


class CollaborativeFilter:
    """KNN-based collaborative filtering for study recommendations."""

    def __init__(self, n_neighbors: int = 5):
        self.n_neighbors = n_neighbors
        self.model = None
        self.user_profiles = []
        self.user_ids = []
        self.is_trained = False
        self._sorted_cats = []
        self._X = None

    def train(self, user_data: list) -> bool:
        if not HAS_SKLEARN or len(user_data) < 3:
            return False

        try:
            all_cats = set()
            for u in user_data:
                all_cats.update(u.get("category_scores", {}).keys())

            if not all_cats:
                return False

            sorted_cats = sorted(all_cats)
            X = []
            self.user_ids = []
            self.user_profiles = user_data

            for u in user_data:
                scores = u.get("category_scores", {})
                row = [scores.get(cat, 0.5) for cat in sorted_cats]
                X.append(row)
                self.user_ids.append(u.get("user_id", 0))

            X = np.array(X)
            k = min(self.n_neighbors, len(X) - 1)
            if k < 1:
                return False

            self.model = NearestNeighbors(n_neighbors=k, metric="cosine")
            self.model.fit(X)
            self.is_trained = True
            self._sorted_cats = sorted_cats
            self._X = X
            return True
        except Exception:
            self.is_trained = False
            return False

    def recommend(self, user_scores: dict, n_recommendations: int = 3) -> list:
        if self.is_trained and self.model is not None:
            try:
                return self._knn_recommend(user_scores, n_recommendations)
            except Exception:
                pass
        return self._weakness_recommend(user_scores, n_recommendations)

    def _knn_recommend(self, user_scores: dict, n_recommendations: int) -> list:
        query = np.array([[user_scores.get(cat, 0.5) for cat in self._sorted_cats]])
        distances, indices = self.model.kneighbors(query)
        neighbor_avg = np.mean(self._X[indices[0]], axis=0)
        user_vec = query[0]
        gaps = neighbor_avg - user_vec
        cat_gaps = list(zip(self._sorted_cats, gaps))
        cat_gaps.sort(key=lambda x: x[1], reverse=True)

        recommendations = []
        for cat_id, gap in cat_gaps[:n_recommendations]:
            priority = "high" if gap > 0.2 else ("medium" if gap > 0.1 else "low")
            recommendations.append({
                "category_id": cat_id,
                "priority": priority,
                "reason": f"Similar users score {gap:.0%} higher in this category",
            })
        return recommendations

    def _weakness_recommend(self, user_scores: dict, n_recommendations: int) -> list:
        if not user_scores:
            return []
        sorted_cats = sorted(user_scores.items(), key=lambda x: x[1])
        recommendations = []
        for cat_id, score in sorted_cats[:n_recommendations]:
            if score < 0.35:
                priority, reason = "high", "Needs significant improvement"
            elif score < 0.60:
                priority, reason = "medium", "Room for improvement"
            else:
                priority, reason = "low", "Minor gaps to address"
            recommendations.append({"category_id": cat_id, "priority": priority, "reason": reason})
        return recommendations
