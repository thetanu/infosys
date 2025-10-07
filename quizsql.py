import random
import os
import sqlite3
from datetime import datetime

# Database setup
def init_database():
    conn = sqlite3.connect('quiz_app.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create quiz_results table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            percentage REAL NOT NULL,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create questions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            question TEXT NOT NULL,
            option1 TEXT NOT NULL,
            option2 TEXT NOT NULL,
            option3 TEXT NOT NULL,
            option4 TEXT NOT NULL,
            correct_answer INTEGER NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

# Insert sample questions if database is empty
def populate_questions():
    conn = sqlite3.connect('quiz_app.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM questions')
    if cursor.fetchone()[0] > 0:
        conn.close()
        return
    
    # Sample questions
    questions = [
        # Maths - Easy
        ('maths', 'easy', 'What is 5 + 3?', '6', '7', '8', '9', 2),
        ('maths', 'easy', 'What is 10 - 4?', '5', '6', '7', '8', 1),
        ('maths', 'easy', 'What is 2 × 3?', '5', '6', '7', '8', 1),
        ('maths', 'easy', 'What is 12 ÷ 4?', '2', '3', '4', '5', 1),
        ('maths', 'easy', 'What is 7 + 8?', '14', '15', '16', '17', 1),
        
        # Maths - Medium
        ('maths', 'medium', 'What is 15 × 12?', '160', '170', '180', '190', 2),
        ('maths', 'medium', 'What is √144?', '10', '11', '12', '13', 2),
        ('maths', 'medium', 'What is 25% of 200?', '40', '50', '60', '70', 1),
        ('maths', 'medium', 'What is 2³?', '6', '8', '9', '10', 1),
        ('maths', 'medium', 'What is 72 ÷ 9?', '6', '7', '8', '9', 2),
        
        # Maths - Difficult
        ('maths', 'difficult', 'What is the value of π approximately?', '3.12', '3.14', '3.16', '3.18', 1),
        ('maths', 'difficult', 'What is 15² - 13²?', '52', '54', '56', '58', 2),
        ('maths', 'difficult', 'If x² = 169, what is x?', '11', '12', '13', '14', 2),
        ('maths', 'difficult', 'What is 7! (factorial)?', '5040', '5140', '5240', '5340', 0),
        ('maths', 'difficult', 'What is log₁₀(1000)?', '2', '3', '4', '5', 1),
        
        # Science - Easy
        ('science', 'easy', 'What planet is known as the Red Planet?', 'Venus', 'Mars', 'Jupiter', 'Saturn', 1),
        ('science', 'easy', 'What gas do plants absorb?', 'Oxygen', 'Nitrogen', 'Carbon Dioxide', 'Hydrogen', 2),
        ('science', 'easy', 'How many legs does a spider have?', '6', '8', '10', '12', 1),
        ('science', 'easy', 'What is H2O?', 'Air', 'Water', 'Salt', 'Sugar', 1),
        ('science', 'easy', 'What is the boiling point of water?', '90°C', '100°C', '110°C', '120°C', 1),
        
        # Science - Medium
        ('science', 'medium', 'What is the powerhouse of the cell?', 'Nucleus', 'Mitochondria', 'Ribosome', 'Chloroplast', 1),
        ('science', 'medium', 'What is the speed of light?', '3×10⁸ m/s', '3×10⁷ m/s', '3×10⁹ m/s', '3×10⁶ m/s', 0),
        ('science', 'medium', 'What is the atomic number of Carbon?', '4', '5', '6', '7', 2),
        ('science', 'medium', 'What force keeps us on Earth?', 'Friction', 'Gravity', 'Magnetism', 'Tension', 1),
        ('science', 'medium', 'What is photosynthesis?', 'Breaking food', 'Making food', 'Breathing', 'Digesting', 1),
        
        # Science - Difficult
        ('science', 'difficult', 'What is Avogadro\'s number?', '6.02×10²³', '6.02×10²²', '6.02×10²⁴', '6.02×10²¹', 0),
        ('science', 'difficult', 'What is DNA made of?', 'Proteins', 'Lipids', 'Nucleotides', 'Carbohydrates', 2),
        ('science', 'difficult', 'What is Newton\'s second law?', 'F=ma', 'E=mc²', 'V=IR', 'PV=nRT', 0),
        ('science', 'difficult', 'What particle has no charge?', 'Proton', 'Electron', 'Neutron', 'Positron', 2),
        ('science', 'difficult', 'What is the pH of pure water?', '6', '7', '8', '9', 1),
        
        # CS - Easy
        ('cs', 'easy', 'What does CPU stand for?', 'Central Process Unit', 'Central Processing Unit', 'Computer Personal Unit', 'Central Processor Unity', 1),
        ('cs', 'easy', 'What does RAM stand for?', 'Random Access Memory', 'Read Access Memory', 'Random Allocated Memory', 'Ready Access Memory', 0),
        ('cs', 'easy', 'What is binary for 5?', '100', '101', '110', '111', 1),
        ('cs', 'easy', 'What is the extension of a Python file?', '.python', '.py', '.pt', '.p', 1),
        ('cs', 'easy', 'What is a bug in programming?', 'Feature', 'Error', 'Code', 'Function', 1),
        
        # CS - Medium
        ('cs', 'medium', 'What is a loop used for?', 'Store data', 'Repeat code', 'Delete code', 'Print code', 1),
        ('cs', 'medium', 'What is OOP?', 'Object Oriented Programming', 'Only One Programming', 'Open Object Programming', 'Optimal Oriented Programming', 0),
        ('cs', 'medium', 'What is a variable?', 'A loop', 'A function', 'A storage container', 'A class', 2),
        ('cs', 'medium', 'What does HTML stand for?', 'Hyper Text Markup Language', 'High Text Markup Language', 'Hyper Transfer Markup Language', 'Home Text Markup Language', 0),
        ('cs', 'medium', 'What is an array?', 'A single value', 'A collection of values', 'A function', 'A loop', 1),
        
        # CS - Difficult
        ('cs', 'difficult', 'What is time complexity of binary search?', 'O(n)', 'O(log n)', 'O(n²)', 'O(1)', 1),
        ('cs', 'difficult', 'What is polymorphism?', 'One form', 'Many forms', 'No form', 'Two forms', 1),
        ('cs', 'difficult', 'What is a stack data structure?', 'FIFO', 'LIFO', 'Random', 'Sequential', 1),
        ('cs', 'difficult', 'What is recursion?', 'Loop', 'Function calling itself', 'Variable', 'Array', 1),
        ('cs', 'difficult', 'What is Big O notation used for?', 'Measure space', 'Measure time complexity', 'Measure errors', 'Measure bugs', 1)
    ]
    
    cursor.executemany('''
        INSERT INTO questions (subject, difficulty, question, option1, option2, option3, option4, correct_answer)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', questions)
    
    conn.commit()
    conn.close()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def register():
    clear_screen()
    print("=" * 50)
    print("REGISTRATION".center(50))
    print("=" * 50)
    name = input("\nEnter your name: ").strip()
    if not name:
        print("Name cannot be empty!")
        input("Press Enter to continue...")
        return None
    
    username = input("Enter username: ").strip()
    if not username:
        print("Username cannot be empty!")
        input("Press Enter to continue...")
        return None
    
    password = input("Enter password: ").strip()
    if not password:
        print("Password cannot be empty!")
        input("Press Enter to continue...")
        return None
    
    try:
        conn = sqlite3.connect('quiz_app.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, username, password) VALUES (?, ?, ?)', 
                      (name, username, password))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        print(f"\nRegistration successful! Welcome, {name}!")
        input("Press Enter to continue...")
        return user_id
    except sqlite3.IntegrityError:
        print("Username already exists!")
        input("Press Enter to continue...")
        return None

def login():
    clear_screen()
    print("=" * 50)
    print("LOGIN".center(50))
    print("=" * 50)
    username = input("\nEnter username: ").strip()
    password = input("Enter password: ").strip()
    
    conn = sqlite3.connect('quiz_app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM users WHERE username = ? AND password = ?', 
                  (username, password))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        print(f"\nLogin successful! Welcome back, {result[1]}!")
        input("Press Enter to continue...")
        return result[0]  # Return user_id
    else:
        print("\nInvalid username or password!")
        input("Press Enter to continue...")
        return None

def choose_subject():
    clear_screen()
    print("=" * 50)
    print("CHOOSE SUBJECT".center(50))
    print("=" * 50)
    print("\n1. Maths")
    print("2. Science")
    print("3. CS (Computer Science)")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    subjects = {'1': 'maths', '2': 'science', '3': 'cs'}
    return subjects.get(choice)

def choose_difficulty():
    clear_screen()
    print("=" * 50)
    print("CHOOSE DIFFICULTY LEVEL".center(50))
    print("=" * 50)
    print("\n1. Easy")
    print("2. Medium")
    print("3. Difficult")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    levels = {'1': 'easy', '2': 'medium', '3': 'difficult'}
    return levels.get(choice)

def choose_num_questions(subject, difficulty):
    conn = sqlite3.connect('quiz_app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM questions WHERE subject = ? AND difficulty = ?', 
                  (subject, difficulty))
    max_q = cursor.fetchone()[0]
    conn.close()
    
    clear_screen()
    print("=" * 50)
    print("NUMBER OF QUESTIONS".center(50))
    print("=" * 50)
    print(f"\nMaximum available questions: {max_q}")
    
    while True:
        try:
            num = int(input(f"Enter number of questions (1-{max_q}): "))
            if 1 <= num <= max_q:
                return num
            else:
                print(f"Please enter a number between 1 and {max_q}")
        except ValueError:
            print("Please enter a valid number")

def conduct_quiz(subject, difficulty, num_questions):
    conn = sqlite3.connect('quiz_app.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, question, option1, option2, option3, option4, correct_answer 
        FROM questions WHERE subject = ? AND difficulty = ?
        ORDER BY RANDOM() LIMIT ?
    ''', (subject, difficulty, num_questions))
    
    questions = cursor.fetchall()
    conn.close()
    
    score = 0
    total = len(questions)
    
    for i, q in enumerate(questions, 1):
        clear_screen()
        print("=" * 50)
        print(f"QUESTION {i}/{total}".center(50))
        print("=" * 50)
        print(f"\n{q[1]}\n")
        
        options = [q[2], q[3], q[4], q[5]]
        for j, opt in enumerate(options, 1):
            print(f"{j}. {opt}")
        
        while True:
            try:
                ans = int(input("\nYour answer (1-4): "))
                if 1 <= ans <= 4:
                    break
                else:
                    print("Please enter a number between 1 and 4")
            except ValueError:
                print("Please enter a valid number")
        
        if ans - 1 == q[6]:
            score += 1
            print("\n✓ Correct!")
        else:
            print(f"\n✗ Wrong! Correct answer: {options[q[6]]}")
        
        input("\nPress Enter to continue...")
    
    return score, total

def save_quiz_result(user_id, subject, difficulty, score, total):
    percentage = (score / total) * 100
    
    conn = sqlite3.connect('quiz_app.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO quiz_results (user_id, subject, difficulty, score, total_questions, percentage)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, subject, difficulty, score, total, percentage))
    conn.commit()
    conn.close()

def show_result(user_id, score, total, subject, difficulty):
    clear_screen()
    print("=" * 50)
    print("QUIZ RESULT".center(50))
    print("=" * 50)
    
    percentage = (score / total) * 100
    
    conn = sqlite3.connect('quiz_app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM users WHERE id = ?', (user_id,))
    name = cursor.fetchone()[0]
    conn.close()
    
    print(f"\nName: {name}")
    print(f"Subject: {subject.upper()}")
    print(f"Difficulty: {difficulty.capitalize()}")
    print(f"\nScore: {score}/{total}")
    print(f"Percentage: {percentage:.2f}%")
    
    if percentage >= 80:
        print("\n🏆 Excellent! Outstanding performance!")
    elif percentage >= 60:
        print("\n👍 Good job! Well done!")
    elif percentage >= 40:
        print("\n📚 Not bad! Keep practicing!")
    else:
        print("\n💪 Don't give up! Practice makes perfect!")
    
    save_quiz_result(user_id, subject, difficulty, score, total)
    
    print("\n" + "=" * 50)
    print("\n1. Reattempt Quiz")
    print("2. View History")
    print("3. Main Menu")
    print("4. Logout")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    return choice

def view_history(user_id):
    clear_screen()
    print("=" * 50)
    print("QUIZ HISTORY".center(50))
    print("=" * 50)
    
    conn = sqlite3.connect('quiz_app.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT subject, difficulty, score, total_questions, percentage, completed_at
        FROM quiz_results WHERE user_id = ?
        ORDER BY completed_at DESC LIMIT 10
    ''', (user_id,))
    
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        print("\nNo quiz history found!")
    else:
        print("\nYour Last 10 Quiz Results:\n")
        for i, r in enumerate(results, 1):
            print(f"{i}. {r[0].upper()} - {r[1].capitalize()}")
            print(f"   Score: {r[2]}/{r[3]} ({r[4]:.1f}%)")
            print(f"   Date: {r[5]}")
            print()
    
    input("Press Enter to continue...")

def main():
    # Initialize database
    init_database()
    populate_questions()
    
    current_user = None
    
    while True:
        if current_user is None:
            clear_screen()
            print("=" * 50)
            print("QUIZ GENERATOR APP".center(50))
            print("=" * 50)
            print("\n1. Register")
            print("2. Login")
            print("3. Exit")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                current_user = register()
            elif choice == '2':
                current_user = login()
            elif choice == '3':
                print("\nThank you for using Quiz Generator App!")
                break
            else:
                print("\nInvalid choice!")
                input("Press Enter to continue...")
        else:
            clear_screen()
            print("=" * 50)
            print("MAIN MENU".center(50))
            print("=" * 50)
            
            subject = choose_subject()
            if not subject:
                print("\nInvalid choice!")
                input("Press Enter to continue...")
                continue
            
            difficulty = choose_difficulty()
            if not difficulty:
                print("\nInvalid choice!")
                input("Press Enter to continue...")
                continue
            
            num_questions = choose_num_questions(subject, difficulty)
            
            score, total = conduct_quiz(subject, difficulty, num_questions)
            
            result_choice = show_result(current_user, score, total, subject, difficulty)
            
            if result_choice == '4':
                print("\nLogging out...")
                current_user = None
                input("Press Enter to continue...")
            elif result_choice == '2':
                view_history(current_user)
            elif result_choice == '3':
                continue

if __name__ == "__main__":
    main()