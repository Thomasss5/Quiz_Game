# 🧩  Quiz Game Web App


## 👥 Team
- Leanza Salvatore  - matricola: 1000084819 -  LM-18 - GitHub [salvlea](https://github.com/salvlea)
- Thomas Morales  -  matricola: 1000071746 -  L-31 - GitHub   [Thomasss5](https://github.com/Thomasss5)

  
[link della Repository](https://github.com/Thomasss5/Progetto_Finale.git)


---

## 🎯 Obiettivo
L'obiettivo del progetto è la realizzazione di un'applicazione interattiva in Python per la gestione e l'esecuzione di quiz a risposta multipla.

L'applicazione è pensata per offrire un'esperienza semplice e intuitiva, permettendo di caricare quiz personalizzati da file JSON, giocare tramite console o interfaccia grafica e ottenere un feedback immediato sulle prestazioni.

---

## 🧠 Descrizione generale
La Quiz Game App consente all'utente di:
1. Caricare uno o più quiz da file JSON
2. Avviare una sessione di gioco tramite il **browser web** 
3. Rispondere alle domande selezionando una delle opzioni disponibili
4. Calcolare automaticamente il punteggio finale
5. Visualizzare il risultato 


---

## 📁 Struttura del progetto

```
Quiz_Game/
├── src_exercises/
│   ├── quiz_manager.py        # Gestione salvataggio/caricamento quiz da JSON
│   ├── app.py                 # Applicazione Web Flask
│   ├── templates/             # Template HTML per l'App Web
│   │   ├── base.html          # Layout CSS di base
│   │   ├── menu.html          # Menu principale
│   │   ├── config.html        # Schermata configurazione quiz
│   │   ├── question.html      # Schermata domanda con timer
│   │   └── results.html       # Schermata risultati finali
│   ├── test_quiz.py           # Unit test (pytest + Flask Client)
│   ├── questions/             # Cartella contenente i quiz JSON
│   │   ├── Astronomia.json    # Quiz Astronomia
│   │   ├── Informatica.json   # Quiz Informatica
│   │   └── ... 
│   └── __init__.py
├── requirements_dev.txt
├── README.md
└── .github/
```

### Struttura dei quiz (JSON)
Ogni quiz è definito tramite un file JSON ed è composto da:
1. **Titolo** del quiz (opzionale se inferibile dal nome file)
2. **Elenco di domande**, ciascuna caratterizzata da:
   - testo della domanda
   - elenco di opzioni di risposta
   - indice della risposta corretta



---

## 🚀 Funzionalità principali

✔️ Caricamento quiz da file JSON dalle diverse categorie

✔️ interfaccia moderna: Web App grafica (Flask/Browser)

✔️ Interfaccia responsiva, colorata (inclusiva di Timer grafico), e Cross-Platform grazie al Web

✔️ Modalià "Mix" (domande random da più categorie) o per Categoria

✔️ Quiz a risposta multipla con feedback immediato per risposte corrette/errate/timeout

✔️ Calcolo automatico del punteggio

---

## 🧪 Testing

I test sono sviluppati con il framework **pytest** e simulano l'interazione web tramite il Flask Test Client.
Il progetto è monitorato tramite GitHub Actions (CI) con Black, Flake8, Isort, Pylint e Mypy.

| Modulo | Coverage |
|------|----------|
| `test_quiz.py` | 99% |
| `app.py` | 93% |
| `quiz_manager.py` | 73% |
| **Totale Copertura Core** | **~94%** |

*(Nota sul Code Coverage: Il report analizza esclusivamente il codice logico Python (`.py`). I file di markup/stile (la cartella `templates/` con i file `.html`) e i dati (la cartella `questions/` con i `.json`) non contengono logica di programmazione e non rientrano nel perimetro del Coverage Testing.)*

Per eseguire i test con il report di coverage:
```bash
cd src_exercises
python3 -m pytest test_quiz.py -v --cov=. 
```

---

## ⚙️ Come eseguire il progetto

### Installazione dipendenze
```bash
pip install -r requirements_dev.txt
```

Assicurarsi di avere installato `flask`

### Avvio da Web App 
```bash
cd src_exercises
python3 app.py
```
Aprire il browser e collegarsi a `http://127.0.0.1:5000`

---

