import pygame
import sys

def main():
    pygame.init()
    pygame.display.set_caption("スパイミッションゲーム")
    screen = pygame.display.set_mode((640, 360))
    clock = pygame.time.Clock()
    img_bg = pygame.image.load("bg1.jpeg") #背景画像の読み込み
    img_chara = [
        pygame.image.load("chara1.jpeg"),
        pygame.image.load("chara2.jpeg")
    ]
    tmr = 0

    while True:
        tmr = tmr + 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  #キーを押すイベントが発生した時
                if event.key == pygame.K_F1: #F1キーなら
                    screen = pygame.display.set_mode((640,360),pygame.FULLSCREEN) #フルスクリーンにする
                if event.key == pygame.K_F2 or event.key == pygame.K_ESCAPE:
                    screen = pygame.display.set_mode((640,360))

        x = tmr%160
        for i in range(5):
            screen.blit(img_bg, [i+160-x, 0])
        screen.blit(img_chara[tmr%2], [224, 160])
        pygame.display.update()
        clock.tick(5)

if __name__ == '__main__':
    main()