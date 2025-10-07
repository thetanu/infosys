from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import sqlite3
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

# Database setup
def init_database():
    conn = sqlite3.connect('quiz_app.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
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

def populate_questions():
    conn = sqlite3.connect('quiz_app.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM questions')
    if cursor.fetchone()[0] > 0:
        conn.close()
        return
    
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

# API Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name', '').strip()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    if not name or not username or not password:
        return jsonify({'success': False, 'message': 'All fields are required'})
    
    try:
        conn = sqlite3.connect('quiz_app.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, username, password) VALUES (?, ?, ?)', 
                      (name, username, password))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        return jsonify({'success': True, 'message': f'Registration successful! Welcome, {name}!'})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'message': 'Username already exists'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    conn = sqlite3.connect('quiz_app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM users WHERE username = ? AND password = ?', 
                  (username, password))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        session['user_id'] = result[0]
        session['username'] = username
        session['name'] = result[1]
        return jsonify({'success': True, 'message': f'Welcome back, {result[1]}!', 'name': result[1]})
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password'})

@app.route('/api/questions', methods=['GET'])
def get_questions():
    subject = request.args.get('subject')
    difficulty = request.args.get('difficulty')
    num = int(request.args.get('num', 5))
    
    conn = sqlite3.connect('quiz_app.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, question, option1, option2, option3, option4, correct_answer 
        FROM questions WHERE subject = ? AND difficulty = ?
        ORDER BY RANDOM() LIMIT ?
    ''', (subject, difficulty, num))
    
    questions = cursor.fetchall()
    conn.close()
    
    result = []
    for q in questions:
        result.append({
            'id': q[0],
            'question': q[1],
            'options': [q[2], q[3], q[4], q[5]],
            'correct_answer': q[6]
        })
    
    return jsonify({'success': True, 'questions': result})

@app.route('/api/submit_result', methods=['POST'])
def submit_result():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    data = request.json
    subject = data.get('subject')
    difficulty = data.get('difficulty')
    score = data.get('score')
    total = data.get('total')
    percentage = (score / total) * 100
    
    conn = sqlite3.connect('quiz_app.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO quiz_results (user_id, subject, difficulty, score, total_questions, percentage)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (session['user_id'], subject, difficulty, score, total, percentage))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Result saved successfully'})

@app.route('/api/history', methods=['GET'])
def get_history():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    conn = sqlite3.connect('quiz_app.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT subject, difficulty, score, total_questions, percentage, completed_at
        FROM quiz_results WHERE user_id = ?
        ORDER BY completed_at DESC LIMIT 10
    ''', (session['user_id'],))
    
    results = cursor.fetchall()
    conn.close()
    
    history = []
    for r in results:
        history.append({
            'subject': r[0],
            'difficulty': r[1],
            'score': r[2],
            'total': r[3],
            'percentage': r[4],
            'date': r[5]
        })
    
    return jsonify({'success': True, 'history': history})

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

if __name__ == '__main__':
    init_database()
    populate_questions()
    print("🚀 Server starting on http://127.0.0.1:5000")
    print("📊 Database initialized successfully!")
    app.run(debug=True, port=5000)