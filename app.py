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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        birthdate = request.form.get('dob')
        # 用戶名、電子郵件或密碼是否為空，若為空，顯示錯誤頁面，提示「請輸入用戶名、電子郵件和密碼」
        if not username or not email or not password:
            return render_template('error.html', error="請輸入用戶名、電子郵件和密碼")

        conn = sqlite3.connect('membership.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM members WHERE username = ?", (username,))
        existing_user = cursor.fetchone()
        # 用戶名是否已存在於資料庫中，若存在，顯示錯誤頁面，提示「用戶名已存在」
        if existing_user:
            conn.close()
            return render_template('error.html', error="用戶名已存在")

        cursor.execute(
            "INSERT INTO members (username, email, password, phone, birthdate) VALUES (?, ?, ?, ?, ?)",
            (username, email, password, phone, birthdate)
        )
        conn.commit()
        conn.close()

        return render_template('login.html')  # 註冊成功，導向登入頁

    # 如果是 GET 方法，就顯示註冊表單
    return render_template('register.html')

@app.route('/edit_profile')
#編輯個人資料
def edit_profile():
    return render_template('edit_profile.html')

@app.template_filter('add_stars')
def add_stars(s):
    return f'★{s}★'

init_db()

