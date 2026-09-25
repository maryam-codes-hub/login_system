from flask import Flask,render_template, request, redirect, url_for
import mysql.connector
import bcrypt

app = Flask(__name__)

# databse connection
db=mysql.connector.connect(
      host="localhost",
      user="root",
      password="Mysql@2026#Db",
      database="login_system"
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
    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
        (username, email, hashed_password)
    )
    db.commit()
    cursor.close()

    return redirect(url_for('login_page'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()

    if user is None:
        return "User not found"

    stored_password = user[3]  # password column

    if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
        return "Login successful!"
    else:
        return "Wrong password"
    
if __name__ == "__main__":
    app.run(debug=True)