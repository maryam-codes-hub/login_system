from flask import Flask,render_template, request, redirect, url_for,session
import mysql.connector
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()  

app = Flask(__name__)
app.secret_key =os.getenv("SECRET_KEY")

# databse connection
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

@app.route('/')
def home():
    return render_template("login.html")
@app.route("/login")
def login_page():
        return render_template("login.html")
@app.route("/signup")
def signup_page():
        return render_template("signup.html")


@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # Password ko hash karna
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Database mein save karna
    cursor = db.cursor()
    try:
       cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
        (username, email, hashed_password)
    )
       db.commit()
       cursor.close()

       return redirect(url_for('login_page'))
    except mysql.connector.errors.IntegrityError:
        cursor.close()
        return "Username or Email already exists. Please try a different one."


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    if not username or not password:
      return "Username and password are required."
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()

    if user is None:
        return "User not found"

    stored_password = user[3]  # password column

    if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
        session['username'] = user[1]   # session mein username save karna
        session['user_id'] = user[0]    # session mein id save karna
        return redirect(url_for('dashboard'))
    else:
        return "Wrong password"

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    return render_template('dashboard.html', username=session['username'])


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))
    
if __name__ == "__main__":
    app.run(debug=True)