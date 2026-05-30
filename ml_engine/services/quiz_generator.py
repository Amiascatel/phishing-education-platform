"""
Adaptive Quiz Generator Service

Selects questions for quizzes based on user knowledge profiles and
adaptive difficulty.
"""

import random
from ml_engine.models.difficulty_predictor import DifficultyPredictor


class QuizGenerator:
    def __init__(self):
        self.difficulty_predictor = DifficultyPredictor()

    def generate_quiz(self, available_questions: list, num_questions: int = 5,
                      quiz_type: str = "adaptive", category_id=None,
                      knowledge_profiles: list = None) -> dict:
        """
        Generate a quiz by selecting optimal questions.

        Returns:
            {question_ids: [...], initial_difficulty: "..."}
        """
        questions = [q for q in available_questions if q.get("is_active", True)]

        if category_id:
            cat_questions = [q for q in questions if q.get("category_id") == category_id]
            if cat_questions:
                questions = cat_questions

        if not questions:
            return {"question_ids": [], "initial_difficulty": "beginner"}

        if quiz_type == "pre_test":
            return self._generate_pretest(questions, num_questions)
        else:
            return self._generate_adaptive(questions, num_questions, knowledge_profiles or [])

    def _generate_pretest(self, questions: list, num_questions: int) -> dict:
        by_diff = {"beginner": [], "intermediate": [], "advanced": []}
        for q in questions:
            diff = q.get("difficulty", "beginner")
            if diff in by_diff:
                by_diff[diff].append(q)

        selected = []
        per_level = max(1, num_questions // 3)

        for diff in ["beginner", "intermediate", "advanced"]:
            pool = by_diff[diff][:]
            random.shuffle(pool)
            selected.extend(pool[:per_level])

        remaining = [q for q in questions if q not in selected]
        random.shuffle(remaining)
        while len(selected) < num_questions and remaining:
            selected.append(remaining.pop())

        return {
            "question_ids": [q["id"] for q in selected[:num_questions]],
            "initial_difficulty": "beginner",
        }

    def _generate_adaptive(self, questions: list, num_questions: int,
                            knowledge_profiles: list) -> dict:
        avg_proficiency = 0.5
        if knowledge_profiles:
            scores = [p.get("proficiency_score", 0.5) for p in knowledge_profiles]
            avg_proficiency = sum(scores) / len(scores) if scores else 0.5

        initial_diff = self.difficulty_predictor.predict(avg_proficiency, avg_proficiency, 0)

        diff_order = {"beginner": 0, "intermediate": 1, "advanced": 2}
        target_idx = diff_order.get(initial_diff, 0)

        def sort_key(q):
            q_idx = diff_order.get(q.get("difficulty", "beginner"), 0)
            return abs(q_idx - target_idx), random.random()

        questions_sorted = sorted(questions, key=sort_key)
        selected = questions_sorted[:num_questions]
        selected.sort(key=lambda q: diff_order.get(q.get("difficulty", "beginner"), 0))

        return {
            "question_ids": [q["id"] for q in selected],
            "initial_difficulty": initial_diff,
        }

    def select_next_question(self, available_questions: list, answers_so_far: list):
        if not available_questions:
            return None

        recent = answers_so_far[-5:] if answers_so_far else []
        if recent:
            recent_accuracy = sum(1 for a in recent if a.get("is_correct", False)) / len(recent)
        else:
            recent_accuracy = 0.5

        if recent_accuracy >= 0.8:
            target, reason = "advanced", "Strong recent performance, increasing difficulty"
        elif recent_accuracy >= 0.5:
            target, reason = "intermediate", "Moderate performance, maintaining current level"
        else:
            target, reason = "beginner", "Struggling with recent questions, reducing difficulty"

        diff_order = {"beginner": 0, "intermediate": 1, "advanced": 2}
        target_idx = diff_order.get(target, 1)

        best = min(
            available_questions,
            key=lambda q: (abs(diff_order.get(q.get("difficulty", "beginner"), 0) - target_idx), random.random()),
        )

        return {
            "next_question_id": best["id"],
            "difficulty": best.get("difficulty", "beginner"),
            "selection_reason": reason,
        }
