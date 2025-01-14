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

@app.route('/selection')
def selection():
    return render_template('selection.html')


def get_random_problem(stage_range, answered_questions):

    random_problem = questions_collection.aggregate([
        {"$match": {"id": {"$gte": stage_range[0], "$lte": stage_range[1]}}},
        {"$match": {"id": {"$nin": answered_questions}}},
        {"$sample": {"size": 1}}
    ])
    return next(random_problem, None)

def start_stage(stage, stage_range):
    """
    ステージの処理をまとめた関数
    """
    # セッションから進行状況を取得
    current_question = session.get('current_question', 1)
    correct_answers = session.get('correct_answers', 0)
    answered_questions = session.get('answered_questions', [])

    # 10問終了した場合
    if current_question > 10:
        session.pop('answered_questions', None)
        return redirect(url_for(f'show_stage{stage}_results'))

    # ランダムに問題を取得
    problem = get_random_problem(stage_range, answered_questions)

    if not problem:
        # 問題が見つからない場合
        session.pop('answered_questions', None)
        return redirect(url_for(f'start_stage{stage}'))
    
    question_text = ""
    options = []
    feedback = []
    correct_answer_index = 0

    if problem:
        for i in range(1, 7):
            question_key = f'question{i}'
            if question_key in problem:
                question_text += problem[question_key] + "<br>"

        if 'options' in problem:
            try:
                options = json.loads(problem['options'])
                feedback = [option['feedback'] for option in options if 'feedback' in option]
            except json.JSONDecodeError:
                print("optionsのデコードに失敗しました。データの形式を確認してください")

        if 'correct_answer' in problem:
            correct_answer_index = int(problem['correct_answer'])

        answered_questions.append(problem['id'])
        session['answered_questions'] = answered_questions

    # HTML にデータを渡す
    return render_template(f"stage{stage}.html", question_text=question_text, options=options, feedback=feedback, 
                           correct_answer_index=correct_answer_index, current_question=current_question, 
                           correct_answers=correct_answers)


@app.route('/stage1')
def start_stage1():
    return start_stage(1, (1, 40))

@app.route('/stage2')
def start_stage2():
    return start_stage(2, (41, 100))

@app.route('/stage3')
def start_stage3():
    return start_stage(3, (101, 139))

@app.route('/stage4')
def start_stage4():
    return start_stage(4, (140, 167))

@app.route('/stage5')
def start_stage5():
    return start_stage(5, (140, 167))

@app.route('/stage6')
def start_stage6():
    return start_stage(6, (140, 167))



@app.route('/stage1story')
def stage1story():
    return render_template('stage1story.html')

@app.route('/stage2story')
def stage2story():
    return render_template('stage2story.html')

@app.route('/stage3story')
def stage3story():
    return render_template('stage3story.html')

@app.route('/stage4story')
def stage4story():
    return render_template('stage4story.html')

@app.route('/stage5story')
def stage5story():
    return render_template('stage5story.html')

@app.route('/stage6story')
def stage6story():
    return render_template('stage6story.html')



@app.route('/stage1_results')
def show_stage1_results():
    correct_answers = session.get('correct_answers', 0)
    total_questions = 10

    session.pop('current_question', None)
    session.pop('correct_answers', None)

    return render_template("stage1_results.html", correct_answers=correct_answers, total_questions=total_questions)

@app.route("/stage2_results")
def show_stage2_results():
    correct_answers = session.get('correct_answers', 0)
    total_questions = 10

    session.pop('current_question', None)
    session.pop('correct_answers', None)

    return render_template("stage2_results.html", correct_answers=correct_answers, total_questions=total_questions)

@app.route("/stage3_results")
def show_stage3_results():
    correct_answers = session.get('correct_answers', 0)
    total_questions = 10

    session.pop('current_question', None)
    session.pop('correct_answers', None)

    return render_template("stage3_results.html", correct_answers=correct_answers, total_questions=total_questions)

@app.route("/stage4_results")
def show_stage4_results():
    correct_answers = session.get('correct_answers', 0)
    total_questions = 10

    session.pop('current_question', None)
    session.pop('correct_answers', None)

    return render_template("stage4_results.html", correct_answers=correct_answers, total_questions=total_questions)

@app.route("/stage5_results")
def show_stage5_results():
    correct_answers = session.get('correct_answers', 0)
    total_questions = 10

    session.pop('current_question', None)
    session.pop('correct_answers', None)

    return render_template("stage5_results.html", correct_answers=correct_answers, total_questions=total_questions)

@app.route("/stage6_results")
def show_stage6_results():
    correct_answers = session.get('correct_answers', 0)
    total_questions = 10

    session.pop('current_question', None)
    session.pop('correct_answers', None)

    return render_template("stage6_results.html", correct_answers=correct_answers, total_questions=total_questions)


if __name__ == '__main__':
    app.run(debug=True)