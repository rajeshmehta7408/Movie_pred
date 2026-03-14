from flask import Flask, render_template, request, redirect, session
import mysql.connector
import joblib
import os
from model import recommend

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Load ML model
model = joblib.load("movie_model.pkl")

def predict_movie(data):
    prediction = model.predict([data])
    return "Hit" if prediction[0] == 1 else "Flop"

# MySQL Connection (ADD YOUR PASSWORD)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # <-- put your mysql password here
    database="movie_db"
)

cursor = db.cursor()

@app.route('/')
def home():
    return render_template("index.html")

# Signup
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        cursor.execute(
            "INSERT INTO users (name,email,password) VALUES (%s,%s,%s)",
            (name,email,password)
        )
        db.commit()
        return redirect('/login')
    return render_template("signup.html")

# Login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        
        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email,password)
        )
        user = cursor.fetchone()
        
        if user:
            session['user'] = user[1]
            return redirect('/dashboard')
        else:
            return "Invalid Credentials"
    return render_template("login.html")

# Dashboard
@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if 'user' in session:
        if request.method == "POST":
            movie = request.form['movie']
            results = recommend(movie)
            return render_template("dashboard.html", movies=results)
        return render_template("dashboard.html")
    return redirect('/login')

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)