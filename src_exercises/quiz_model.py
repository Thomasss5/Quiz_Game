import json
from typing import List, Dict, Optional

class Question:
    def __init__(self, text: str, options: List[str], correct_index: int):
        self.text = text
        self.options = options
        self.correct_index = correct_index

    def is_correct(self, answer_index: int) -> bool:
        return 0 <= answer_index < len(self.options) and answer_index == self.correct_index

    def to_dict(self) -> Dict:
        return {
            "text": self.text,
            "options": self.options,
            "correct_index": self.correct_index
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Question':
        return cls(data["text"], data["options"], data["correct_index"])

class Quiz:
    def __init__(self, title: str, questions: List[Question] = None):
        self.title = title
        self.questions = questions if questions else []
        self.score = 0
        self.current_question_index = 0

    def add_question(self, question: Question):
        self.questions.append(question)

    def get_question(self, index: int) -> Optional[Question]:
        if 0 <= index < len(self.questions):
            return self.questions[index]
        return None

    def answer_current_question(self, answer_index: int) -> bool:
        question = self.get_question(self.current_question_index)
        if question and question.is_correct(answer_index):
            self.score += 1
            self.current_question_index += 1
            return True
        self.current_question_index += 1
        return False

    def is_finished(self) -> bool:
        return self.current_question_index >= len(self.questions)

    def reset(self):
        self.score = 0
        self.current_question_index = 0

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "questions": [q.to_dict() for q in self.questions]
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Quiz':
        quiz = cls(data["title"])
        for q_data in data.get("questions", []):
            quiz.add_question(Question.from_dict(q_data))
        return quiz
