import unittest
import os
import shutil
from quiz_model import Question, Quiz
from quiz_manager import QuizManager

class TestQuizLogic(unittest.TestCase):
    def setUp(self):
        self.q1 = Question("Q1", ["A", "B", "C"], 0)
        self.q2 = Question("Q2", ["X", "Y"], 1)
        self.quiz = Quiz("Test Quiz")
        self.quiz.add_question(self.q1)
        self.quiz.add_question(self.q2)

    def test_question_correctness(self):
        self.assertTrue(self.q1.is_correct(0))
        self.assertFalse(self.q1.is_correct(1))
        self.assertFalse(self.q1.is_correct(99)) # Out of range

    def test_quiz_flow(self):
        self.assertEqual(self.quiz.score, 0)
        self.assertEqual(self.quiz.current_question_index, 0)
        
        # Answer first question correctly
        self.quiz.answer_current_question(0)
        self.assertEqual(self.quiz.score, 1)
        self.assertEqual(self.quiz.current_question_index, 1)
        
        # Answer second question incorrectly
        self.quiz.answer_current_question(0)
        self.assertEqual(self.quiz.score, 1)
        self.assertEqual(self.quiz.current_question_index, 2)
        
        self.assertTrue(self.quiz.is_finished())

    def test_quiz_reset(self):
        self.quiz.answer_current_question(0)
        self.quiz.reset()
        self.assertEqual(self.quiz.score, 0)
        self.assertEqual(self.quiz.current_question_index, 0)

class TestQuizManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_quizzes"
        self.manager = QuizManager(self.test_dir)
        self.quiz = Quiz("Test Quiz")
        self.quiz.add_question(Question("Q1", ["A", "B"], 0))

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_save_and_load(self):
        self.manager.save_quiz(self.quiz, "test_quiz")
        loaded_quiz = self.manager.load_quiz("test_quiz")
        
        self.assertIsNotNone(loaded_quiz)
        self.assertEqual(loaded_quiz.title, "Test Quiz")
        self.assertEqual(len(loaded_quiz.questions), 1)
        self.assertEqual(loaded_quiz.questions[0].text, "Q1")

if __name__ == '__main__':
    unittest.main()
