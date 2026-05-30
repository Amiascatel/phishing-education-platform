"""ML Engine configuration — replaces FastAPI config.py."""
import os
from pathlib import Path


class MLSettings:
    def __init__(self):
        base = Path(__file__).resolve().parent
        self.model_dir = str(base / 'trained_models')
        os.makedirs(self.model_dir, exist_ok=True)


settings = MLSettings()
