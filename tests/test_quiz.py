import json
import os
import shutil

import pytest

from quiz_manager import QuizManager

# =====================================================================
# TEST PER QUIZ_MANAGER.PY (invariati)
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
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)

        loaded = self.manager.load_quiz_from_json(path)
        assert len(loaded) == 1
        assert loaded[0]["text"] == "Q1"


# =====================================================================
# TEST PER APP.PY (Flask)
# =====================================================================


class TestFlaskApp:
    @pytest.fixture
    def client(self):
        """Crea un test client Flask."""
        from app import app

        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "test-secret"
        with app.test_client() as client:
            yield client

    def test_menu_loads(self, client):
        """Verifica che il menu principale si carichi."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"QUIZ UNIVERSE" in response.data

    def test_menu_shows_categories(self, client):
        """Verifica che il menu mostri le categorie disponibili."""
        response = client.get("/")
        assert response.status_code == 200
        # Deve contenere il dropdown o almeno il testo MIX
        assert b"MIX" in response.data

    def test_config_page_mix(self, client):
        """Verifica la pagina di configurazione per la modalità MIX."""
        response = client.post("/config", data={"mode": "MIX"})
        assert response.status_code == 200
        assert b"CONFIGURA QUIZ" in response.data
        assert b"MIX" in response.data

    def test_config_page_category(self, client):
        """Verifica la pagina di configurazione per una categoria specifica."""
        response = client.post(
            "/config", data={"mode": "CAT", "category": "Astronomia"}
        )
        assert response.status_code == 200
        assert b"CONFIGURA QUIZ" in response.data
        assert b"Astronomia" in response.data

    def test_start_quiz_redirect(self, client):
        """Verifica che lo start del quiz faccia redirect al quiz."""
        # Prima configuriamo la sessione
        with client.session_transaction() as sess:
            sess["mode"] = "MIX"
            sess["category"] = "MIX"

        response = client.post("/start", data={"total_questions": "5"})
        # Deve fare redirect a /quiz o a /menu se non ci sono domande
        assert response.status_code == 302

    def test_start_category_quiz(self, client):
        """Verifica che si possa avviare un quiz per categoria."""
        with client.session_transaction() as sess:
            sess["mode"] = "CAT"
            sess["category"] = "Astronomia"

        response = client.post(
            "/start", data={"total_questions": "5"}, follow_redirects=True
        )
        assert response.status_code == 200

    def test_results_page(self, client):
        """Verifica la pagina dei risultati."""
        with client.session_transaction() as sess:
            sess["score"] = 7
            sess["total"] = 10

        response = client.get("/results")
        assert response.status_code == 200
        assert b"QUIZ CONCLUSO" in response.data
        assert b"7" in response.data
        assert b"10" in response.data

    def test_answer_without_selection(self, client):
        """Verifica che inviare senza selezione faccia redirect."""
        with client.session_transaction() as sess:
            sess["correct_answer"] = "Risposta A"

        response = client.post("/answer", data={})
        assert response.status_code == 302

    def test_next_question(self, client):
        """Verifica che next incrementi l'indice e faccia redirect."""
        with client.session_transaction() as sess:
            sess["current_index"] = 2
            sess["answered"] = True
            sess["feedback"] = None

        response = client.post("/next")
        assert response.status_code == 302

    def test_full_quiz_flow(self, client):
        """Test end-to-end del flusso completo del quiz."""
        # 1. Menu
        response = client.get("/")
        assert response.status_code == 200

        # 2. Config
        response = client.post("/config", data={"mode": "MIX"})
        assert response.status_code == 200

        # 3. Start
        with client.session_transaction() as sess:
            sess["mode"] = "MIX"
            sess["category"] = "MIX"
        response = client.post(
            "/start", data={"total_questions": "5"}, follow_redirects=True
        )
        assert response.status_code == 200

    def test_timeout_answer(self, client):
        """Verifica che il timeout venga gestito correttamente."""
        with client.session_transaction() as sess:
            sess["correct_answer"] = "Mercurio"
            sess["current_index"] = 0
            sess["score"] = 0
            sess["questions"] = [
                {
                    "text": "Q1",
                    "options": ["A"],
                    "correct_index": 0,
                    "source_cat": "TEST",
                }
            ]
            sess["total"] = 1

        response = client.post("/answer", data={"timeout": "true"})
        assert response.status_code == 302


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
