import pygame
import sys
import json
import os

# 画面サイズの設定
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# 色の設定
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ユーザーデータをロードする関数
def load_user_data():
    if os.path.exists("user_data.json"):
        with open("user_data.json", "r") as file:
            return json.load(file)
    return {}

# ファイルにユーザー情報を保存する関数
def save_user_data(username, password):
    # 既存のデータをロード
    user_data = load_user_data()

    # 新しいユーザー情報を追加
    user_data[username] = {
        "username": username,
        "password": password
    }

    # 更新されたデータを保存
    with open("user_data.json", "w") as file:
        json.dump(user_data, file)

# ログイン機能
def login_user(username, password):
    user_data = load_user_data()

    if username in user_data and user_data[username]['password'] == password:
        return True  # ログイン成功
    return False  # ログイン失敗

# メインのゲーム関数
def main():
    pygame.init()
    pygame.display.set_caption("ユーザー登録とログイン")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None, 32)

    # 入力ボックスの初期設定
    input_box = pygame.Rect(100, 100, 140, 32)  # ユーザー名入力ボックス
    password_box = pygame.Rect(100, 200, 140, 32)  # パスワード入力ボックス
    color_inactive = pygame.Color('lightskyblue3')  # 非アクティブ時の色
    color_active = pygame.Color('dodgerblue2')      # アクティブ時の色

    username_active = False
    password_active = False
    username = ''
    password = ''
    color = color_inactive

    message = ''

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # ユーザー名入力ボックスのクリック判定
                if input_box.collidepoint(event.pos):
                    username_active = not username_active
                else:
                    username_active = False

                # パスワード入力ボックスのクリック判定
                if password_box.collidepoint(event.pos):
                    password_active = not password_active
                else:
                    password_active = False

                color = color_active if username_active or password_active else color_inactive

            if event.type == pygame.KEYDOWN:
                if username_active:
                    if event.key == pygame.K_RETURN:
                        print("ユーザー名:", username)
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode

                if password_active:
                    if event.key == pygame.K_RETURN:
                        # ユーザー登録またはログイン処理
                        if login_user(username, password):
                            message = "ログイン成功!"
                        else:
                            save_user_data(username, password)
                            message = "新規登録成功!"
                    elif event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode

        screen.fill(WHITE)

        # ユーザー名の入力ボックス描画
        txt_surface = font.render(username, True, BLACK)
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        # パスワードの入力ボックス描画
        password_surface = font.render('*' * len(password), True, BLACK)
        screen.blit(password_surface, (password_box.x+5, password_box.y+5))
        pygame.draw.rect(screen, color, password_box, 2)

        # メッセージ表示（ログイン成功や新規登録成功）
        message_surface = font.render(message, True, BLACK)
        screen.blit(message_surface, (100, 300))

        pygame.display.flip()

if __name__ == '__main__':
    main()
