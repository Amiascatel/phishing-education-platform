from django.apps import AppConfig


class MlEngineConfig(AppConfig):
    name = 'ml_engine'
    verbose_name = 'ML Engine'

    def ready(self):
        """Pre-load ML models when Django starts."""
        try:
            from ml_engine.models.chatbot import chatbot  # noqa — triggers singleton init
            from ml_engine.models.difficulty_predictor import DifficultyPredictor
            from ml_engine.data.seed_data import SEED_TRAINING_DATA
            predictor = DifficultyPredictor()
            predictor.train(SEED_TRAINING_DATA)
        except Exception:
            pass  # Never crash Django if ML deps missing
