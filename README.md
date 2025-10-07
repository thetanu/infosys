📋  AI Based Quiz Generator Project-

🎯 What is this project?
A AI-based quiz application where users can register, login, take quizzes on different subjects, and view their score history. All data is stored permanently in a database.

🏗️ Project Architecture (3 Main Parts):
1. Frontend (HTML/CSS/JavaScript)
The beautiful website interface users see
Handles button clicks, form inputs, and displays
Sends requests to backend when user performs actions

2. Backend (Python Flask Server)
Acts as the middleman between website and database
Handles user registration, login, and quiz logic
Processes requests and sends responses back to frontend

3. Database (SQLite)
Stores all data permanently
Contains 3 tables: users, questions, and quiz results
Even after closing the app, data remains saved


🔄 How It Works (User Flow):
Step 1: User Opens Website
→ Sees welcome screen with Login/Register buttons
Step 2: Registration
→ User fills name, username, password
→ Frontend sends data to Flask backend
→ Backend saves user in database
→ Success message shown
Step 3: Login
→ User enters username & password
→ Backend checks if credentials match database
→ If correct, user enters main menu
Step 4: Take Quiz
→ User selects: Subject (Maths/Science/CS) → Difficulty (Easy/Medium/Hard) → Number of questions
→ Backend fetches random questions from database
→ Frontend displays questions one by one
→ User selects answers
Step 5: View Results
→ Score calculated and displayed
→ Result saved in database with timestamp
→ User can reattempt or view history

📊 Database Tables:
1. users table
Stores: id, name, username, password, registration date
2. quiz_results table
Stores: user_id, subject, difficulty, score, percentage, date/time
3. ai_generated_questions


💻 Technologies Used

Frontend: HTML5, CSS3, JavaScript (ES6)
Backend: Python, Flask framework
Database: SQLite3
API Style: RESTful JSON API
Session Management: Flask sessions
Uses OpenAI GPT API 

✨ Key Features:
✅ User authentication (register/login)
✅ Random question selection
✅ Real-time score calculation
✅ Quiz history tracking (last 10 attempts)
✅ Responsive, modern UI design
✅ Permanent data storage
✅Implemented NLP-based question generation via OpenAI API

🎨 Why This Architecture?
Separation of Concerns:

Frontend = User Interface (what users see)
Backend = Business Logic (processes data)
Database = Data Storage (remembers everything)


Scalable (can add more features)
Secure (passwords stored in database, not visible in frontend)
Professional industry-standard structure
