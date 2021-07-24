import pygame, sys
from peashooter import *
from sunflower import *
from sun import *
from zone import *
from zombie import *

pygame.init()
screen_size = (1200, 600)
screen = pygame.display.set_mode(screen_size)
# 图标
pygame.display.set_caption('pvz')
icon = pygame.image.load('images/icon.ico')
pygame.display.set_icon(icon)
# 背景
backgroup = pygame.image.load('images/Background.jpg').convert()
# 卡槽
card_slot = pygame.image.load('images/cardSlot.png').convert()
# 暂停
pause_draw = pygame.image.load('images/pause.png').convert_alpha()
# 赢
win_draw = pygame.image.load('images/win.jpg').convert_alpha()
# 输
eat_draw = pygame.image.load('images/eat.jpg').convert_alpha()
# card
card = pygame.image.load('images/cards/card_peashooter.png').convert()
card1 = pygame.image.load('images/cards/card_sunflower.png').convert()
card_rect = card.get_rect()
card1_rect = card1.get_rect()
win_rect = win_draw.get_rect()
scale = 0.79
# 更改比例
card = pygame.transform.scale(card, (int(card_rect.width * scale), int(card_rect.height * scale)))
card1 = pygame.transform.scale(card1, (int(card1_rect.width * scale), int(card1_rect.height * scale)))
win_draw = pygame.transform.scale(win_draw, (int(win_rect.width * 0.55), int(win_rect.height * 0.55)))
# 阳光数
sunnum = '50'
font = pygame.font.SysFont('arial', 20)
fontImg = font.render(sunnum, True, (0, 0, 0))
# 出怪频率
tmp = 450
gameover = 'Thanks for serching bugs!'
font1 = pygame.font.SysFont('Arial', 80)
fontImg1 = font1.render(gameover, True, (255, 0, 0))

# 主函数
def main():
    global sunnum,font,fontImg,tmp,font1,fontImg1
    block = pygame.time.Clock()
    clickimage = []
    peaList = []
    sunFlowerList = []
    zombieList=[]
    zombie=Zombie()
    zombieList.append(zombie)
    #僵尸的敌人
    enemy_zombie_list=[]
    #花朵产生的太阳列表
    flower_product_list=[]

    sunList=[]
    index = 0
    # 是否点击了卡片
    is_pick = False
    pick_type = None
    #区域是否种植了植物
    is_plant=False
    #太阳下落的时间
    SUN_EVENT=pygame.USEREVENT+1
    #pygame.time.set_timer(SUN_EVENT,8000)

    z=Zone()
    bulletList=[]
    PAUSED = 0

    pygame.mixer.init()
    pygame.mixer.music.load('Nyan Cat.ogg')
    pygame.mixer.music.play(-1, 2)
    

    while 1:
        if index % 300 == 0:
            sun_event = pygame.event.Event(SUN_EVENT, {"message": "事件触发"})
            pygame.event.post(sun_event)
        block.tick(17)
        press = pygame.mouse.get_pressed()
        # 判断事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type==SUN_EVENT:
                sun=Sun()
                sunList.append(sun)
                
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    if PAUSED == 0:
                        PAUSED = 1
                    elif PAUSED == 1:
                        PAUSED = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if not is_pick:
                    if 330 <= x <= 330 + card.get_rect().width and 10 <= y <= 10 + card.get_rect().height and int(sunnum) >= 100:
                        clickimage.append(Peashooter())
                        pick_type = 'pea'
                        is_pick = True

                    if 400 <= x <= 400 + card1.get_rect().width and 10 <= y <= 10 + card1.get_rect().height and int(sunnum) >= 50:
                        clickimage.append(SunFlower())
                        pick_type = 'flower'
                        is_pick = True
                else :
                    if 330 <= x <= 330 + card.get_rect().width and 10 <= y <= 10 + card.get_rect().height:
                        clickimage = []
                        is_pick = False
                    if 400 <= x <= 400 + card1.get_rect().width and 10 <= y <= 10 + card1.get_rect().height:
                        clickimage = []
                        is_pick = False
                    if z.is_plant_zone(x,y):
                        if z.getIndex(x,y) and not is_plant:
                            a,b=z.getIndex(x,y)
                            if pick_type == 'pea' and z.plantInfo[b][a]==0:
                                p = Peashooter()
                                p.zone=z.getGridPos(a,b)
                                sunnum = str(int(sunnum) - 100)
                                fontImg = font.render(sunnum, True, (0, 0, 0))
                                is_plant=True
                                peaList.append(p)
                                enemy_zombie_list.append(p)
                                clickimage.clear()
                                is_pick = False
                                z.plantInfo[b][a]=1

                            elif pick_type == 'flower'and z.plantInfo[b][a]==0:
                                f = SunFlower()
                                f.zone = z.getGridPos(a, b)
                                sunnum = str(int(sunnum) - 50)
                                fontImg = font.render(sunnum, True, (0, 0, 0))
                                is_plant = True
                                sunFlowerList.append(f)
                                enemy_zombie_list.append(f)
                                clickimage.clear()
                                is_pick = False
                                z.plantInfo[b][a] = 1
                        else:
                            is_plant=False

            # 收集太阳
            if event.type == pygame.MOUSEMOTION:
                x,y = pygame.mouse.get_pos()
                for sun in sunList:
                    if sun.rect.collidepoint((x,y)):
                        sunList.remove(sun)
                        sunnum=str(int(sunnum)+25)
                        fontImg = font.render(sunnum, True, (0, 0, 0))
                for sun in flower_product_list:
                    if sun.rect.collidepoint((x, y)):
                        flower_product_list.remove(sun)
                        sunnum = str(int(sunnum) + 25)
                        fontImg = font.render(sunnum, True, (0, 0, 0))

        if PAUSED == 0:
            screen.blit(backgroup, (0, 0))# 绘制背景
            screen.blit(card_slot, (250, 0))# 卡槽
            screen.blit(card, (330, 10))# card
            screen.blit(card1, (400, 10))
            screen.blit(fontImg, (280, 60))# sunnum
            
            # 鼠标拿起的植物
            for image in clickimage:
                screen.blit(image.images[0], (x - 30, y - 50))

            for pea in peaList:
                if pea.isLive:
                    if index%25==1:
                        bullet = pea.shot()
                        bulletList.append(bullet)
                    screen.blit(pea.images[index % 13], pea.zone)
                else:
                    z.plantInfo[b][a]=0
                    peaList.remove(pea)
                    enemy_zombie_list.remove(pea)
            
            #太阳花
            for sunFlower in sunFlowerList:
                if sunFlower.isLive:
                    screen.blit(sunFlower.images[index % 18], sunFlower.zone)
                    sunFlower.product_sun_rate+=1
                    if sunFlower.product_sun_rate==100:
                        sunFlower.productSun(flower_product_list)
                        sunFlower.product_sun_rate=0
                else:
                    z.plantInfo[b][a]=0
                    sunFlowerList.remove(sunFlower)
                    enemy_zombie_list.remove(sunFlower)
            for sun in sunList:
                screen.blit(sun.images[index % 22], sun.rect)
                if sun.rect.top<=480:
                    sun.down()
            
            #花朵生的太阳
            for sun in flower_product_list:
                screen.blit(sun.images[index % 22], sun.rect)

            for bullet in bulletList:
                if bullet.status:
                    screen.blit(bullet.image,bullet.rect)
                    bullet.move()
                    bullet.hit(zombieList)
                else:
                    bulletList.remove(bullet)

            #僵尸
            for zombie in zombieList:
                if zombie.rect[0] < 100:
                    PAUSED = 2
                if zombie.islive:
                    zombie.changimage()
                    screen.blit(zombie.images[index % 21], zombie.rect)
                    zombie.move()
                    zombie.attack(enemy_zombie_list)
                else:
                    zombieList.remove(zombie)
            index += 1

        if index % tmp == 0:
            zombieList.append(Zombie())
            tmp *= 0.7

        if len(zombieList) == 0:
            PAUSED = 3

        if PAUSED == 1:
            screen.blit(pause_draw,(500,130))
        elif PAUSED == 2:
            screen.blit(eat_draw,(350, 130))
        elif PAUSED == 3:
            screen.blit(win_draw, (350, 130))
            screen.blit(fontImg1, (280, 250))

        print('zombielist', len(zombieList))
        print('bulletList', len(bulletList))
        print('sunList', len(sunList))
        print('sunFlowerList', len(sunFlowerList))
        print('peaList', len(peaList))
        print('flower_product_list',len(flower_product_list))
        print('tmp',tmp)
        for i in z.plantInfo:
            print(i)

        pygame.display.update()


if __name__ == '__main__':
    main()
