from flask import Flask, render_template, request, session, redirect, url_for
import mysql.connector
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"

db = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="Neha@2718",  
    database="mcq_test"
)
cursor = db.cursor(dictionary=True)


@app.route('/')
def home():
    return render_template('home.html') 

@app.route('/start_test')
def start_test():
    """Fetch 10 random MCQs from MySQL"""
    cursor.execute("SELECT * FROM questions ORDER BY RAND() LIMIT 10")
    questions = cursor.fetchall()

    if not questions:
        return "No questions available in the database."

    session['test_questions'] = {str(q['id']): None for q in questions}  
    return render_template('test.html', questions=questions)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    """Store user answers"""
    question_id = request.form.get('question_id')
    selected_option = request.form.get('selected_option')

    if 'test_questions' in session:
        session['test_questions'][question_id] = selected_option

    return redirect(url_for('start_test'))

@app.route('/summary')
def summary():
    """Calculate score"""
    correct_count = 0
    total_questions = len(session.get('test_questions', {}))

    for qid, user_answer in session.get('test_questions', {}).items():
        cursor.execute("SELECT correct_option FROM questions WHERE id = %s", (qid,))
        correct_option = cursor.fetchone()['correct_option']

        if user_answer and int(user_answer) == correct_option:
            correct_count += 1

    return render_template('summary.html', correct_count=correct_count, total_questions=total_questions)


if __name__ == '__main__':
    app.run(debug=True)
