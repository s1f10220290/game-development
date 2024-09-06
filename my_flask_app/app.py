from flask import Flask, render_template, request, redirect, url_for
import subprocess
import os

app = Flask(__name__)

# ユーザー情報の保存用辞書
users = {"admin": "password"}  # 初期のユーザー情報

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.get(username) == password:
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="ログイン失敗")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        if new_username and new_password:
            users[new_username] = new_password
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
    if os.name == 'nt':  # Windows環境の場合
        subprocess.Popen(['python', 'game.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:  # Unix系環境の場合 (Linux, macOS)
        subprocess.Popen(['python3', 'game.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if __name__ == '__main__':
    app.run(debug=True)