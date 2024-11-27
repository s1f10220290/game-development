from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import subprocess
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import random
import json

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

@app.route('/stage1')
def start_stage1():
    # セッションから進行状況を取得
    current_question = session.get('current_question', 1)
    correct_answers = session.get('correct_answers', 0)
    answered_questions = session.get('answered_questions', [])

    # 10問終了した場合
    if current_question > 10:
        session.pop('answered_questions', None)
        return redirect(url_for('show_results'))

    # MongoDB からランダムに1つの問題を取得
    random_problem = questions_collection.aggregate([
        {"$match": {"id": {"$gte": 1, "$lte": 40}}},
        {"$match": {"id": {"$nin": answered_questions}}},
        {"$sample": {"size": 1}}
    ])
    problem = next(random_problem, None)

    if not problem:
        # 問題が見つからない場合
        session.pop('answered_questions', None)
        return redirect(url_for('start_stage1'))

    question_text = ""
    options = []
    feedback = []
    correct_answer_index = 0

    if problem:
        if 'question1' in problem:
            question_text += problem['question1'] + "<br>"
        if 'question2' in problem:
            question_text += problem['question2'] + "<br>"
        if 'question3' in problem:
            question_text += problem['question3'] + "<br>"
        if 'question4' in problem:
            question_text += problem['question4'] + "<br>"
        if 'question5' in problem:
            question_text += problem['question5'] + "<br>"

        if 'options' in problem:
            try:
                options = json.loads(problem['options'])
                feedback = [option['feedback'] for option in options if 'feedback' in option]
            except json.JSONDecodeError:
                print("optionsのデコードに失敗しました。データの形式を確認してください")

        if 'correct_answer' in problem:
            correct_answer_index = int(problem['correct_answer'])
        
        # 出題済みの問題IDをセッションに追加
        answered_questions.append(problem['id'])
        session['answered_questions'] = answered_questions

    # 取得した質問を stage1.html に渡す
    return render_template("stage1.html", question_text=question_text, options=options, feedback=feedback, correct_answer_index=correct_answer_index, current_question=current_question, correct_answers=correct_answers)

@app.route('/stage2')
def start_stage2():
    # セッションから進行状況を取得
    current_question = session.get('current_question', 1)
    correct_answers = session.get('correct_answers', 0)

    # 10問終了した場合
    if current_question > 10:
        return redirect(url_for('show_results'))

    # MongoDB からランダムに1つの問題を取得
    random_problem = questions_collection.aggregate([
        {"$match": {"id": {"$gte": 41, "$lte": 80}}},
        {"$sample": {"size": 1}}
    ])
    problem = next(random_problem, None)

    question_text = ""
    options = []
    correct_answer_index = 0

    if problem:
        if 'question1' in problem:
            question_text += problem['question1'] + "<br>"
        if 'question2' in problem:
            question_text += problem['question2'] + "<br>"
        if 'question3' in problem:
            question_text += problem['question3'] + "<br>"
        if 'question4' in problem:
            question_text += problem['question4'] + "<br>"
        if 'question5' in problem:
            question_text += problem['question5'] + "<br>"
        if 'question6' in problem:
            question_text += problem['question6'] + "<br>"

        if 'options' in problem:
            try:
                options = json.loads(problem['options'])
            except json.JSONDecodeError:
                print("optionsのデコードに失敗しました。データの形式を確認してください")

        if 'correct_answer' in problem:
            correct_answer_index = int(problem['correct_answer'])
    
    if not question_text:
        question_text = "問題が見つかりませんでした。"

    # 取得した質問を stage2.html に渡す
    return render_template("stage2.html", question_text=question_text, options=options, correct_answer_index=correct_answer_index, current_question=current_question, correct_answers=correct_answers)


@app.route('/selection')
def selection():
    return render_template('selection.html')

@app.route('/results')
def show_results():
    correct_answers = session.get('correct_answers', 0)
    total_questions = 10

    session.pop('current_question', None)
    session.pop('correct_answers', None)

    return render_template("results.html", correct_answers=correct_answers, total_questions=total_questions)   

if __name__ == '__main__':
    app.run(debug=True)
