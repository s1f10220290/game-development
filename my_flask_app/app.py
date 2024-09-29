from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
import subprocess
from pymongo import MongoClient


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # セッション管理のためのシークレットキー

# MongoDBの設定
MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'user_database'
USER_COLLECTION = 'users'

# ユーザーデータをMongoDBから読み込む
def load_users_from_db():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    users_collection = db[USER_COLLECTION]
    
    users = {}
    for user in users_collection.find():
        users[user['username']] = user['password']  # パスワードは平文で保存されている前提
    return users

# ユーザーをMongoDBに保存
def save_user_to_db(username, password):
    client = MongoClient(MONGO_URI) # MongoDBに接続
    db = client[DB_NAME]
    users_collection = db[USER_COLLECTION]
    
    # ユーザー情報追加
    users_collection.insert_one({'username': username, 'password': password})



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        
        # ユーザー名とパスワードが入力されているか確認
        if not new_username or not new_password:
            return render_template('register.html', error="すべてのフィールドを入力してください。")
        
        users = load_users_from_db()

        # 既に同じユーザー名が存在しないか確認
        if new_username in users:
            return render_template('register.html', error="そのユーザー名は既に使用されています。")
        
        # 新しいユーザーを登録し、MongoDBに保存
        save_user_to_db(new_username, new_password)  # MongoDBに保存
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # DBから最新のユーザーデータを読み込む
        users = load_users_from_db()
        
        # ログイン処理
        if username in users and users[username] == password:
            session['username'] = username  # セッションにユーザー名を保存
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="ログイン失敗。正しいユーザー名とパスワードを入力してください。")
    
    return render_template('login.html')




@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' in session:
        username = session['username']  # 現在ログインしているユーザー名を取得
        return render_template('home.html', username=username)
    else:
        return redirect(url_for('login'))  # ログインしていない場合はログインページにリダイレクト


@app.route('/start_game', methods=['POST'])
def start_game_route():
    if 'username' in session:
        username = session['username']  # 現在ログインしているユーザー名を取得
        start_game(username)  # ユーザー名を渡してゲームを開始
        return render_template('game_running.html', username=username)  # ゲームが起動した後にリダイレクト
    else:
        return redirect(url_for('login'))  # ログインしていない場合はログインページにリダイレクト

def start_game(username):
    try:
        if os.name == 'nt':  # Windows環境の場合
            subprocess.Popen(['python', 'game.py', username], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:  # Unix系環境の場合 (Linux, macOS)
            subprocess.Popen(['python3', 'game.py', username], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        print(f"ゲーム起動中にエラーが発生しました: {e}")

@app.route('/logout')
def logout():
    session.pop('username', None)  # セッションからユーザー名を削除
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
