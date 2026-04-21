import random
import os
import sys
import pygame as pg

WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

""""
画面の範囲の判定
引数    :コウカトンのRect or 爆弾Rect
戻り値:X,Y,XYの判定結果(Ture:画面内,falise:画面内)
""" 
def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    black = pg.Surface((WIDTH, HEIGHT))
    black.fill((0, 0, 0))
    black.set_alpha(200)

    font = pg.font.Font(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))

    kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    left = kk_img.get_rect(center=(WIDTH//2 - 200, HEIGHT//2))
    right = kk_img.get_rect(center=(WIDTH//2 + 200, HEIGHT//2))

    screen.blit(black, (0, 0))
    screen.blit(kk_img, left)
    screen.blit(kk_img, right)
    screen.blit(text, text_rect)

    pg.display.update()
    pg.time.delay(5000)


def init_bb_imgs():
    bb_imgs = []
    for r in range(1, 11):
        img = pg.Surface((20*r, 20*r))
        pg.draw.circle(img, (255, 0, 0), (10*r, 10*r), 10*r)
        img.set_colorkey((0, 0, 0))
        bb_imgs.append(img)
    bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs


def get_kk_imgs():
    org = pg.image.load("fig/3.png")
    imgs = {
        (0, 0): pg.transform.rotozoom(org, 0, 0.9),
        (5, 0): pg.transform.rotozoom(org, 0, 0.9),
        (-5, 0): pg.transform.rotozoom(org, 180, 0.9),
        (0, -5): pg.transform.rotozoom(org, 90, 0.9),
        (0, 5): pg.transform.rotozoom(org, -90, 0.9),
    }
    return imgs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")

    kk_imgs = get_kk_imgs()
    kk_img = kk_imgs[(0, 0)]
    kk_rct = kk_img.get_rect(center=(300, 200))

    clock = pg.time.Clock()
    tmr = 0

    bb_imgs, bb_accs = init_bb_imgs()
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect(center=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
    vx, vy = 5, 5

    DELTA = {
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, 5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (5, 0)
    }

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        screen.blit(bg_img, (0, 0))

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        old = kk_rct.copy()
        kk_rct.move_ip(sum_mv[0], sum_mv[1])

        if check_bound(kk_rct) != (True, True):
            kk_rct = old

        if tuple(sum_mv) in kk_imgs:
            kk_img = kk_imgs[tuple(sum_mv)]

        screen.blit(kk_img, kk_rct)

        idx = min(tmr // 500, 9)
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]
        bb_img = bb_imgs[idx]

        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height

        bb_rct.move_ip(avx, avy)

        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        screen.blit(bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()