# 🧩  Quiz Game Web App


## 👥 Team
- Leanza Salvatore  - matricola: 1000084819 -  LM-18 - GitHub [salvlea](https://github.com/salvlea)
- Thomas Morales  -  matricola: 1000071746 -  L-31 - GitHub   [Thomasss5](https://github.com/Thomasss5)

  
[Repository Link](https://github.com/Thomasss5/Progetto_Finale.git)


---

## 🎯 Objective
The goal of this project is to create an interactive Python application for managing and playing multiple-choice quizzes.

The app is designed to provide a simple and intuitive experience, allowing users to load custom quizzes from JSON files, play via a web interface, and receive immediate feedback on their performance.

---

## 🧠 General Description
The **Quiz Game App** allows users to:
1. Load one or more quizzes from **JSON** files.
2. Start a gaming session via a **web browser**.
3. Answer questions by selecting one of the available options.
4. Automatically calculate the **final score**.
5. Display the final results.

---

## 📁 Project Structure

```
Quiz_Game/
├── src_exercises/
│   ├── quiz_manager.py        # Handles saving/loading quizzes from JSON
│   ├── app.py                 # Flask Web Application
│   ├── templates/             # HTML Templates for the Web App
│   │   ├── base.html          # Base CSS layout
│   │   ├── menu.html          # Main menu
│   │   ├── config.html        # Quiz configuration screen
│   │   ├── question.html      # Question screen with timer
│   │   └── results.html       # Final results screen
│   ├── test_quiz.py           # Unit test (pytest + Flask Client)
│   ├── questions/             # Folder containing JSON quizzes
│   │   ├── Astronomia.json    # Astronomy Quiz
│   │   ├── Informatica.json   # Computer Science Quiz 
│   │   └── ... 
│   └── __init__.py
├── requirements_dev.txt
├── README.md
└── .github/
```

### Quiz Structure (JSON)
Each quiz is defined by a JSON file and consists of:
1. **Title** of the quiz (optional if inferred from the filename).
2. **List of Questions**, each featuring:
   - Question text.
   - List of answer options.
   - Index of the correct answer.


---

## 🚀 Key Features

✔️ Dynamic Loading: Load quizzes from JSON files across various categories.

✔️ Modern Interface: Graphical Web App powered by Flask.

✔️ User Experience: Responsive, colorful interface (including a visual timer), and cross-platform compatibility via the web.

✔️ Game Modes: "Mix" mode (random questions from multiple categories) or specific "Category" mode.

✔️ Instant Feedback: Multiple-choice format with immediate feedback for correct/incorrect/timeout responses.

✔️ Scoring: Automatic calculation of the final score.

---

## 🧪 Testing

Tests are developed using the **pytest** framework and simulate web interaction via the Flask Test Client. The project is monitored through GitHub Actions (CI) using Black, Flake8, Isort, Pylint, and Mypy.

| Modulo | Coverage |
|------|----------|
| `test_quiz.py` | 99% |
| `app.py` | 93% |
| `quiz_manager.py` | 73% |
| **Totale Core Coverage** | **~94%** |

*Note on Code Coverage: The report exclusively analyzes Python logic files (.py). Markup/style files (the templates/ folder) and data files (the questions/ folder) do not contain programming logic and are therefore outside the scope of coverage testing.*

To run tests with the coverage report:
```bash
cd src_exercises
python3 -m pytest test_quiz.py -v --cov=. 
```

---

## ⚙️ How to Run the Project 

### Dependency Installation
```bash
pip install -r requirements_dev.txt
```

Ensure that **Flask** is installed.

### Launching the Web App
```bash
cd src_exercises
python3 app.py
```
Open your browser and navigate to: http://127.0.0.1:5000

---

