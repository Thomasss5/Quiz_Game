import os
import random

from flask import Flask, redirect, render_template, request, session, url_for

from quiz_manager import QuizManager

app = Flask(__name__)
app.secret_key = os.urandom(24)

QUESTIONS_DIR = "questions"
manager = QuizManager(quizzes_dir=QUESTIONS_DIR)


def get_categories():
    """Restituisce la lista delle categorie disponibili dai file JSON."""
    if not os.path.exists(QUESTIONS_DIR):
        os.makedirs(QUESTIONS_DIR)
    return [
        f.replace(".json", "") for f in os.listdir(QUESTIONS_DIR) if f.endswith(".json")
    ]


@app.route("/")
def menu():
    """Menu principale - corrisponde a setup_main_menu() di gui.py."""
    categories = get_categories()
    return render_template("menu.html", categories=categories)


@app.route("/config", methods=["POST"])
def config():
    """Schermata configurazione quiz - corrisponde a ask_questions_count() di gui.py."""
    mode = request.form.get("mode", "MIX")
    category = request.form.get("category", "")

    session["mode"] = mode
    session["category"] = category if mode == "CAT" else "MIX"

    return render_template("config.html", mode=mode, category=session["category"])


@app.route("/start", methods=["POST"])
def start():
    """Inizializza il quiz nella sessione - corrisponde a start_category/mixed_quiz() di gui.py."""
    total_questions = int(request.form.get("total_questions", 10))
    mode = session.get("mode", "MIX")
    category = session.get("category", "")

    all_questions = []

    if mode == "CAT" and category:
        file_path = os.path.join(QUESTIONS_DIR, f"{category}.json")
        questions = manager.load_quiz_from_json(file_path)
        valid = [
            q
            for q in questions
            if isinstance(q, dict) and "text" in q and "options" in q
        ]
        for q in valid:
            q["source_cat"] = category.upper()
        all_questions = valid
    else:
        files = [f for f in os.listdir(QUESTIONS_DIR) if f.endswith(".json")]
        for file in files:
            category_name = file.replace(".json", "").upper()
            questions = manager.load_quiz_from_json(os.path.join(QUESTIONS_DIR, file))
            for q in questions:
                if isinstance(q, dict) and "text" in q and "options" in q:
                    q["source_cat"] = category_name
                    all_questions.append(q)

    if not all_questions:
        return redirect(url_for("menu"))

    random.shuffle(all_questions)
    selected = all_questions[: min(len(all_questions), total_questions)]

    # Salviamo nella sessione
    session["questions"] = selected
    session["current_index"] = 0
    session["score"] = 0
    session["total"] = len(selected)
    session["answered"] = False
    session["feedback"] = None

    return redirect(url_for("quiz"))


@app.route("/quiz")
def quiz():
    """Mostra la domanda corrente - corrisponde a show_question() di gui.py."""
    questions = session.get("questions", [])
    index = session.get("current_index", 0)
    score = session.get("score", 0)
    total = session.get("total", 0)

    if index >= len(questions):
        return redirect(url_for("results"))

    q_data = questions[index]
    options = q_data.get("options", [])
    correct_idx = q_data.get("correct_index", 0)

    # Mescola le opzioni mantenendo traccia della risposta corretta
    correct_answer = options[correct_idx]
    shuffled_opts = list(options)
    random.shuffle(shuffled_opts)

    session["correct_answer"] = correct_answer
    session["shuffled_options"] = shuffled_opts

    # Controlla se c'è un feedback da mostrare
    feedback = session.get("feedback")
    answered = session.get("answered", False)

    return render_template(
        "question.html",
        question_text=q_data.get("text", ""),
        category=q_data.get("source_cat", "GENERALE"),
        options=shuffled_opts,
        current=index + 1,
        total=total,
        score=score,
        time_limit=20,
        answered=answered,
        feedback=feedback,
    )


@app.route("/answer", methods=["POST"])
def answer():
    """Verifica la risposta - corrisponde a handle_answer() di gui.py."""
    selected_option = request.form.get("option", "")
    timeout = request.form.get("timeout", "false") == "true"
    correct_answer = session.get("correct_answer", "")

    if not timeout and not selected_option:
        return redirect(url_for("quiz"))

    if not timeout and selected_option == correct_answer:
        session["score"] = session.get("score", 0) + 1
        feedback = {
            "text": "RISPOSTA ESATTA!",
            "color": "correct",
            "correct_answer": correct_answer,
        }
    elif timeout:
        feedback = {
            "text": "TEMPO SCADUTO!",
            "detail": f"La risposta corretta era: {correct_answer}",
            "color": "timeout",
            "correct_answer": correct_answer,
        }
    else:
        feedback = {
            "text": "RISPOSTA ERRATA!",
            "detail": f"La risposta corretta era: {correct_answer}",
            "color": "incorrect",
            "correct_answer": correct_answer,
        }

    session["answered"] = True
    session["feedback"] = feedback

    return redirect(url_for("quiz"))


@app.route("/next", methods=["POST"])
def next_question():
    """Passa alla domanda successiva - corrisponde a next_question() di gui.py."""
    session["current_index"] = session.get("current_index", 0) + 1
    session["answered"] = False
    session["feedback"] = None
    return redirect(url_for("quiz"))


@app.route("/results")
def results():
    """Mostra i risultati - corrisponde a show_results() di gui.py."""
    score = session.get("score", 0)
    total = session.get("total", 0)
    return render_template("results.html", score=score, total=total)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
