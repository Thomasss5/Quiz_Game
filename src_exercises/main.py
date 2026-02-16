import os
import sys
from quiz_manager import QuizManager
from quiz_model import Quiz, Question

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("=" * 40)
    print("       QUIZ GAME CONSOLE APP       ")
    print("=" * 40)

def play_quiz(quiz: Quiz):
    quiz.reset()
    while not quiz.is_finished():
        clear_screen()
        print_header()
        print(f"Quiz: {quiz.title}")
        print(f"Score: {quiz.score}/{len(quiz.questions)}")
        print("-" * 40)
        
        q = quiz.get_question(quiz.current_question_index)
        print(f"Question {quiz.current_question_index + 1}: {q.text}")
        print()
        
        for i, option in enumerate(q.options):
            print(f"{i + 1}. {option}")
        
        print()
        try:
            choice = int(input("Enter your choice (number): ")) - 1
            if 0 <= choice < len(q.options):
                correct = q.is_correct(choice)
                quiz.answer_current_question(choice)
                if correct:
                    print("\nCorrect! ✅")
                else:
                    print(f"\nWrong! ❌ The correct answer was: {q.options[q.correct_index]}")
                input("\nPress Enter to continue...")
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")
        except ValueError:
            print("Invalid input. Please enter a number.")
            input("Press Enter to continue...")

    clear_screen()
    print_header()
    print("QUIZ FINISHED!")
    print(f"Final Score: {quiz.score}/{len(quiz.questions)}")
    
    percentage = (quiz.score / len(quiz.questions)) * 100
    if percentage == 100:
        print("Perfect! 🏆")
    elif percentage >= 70:
        print("Great job! 👏")
    else:
        print("Better luck next time! 💪")
    
    input("\nPress Enter to return to menu...")

def create_quiz(manager: QuizManager):
    clear_screen()
    print_header()
    print("CREATE NEW QUIZ")
    
    title = input("Enter quiz title: ")
    quiz = Quiz(title)
    
    while True:
        print(f"\nAdding Question #{len(quiz.questions) + 1}")
        text = input("Question text (or 'done' to finish): ")
        if text.lower() == 'done':
            break
            
        options = []
        while True:
            opt = input(f"Option {len(options) + 1} (or 'done' to finish options): ")
            if opt.lower() == 'done':
                if len(options) < 2:
                    print("You need at least 2 options.")
                    continue
                break
            options.append(opt)
            
        while True:
            try:
                correct_idx = int(input(f"Enter correct option number (1-{len(options)}): ")) - 1
                if 0 <= correct_idx < len(options):
                    break
                print("Invalid option number.")
            except ValueError:
                print("Please enter a number.")
        
        quiz.add_question(Question(text, options, correct_idx))
        print("Question added!")
    
    if quiz.questions:
        filename = input("Enter filename to save (e.g. my_quiz): ")
        manager.save_quiz(quiz, filename)
        print("Quiz saved successfully!")
    else:
        print("No questions added. Quiz discarded.")
    input("\nPress Enter to continue...")

def main():
    manager = QuizManager()
    
    while True:
        clear_screen()
        print_header()
        print("1. Play a Quiz")
        print("2. Create a Quiz")
        print("3. Exit")
        print()
        
        choice = input("Select an option: ")
        
        if choice == '1':
            quizzes = manager.list_quizzes()
            if not quizzes:
                print("\nNo quizzes found. Create one first!")
                input("Press Enter to continue...")
                continue
                
            print("\nAvailable Quizzes:")
            for i, f in enumerate(quizzes):
                print(f"{i + 1}. {f}")
            
            try:
                q_idx = int(input("\nSelect a quiz number: ")) - 1
                if 0 <= q_idx < len(quizzes):
                    quiz = manager.load_quiz(quizzes[q_idx])
                    if quiz:
                        play_quiz(quiz)
                else:
                    print("Invalid selection.")
                    input("Press Enter to continue...")
            except ValueError:
                print("Invalid input.")
                input("Press Enter to continue...")
                
        elif choice == '2':
            create_quiz(manager)
            
        elif choice == '3':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
