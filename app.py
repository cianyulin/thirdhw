from flask import Flask, render_template, request
import os
import sqlite3

def init_db():
    db_path = 'membership.db'
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
                iid INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                phone TEXT,
                birthdate TEXT
            )
        ''')
        cursor.execute('''
            INSERT OR IGNORE INTO members (username, email, password, phone, birthdate)
            VALUES (?, ?, ?, ?, ?)
        ''', ("admin", "admin@example.com", "admin123", "0912345678", "1990-01-01"))
        conn.commit()
        conn.close()

app = Flask(__name__)

@app.route('/')
#首頁
def index():
    return render_template('index.html')

@app.route('/login')
#登入
def login():
    return render_template('login.html')

@app.route('/welcome', methods=['GET', 'POST'])
#歡迎頁面
def welcome():
    if request.method == 'POST':
        # Logic to handle POST request (e.g., retrieve user data)
        user_name = request.form.get('email', 'Guest')  # Example: retrieve email as username
        return render_template('welcome.html', user_name=user_name)
    return render_template('welcome.html')

@app.route('/register')
#註冊
def register():
    return render_template('register.html')

@app.route('/edit_profile')
#編輯個人資料
def edit_profile():
    return render_template('edit_profile.html')

@app.template_filter('add_stars')
def add_stars(s):
    return f'★{s}★'

init_db()

