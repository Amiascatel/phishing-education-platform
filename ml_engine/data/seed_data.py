"""
Seed data for initial model training.

Provides synthetic training examples to bootstrap the ML models
before real user data is available.
"""

SEED_TRAINING_DATA = [
    {"proficiency_score": 0.1, "recent_accuracy": 0.2, "num_answers": 3, "target_difficulty": "beginner"},
    {"proficiency_score": 0.2, "recent_accuracy": 0.3, "num_answers": 5, "target_difficulty": "beginner"},
    {"proficiency_score": 0.25, "recent_accuracy": 0.4, "num_answers": 8, "target_difficulty": "beginner"},
    {"proficiency_score": 0.3, "recent_accuracy": 0.35, "num_answers": 4, "target_difficulty": "beginner"},
    {"proficiency_score": 0.35, "recent_accuracy": 0.5, "num_answers": 10, "target_difficulty": "intermediate"},
    {"proficiency_score": 0.4, "recent_accuracy": 0.5, "num_answers": 12, "target_difficulty": "intermediate"},
    {"proficiency_score": 0.5, "recent_accuracy": 0.6, "num_answers": 15, "target_difficulty": "intermediate"},
    {"proficiency_score": 0.55, "recent_accuracy": 0.55, "num_answers": 8, "target_difficulty": "intermediate"},
    {"proficiency_score": 0.6, "recent_accuracy": 0.7, "num_answers": 20, "target_difficulty": "intermediate"},
    {"proficiency_score": 0.65, "recent_accuracy": 0.65, "num_answers": 18, "target_difficulty": "intermediate"},
    {"proficiency_score": 0.7, "recent_accuracy": 0.75, "num_answers": 25, "target_difficulty": "advanced"},
    {"proficiency_score": 0.75, "recent_accuracy": 0.8, "num_answers": 22, "target_difficulty": "advanced"},
    {"proficiency_score": 0.8, "recent_accuracy": 0.85, "num_answers": 30, "target_difficulty": "advanced"},
    {"proficiency_score": 0.85, "recent_accuracy": 0.9, "num_answers": 28, "target_difficulty": "advanced"},
    {"proficiency_score": 0.9, "recent_accuracy": 0.95, "num_answers": 35, "target_difficulty": "advanced"},
]
