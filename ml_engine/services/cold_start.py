"""
Cold Start Handler

Provides sensible defaults for new users with no quiz history.
"""


class ColdStartHandler:
    """Handles new users with no prior quiz data."""

    def get_default_profiles(self, category_ids: list) -> list:
        return [
            {
                "category_id": cat_id,
                "estimated_level": "beginner",
                "proficiency_score": 0.3,
                "confidence": 0.1,
            }
            for cat_id in category_ids
        ]

    def get_starter_recommendations(self, category_ids: list) -> list:
        return [
            {
                "category_id": cat_id,
                "priority": "high",
                "reason": "Start learning about this topic",
            }
            for cat_id in category_ids[:3]
        ]
