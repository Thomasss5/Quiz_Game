import tkinter as tk
from tkinter import messagebox, simpledialog
from quiz_manager import QuizManager
from quiz_model import Quiz

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game")
        self.root.geometry("600x500")
        self.root.configure(bg="#1a1a2e")
        
        self.manager = QuizManager()
        self.current_quiz = None
        
        self.setup_main_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def setup_main_menu(self):
        self.clear_window()
        
        frame = tk.Frame(self.root, bg="#1a1a2e")
        frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        title = tk.Label(frame, text="QUIZ GAME", font=("Helvetica", 24, "bold"), bg="#1a1a2e", fg="#00d9ff")
        title.pack(pady=40)
        
        quizzes = self.manager.list_quizzes()
        
        if not quizzes:
            tk.Label(frame, text="No quizzes found.", bg="#1a1a2e", fg="#ffffff", font=("Arial", 14)).pack()
        else:
            tk.Label(frame, text="Select a Quiz:", bg="#1a1a2e", fg="#ffffff", font=("Arial", 14, "bold")).pack(pady=10)
            
            self.quiz_var = tk.StringVar(value=quizzes[0])
            quiz_list = tk.OptionMenu(frame, self.quiz_var, *quizzes)
            quiz_list.config(width=30, font=("Arial", 10), bg="#16213e", fg="#ffffff", activebackground="#0f3460", activeforeground="#00d9ff", highlightthickness=0)
            quiz_list.pack(pady=10)
            
            play_btn = tk.Button(frame, text="Play Quiz", command=self.start_quiz, 
                               bg="#00d9ff", fg="#1a1a2e", font=("Arial", 14, "bold"), padx=30, pady=12, 
                               activebackground="#00b4d8", activeforeground="#ffffff", relief="flat", cursor="hand2")
            play_btn.pack(pady=20)

        quit_btn = tk.Button(frame, text="Exit", command=self.root.quit, 
                          bg="#00d9ff", fg="#1a1a2e", font=("Arial", 14, "bold"), padx=30, pady=12, 
                               activebackground="#00b4d8", activeforeground="#ffffff", relief="flat", cursor="hand2")
        quit_btn.pack(side="bottom", pady=20)

    def start_quiz(self):
        filename = self.quiz_var.get()
        self.current_quiz = self.manager.load_quiz(filename)
        if self.current_quiz:
            self.current_quiz.reset()
            self.show_question()
        else:
            messagebox.showerror("Error", "Could not load quiz.")

    def show_question(self):
        self.clear_window()
        
        if self.current_quiz.is_finished():
            self.show_results()
            return
            
        q = self.current_quiz.get_question(self.current_quiz.current_question_index)
        
        # Header
        header_frame = tk.Frame(self.root, bg="#16213e")
        header_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(header_frame, text=f"Quiz: {self.current_quiz.title}", bg="#16213e", fg="#00d9ff", font=("Arial", 12, "bold")).pack(side='left')
        tk.Label(header_frame, text=f"Score: {self.current_quiz.score}", bg="#16213e", fg="#ffd60a", font=("Arial", 12, "bold")).pack(side='right')
        
        # Question
        content_frame = tk.Frame(self.root, bg="#1a1a2e")
        content_frame.pack(expand=True, fill='both', padx=40)
        
        progress = f"Question {self.current_quiz.current_question_index + 1} of {len(self.current_quiz.questions)}"
        tk.Label(content_frame, text=progress, bg="#1a1a2e", fg="#a8dadc", font=("Arial", 11)).pack(pady=(20, 5))
        
        q_label = tk.Label(content_frame, text=q.text, bg="#1a1a2e", fg="#ffffff", font=("Helvetica", 18, "bold"), wraplength=500, justify="center")
        q_label.pack(pady=20)
        
        # Options
        for i, option in enumerate(q.options):
            btn = tk.Button(content_frame, text=option, command=lambda idx=i: self.answer(idx),
                          font=("Arial", 14, "bold"), bg="#00d9ff", fg="#1a1a2e", 
                          activebackground="#00b4d8", activeforeground="#ffffff", 
                          relief="flat", bd=0, padx=20, cursor="hand2")
            btn.pack(fill='x', pady=10, ipady=12)

    def answer(self, index):
        correct = self.current_quiz.answer_current_question(index)
        if correct:
            messagebox.showinfo("Result", "Correct! ✅")
        else:
            q = self.current_quiz.get_question(self.current_quiz.current_question_index - 1)
            messagebox.showerror("Result", f"Wrong! ❌\nCorrect answer: {q.options[q.correct_index]}")
        
        self.show_question()

    def show_results(self):
        self.clear_window()
        
        frame = tk.Frame(self.root, bg="#1a1a2e")
        frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        tk.Label(frame, text="QUIZ FINISHED!", font=("Helvetica", 24, "bold"), bg="#1a1a2e", fg="#00d9ff").pack(pady=40)
        
        score_text = f"Final Score: {self.current_quiz.score} / {len(self.current_quiz.questions)}"
        tk.Label(frame, text=score_text, font=("Arial", 20, "bold"), bg="#1a1a2e", fg="#ffd60a").pack(pady=20)
        
        percentage = (self.current_quiz.score / len(self.current_quiz.questions)) * 100
        msg = ""
        if percentage == 100: msg = "Perfect! 🏆"
        elif percentage >= 70: msg = "Great job! 👏"
        else: msg = "Better luck next time! 💪"
        
        tk.Label(frame, text=msg, font=("Arial", 16, "italic"), bg="#1a1a2e", fg="#a8dadc").pack(pady=10)
        
        tk.Button(frame, text="Back to Menu", command=self.setup_main_menu,
                bg="#00d9ff", fg="#1a1a2e", font=("Arial", 14, "bold"), padx=30, pady=12, 
                activebackground="#00b4d8", activeforeground="#ffffff", relief="flat", cursor="hand2").pack(pady=40)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
