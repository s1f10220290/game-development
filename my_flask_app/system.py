import pygame
import sys
import json

# 画面サイズの設定
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# 色の設定
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ファイルにユーザー情報を保存する関数
def save_user_data(username, password):
    user_data = {"username": username, "password": password}
    with open("user_data.json", "w") as file:
        json.dump(user_data, file)

# メインのゲーム関数
def main():
    pygame.init()
    pygame.display.set_caption("ユーザー登録")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None, 32)

    input_box = pygame.Rect(100, 100, 140, 32)  # 入力ボックスの位置とサイズ
    color_inactive = pygame.Color('lightskyblue3')  # 非アクティブ状態の色
    color_active = pygame.Color('dodgerblue2')      # アクティブ状態の色
    color = color_inactive
    active = False
    text = ''
    
    # パスワード入力ボックス
    password_box = pygame.Rect(100, 200, 140, 32)
    password_active = False
    password = ''

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # ユーザー名入力ボックスのクリック判定
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                
                # パスワード入力ボックスのクリック判定
                if password_box.collidepoint(event.pos):
                    password_active = not password_active
                else:
                    password_active = False

                color = color_active if active else color_inactive

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print("ユーザー名:", text)
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

                if password_active:
                    if event.key == pygame.K_RETURN:
                        save_user_data(text, password)
                        print("パスワード:", password)
                    elif event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode

        screen.fill(WHITE)
        
        # ユーザー名の入力ボックス描画
        txt_surface = font.render(text, True, BLACK)
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        # パスワードの入力ボックス描画
        password_surface = font.render('*' * len(password), True, BLACK)
        screen.blit(password_surface, (password_box.x+5, password_box.y+5))
        pygame.draw.rect(screen, color, password_box, 2)

        pygame.display.flip()

if __name__ == '__main__':
    main()
