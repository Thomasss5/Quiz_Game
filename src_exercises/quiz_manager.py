import json
import os
from typing import List


class QuizManager:
    def __init__(self, quizzes_dir: str = "questions"):
        self.quizzes_dir = quizzes_dir
        if not os.path.exists(self.quizzes_dir):
            os.makedirs(self.quizzes_dir)

    def load_quiz_from_json(self, path: str) -> List[dict]:
        try:
            # Se il percorso non è assoluto, cerchiamo nella cartella questions
            if not os.path.exists(path):
                path = os.path.join(self.quizzes_dir, os.path.basename(path))

            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Restituiamo direttamente la lista delle domande
            if isinstance(data, list):
                return data
            if isinstance(data, dict) and "questions" in data:
                return data["questions"]

            return []

        except (OSError, json.JSONDecodeError) as e:
            print(f"Errore caricamento nel file {path}: {e}")
            return []
