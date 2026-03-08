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
2. Avviare una sessione di gioco tramite **console** (`main.py`) o **interfaccia grafica** (`gui.py`)
3. Rispondere alle domande selezionando una delle opzioni disponibili
4. Calcolare automaticamente il punteggio finale
5. Visualizzare il risultato 
6. Creare nuovi quiz direttamente dall'applicazione console


---

## 📁 Struttura del progetto

```
Quiz_Game/
├── src_exercises/
│   ├── quiz_model.py          # Classi Question e Quiz (logica core)
│   ├── quiz_manager.py        # Gestione salvataggio/caricamento quiz da JSON
│   ├── main.py                # Interfaccia console (CLI)
│   ├── gui.py                 # Interfaccia grafica (Tkinter)
│   ├── test_quiz.py           # Unit test (pytest)
│   ├── Cultura_Genrale.json   # Quiz di cultura generale (10 domande)
│   ├── Informatica.json       # Quiz di informatica (10 domande)
│   └── __init__.py
├── requirements_dev.txt
├── README.md
└── .github/
```

### Struttura dei quiz (JSON)
Ogni quiz è definito tramite un file JSON ed è composto da:
1. **Titolo** del quiz
2. **Elenco di domande**, ciascuna caratterizzata da:
   - testo della domanda
   - elenco di opzioni di risposta
   - indice della risposta corretta



---

## 🚀 Funzionalità principali

✔️ Caricamento quiz da file JSON

✔️ Doppia interfaccia: console (CLI) e grafica (Tkinter)

✔️ Quiz a risposta multipla

✔️ Creazione di nuovi quiz da console

✔️ Calcolo automatico del punteggio

✔️ Feedback visivo sul risultato finale

✔️ Gestione di quiz multipli selezionabili

---

## 🧪 Testing

I test sono sviluppati con il framework **pytest** e coprono il **99%** del codice sorgente.

| File | Coverage |
|------|----------|
| `quiz_model.py` | 100% |
| `quiz_manager.py` | 100% |
| `main.py` | 98% |
| `gui.py` | 95% |
| **Totale** | **99%** |

Per eseguire i test con il report di coverage:
```bash
python3 -m pytest test_quiz.py -v --cov=. --cov-report=term-missing
```

---

## ⚙️ Come eseguire il progetto

### Installazione dipendenze
```bash
pip install -r requirements_dev.txt
```

### Avvio da console
```bash
cd src_exercises
python3 main.py
```

### Avvio con interfaccia grafica
```bash
cd src_exercises
python3 gui.py
```

---

