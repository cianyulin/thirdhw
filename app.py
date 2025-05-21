from flask import Flask, render_template, request
import logging

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

