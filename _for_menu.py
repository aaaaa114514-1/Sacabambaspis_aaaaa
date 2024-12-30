import pygame
import sys
import time
import pygetwindow as gw
import os
from bgmplayer import BgmPlayer
from load_picture import pictures



'''
wall_bgp:
    screen_image(Surface):  窗口
    bgp(Surface):           背景图
    bgp_rect(Rect):         背景图矩形
    walled_bgp(Surface):    已绘制墙体的背景图
    wall_images([Surface]): 墙体图片列表
    wall_map([[]]):         地图(0-地面 >0-墙体)

    build_map():                    将墙体按照地图绘制在walled_bgp上
    can_move(direction): -> bool    判定移动后图片是否出界
        direction([int,int]):           移动方向向量
    move(direction):                移动背景图和所有墙体(带边缘判定)
        direction([int,int]):           移动方向向量
    display():                      将walled_bgp绘制在屏幕上
'''
class wall_bgp:
    def __init__(self, screen_image:pygame.Surface, bgp:pygame.Surface, wall_images:list[pygame.Surface], wallmap=None):
        self.screen_image = screen_image
        self.bgp = bgp
        self.bgp_rect = bgp.get_rect()
        if wallmap == None:
            wallmap = []
        self.wallmap = wallmap
        self.wall_images = wall_images
        self.walled_bgp = self.bgp.copy()
        self.build_map()
        
    def build_map(self):
        for i in range(len(self.wallmap)):
            for j in range(len(self.wallmap[i])):
                if self.wallmap[i][j]:
                    self.walled_bgp.blit(self.wall_images[self.wallmap[i][j]-1], (50*j, 50*i))
            
    def can_move(self, direction:list):
        if self.bgp_rect.left + direction[0] <= 0 and self.bgp_rect.right + direction[0] >= 750 and self.bgp_rect.top + direction[1] <= 0 and self.bgp_rect.bottom + direction[1] >= 560:
            return 1
        else:
            return 0

    def move(self, direction):
        if self.bgp_rect.left + direction[0] <= 0 and self.bgp_rect.right + direction[0] >= 750:
            self.bgp_rect.x += direction[0]
        if self.bgp_rect.top + direction[1] <= 0 and self.bgp_rect.bottom + direction[1] >= 560:
            self.bgp_rect.y += direction[1]
        self.display()

    def display(self):
        self.screen_image.blit(self.walled_bgp, self.bgp_rect.topleft)




'''
player:
    font1(Font)             侧边栏字体(大)
    player_list([int])      玩家列表
    player_num(int)         玩家编号
    screen_image(Surface)   窗口
    images([[Surface],...]) 形象: [[knight1_1, knight1_2, ...],[knight2_1, knight2_2, ...]]
    side_player(Surface)    本角色侧边栏图片
    state(int)              状态: 1-up 2-down 3-left 4-right
    damage_value(int)       伤害
    full_hp(int)            最高血量
    hp(int)                 血量
    full_magic(int)         最高魔法值
    magic(int)              魔法值
    last_time(int)          玩家上次移动毫秒值
    pace_time(int)          玩家上次更新帧的毫秒值
    image_num(int)          上次形象编号
    rect(Rect)              玩家矩形对象
    wallmap([[]])           地图
    is_alive(bool)          存活状态: 1-alive 0-dead

    goto(direction, destination):   前往固定地点,设置确定朝向(无检验)
        direction(int)                  朝向:   1-up 2-down 3-left 4-right
        destination([int,int])          目的地: list:[x,y]
    can_goto(direction):            检验是否能够前往目标地点(边界检验和墙体检验)
    display():                      打印当前角色及其侧边栏面板
    move(direction):                固定方向移动speed格(有边界校验)
        direction(int)                  朝向:   1-up 2-down 3-left 4-right
    hp_set(new_hp):                 设置血量(有上下限校验)
        new_hp(int)                     新的血量
    damage(damage):                 结算受到的伤害
        damage(int)                     受到的伤害值(有上下限校验)
    is_dying():                     检验是否死亡
'''

class player:
    pygame.font.init()
    font1 = pygame.font.Font('Text\\xiangfont.ttf', 25)
    player_list = []

    def __init__(self, screenin: pygame.Surface, wallmap, imagesin: list[list[pygame.Surface]], side_player: pygame.Surface, damage_value: int, full_hp: int, full_magic: int, speed:int):
        self.player_list.append(len(self.player_list) + 1)
        self.player_num = self.player_list[-1]
        self.screen_image = screenin
        self.images = imagesin
        self.side_player = side_player
        self.damage_value = damage_value
        self.full_hp = full_hp
        self.hp = self.full_hp
        self.full_magic = full_magic
        self.magic = self.full_magic
        self.speed = speed
        self.state = 2
        self.last_time = pygame.time.get_ticks()
        self.pace_time = pygame.time.get_ticks()
        self.image_num = 0
        self.rect = self.images[0][0].get_rect(center=[20+30*self.player_num, 500])
        self.wallmap = wallmap
        self.is_alive = 1

    def goto(self, direction, destination=None):
        if destination is None:
            destination = [self.rect.x, self.rect.y]
        self.state = direction
        self.rect.center = destination 

    def can_goto(self, direction:int):
        new_rect = self.rect.copy()
        if direction == 1:
            new_rect.y -= 3
        elif direction == 2:
            new_rect.y += 3
        elif direction == 3:
            new_rect.x -= 3
        elif direction == 4:
            new_rect.x += 3

        top_left = (new_rect.left, new_rect.top)
        top_right = (new_rect.right, new_rect.top)
        bottom_left = (new_rect.left, new_rect.bottom)
        bottom_right = (new_rect.right, new_rect.bottom)

        if new_rect.left <= 0 or new_rect.right >= 750 or new_rect.top < 0 or new_rect.bottom > 560:
            return False

        for corner in [top_left, top_right, bottom_left, bottom_right]:
            try:
                if self.wallmap[(corner[1]) // 50][(corner[0]) // 50] != 0:
                    return False
            except IndexError:
                return True
        return True


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
        self.screen_image.blit(self.images[self.state - 1][self.image_num], self.rect)


    def move(self, direction):
        if pygame.time.get_ticks() - self.last_time >= 10:
            self.last_time = pygame.time.get_ticks()
            self.state = direction
            if direction == 1 and self.rect.top >= 1 and self.can_goto(1): 
                self.rect.y -= self.speed
            elif direction == 2 and self.rect.bottom <= 560 and self.can_goto(2):  
                self.rect.y += self.speed
            elif direction == 3 and self.rect.left >= 1 and self.can_goto(3): 
                self.rect.x -= self.speed
            elif direction == 4 and self.rect.right <= 749 and self.can_goto(4):  
                self.rect.x += self.speed
            if pygame.time.get_ticks() - self.pace_time >= 25:
                self.pace_time = pygame.time.get_ticks()
                if self.image_num >= len(self.images[self.state - 1]) - 1:
                    self.image_num = 0
                else:
                    self.image_num += 1


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
        self.is_dying()

    def is_dying(self):
        if self.hp == 0:
            self.hp = self.full_hp

'''
bullet:
    screen_image(Surface)       窗口
    image(Surface)              子弹形象
    is_show(bool)               是否显示    0-隐藏 1-显示
    from_player(player)         伤害来源:   0-来源于非玩家(或玩家的治疗) player1-来源于玩家1 player2-来源于玩家2
    damage(int)                 伤害:       +为伤害 -为治疗
    damage_range(float)         伤害半径
    speed([float, float])       速度:       x_speed(右) y_speed(下)
    last_time(int)              子弹上次移动毫秒值
    rect(Rect)                  子弹矩形对象
    can_through_wall(bool)      子弹是否能够穿墙:   0-不能穿墙 1-穿墙

    display():                                          绘制子弹(如状态为显示)
    move():                                             向固定方向移动并绘制
    hit(target):                                        消除并造成伤害
        target(<player> or <enemy> or 0)                    目标
    is_hit_wall(camera_left_top, wallmap):  -> bool     判断是否撞到边界 或 墙(可穿墙的不判定): 0-未撞到 1-撞到
        camera_left_top([int,int]):                         镜头左上角坐标
        wallmap([[int]]):                                   地图
    detect(targets, camera_left_top, wallmap): -> int   检查是否撞到列表内的目标或边界 或 墙(可穿墙的不判定): -1 - 撞到并删除该子弹 0 - 未撞到
        targets([<player> or <enemy>]):                     子弹需要判定的目标
        camera_left_top([int,int]):                         镜头左上角坐标
        wallmap([[int]]):                                   地图
'''
class bullet:
    def __init__(self, screenin:pygame.Surface, imagein:pygame.Surface, from_player:player, damage_range:float, b_location:list, speed:list, can_through_wall:bool=False):
        self.screen_image = screenin
        self.image = imagein
        self.is_show = 1
        self.damage = from_player.damage_value
        if self.damage >= 0:
            self.from_player = from_player
        else:
            self.from_player = 0
        self.damage_range = damage_range
        self.speed = speed
        self.last_time = pygame.time.get_ticks()
        self.rect = self.image.get_rect(center=b_location) 
        self.can_through_wall = can_through_wall

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

    def is_hit_wall(self, wallmap:list):
        if self.rect.left < 0 or self.rect.top < 0 or self.rect.right > 750 or self.rect.bottom > 560:
            return True
        if not self.can_through_wall:
            try:
                if wallmap[(self.rect.centery) // 50][(self.rect.centerx) // 50] != 0:
                    return True
            except IndexError:
                return False

    def detect(self, targets:list, wallmap:list):
        if self.is_hit_wall(wallmap):
            self.hit(0)
            return -1
        else:
            for target in targets:
                if (target.rect.centerx - self.rect.centerx) ** 2 + (target.rect.centery - self.rect.centery) ** 2 <= self.damage_range ** 2:
                    self.hit(target)
                    return -1
            return 0

def menu(screen_image:pygame.Surface, player_num:int):
    pygame.init()

    pic = pictures()
    map_0 = []
    with open(f'Maps\\map0.txt','r') as f:
        for line in f:
            map_0.append(list(map(int,line.strip())))
    walls = wall_bgp(screen_image, pic.village, pic.wall_images, map_0)
    player1 = player(screen_image, walls.wallmap, pic.Knight, pic.sideplayer1, 10, 114, 100, 4)
    player1.goto(2)
    if player_num == 2:
        player2 = player(screen_image, walls.wallmap, pic.Knightress, pic.sideplayer2, 10, 514, 100, 4)
        player2.goto(2)
        players = [player1, player2]
    else:
        players = [player1]

    bullets = []

    bgm = BgmPlayer()
    bgm.play('Soul_Soil.mp3', -1)

    def minimize_window():
        window = gw.getWindowsWithTitle('Soul Knight')[0]
        window.minimize()

    def playercheck(a_player:player, K_up, K_down, K_left, K_right):
        if a_player.is_alive == 1:
            if keypressed[K_up] and not keypressed[K_down]:
                a_player.move(1)
                flipper()
            elif keypressed[K_down] and not keypressed[K_up]:
                a_player.move(2)
                flipper()
            elif keypressed[K_left] and not keypressed[K_right]:
                a_player.move(3)
                flipper()
            elif keypressed[K_right] and not keypressed[K_left]:
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
        walls.display()
        screen_image.blit(pic.sidebox, (750, 0))
        for player_0 in players:
            if player_0.is_alive == 1:
                player_0.display()
        for bullet_0 in bullets:
            bullet_0.move()
        pygame.display.flip()


    flipper()

    clock = pygame.time.Clock()
    while True:
        clock.tick(50)
        bullets_to_remove = []
        for bullet_0 in bullets:
            bullet_0.move()
            if bullet_0.from_player == player1:
                result = bullet_0.detect([player2], map_0)
                if result == -1:
                    bullets_to_remove.append(bullet_0)
            elif bullet_0.from_player == player2:
                result = bullet_0.detect([player1], map_0)
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

            for player_0 in players:
                if player_0.player_num == 1 and player_0.is_alive == 1 and event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    bullets.append(bullet(screen_image, pic.bullet1, player_0, 20, [player_0.rect.centerx, player_0.rect.centery][:], state_trans(player_0.state,4)))
                    bullets[-1].display()
                if player_0.player_num == 2 and player_0.is_alive == 1 and event.type == pygame.KEYDOWN and event.key == pygame.K_RCTRL:
                    bullets.append(bullet(screen_image, pic.bullet1, player_0, 20, [player_0.rect.centerx, player_0.rect.centery][:], state_trans(player_0.state,4)))
                    bullets[-1].display()

        if pygame.display.get_active():
            bgm.unpause()
        else:
            bgm.pause()

        keypressed = pygame.key.get_pressed()
        for player_0 in players:
            if player_0.player_num == 1:
                playercheck(player1, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)
            elif player_0.player_num == 2:
                playercheck(player2, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
        if players[0].is_alive == 0:
            del players[0]
        if players[-1].is_alive == 0:
            del players[-1]
        
        flipper()


if __name__ == '__main__':
    screen_image = pygame.display.set_mode((900, 560))
    pygame.display.set_caption('Soul Knight')
    menu(screen_image, 2)