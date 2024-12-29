import pygame
import sys
import time
import pygetwindow as gw
import os
from bgmplayer import BgmPlayer
from load_picture import pictures

'''
player:
    font1(Font)             侧边栏字体(大)
    player_list([int])      玩家列表
    player_num(int)         玩家编号
    screen_image(Surface)   窗口
    images([Surface])       形象: [knight1, knight2, ...]
    side_player(Surface)    本角色侧边栏图片
    state(int)              状态: 1-up 2-down 3-left 4-right
    damage_value(int)             伤害
    full_hp(int)            最高血量
    hp(int)                 血量
    full_magic(int)         最高魔法值
    magic(int)              魔法值
    location([int,int])     位置
    last_time(int)          玩家上次移动毫秒值
    rect(Rect)              玩家矩形对象

    goto(direction, destination):
        direction(int)          朝向:   1-up 2-down 3-left 4-right
        destination([int,int])  目的地: list:[x,y]
    display():          打印当前角色及其侧边栏面板
    move(direction):    固定方向移动speed格(有边界校验)
        direction(int)          朝向:   1-up 2-down 3-left 4-right
    hp_set(new_hp):     设置血量(有上下限校验)
        new_hp(int)             新的血量
    damage(damage):     结算受到的伤害
        damage(int)     受到的伤害值(有上下限校验)
'''

class player:
    pygame.font.init()
    font1 = pygame.font.Font('Text\\xiangfont.ttf', 25)
    player_list = []

    def __init__(self, screenin: pygame.surface, imagesin: pygame.surface, side_player: pygame.surface, damage_value: int, full_hp: int, full_magic: int):
        self.player_list.append(len(self.player_list) + 1)
        self.player_num = self.player_list[-1]
        self.screen_image = screenin
        self.images = imagesin
        self.side_player = side_player
        self.damage_value = damage_value
        self.full_hp = full_hp
        self.hp = self.full_hp
        self.full_magic = full_magic
        self.magic = 100
        self.location = [350, 255] 
        self.state = 2
        self.last_time = pygame.time.get_ticks()
        self.rect = self.images[0].get_rect(center=self.location) 

    def goto(self, direction, destination=None):
        if destination is None:
            destination = self.location
        if destination[0] <= 750 and destination[0] >= 1 and destination[1] <= 510 and destination[1] >= 1:
            self.state = direction
            self.rect.center = destination 
            self.location = list(self.rect.center)

    def display(self):
        if self.player_num == 1:
            self.screen_image.blit(self.side_player, (750, 0))
            now_text = self.font1.render(str(self.hp), True, (255, 0, 0))
            self.screen_image.blit(now_text, (845, 32))
            now_text = self.font1.render(str(self.magic), True, (0, 0, 255))
            self.screen_image.blit(now_text, (845, 65))
        elif self.player_num == 2:
            self.screen_image.blit(self.side_player, (750, 115))
            now_text = self.font1.render(str(self.hp), True, (255, 0, 0))
            self.screen_image.blit(now_text, (845, 147))
            now_text = self.font1.render(str(self.magic), True, (0, 0, 255))
            self.screen_image.blit(now_text, (845, 180))
        self.screen_image.blit(self.images[self.state - 1], self.rect) 

    def move(self, direction):
        if pygame.time.get_ticks() - self.last_time >= 10:
            self.last_time = pygame.time.get_ticks()
            speed = 3
            if direction == 1 and self.rect.top >= 6: 
                self.rect.y -= speed
            elif direction == 2 and self.rect.bottom <= 510:  
                self.rect.y += speed
            elif direction == 3 and self.rect.left >= 6: 
                self.rect.x -= speed
            elif direction == 4 and self.rect.right <= 745:  
                self.rect.x += speed
            self.location = list(self.rect.center)  
            self.goto(direction)


    def hp_set(self, new_hp):
        if new_hp >= 0 and new_hp <= self.full_hp:
            self.hp = new_hp

    def damage(self, damage):
        if damage >= self.hp:
            self.hp = 0
        else:
            self.hp -= damage
            if self.hp > self.full_hp:
                self.hp = self.full_hp

'''
bullet:
    screen_image(Surface)       窗口
    image(Surface)              子弹形象
    is_show(Bool)               是否显示    0-隐藏 1-显示
    from_player(player)            伤害来源:   0-来源于非玩家 player1-来源于玩家1 player2-来源于玩家2
    damage(int)                 伤害:       +为伤害 -为治疗
    damage_range(float)         伤害半径
    speed([float, float])       速度:       x_speed(右) y_speed(下)
    last_time(int)              子弹上次移动毫秒值
    rect(Rect)                  子弹矩形对象

    display():          绘制子弹(如状态为显示)
    move():             向固定方向移动并绘制
    hit(target):        消除并造成伤害
        target(<player> or <enemy> or 0)    目标
'''
class bullet:
    def __init__(self, screenin: pygame.surface, imagein: pygame.surface, from_player: player, damage_range: float, b_location: list, speed: list):
        self.screen_image = screenin
        self.image = imagein
        self.is_show = 1
        self.from_player = from_player
        self.damage = from_player.damage_value
        self.damage_range = damage_range
        self.speed = speed
        self.last_time = pygame.time.get_ticks()
        self.rect = self.image.get_rect(center=b_location) 

    def display(self):
        if self.is_show:
            self.screen_image.blit(self.image, self.rect)
            pygame.display.flip()

    def move(self):
        if pygame.time.get_ticks() - self.last_time >= 10:
            self.last_time = pygame.time.get_ticks()
            self.rect.x += self.speed[0]
            self.rect.y += self.speed[1]
            self.display()

    def hit(self, target):
        if target != 0:
            target.damage(self.damage)
        self.is_show = 0

    def detect(self, locations: list):
        if self.rect.left < 0 or self.rect.top < 0 or self.rect.right > 750 or self.rect.bottom > 510:
            print('0010')
            self.hit(0)
            return -1
        else:
            for target in locations:
                if (target[0] - self.rect.centerx) ** 2 + (target[1] - self.rect.centery) ** 2 <= self.damage_range ** 2:
                    self.hit(target[2])
                    return -1
            return 0

def menu(screen_image:pygame.Surface):
    pygame.init()

    pic = pictures()

    player1 = player(screen_image, [pic.knight1, pic.knight2, pic.knight3, pic.knight4], pic.sideplayer1, 10, 114, 100)
    player1.goto(2)
    player2 = player(screen_image, [pic.knight1, pic.knight2, pic.knight3, pic.knight4], pic.sideplayer2, 10, 514, 100)
    player2.goto(2)
    bullets = []

    bgm = BgmPlayer()
    bgm.play('Soul_Soil.mp3', -1)

    def minimize_window():
        window = gw.getWindowsWithTitle('Soul Knight')[0]
        window.minimize()

    def playercheck(a_player:player, K_up, K_down, K_left, K_right, K_attack):
        if keypressed[K_up] and not keypressed[K_down]:
            a_player.move(1)
            flipper()
        if keypressed[K_down] and not keypressed[K_up]:
            a_player.move(2)
            flipper()
        if keypressed[K_left] and not keypressed[K_right]:
            a_player.move(3)
            flipper()
        if keypressed[K_right] and not keypressed[K_left]:
            a_player.move(4)
            flipper()

    def state_trans(state,speed):
        if state == 1:
            return [0,-speed]
        elif state == 2:
            return [0,speed]
        elif state == 3:
            return [-speed,0]
        else:
            return [speed,0]

    def flipper():
        screen_image.blit(pic.grass, (0,0))
        screen_image.blit(pic.sidebox, (750, 0))
        player1.display()
        player2.display()
        pygame.display.flip()
        for bullet_0 in bullets:
            bullet_0.move()

    flipper()

    clock = pygame.time.Clock()
    while True:
        bullets_to_remove = []
        for bullet_0 in bullets:
            bullet_0.move()
            if bullet_0.from_player == player1:
                result = bullet_0.detect([[player2.location[0], player2.location[1], player2]])
                if result == -1:
                    bullets_to_remove.append(bullet_0)
            elif bullet_0.from_player == player2:
                result = bullet_0.detect([[player1.location[0], player1.location[1], player1]])
                if result == -1:
                    bullets_to_remove.append(bullet_0)
        for bullet_0 in bullets_to_remove:
            if bullet_0 in bullets:
                bullets.remove(bullet_0)

                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    bgm.pause()
                    minimize_window()
                    os.startfile('Pictures\K_Boss.pdf')
                if event.key == pygame.K_p:
                    print(bullets)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_q and player1.magic >= 5:
                player1.magic -= 5
                bullets.append(bullet(screen_image, pic.bullet1, player1, 20, player1.location[:], state_trans(player1.state,4)))
                bullets[-1].display()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RCTRL and player2.magic >= 5:
                player2.magic -= 5
                bullets.append(bullet(screen_image, pic.bullet1, player2, 20, player2.location[:], state_trans(player2.state,4)))
                bullets[-1].display()

        if pygame.display.get_active():
            bgm.unpause()
        else:
            bgm.pause()

        keypressed = pygame.key.get_pressed()
        playercheck(player1, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_q)
        playercheck(player2, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_KP_DIVIDE)
        flipper()


if __name__ == '__main__':
    screen_image = pygame.display.set_mode((900, 560))
    pygame.display.set_caption('Soul Knight')
    menu(screen_image)