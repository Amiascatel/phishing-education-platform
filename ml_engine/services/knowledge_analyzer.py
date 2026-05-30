"""
Knowledge Analyzer Service

Analyzes quiz results to update user knowledge profiles per category.
"""

from ml_engine.models.knowledge_estimator import KnowledgeEstimator


class KnowledgeAnalyzer:
    def __init__(self):
        self.estimator = KnowledgeEstimator()

    def assess_knowledge(self, answers: list, current_profiles: list) -> dict:
        """
        Assess user knowledge based on quiz answers.

        Args:
            answers: List of {category_id, difficulty, is_correct, time_seconds}
            current_profiles: List of {category_id, proficiency_score, estimated_level}

        Returns:
            {updated_profiles: [...], overall_level: "..."}
        """
        by_category = {}
        for answer in answers:
            cat_id = answer.get("category_id", 0)
            if cat_id not in by_category:
                by_category[cat_id] = []
            by_category[cat_id].append(answer)

        current_lookup = {}
        for profile in current_profiles:
            current_lookup[profile.get("category_id", 0)] = profile

        updated_profiles = []
        all_scores = []

        for cat_id, cat_answers in by_category.items():
            current = current_lookup.get(cat_id, {})
            current_score = current.get("proficiency_score", 0.5)

            result = self.estimator.estimate_proficiency(cat_answers, current_score)

            updated_profiles.append({
                "category_id": cat_id,
                "estimated_level": result["estimated_level"],
                "proficiency_score": result["proficiency_score"],
                "confidence": result["confidence"],
            })
            all_scores.append(result["proficiency_score"])

        if all_scores:
            avg_score = sum(all_scores) / len(all_scores)
        else:
            avg_score = 0.5

        if avg_score < 0.35:
            overall_level = "beginner"
        elif avg_score < 0.70:
            overall_level = "intermediate"
        else:
            overall_level = "advanced"

        return {
            "updated_profiles": updated_profiles,
            "overall_level": overall_level,
        }
