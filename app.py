from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3
import re

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

# Helper function to validate date format
def is_valid_date(date_str):
    return re.match(r'^\d{4}-\d{2}-\d{2}$', date_str) is not None

@app.route('/')
#首頁
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
#登入
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # 查詢資料庫
        conn = sqlite3.connect('membership.db')
        cursor = conn.cursor()
        cursor.execute("SELECT iid, username FROM members WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        conn.close()

        # 檢查帳密是否正確
        if user:
            iid = user[0]  # 使用者 ID
            username = user[1]  # 使用者名稱
            return render_template('welcome.html', user_name=username, iid=iid)
        else:
            return render_template('error.html', error="電子郵件或密碼錯誤")

    # GET 方法時顯示登入頁面
    return render_template('login.html')


@app.route('/welcome', methods=['GET', 'POST'])
#歡迎頁面
def welcome():
    if request.method == 'POST':
        # Logic to handle POST request (e.g., retrieve user data)
        user_name = request.form.get('email', 'Guest')  # Example: retrieve email as username
        return render_template('welcome.html', user_name=user_name)
    return render_template('welcome.html')

@app.route('/register', methods=['GET', 'POST'])
#註冊
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

        # Optional validation for date format
        if birthdate and not is_valid_date(birthdate):
            return render_template('error.html', error="出生年月日格式不正確，請使用 YYYY-MM-DD 格式")

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

@app.route('/edit_profile/<int:iid>', methods=['GET', 'POST'])
def edit_profile(iid):
    conn = sqlite3.connect('membership.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        birthdate = request.form.get('dob')

        # Optional validation for date format
        if birthdate and not is_valid_date(birthdate):
            conn.close()
            return render_template('error.html', error="出生年月日格式不正確，請使用 YYYY-MM-DD 格式")

        # 檢查欄位是否為空
        if not email or not password:
            conn.close()
            return render_template('error.html', error="請輸入電子郵件和密碼")

        # 電子郵件是否已被其他使用者使用（不包括自己）
        cursor.execute("SELECT * FROM members WHERE email = ? AND iid != ?", (email, iid))
        if cursor.fetchone():
            conn.close()
            return render_template('error.html', error="電子郵件已被使用")

        # 更新資料
        cursor.execute("""
            UPDATE members
            SET email = ?, password = ?, phone = ?, birthdate = ?
            WHERE iid = ?
        """, (email, password, phone, birthdate, iid))
        conn.commit()

        # 再次抓 username 傳回 welcome 頁
        cursor.execute("SELECT username FROM members WHERE iid = ?", (iid,))
        user = cursor.fetchone()
        conn.close()

        if user:
            return render_template('welcome.html', user_name=user[0], iid=iid)
        else:
            return render_template('error.html', error="找不到使用者")

    # GET 方法：只抓 username 顯示在表單（其他不預填）
    cursor.execute("SELECT username FROM members WHERE iid = ?", (iid,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return render_template('error.html', error="用戶不存在")

    return render_template('edit_profile.html', user={
        'username': user[0]
    }, iid=iid)

@app.route('/delete/<int:iid>', methods=['GET'])
def delete_user(iid):
    conn = sqlite3.connect('membership.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM members WHERE iid = ?", (iid,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.template_filter('add_stars')
def add_stars(s):
    return f'★{s}★'

init_db()

