from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'anum_secret_key'
bcrypt = Bcrypt(app)

# Neon DB connection
conn = psycopg2.connect("postgresql://neondb_owner:npg_XibBn1K8PhZV@ep-black-bush-a5i7t6bx-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require")

@app.route('/')
def home():
    return render_template('login_register.html')  # Login form + link to register

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()

    if user and bcrypt.check_password_hash(user[0], password):
        session['user'] = username
        return redirect(url_for('questionnaire'))
    else:
        return "Invalid login. <a href='/'>Try again</a>"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            conn.commit()
            cur.close()
            return "User registered successfully! <a href='/'>Login here</a>."
        except Exception as e:
            conn.rollback()
            cur.close()
            return f"Error: {e}"

    return render_template('register.html')

@app.route('/questionnaire')
def questionnaire():
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template('questionnaire.html', username=session['user'])

@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    if 'user' not in session:
        return redirect(url_for('home'))

    # Collect form data
    username = session['user']
    age = request.form.get('age')
    gender = request.form.get('gender')
    weight = request.form.get('weight')
    email = request.form.get('email')

    q1 = request.form.get('q1')
    q2 = request.form.get('q2')
    q3 = request.form.get('q3')
    q4 = request.form.get('q4')
    q5 = request.form.get('q5')
    q6 = request.form.get('q6')
    q7 = request.form.get('q7')
    q8 = request.form.get('q8')
    q9 = request.form.get('q9')
    q10 = request.form.get('q10')

    # Insert into Neon DB
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO user_answers (username, age, gender, weight, email, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (username, age, gender, weight, email, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10))
        conn.commit()
        cur.close()
        return "Answers submitted successfully!"
    except Exception as e:
        conn.rollback()
        return f"Error saving answers: {e}"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
