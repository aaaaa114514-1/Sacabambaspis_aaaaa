import pygame
import sys
import time
import pygetwindow as gw
import os
from bgmplayer import BgmPlayer
from load_picture import pictures

class camera:
    def __init__(self, left_top:list):
        self.edges = [100, 600, 100, 460]
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
                    entity.rect.x += distance
                walls.move([distance,0])
                self.left_top = [self.left_top[0]+distance,self.left_top[1]]
                return 1
            elif self.can_move(players, walls, [distance,0])[3] == 2:
                return 1
        else:
            return 0


'''
wall:bgp:
    screen_image(Surface):  窗口
    bgp(Surface):           背景图
    bgp_rect(Rect):         背景图矩形
    walled_bgp(Surface):    已绘制墙体的背景图
    wall_images([Surface]): 墙体图片列表
    wall_map([[]]):         地图(0-地面 >0-墙体)

    build_map():                将墙体按照地图绘制在walled_bgp上
    move(direction):            移动背景图和所有墙体(带边缘判定)
        direction([int,int]):   移动方向向量
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
    images([Surface])       形象: [knight1, knight2, ...]
    side_player(Surface)    本角色侧边栏图片
    state(int)              状态: 1-up 2-down 3-left 4-right
    damage_value(int)             伤害
    full_hp(int)            最高血量
    hp(int)                 血量
    full_magic(int)         最高魔法值
    magic(int)              魔法值
    last_time(int)          玩家上次移动毫秒值
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

    def __init__(self, screenin: pygame.Surface, wallmap, imagesin: list[pygame.Surface], side_player: pygame.Surface, damage_value: int, full_hp: int, full_magic: int):
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
        self.state = 2
        self.last_time = pygame.time.get_ticks()
        self.rect = self.images[0].get_rect(center=[350, 255])
        self.wallmap = wallmap
        self.is_alive = 1

    def goto(self, direction, destination=None):
        if destination is None:
            destination = [self.rect.x, self.rect.y]
        self.state = direction
        self.rect.center = destination 

    def can_goto(self, direction, camera_left_top:list):
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
        self.screen_image.blit(self.images[self.state - 1], self.rect) 

    def move(self, direction, camera_left_top):
        if pygame.time.get_ticks() - self.last_time >= 10:
            self.last_time = pygame.time.get_ticks()
            self.state = direction
            speed = 3
            if direction == 1 and self.rect.top >= 1 and self.can_goto(1,camera_left_top): 
                self.rect.y -= speed
            elif direction == 2 and self.rect.bottom <= 560 and self.can_goto(2,camera_left_top):  
                self.rect.y += speed
            elif direction == 3 and self.rect.left >= 1 and self.can_goto(3,camera_left_top): 
                self.rect.x -= speed
            elif direction == 4 and self.rect.right <= 749 and self.can_goto(4,camera_left_top):  
                self.rect.x += speed


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
            self.is_alive = 0

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
        if self.rect.left < 0 or self.rect.top < 0 or self.rect.right > 750 or self.rect.bottom > 560:
            print('0010')
            self.hit(0)
            return -1
        else:
            for target in locations:
                if (target[0] - self.rect.centerx) ** 2 + (target[1] - self.rect.centery) ** 2 <= self.damage_range ** 2:
                    self.hit(target[2])
                    return -1
            return 0

def fight():
    pygame.init()
    screen_image = pygame.display.set_mode((900, 560))
    screen_rect = screen_image.get_rect()
    pygame.display.set_caption('Soul Knight')

    pic = pictures()

    walls = wall_bgp(screen_image, pic.grass, pic.wall_images, [[0,1,0,1,1,1,0,0,0,0,0,0,0,1],[0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,1,1,1,1,1,1,0,0,0,0,0,1],[2,0,3,4,2,1,2,1,0,0,0,0,0,1],[0,0,0,0,0,0,0,0,0,0,0,0,0,1],[0,0,0,0,0,0,0,0,0,0,0,0,0,1],[0,0,0,0,0,0,0,0,0,0,0,0,0,1],[0,0,0,0,0,0,0,0,0,0,0,0,0,1]])
    player1 = player(screen_image, walls.wallmap, [pic.knight1, pic.knight2, pic.knight3, pic.knight4], pic.sideplayer1, 10, 114, 100)
    player1.goto(2)
    player2 = player(screen_image, walls.wallmap, [pic.knight1, pic.knight2, pic.knight3, pic.knight4], pic.sideplayer2, 10, 514, 100)
    player2.goto(2)
    players = [player1, player2]
    bullets = []

    camera_0 = camera([0,0])

    bgm = BgmPlayer()
    bgm.play('Soul_Soil.mp3', -1)

    def minimize_window():
        window = gw.getWindowsWithTitle('Soul Knight')[0]
        window.minimize()

    def playercheck(a_player:player, K_up, K_down, K_left, K_right):
        if a_player.is_alive == 1:
            if keypressed[K_up] and not keypressed[K_down]:
                a_player.move(1,camera_0.left_top)
                flipper()
            if keypressed[K_down] and not keypressed[K_up]:
                a_player.move(2,camera_0.left_top)
                flipper()
            if keypressed[K_left] and not keypressed[K_right]:
                a_player.move(3,camera_0.left_top)
                flipper()
            if keypressed[K_right] and not keypressed[K_left]:
                a_player.move(4,camera_0.left_top)
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
        #screen_image.blit(pic.grass, (0,0))
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
        bullets_to_remove = []
        for bullet_0 in bullets:
            bullet_0.move()
            if bullet_0.from_player == player1:
                result = bullet_0.detect([[player2.rect.x, player2.rect.y, player2]])
                if result == -1:
                    bullets_to_remove.append(bullet_0)
            elif bullet_0.from_player == player2:
                result = bullet_0.detect([[player1.rect.x, player1.rect.y, player1]])
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

            if player1.is_alive == 1 and event.type == pygame.KEYDOWN and event.key == pygame.K_q and player1.magic >= 5:
                player1.magic -= 5
                bullets.append(bullet(screen_image, pic.bullet1, player1, 20, [player1.rect.x, player1.rect.y][:], state_trans(player1.state,4)))
                bullets[-1].display()
            if player2.is_alive == 1 and event.type == pygame.KEYDOWN and event.key == pygame.K_RCTRL and player2.magic >= 5:
                player2.magic -= 5
                bullets.append(bullet(screen_image, pic.bullet1, player2, 20, [player2.rect.x, player2.rect.y][:], state_trans(player2.state,4)))
                bullets[-1].display()

        if pygame.display.get_active():
            bgm.unpause()
        else:
            bgm.pause()

        keypressed = pygame.key.get_pressed()
        playercheck(player1, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)
        playercheck(player2, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
        camera_0.move_check(players, [], bullets, walls)
        flipper()


if __name__ == '__main__':
    fight()