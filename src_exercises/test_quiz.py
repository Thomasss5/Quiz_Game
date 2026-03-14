import os
import json
import shutil
import pytest
import tkinter as tk
from unittest.mock import MagicMock, patch
from gui import QuizApp
from quiz_manager import QuizManager

# =====================================================================
# TEST PER QUIZ_MANAGER.PY
# =====================================================================

class TestQuizManager:
    def setup_method(self):
        self.test_dir = "test_questions"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
        self.manager = QuizManager(self.test_dir)

    def teardown_method(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_load_quiz_from_json_list_format(self):
        path = os.path.join(self.test_dir, "list.json")
        data = [{"text": "Q1", "options": ["A", "B"], "correct_index": 0}]
        with open(path, "w") as f:
            json.dump(data, f)
        
        loaded = self.manager.load_quiz_from_json(path)
        assert len(loaded) == 1
        assert loaded[0]["text"] == "Q1"

# =====================================================================
# TEST PER GUI.PY
# =====================================================================

class TestGuiApp:
    @pytest.fixture
    def app(self):
        """Crea un'istanza dell'app con root mockato."""
        root = tk.Tk()
        with patch("os.listdir", return_value=["test_cat.json"]):
            with patch("gui.QuizManager") as mock_mgr:
                app_instance = QuizApp(root)
                yield app_instance
        root.destroy()

    def test_ask_questions_count_setup(self, app):
        """Testa se la schermata di configurazione salva la categoria correttamente."""
        # Mock della combobox
        app.cat_combo = MagicMock()
        app.cat_combo.get.return_value = "Scienza"
        
        app.ask_questions_count("CAT")
        
        assert app.selected_category_name == "Scienza"
        # Verifica che sia stato creato lo slider (Scale)
        assert any(isinstance(w, tk.Scale) for w in app.root.winfo_children()[0].winfo_children())

    def test_start_category_quiz_with_limit(self, app):
        """Verifica che il quiz carichi solo il numero di domande richiesto dallo slider."""
        app.selected_category_name = "test_cat"
        app.total_questions_requested = 5
        
        # Creiamo 10 domande finte
        fake_questions = [{"text": f"Q{i}", "options": ["A"], "correct_index": 0} for i in range(10)]
        
        with patch.object(app.manager, 'load_quiz_from_json', return_value=fake_questions):
            app.start_category_quiz()
            # Deve averne caricate solo 5
            assert len(app.current_questions) == 5

    def test_handle_answer_timeout(self, app):
        """Verifica che il timeout mostri la risposta corretta salvata."""
        app.current_correct_answer = "Risposta Esatta"
        app.options_frame = tk.Frame(app.root)
        app.action_btn = tk.Button(app.root)
        
        # Eseguiamo handle_answer come se il tempo fosse scaduto
        app.handle_answer(correct_text="Risposta Esatta", timeout=True)
        
        # Verifichiamo che i widget delle opzioni siano disabilitati
        assert app.action_btn.cget("text") == "PROSSIMA DOMANDA"

    def test_start_mixed_quiz_logic(self, app):
        """Testa la logica del mix di domande da più file."""
        app.total_questions_requested = 10
        fake_q = [{"text": "Q", "options": ["A"], "correct_index": 0}]
        
        with patch("os.listdir", return_value=["cat1.json", "cat2.json"]):
            with patch.object(app.manager, 'load_quiz_from_json', return_value=fake_q):
                app.start_mixed_quiz()
                assert len(app.current_questions) <= 10
                assert "source_cat" in app.current_questions[0]

    def test_timer_countdown(self, app):
        """Verifica che il timer decrementi il tempo."""
        from tkinter import ttk
        app.remaining_time = 20
        app.timer_label = tk.Label(app.root)
        app.timer_progress = ttk.Progressbar(app.root, maximum=20)
        app.timer_progress['value'] = 20
        
        with patch.object(app.root, 'after'):
            app.update_timer()
            assert app.remaining_time == 19
            assert app.timer_progress['value'] == 19

    def test_confirm_quit_dialog(self, app):
        """Verifica il ritorno al menu dopo conferma."""
        with patch("gui.messagebox.askyesno", return_value=True):
            with patch.object(app, 'setup_main_menu') as mock_menu:
                app.confirm_quit()
                mock_menu.assert_called_once()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])