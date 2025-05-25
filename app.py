from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
from flask_bcrypt import Bcrypt
from knn_model import predict_disorder

app = Flask(__name__)
app.secret_key = 'anum_secret_key'
bcrypt = Bcrypt(app)

# Neon DB connection
conn = psycopg2.connect("postgresql://neondb_owner:npg_XibBn1K8PhZV@ep-black-bush-a5i7t6bx-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require")

# 🚀 HOME route (Main Landing Page with bg image/video)
@app.route('/')
def home():
    return render_template('home.html')  # <- NEW main homepage with bg video + navbar

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')
# 💻 LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
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
            return "Invalid login. <a href='/login'>Try again</a>"

    return render_template('login.html')  # login form

# 📝 REGISTER
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
            return redirect(url_for('login'))
        except Exception as e:
            conn.rollback()
            cur.close()
            return f"Error: {e}"

    return render_template('register.html')

# 🌈 QUESTIONNAIRE PAGE
# Add this at the top with other imports
from functools import wraps

# Create login_required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Update your questionnaire route
@app.route('/questionnaire')
@login_required  # Add this decorator
def questionnaire():
    return render_template('questionnaire.html', username=session['user'])

# 🔍 SUBMIT ANSWERS & PREDICT
@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    if 'user' not in session:
        return redirect(url_for('login'))

    username = session['user']
    age = request.form.get('age')
    gender = request.form.get('gender')
    weight = request.form.get('weight')
    email = request.form.get('email')

    answers = [request.form.get(f"q{i}") for i in range(1, 11)]

    try:
        result = predict_disorder(answers)

        tips = tips_dict = {
            'adhd': ["Break tasks down.", "Use timers.", "Stick to routines."],
            'ocd': ["Challenge thoughts.", "Avoid reassurance.", "Try ERP."],
            'ptsd': ["Use grounding.", "Avoid triggers.", "Talk to a therapist."],
            'bpd': ["Use DBT.", "Journal often.", "Set boundaries."],
            'none': ["Stay positive and reach out when needed."]
        }

        tips = tips_dict.get(result, ["Stay positive and reach out when needed."])

        return render_template("result.html", result=result, name=username, tips=tips)

    except Exception as e:
        conn.rollback()
        return f"Error saving answers: {e}"

# 🔐 LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# 🔧 RUN THE APP
if __name__ == '__main__':
    app.run(debug=True)
