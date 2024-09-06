from flask import Flask, render_template, request, redirect, url_for
import subprocess

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
    # game.pyを実行し、結果を取得
    output = start_game()
    return render_template('game.html', output=output)

def start_game():
    # game.pyを実行して、その出力をキャプチャ
    result = subprocess.check_output(['python', 'game.py'], universal_newlines=True)
    return result

if __name__ == '__main__':
    app.run(debug=True)