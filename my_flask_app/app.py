from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import subprocess
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # セッション管理のためのシークレットキー

# MongoDB Atlasの接続URIを設定
app.config['MONGO_URI'] = 'mongodb+srv://s1f102201762:seomi263@teamproject.bq9kb.mongodb.net/?retryWrites=true&w=majority&appName=teamproject'

# MongoDBクライアントを作成
client = MongoClient(app.config['MONGO_URI'])
db = client['user_database']  # 使用するデータベース名
questions_collection = db['questions']

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # ユーザー名が既に存在するか確認
        existing_user = db.users.find_one({'username': username})
        if existing_user:
            return jsonify({"message": "ユーザー名はすでに存在します。"}), 400

        # パスワードをハッシュ化
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # ユーザー情報をデータベースに保存
        result = db.users.insert_one({'username': username, 'password': hashed_password})
        
        if result.inserted_id:
            return redirect(url_for('login'))  # ログインページにリダイレクト
        return jsonify({"message": "User registration failed."}), 400
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # データベースからユーザーを取得
        user = db.users.find_one({'username': username})
        
        # ユーザーが存在するか確認
        if user and bcrypt.check_password_hash(user['password'], password):
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

@app.route('/stage1')
def stage1():
    # MongoDB からランダムに1つの問題を取得
    random_problem = questions_collection.aggregate([{"$sample": {"size": 1}}])
    
    # 取得した問題文を変数に格納
    problem = next(random_problem, None)  # None をデフォルトに設定して安全に取得
    question_text = problem["question"] if problem else "問題が見つかりませんでした。"
    
    # テンプレートに問題文を渡す
    return render_template('stage1.html', question_text=question_text)