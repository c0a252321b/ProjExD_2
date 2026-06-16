import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, +5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(+5, 0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#練習３
#               引数はpygameのRectクラス   戻り値はbool型を要素に持つタプル
def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんrct or 爆弾rct
    戻り値：
    """
    yoko, tate =True, True
    #True：はみ出てない,False：はみ出てる
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False

    return yoko, tate

def main():
    #こうかとん初期化
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0
    #練習２：爆弾初期化 28~35
    bb_img = pg.Surface((20, 20)) #空のSurface作成。20×20のキャンバス
    pg.draw.circle( bb_img,(255, 0, 0), (10, 10), 10)
    bb_rct = kk_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT) #rectの中心座標を乱数で生成。タプル。
    # bb_rct.centerx = random.randint(0, WIDTH)
    # bb_rct.centery = random.randint(0, HEIGHT) #横座標と縦座標を別々に指定もできる
    bb_img.set_colorkey((0, 0, 0))
    vx, vy = +5, +5#移動速度設定
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: #pg.QUIT：×ボタン
                return
        if kk_rct.colliderect(bb_rct):#kk_rctがbb_rctと重なったら
            print("ゲームオーバー")
            return #main関数から抜ける
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key, mv in DELTA.items():#練習１辞書をfor文で回す
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):#練習３True, Trueでなかったら＝はみ出てたら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
            #動く予定の距離分マイナスして無かったことにする

        bb_rct.move_ip(vx, vy)#練習２：移動させる
        yoko, tate = check_bound(bb_rct)#練習３
        if not yoko:
            vx *= -1 #マイナス1掛けて反転
        if not tate:
            vy *= -1
            

        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)#練習２：描画
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
