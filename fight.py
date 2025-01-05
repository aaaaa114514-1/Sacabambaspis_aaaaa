import pygame
import pygame_gui
import sys
import pygetwindow as gw
import os
from bgmplayer import BgmPlayer
from load_picture import pictures
from kits import Kits
import random
import json
import transition_effect


'''
camara:
    edges([int,int,int,int]):   镜头移动判定边界位置(上/下/左/右)
    left_top([int,int]):        地图左上角在当前镜头的坐标

    can_move(player, walls, direction):   -> [int,int,int,int]              判定是否能够移动, 返回值为0的元素表示不可[上/下/左/右]移动镜头, 为1则可以移动镜头; 若返回[2,2,2,2]则是地图到达边界
        player([player, ...]):                                                  所有玩家
        walls(wall_bgp):                                                        墙与背景图对象
        direction([int,int]):                                                   移动向量
    move_check(players, enemies, bullets, walls):                           判断是否需要移动镜头的移动检测函数
        players([player, ...]):                                                 所有玩家
        enemies([enemy, ...]):                                                  所有敌人
        bullets([bullet, ...]):                                                 子弹列表
        walls(wall_bgp):                                                        墙与背景图对象
    move(direction, distance, players, enemies, bullets, walls): -> int     移动镜头(含检测能否移动镜头), 返回值为是否无需强制移动至镜头移动判定边界上
        direction(int):                                                         方向: 1-上 2-下 3-左 4-右
        distance(int):                                                          移动距离
        players([player, ...]):                                                 所有玩家
        enemies([enemy, ...]):                                                  所有敌人
        bullets([bullet, ...]):                                                 子弹列表
        walls(wall_bgp):                                                        墙与背景图对象
'''

class camera:
    def __init__(self, left_top:list):
        self.edges = [120, 580, 120, 440]
        self.left_top = left_top

    def can_move(self, players:list, walls, direction:list):
        if walls.can_move(direction):
            result = [1,1,1,1]
            for player_0 in players:
                if player_0.rect.y >= self.edges[3]:
                    result[1] = 0
                if player_0.rect.y <= self.edges[2]:
                    result[0] = 0
                if player_0.rect.x >= self.edges[1]:
                    result[3] = 0
                if player_0.rect.x <= self.edges[0]:
                    result[2] = 0
            return result
        else:
            return [2,2,2,2]
    
    def move_check(self, players:list, enemies:list, bullets:list, walls):
        for player_0 in players:
            if player_0.rect.y > self.edges[3]:
                if not self.move(1, player_0.rect.y - self.edges[3], players, enemies, bullets, walls):
                    player_0.rect.y = self.edges[3]
                    player_0.rect.y = self.edges[3]
            elif player_0.rect.y < self.edges[2]:
                if not self.move(2, self.edges[2] - player_0.rect.y, players, enemies, bullets, walls):
                    player_0.rect.y = self.edges[2]
                    player_0.rect.y = self.edges[2]
            elif player_0.rect.x > self.edges[1]:
                if not self.move(3, player_0.rect.x - self.edges[1], players, enemies, bullets, walls):
                    player_0.rect.x = self.edges[1]
                    player_0.rect.x = self.edges[1]
            elif player_0.rect.x < self.edges[0]:
                if not self.move(4, self.edges[0] - player_0.rect.x, players, enemies, bullets, walls):
                    player_0.rect.x = self.edges[0]
                    player_0.rect.x = self.edges[0]

    def move(self, direction:int, distance:int, players:list, enemies:list, bullets:list, walls):
        if direction == 1:
            if self.can_move(players, walls, [0,-distance])[0] == 1:
                for entity in players:
                    entity.rect.y -= distance
                for entity in enemies:
                    entity.rect.y -= distance
                for entity in bullets:
                    entity.location[1] -= distance
                    entity.rect.y -= distance
                walls.move([0,-distance])
                self.left_top = [self.left_top[0],self.left_top[1]-distance]
                return 1
            elif self.can_move(players, walls, [0,-distance])[0] == 2:
                return 1
        elif direction == 2:
            if self.can_move(players, walls, [0,distance])[1] == 1:
                for entity in players:
                    entity.rect.y += distance
                for entity in enemies:
                    entity.rect.y += distance
                for entity in bullets:
                    entity.location[1] += distance
                    entity.rect.y += distance
                walls.move([0,distance])
                self.left_top = [self.left_top[0],self.left_top[1]+distance]
                return 1
            elif self.can_move(players, walls, [0,distance])[1] == 2:
                return 1
        elif direction == 3:
            if self.can_move(players, walls, [-distance,0])[2] == 1:
                for entity in players:
                    entity.rect.x -= distance
                for entity in enemies:
                    entity.rect.x -= distance
                for entity in bullets:
                    entity.location[0] -= distance
                    entity.rect.x -= distance
                walls.move([-distance,0])
                self.left_top = [self.left_top[0]-distance,self.left_top[1]]
                return 1
            elif self.can_move(players, walls, [-distance,0])[2] == 2:
                return 1
        elif direction == 4:
            if self.can_move(players, walls, [distance,0])[3] == 1:
                for entity in players:
                    entity.rect.x += distance
                for entity in enemies:
                    entity.rect.x += distance
                for entity in bullets:
                    entity.location[0] += distance
                    entity.rect.x += distance
                walls.move([distance,0])
                self.left_top = [self.left_top[0]+distance,self.left_top[1]]
                return 1
            elif self.can_move(players, walls, [distance,0])[3] == 2:
                return 1
        else:
            return 0


'''
wall_bgp:
    screen_image(Surface):  窗口
    bgp(Surface):           背景图
    bgp_rect(Rect):         背景图矩形
    walled_bgp(Surface):    已绘制墙体的背景图
    wall_images([Surface]): 墙体图片列表
    wall_map([[]]):         地图(0-地面 >0-墙体)

    show_portal(portal_pic, portal_location):       显示传送门
        portal_pic(Surface):                            传送门图片
        portal_location([int,int]):                     传送门位置
    build_map():                                    将墙体按照地图绘制在walled_bgp上
    can_move(direction): -> bool                    判定移动后图片是否出界
        direction([int,int]):                           移动方向向量
    move(direction):                                移动背景图和所有墙体(带边缘判定)
        direction([int,int]):                           移动方向向量
    display():                                      将walled_bgp绘制在屏幕上
'''
class wall_bgp:
    def __init__(self, screen_image:pygame.Surface, bgp:pygame.Surface, wall_images:list[pygame.Surface], wallmap:list=None):
        self.screen_image = screen_image
        self.bgp = bgp
        self.bgp_rect = bgp.get_rect()
        if wallmap == None:
            wallmap = []
        self.wallmap = wallmap
        self.wall_images = wall_images
        self.walled_bgp = self.bgp.copy()
        self.build_map()

    def show_portal(self, portal_pic:pygame.Surface, portal_location:list):
        self.walled_bgp.blit(portal_pic, portal_location)
        
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
bullet:
    screen_image(Surface)               窗口
    image(Surface)                      子弹形象
    is_show(bool)                       是否显示    0-隐藏 1-显示
    from_player(<player> or <enemy>)    伤害来源:   0-来源于非玩家(或玩家的治疗)
    damage(int)                         伤害:       +为伤害 -为治疗
    damage_range(float)                 伤害半径
    speed([float, float])               速度:       x_speed(右) y_speed(下)
    last_time(int)                      子弹上次移动毫秒值
    rect(Rect)                          子弹矩形对象
    can_through_wall(bool)              子弹是否能够穿墙:   0-不能穿墙 1-穿墙

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
    def __init__(self, screenin:pygame.Surface, imagein:pygame.Surface, from_player, damage_range:float, b_location:list, speed:list, can_through_wall:bool=False):
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
        self.location = [b_location[0], b_location[1]]
        self.can_through_wall = can_through_wall

    def display(self):
        if self.is_show:
            self.screen_image.blit(self.image, self.rect)

    def move(self):
        if pygame.time.get_ticks() - self.last_time >= 10:
            self.last_time = pygame.time.get_ticks()
            self.location[0] += self.speed[0]
            self.location[1] += self.speed[1]
            self.rect.x = self.location[0]
            self.rect.y = self.location[1]

    def hit(self, target):
        if target != 0:
            if target.damage(self.damage) == 0:
                self.from_player.magic_add(30)
        self.is_show = 0

    def is_hit_wall(self, camera_left_top:list, wallmap:list):
        if self.rect.left < 0 or self.rect.top < 0 or self.rect.right > 750 or self.rect.bottom > 560:
            return True
        if not self.can_through_wall:
            try:
                if wallmap[(self.rect.centery - camera_left_top[1]) // 50][(self.rect.centerx - camera_left_top[0]) // 50] != 0:
                    return True
            except IndexError:
                return False

    def detect(self, targets:list, camera_left_top:list, wallmap:list):
        if self.is_hit_wall(camera_left_top, wallmap):
            self.hit(0)
            return -1
        else:
            for target in targets:
                if (target.rect.centerx - self.rect.centerx) ** 2 + (target.rect.centery - self.rect.centery) ** 2 <= self.damage_range ** 2:
                    self.hit(target)
                    return -1
            return 0



'''
player:
    font1(Font)             侧边栏字体(大)
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
    attack_time(int)        玩家上次攻击毫秒值
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
    damage(damage_v):               结算受到的伤害
        damage_v(int)                   受到的伤害值(有上下限校验)
    is_dying():                     检验是否死亡
'''

class player:
    pygame.font.init()
    font1 = pygame.font.Font('Text\\xiangfont.ttf', 25)

    def __init__(self, player_num, screenin: pygame.Surface, wallmap, imagesin: list[list[pygame.Surface]], side_player: pygame.Surface, damage_value: int, full_hp: int, full_magic: int, speed:int):
        self.player_num = player_num
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
        self.attack_time = pygame.time.get_ticks()
        self.image_num = 0
        self.rect = self.images[0][0].get_rect(center=[150, 260])
        self.wallmap = wallmap
        self.is_alive = 1

    def goto(self, direction, destination=None):
        if destination is None:
            destination = [self.rect.x, self.rect.y]
        self.state = direction
        self.rect.center = destination 

    def can_goto(self, direction:int, camera_left_top:list):
        new_rect = self.rect.copy()
        if direction == 1:
            new_rect.y -= self.speed
        elif direction == 2:
            new_rect.y += self.speed
        elif direction == 3:
            new_rect.x -= self.speed
        elif direction == 4:
            new_rect.x += self.speed

        top_left = (new_rect.left, new_rect.top)
        top_right = (new_rect.right, new_rect.top)
        bottom_left = (new_rect.left, new_rect.bottom)
        bottom_right = (new_rect.right, new_rect.bottom)

        if new_rect.left < 0 or new_rect.right > 750 or new_rect.top < 0 or new_rect.bottom > 560:
            return False

        for corner in [top_left, top_right, bottom_left, bottom_right]:
            try:
                if self.wallmap[(corner[1]-camera_left_top[1]) // 50][(corner[0]-camera_left_top[0]) // 50] != 0:
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


    def move(self, direction, camera_left_top):
        if pygame.time.get_ticks() - self.last_time >= 10:
            self.last_time = pygame.time.get_ticks()
            self.state = direction
            if direction == 1 and self.rect.top >= 1 and self.can_goto(1,camera_left_top): 
                self.rect.y -= self.speed
            elif direction == 2 and self.rect.bottom <= 560 and self.can_goto(2,camera_left_top):  
                self.rect.y += self.speed
            elif direction == 3 and self.rect.left >= 1 and self.can_goto(3,camera_left_top): 
                self.rect.x -= self.speed
            elif direction == 4 and self.rect.right <= 749 and self.can_goto(4,camera_left_top):  
                self.rect.x += self.speed
        if pygame.time.get_ticks() - self.pace_time >= 25:
            self.pace_time = pygame.time.get_ticks()
            if self.image_num >= len(self.images[self.state - 1]) - 1:
                self.image_num = 0
            else:
                self.image_num += 1

    def magic_add(self, add_magic):
        if self.magic + add_magic > self.full_magic:
            self.magic = self.full_magic
        else:
            self.magic += add_magic

    def hp_set(self, new_hp):
        if new_hp >= 0 and new_hp <= self.full_hp:
            self.hp = new_hp

    def damage(self, damage_v):
        if damage_v >= self.hp:
            self.hp = 0
        else:
            self.hp -= damage_v
            if self.hp > self.full_hp:
                self.hp = self.full_hp
        self.is_dying()
        return 1

    def is_dying(self):
        if self.hp == 0:
            self.is_alive = 0


'''
enemy:
    screen_image(Surface)   窗口
    type(int)               类型: 0-普通 1-BOSS
    images(Surface)         形象
    image_num(int)          形象编号
    state(int)              状态: 1-up 2-down 3-left 4-right
    damage_value(int)       伤害
    full_hp(int)            最高血量
    hp(int)                 血量
    full_magic(int)         最高魔法值
    magic(int)              魔法值
    last_time(int)          玩家上次移动毫秒值
    rect(Rect)              玩家矩形对象
    wallmap([[]])           地图
    is_alive(bool)          存活状态: 1-alive 0-dead
    motion([[int,int],...]) 移动路径
    motion_i(int)           当前移动路径索引
    speed(float)            移动速度
    pace_time(int)          玩家上次更新帧的毫秒值
    attack_time(int)        玩家上次攻击毫秒值
    attack_dt(int)          攻击间隔毫秒值

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

class enemy:
    def __init__(self, type_in:int, screen_image:pygame.Surface, images:list[list[pygame.Surface]], hp:int, damage_value:int, damage_range:float, bullet_speed:int, bullet_image:pygame.Surface, bullet_ctw:bool, motion:list, speed:float, attack_dt:int):
        self.screen_image = screen_image
        self.type = type_in
        if self.type == 1:
            self.pic = pictures()
            self.is_raging = 0
        self.images = images
        self.image_num = 0
        self.state = 2
        self.rect = self.images[0][0].get_rect(center=motion[0])
        self.full_hp = hp
        self.hp = hp
        self.damage_value = damage_value
        self.damage_range = damage_range
        self.bullet_speed = bullet_speed
        self.bullet_image = bullet_image
        self.bullet_ctw = bullet_ctw
        self.motion = motion
        self.motion_i = 0
        self.speed = speed
        self.last_time = pygame.time.get_ticks()
        self.pace_time = pygame.time.get_ticks()
        self.attack_time = pygame.time.get_ticks()
        self.is_alive = 1
        self.attack_dt = attack_dt

    def vect(self, loca_0:list, loca_1:list,speed:float=1):
        dx = loca_1[0] - loca_0[0]
        dy = loca_1[1] - loca_0[1]
        d = (dx**2+dy**2)**0.5
        if d != 0:
            return [dx/d*speed, dy/d*speed]
        else:
            return [0,0]
    
    def set_state(self, posi_0:list, posi_1:list):
        vect_0 = self.vect(posi_0,posi_1)
        if vect_0[0]+vect_0[1]>0:
            if vect_0[0]>vect_0[1]:
                self.state = 4
            else:
                self.state = 2
        else:
            if vect_0[0]>vect_0[1]:
                self.state = 1
            else:
                self.state = 3

    def move(self, camera_lefttop:list):
        if pygame.time.get_ticks() - self.last_time >= 10:
            self.last_time = pygame.time.get_ticks()
            if (self.rect.centerx - camera_lefttop[0] - self.motion[self.motion_i][0])**2 + (self.rect.centery - camera_lefttop[1] - self.motion[self.motion_i][1])**2 <= self.speed ** 2:
                self.rect.center = [(self.motion[self.motion_i][0]+camera_lefttop[0]),(self.motion[self.motion_i][1]+camera_lefttop[1])]
                if self.motion_i == len(self.motion)-1:
                    self.motion_i = 0
                    self.set_state(self.motion[len(self.motion)-1],self.motion[0])
                else:
                    self.motion_i += 1
                    self.set_state(self.motion[self.motion_i-1],self.motion[self.motion_i])
            else:
                movement = self.vect([self.rect.centerx-camera_lefttop[0],self.rect.centery-camera_lefttop[1]], self.motion[self.motion_i],self.speed)
                self.rect.centerx += movement[0]
                self.rect.centery += movement[1]
        if pygame.time.get_ticks() - self.pace_time >= 30:
            self.pace_time = pygame.time.get_ticks()
            if self.image_num >= len(self.images[self.state - 1]) - 1:
                self.image_num = 0
            else:
                self.image_num += 1

    def attack(self, target_player_loca:list):
        if pygame.time.get_ticks() - self.attack_time > self.attack_dt:
            self.attack_time = pygame.time.get_ticks()
            if self.type == 0:
                return bullet(self.screen_image, self.bullet_image, self, self.damage_range, self.rect.center, self.vect(self.rect.center, target_player_loca, self.bullet_speed), self.bullet_ctw)
            elif self.type == 1:
                return [bullet(self.screen_image, self.bullet_image, self, self.damage_range, self.rect.center, self.vect(self.rect.center, target_player_loca, self.bullet_speed+1), True),
                        bullet(self.screen_image, self.pic.bullet3, self, self.damage_range, self.rect.center, self.vect(self.rect.center, (target_player_loca[0]+50, target_player_loca[1]+50), self.bullet_speed), self.bullet_ctw),
                        bullet(self.screen_image, self.pic.bullet3, self, self.damage_range, self.rect.center, self.vect(self.rect.center, (target_player_loca[0]-50, target_player_loca[1]-50), self.bullet_speed), self.bullet_ctw),
                        bullet(self.screen_image, self.pic.bullet3, self, self.damage_range, self.rect.center, self.vect(self.rect.center, (target_player_loca[0]+50, target_player_loca[1]-50), self.bullet_speed), self.bullet_ctw),
                        bullet(self.screen_image, self.pic.bullet3, self, self.damage_range, self.rect.center, self.vect(self.rect.center, (target_player_loca[0]-50, target_player_loca[1]+50), self.bullet_speed), self.bullet_ctw)]

    def display(self):
        if self.rect.right > 0 and self.rect.left < 750 and self.rect.bottom > 0 and self.rect.top < 560:
            pygame.draw.rect(self.screen_image,(50,50,50),(self.rect.left, self.rect.bottom+1, self.rect.width, 6))
            pygame.draw.rect(self.screen_image,(255,0,0),(self.rect.left, self.rect.bottom+2, (self.hp/self.full_hp)*self.rect.width, 4))
            self.screen_image.blit(self.images[self.state-1][self.image_num],self.rect)

    def damage(self, damage_v:int):
        if damage_v >= self.hp:
            self.hp = 0
        else:
            self.hp -= damage_v
            if self.hp > self.full_hp:
                self.hp = self.full_hp
        if self.type == 1 and self.is_raging == 0 and self.hp <= self.full_hp//2 and self.is_alive == 1:
            self.is_raging = 1
            self.attack_dt = int(self.attack_dt * 0.8)
            self.damage_value = self.damage_value * 2
            self.bullet_image = self.pic.bullet2
        return self.is_dying()

    def is_dying(self):
        if self.hp == 0:
            self.is_alive = 0
            return 0
        else:
            return 1


'''
fight(screen_image, player_num_list, level_num, player_info):     -> bool   战斗场景
    screen_image(Surface):                                                      窗口
    player_num_list(list):                                                      玩家, 如[1,2],[1]或[2]
    level_num(int):                                                             关卡编号
    player_info([[int,int,int,int,float,bool,int,int,Surface],]):               玩家信息:   [[血量, 魔法值, 速度, 伤害, 溅射范围, 子弹能否穿墙, 子弹消耗魔法值, 子弹速度, 子弹形象],]
'''
def fight(screen_image:pygame.Surface, player_num_list:list, level_num:int, player_info:list):
    pygame.init()
    manager = pygame_gui.UIManager((900,560))
    with open(f'Levels\Level{level_num}.txt', 'r') as file:
        file_content = file.read()
    level_data = json.loads(file_content)

    pic = pictures()
    map_0 = []
    with open(f'Maps\\map{level_data["map"]}.txt','r') as f:
        for line in f:
            map_0.append(list(map(int,line.strip())))
    walls = wall_bgp(screen_image, pic.big_grass, pic.wall_images, map_0)
    players:list[player] = []
    if 1 in player_num_list:
        player1 = player(1, screen_image, walls.wallmap, pic.Knight, pic.sideplayer1, player_info[0][3], player_info[0][0], player_info[0][1], player_info[0][2])
        player1.goto(2)
        players.append(player1)
    if 2 in player_num_list:
        player2 = player(2, screen_image, walls.wallmap, pic.Knightress, pic.sideplayer2, player_info[1][3], player_info[1][0], player_info[1][1], player_info[1][2])
        player2.goto(2)
        players.append(player2)

    enemies:list[enemy] = []
    enemy_pics = [pic.Bird, pic.Boss]
    bullet_pics = [pic.bullet0, pic.bullet1, pic.bullet2, pic.bullet3, pic.bullet4]
    for enemy_data in level_data['enemies']:
        enemies.append(enemy(enemy_data['type'],screen_image,enemy_pics[enemy_data['type']],enemy_data['hp'],enemy_data['damage'],enemy_data['damage_range'],enemy_data['bullet_speed'],bullet_pics[enemy_data['bullet_image']],enemy_data['bullet_ctw'],enemy_data['motion'],enemy_data['speed'],enemy_data['attack_dt']))

    bullets:list[bullet] = []

    camera_0 = camera([0,0])

    bgm = BgmPlayer()
    bgm.play(level_data['bgm'], -1)

    kits_0 = Kits(screen_image, manager, bgm, 2, ['quit','volume'])
    time_delta = 0
    winning = 0
    status_text = ''

    def minimize_window():
        window = gw.getWindowsWithTitle('Soul Knight')[0]
        window.minimize()

    def playercheck(a_player:player, K_up, K_down, K_left, K_right):
        if a_player.is_alive == 1:
            if keypressed[K_up] and not keypressed[K_down]:
                a_player.move(1,camera_0.left_top)
            elif keypressed[K_down] and not keypressed[K_up]:
                a_player.move(2,camera_0.left_top)
            elif keypressed[K_left] and not keypressed[K_right]:
                a_player.move(3,camera_0.left_top)
            elif keypressed[K_right] and not keypressed[K_left]:
                a_player.move(4,camera_0.left_top)

    def state_trans(state,speed):
        if state == 1:
            return [0,-speed]
        elif state == 2:
            return [0,speed]
        elif state == 3:
            return [-speed,0]
        else:
            return [speed,0]

    def flipper(is_flip=True):
        walls.display()
        for bullet_0 in bullets:
            bullet_0.display()
        for enemy_0 in enemies:
            if enemy_0.is_alive == 1:
                enemy_0.display()
        screen_image.blit(pic.sidebox, (750, 0))
        for player_0 in players:
            if player_0.is_alive == 1:
                player_0.display()
        kits_0.set_label(status_text)
        manager.update(time_delta)
        manager.draw_ui(screen_image)
        if is_flip:
            pygame.display.flip()


    flipper(False)
    transition_effect.level_fade_in(screen_image, level_num)

    clock = pygame.time.Clock()
    while True:
        time_delta = clock.tick(50) / 1000.0
        bullets_to_remove = []
        for bullet_0 in bullets:
            bullet_0.move()
            if bullet_0.from_player in players:
                result = bullet_0.detect(enemies, camera_0.left_top, map_0)
                if result == -1:
                    bullets_to_remove.append(bullet_0)
            else:
                result = bullet_0.detect(players, camera_0.left_top, map_0)
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
                if winning == 2 and event.key == pygame.K_SPACE:
                    return 1

            for player_0 in players:
                if player_0.player_num == 1 and player_0.is_alive == 1 and event.type == pygame.KEYDOWN and event.key == pygame.K_m and player_0.magic >= player_info[0][6] and (pygame.time.get_ticks()-player_0.attack_time > 250):
                    player_0.magic -= player_info[0][6]
                    bullets.append(bullet(screen_image, player_info[0][8], player_0, player_info[0][4], [player_0.rect.centerx, player_0.rect.centery][:], state_trans(player_0.state,player_info[0][7]),player_info[0][5]))
                    bullets[-1].display()
                if player_0.player_num == 2 and player_0.is_alive == 1 and event.type == pygame.MOUSEBUTTONDOWN and player_0.magic >= player_info[1][6] and (pygame.time.get_ticks()-player_0.attack_time > 250):
                    player_0.magic -= player_info[1][6]
                    bullets.append(bullet(screen_image, player_info[1][8], player_0, player_info[1][4], [player_0.rect.centerx, player_0.rect.centery][:], state_trans(player_0.state,player_info[1][7]),player_info[1][5]))
                    bullets[-1].display()

        manager.process_events(event)

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
        if len(players) > 1 and players[1].is_alive == 0:
            del players[1]
        if len(players) > 0 and players[0].is_alive == 0:
            del players[0]
        if len(players) == 0:
            return 0

        for enemy_0 in enemies:
            if enemy_0.is_alive == 0:
                enemies.remove(enemy_0)
            else:
                enemy_0.move(camera_0.left_top)
            player_0 = random.choice(players)
            bullet_to_add = enemy_0.attack(player_0.rect.center)
            if type(bullet_to_add) == bullet:
                bullets.append(bullet_to_add)
            elif type(bullet_to_add) == list:
                for bullet_0 in bullet_to_add:
                    bullets.append(bullet_0)

        if enemies == [] and winning == 0:
            winning = 1
            walls.show_portal(pic.portal, level_data['portal'])

        if kits_0.is_quiting() or players == []:
            return 0
        
        camera_0.move_check(players, enemies, bullets, walls)

        kits_0.check_voluming()
        kits_0.check_adjusting_volume()
        if winning:
            for player_0 in players:
                if player_0.rect.centerx-camera_0.left_top[0] > level_data['portal'][0]+100 or player_0.rect.centerx-camera_0.left_top[0] < level_data['portal'][0] or player_0.rect.centery-camera_0.left_top[1] > level_data['portal'][1]+100 or player_0.rect.centery-camera_0.left_top[1] < level_data['portal'][1]-25:
                    status_text = 'Go to portal and win!'
                    winning = 1
                    break
            else:
                status_text = 'Space: win!'
                winning = 2
            manager.process_events(event)
        flipper()



if __name__ == '__main__':
    pic = pictures
    screen_image = pygame.display.set_mode((900, 560))
    pygame.display.set_caption('Soul Knight')
    fight(screen_image, [2], 2, [[100,100,4,10,20,True,3,6,pic.bullet1],[500,100,6,20,30,False,5,3,pic.bullet2]])

    #[[0血量, 1魔法值, 2速度, 3伤害, 4溅射范围, 5子弹能否穿墙, 6子弹消耗魔法值, 7子弹速度, 8子弹形象],]