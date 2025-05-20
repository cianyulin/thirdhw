from flask import Flask, render_template
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

@app.route('/register')
#註冊
def register():
    return render_template('register.html')

@app.route('/edit_profile')
#編輯個人資料
def edit_profile():
    return render_template('edit_profile.html')

