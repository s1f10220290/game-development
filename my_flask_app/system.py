from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = "secret_key"  # セッション用

# ユーザーデータをロードする関数
def load_user_data():
    if os.path.exists("user_data.json"):
        with open("user_data.json", "r") as file:
            return json.load(file)
    return {}

# ファイルにユーザー情報を保存する関数
def save_user_data(username, password):
    user_data = load_user_data()
    if username in user_data:
        return False  # ユーザーが既に存在する場合
    user_data[username] = {"username": username, "password": password}
    with open("user_data.json", "w") as file:
        json.dump(user_data, file)
    return True  # 新規登録成功

@app.route('/')
def index():
    return render_template('register.html')

# ユーザー登録処理
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    
    if save_user_data(username, password):
        flash('新規登録が成功しました！')
        return redirect(url_for('index'))
    else:
        flash('ユーザー名が既に存在します。')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
