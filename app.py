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
if __name__ == "__main__":
    app.run(debug=True)