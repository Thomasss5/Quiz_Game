import json
import os
from typing import List, Optional
from quiz_model import Quiz

class QuizManager:
    def __init__(self, quizzes_dir: str = "."):
        self.quizzes_dir = quizzes_dir
        if not os.path.exists(self.quizzes_dir):
            os.makedirs(self.quizzes_dir)

    def save_quiz(self, quiz: Quiz, filename: str):
        if not filename.endswith('.json'):
            filename += '.json'
        path = os.path.join(self.quizzes_dir, filename)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(quiz.to_dict(), f, indent=4, ensure_ascii=False)

    def load_quiz(self, filename: str) -> Optional[Quiz]:
        if not filename.endswith('.json'):
            filename += '.json'
        path = os.path.join(self.quizzes_dir, filename)
        if not os.path.exists(path):
            return None
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return Quiz.from_dict(data)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading quiz {filename}: {e}")
            return None

    def list_quizzes(self) -> List[str]:
        files = [f for f in os.listdir(self.quizzes_dir) if f.endswith('.json')]
        return files
