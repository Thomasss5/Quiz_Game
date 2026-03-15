import tkinter as tk
from tkinter import messagebox, font, ttk
import os
import random

try:
    from quiz_manager import QuizManager
except ImportError:
    messagebox.showerror("Errore", "Non trovo quiz_manager.py!")
    exit()

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Universe Pro")
        self.root.geometry("850x800")

        # Palette Colori
        self.bg_color = "#2D3436"
        self.text_color = "#dfe6e9"
        self.accent_color = "#00b894"
        self.mix_color = "#0984e3"
        self.correct_color = "#55efc4"
        self.incorrect_color = "#ff7675"
        self.timer_color = "#fab1a0"
        
        self.root.configure(bg=self.bg_color)
        
        # Variabili di stato
        self.time_limit = 20 
        self.remaining_time = self.time_limit
        self.timer_job = None 
        self.current_correct_answer = ""
        self.total_questions_requested = 10
        self.selected_category_name = "" # Variabile salvavita per evitare il crash

        # Font
        self.title_font = font.Font(family="Helvetica", size=32, weight="bold")
        self.category_font = font.Font(family="Helvetica", size=12, slant="italic")
        self.question_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.timer_font = font.Font(family="Helvetica", size=16, weight="bold")

        self.questions_dir = "questions"
        self.manager = QuizManager(quizzes_dir=self.questions_dir)
        self.current_questions = []
        self.current_index = 0
        self.score = 0
        self.selected_option = tk.StringVar()

        self.setup_main_menu()

    def clear_window(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        for widget in self.root.winfo_children():
            widget.destroy()

    def setup_main_menu(self):
        self.clear_window()
        container = tk.Frame(self.root, bg=self.bg_color)
        container.pack(expand=True)

        tk.Label(container, text="QUIZ UNIVERSE", font=self.title_font, 
                 bg=self.bg_color, fg=self.accent_color).pack(pady=(0, 10))
        
        tk.Label(container, text="Metti alla prova la tua conoscenza", font=("Helvetica", 11), 
                 bg=self.bg_color, fg="#b2bec3").pack(pady=(0, 40))

        tk.Button(container, text="MODALITÀ MIX (RANDOM)", font=self.button_font, 
                  bg=self.mix_color, fg="white", relief="flat", width=35, pady=15,
                  command=lambda: self.ask_questions_count("MIX")).pack(pady=10)
        
        tk.Label(container, text="SCEGLI UNA CATEGORIA:", font=self.category_font, 
                 bg=self.bg_color, fg=self.accent_color).pack(pady=(30, 10))

        if not os.path.exists(self.questions_dir):
            os.makedirs(self.questions_dir)
            
        categories = [f.replace(".json", "") for f in os.listdir(self.questions_dir) if f.endswith(".json")]
        
        if categories:
            self.cat_combo = ttk.Combobox(container, values=categories, state="readonly", font=("Helvetica", 12), width=30)
            self.cat_combo.current(0)
            self.cat_combo.pack(pady=10, ipady=5)

            tk.Button(container, text="GIOCA CATEGORIA", font=self.button_font, bg=self.accent_color, 
                      fg="white", relief="flat", width=35, pady=10, 
                      command=lambda: self.ask_questions_count("CAT")).pack(pady=5)

    def ask_questions_count(self, mode):
        """Salva la categoria e mostra lo slider per il numero di domande."""
        # Salviamo il nome della categoria PRIMA di distruggere il widget cat_combo
        if mode == "CAT":
            self.selected_category_name = self.cat_combo.get()
        else:
            self.selected_category_name = "MIX"
            
        self.clear_window()
        
        container = tk.Frame(self.root, bg=self.bg_color)
        container.pack(expand=True)

        tk.Label(container, text="CONFIGURA QUIZ", font=self.title_font, 
                 bg=self.bg_color, fg=self.accent_color).pack(pady=20)
        
        tk.Label(container, text=f"Modalità: {self.selected_category_name}", font=self.question_font, 
                 bg=self.bg_color, fg=self.text_color).pack(pady=10)

        tk.Label(container, text="Quante domande vuoi affrontare?", 
                 bg=self.bg_color, fg="#b2bec3", font=("Helvetica", 10)).pack(pady=20)

        count_slider = tk.Scale(container, from_=5, to=20, orient="horizontal", length=300,
                                bg=self.bg_color, fg="white", highlightthickness=0,
                                font=self.button_font, troughcolor="#34495e")
        count_slider.set(10)
        count_slider.pack(pady=10)

        def confirm_and_start():
            self.total_questions_requested = count_slider.get()
            if mode == "MIX":
                self.start_mixed_quiz()
            else:
                self.start_category_quiz()

        tk.Button(container, text="INIZIA QUIZ", font=self.button_font, bg=self.accent_color,
                  fg="white", relief="flat", width=25, pady=15, command=confirm_and_start).pack(pady=40)
        
        tk.Button(container, text="ANNULLA", font=self.button_font, bg=self.incorrect_color,
                  fg="white", relief="flat", width=25, command=self.setup_main_menu).pack()

    def start_category_quiz(self):
        selected = self.selected_category_name 
        file_path = os.path.join(self.questions_dir, f"{selected}.json")
        questions = self.manager.load_quiz_from_json(file_path)
        
        valid = [q for q in questions if isinstance(q, dict) and "text" in q and "options" in q]
        if valid:
            for q in valid: q["source_cat"] = selected.upper()
            random.shuffle(valid)
            self.current_questions = valid[:min(len(valid), self.total_questions_requested)]
            self.current_index = 0
            self.score = 0
            self.show_question()

    def start_mixed_quiz(self):
        all_questions = []
        files = [f for f in os.listdir(self.questions_dir) if f.endswith(".json")]
        
        for file in files:
            category_name = file.replace(".json", "").upper()
            questions = self.manager.load_quiz_from_json(os.path.join(self.questions_dir, file))
            for q in questions:
                if isinstance(q, dict) and "text" in q and "options" in q:
                    q["source_cat"] = category_name 
                    all_questions.append(q)

        if not all_questions:
            messagebox.showwarning("Errore", "Nessun file JSON trovato!")
            self.setup_main_menu()
            return

        random.shuffle(all_questions)
        self.current_questions = all_questions[:min(len(all_questions), self.total_questions_requested)]
        self.current_index = 0
        self.score = 0
        self.show_question()

    def confirm_quit(self):
        if messagebox.askyesno("Torna al Menu", "Vuoi davvero interrompere il quiz attuale?"):
            self.setup_main_menu()

    def update_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            if hasattr(self, 'timer_label') and self.timer_label.winfo_exists():
                self.timer_label.config(text=f"Tempo: {self.remaining_time}s")
                self.timer_progress['value'] = self.remaining_time
                self.timer_job = self.root.after(1000, self.update_timer)
        else:
            self.handle_answer(correct_text=self.current_correct_answer, timeout=True)

    def show_question(self):
        self.clear_window()
        self.selected_option.set(None)

        if self.current_index >= len(self.current_questions):
            self.show_results()
            return

        q_data = self.current_questions[self.current_index]
        
        try:
            options = q_data.get("options", [])
            correct_idx = q_data.get("correct_index", 0)
            self.current_correct_answer = options[correct_idx]
        except:
            self.next_question()
            return

        # Header
        header = tk.Frame(self.root, bg="#34495e")
        header.pack(fill="x")
        
        tk.Button(header, text="MENU", font=("Helvetica", 9, "bold"), bg="#e67e22", fg="white",
                  relief="flat", command=self.confirm_quit, padx=10).pack(side="left", padx=10, pady=5)

        tk.Label(header, text=f"Domanda {self.current_index+1}/{len(self.current_questions)}", 
                 bg="#34495e", fg="white").pack(side="left", padx=20)
        
        tk.Label(header, text=f"Punti: {self.score}", bg="#34495e", fg=self.accent_color, 
                 font=("Helvetica", 12, "bold")).pack(side="right", padx=15)

        tk.Label(self.root, text=f"CATEGORIA: {q_data.get('source_cat', 'GENERALE')}", 
                 font=self.category_font, bg=self.bg_color, fg=self.accent_color).pack(pady=(20, 0))

        # Timer
        self.remaining_time = self.time_limit
        self.timer_label = tk.Label(self.root, text=f"Tempo: {self.remaining_time}s", 
                                    font=self.timer_font, bg=self.bg_color, fg=self.timer_color)
        self.timer_label.pack(pady=5)
        self.timer_progress = ttk.Progressbar(self.root, orient="horizontal", length=300, 
                                             mode="determinate", maximum=self.time_limit)
        self.timer_progress['value'] = self.time_limit
        self.timer_progress.pack()

        # Domanda
        tk.Label(self.root, text=q_data.get("text", ""), font=self.question_font, 
                 bg=self.bg_color, fg=self.text_color, wraplength=700, pady=40).pack()

        # Opzioni
        self.options_frame = tk.Frame(self.root, bg=self.bg_color)
        self.options_frame.pack()

        shuffled_opts = list(options)
        random.shuffle(shuffled_opts)

        for opt in shuffled_opts:
            tk.Radiobutton(self.options_frame, text=opt, variable=self.selected_option, value=opt,
                           font=("Helvetica", 13), bg="#34495e", fg=self.text_color,
                           selectcolor=self.accent_color, indicatoron=False, 
                           width=50, pady=10, relief="flat", cursor="hand2").pack(pady=5)

        self.action_btn = tk.Button(self.root, text="CONFERMA RISPOSTA", font=self.button_font, 
                                     bg=self.accent_color, fg="white", relief="flat", 
                                     width=30, pady=15, 
                                     command=lambda: self.handle_answer(self.current_correct_answer))
        self.action_btn.pack(side="bottom", pady=40)

        self.update_timer()

    def handle_answer(self, correct_text=None, timeout=False):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        if correct_text is None:
            correct_text = self.current_correct_answer
        if not timeout and not self.selected_option.get():
            return
        for child in self.options_frame.winfo_children():
            child.configure(state="disabled")

        if not timeout and self.selected_option.get() == correct_text:
            self.score += 1
            res, col = "RISPOSTA ESATTA!", self.correct_color
        elif timeout:
            res, col = f"TEMPO SCADUTO!\nLa risposta corretta era: {correct_text}", self.timer_color
        else:
            res, col = f"RISPOSTA ERRATA!\nLa risposta corretta era: {correct_text}", self.incorrect_color

        tk.Label(self.root, text=res, font=("Helvetica", 15, "bold"), 
                 bg=self.bg_color, fg=col, justify="center").pack(side="bottom", pady=5)
        self.action_btn.config(text="PROSSIMA DOMANDA", bg=self.mix_color, command=self.next_question)

    def next_question(self):
        self.current_index += 1
        self.show_question()

    def show_results(self):
        self.clear_window()
        tk.Label(self.root, text="QUIZ CONCLUSO!", font=self.title_font, bg=self.bg_color, fg=self.accent_color).pack(pady=50)
        tk.Label(self.root, text=f"Punteggio finale: {self.score}/{len(self.current_questions)}", 
                 font=self.question_font, bg=self.bg_color, fg=self.text_color).pack(pady=10)
        tk.Button(self.root, text="TORNA AL MENU", font=self.button_font, bg=self.mix_color,
                  fg="white", relief="flat", width=25, pady=15, command=self.setup_main_menu).pack(pady=50)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()