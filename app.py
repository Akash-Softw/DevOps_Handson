from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)
DB_NAME = "UserCreden.db"

# --- Initialize Database ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT,
        password TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

init_db()

# --- Serve the HTML ---
@app.route("/")
def home():
    return render_template("index.html")

# --- Signup Logic ---
@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                       (username, email, password))
        conn.commit()
        msg = "Signup successful! Now login."
    except sqlite3.IntegrityError:
        msg = "Username already exists!"
    conn.close()
    
    return render_template("index.html", message=msg)

# --- Login Logic ---
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        msg = f"Welcome, {username}!"
    else:
        msg = "Invalid username or password!"
    
    return render_template("index.html", message=msg)

if __name__ == "__main__":
    app.run(debug=True)
