from flask import Flask, render_template, request, redirect, url_for
import json
import os
import subprocess

app = Flask(__name__)

# JSONファイルのパスを既存の 'user_data.json' に変更
USER_DATA_FILE = 'user_data.json'

# ユーザーデータをファイルから読み込む関数
def load_users_from_file():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

# ユーザーデータをファイルに保存する関数
def save_users_to_file(users):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file, indent=4)

# ユーザーデータの読み込み
users = load_users_from_file()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # ファイルから最新のユーザーデータを読み込む
        users = load_users_from_file()
        
        # ログイン処理：ユーザーが存在し、パスワードが一致するか確認
        if username in users and users[username] == password:
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="ログイン失敗。正しいユーザー名とパスワードを入力してください。")
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        
        # ユーザー名とパスワードが入力されているか確認
        if not new_username or not new_password:
            return render_template('register.html', error="すべてのフィールドを入力してください。")
        
        # 既に同じユーザー名が存在しないか確認
        if new_username in users:
            return render_template('register.html', error="そのユーザー名は既に使用されています。")
        
        # 新しいユーザーを登録し、ファイルに保存
        users[new_username] = new_password
        save_users_to_file(users)
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/start_game', methods=['POST'])
def start_game_route():
    # Pygameを別プロセスで非同期に実行
    start_game()
    return render_template('game_running.html')  # ゲームが起動した後に表示するページ

def start_game():
    # ゲームを別プロセスで実行
    try:
        if os.name == 'nt':  # Windows環境の場合
            subprocess.Popen(['python', 'game.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:  # Unix系環境の場合 (Linux, macOS)
            subprocess.Popen(['python3', 'game.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        print(f"ゲーム起動中にエラーが発生しました: {e}")

if __name__ == '__main__':
    app.run(debug=True)
