import pygame
import os

'''
pictures:
    load_images(name, frame_num, size):     加载图片
        name(str):                              图片名称
        frame_num(int):                         帧数
        size(tuple):                            大小
'''
class pictures:
    def __init__(self):
        pass

    def load_images(name:str, frame_num:int, size:tuple):
        result = [[],[],[],[]]
        for i in range(4):
            for frame in range(frame_num):
                result[i].append(pygame.image.load(f'Pictures\\{name}\\{name}{i+1}_{frame+1}.png'))
                result[i].append(pygame.transform.scale(result[i][frame], size))
        return result
    
    Soul_knight_background = pygame.image.load('Pictures\Soul_knight_background.jpg')
    Soul_knight_background = pygame.transform.scale(Soul_knight_background, (900,560))
    Soul_knight_background2 = pygame.image.load('Pictures\Soul_knight_background2.png')
    Soul_knight_background2 = pygame.transform.scale(Soul_knight_background2, (900,560))
    Title = pygame.image.load('Pictures\Title.png')
    Author = pygame.image.load('Pictures\Author.jpg')
    Author = pygame.transform.scale(Author, (150, 52.5))

    Alice = load_images('Alice', 4, (33,47))
    Bob = load_images('Bob', 4, (33,49))
    Knight = load_images('Knight', 4, (33,49))
    Knightress = load_images('Knightress', 4, (33,47))
    Bird = load_images('Bird', 4, (64,60))
    Boss = load_images('Boss', 4, (96,96))
    # TestEnemy = load_images('TestEnemy', 4,(64,60))

    bullet0 = pygame.image.load('Pictures\Bullets\Bullet0.png')
    bullet0 = pygame.transform.scale(bullet0, (10, 10))
    bullet1 = pygame.image.load('Pictures\Bullets\Bullet1.png')
    bullet1 = pygame.transform.scale(bullet1, (10, 10))
    bullet2 = pygame.image.load('Pictures\Bullets\Bullet2.png')
    bullet2 = pygame.transform.scale(bullet2, (15, 15))
    bullet3 = pygame.image.load('Pictures\Bullets\Bullet3.png')
    bullet3 = pygame.transform.scale(bullet3, (10, 10))
    bullet4 = pygame.image.load('Pictures\Bullets\Bullet4.png')
    bullet4 = pygame.transform.scale(bullet4, (20, 20))

    bullet0_big = pygame.image.load('Pictures\Bullets\Bullet0.png')
    bullet0_big = pygame.transform.scale(bullet0_big, (40, 40))
    bullet1_big = pygame.image.load('Pictures\Bullets\Bullet1.png')
    bullet1_big = pygame.transform.scale(bullet1_big, (40, 40))
    bullet2_big = pygame.image.load('Pictures\Bullets\Bullet2.png')
    bullet2_big = pygame.transform.scale(bullet2_big, (60, 60))
    bullet3_big = pygame.image.load('Pictures\Bullets\Bullet3.png')
    bullet3_big = pygame.transform.scale(bullet3_big, (40, 40))
    bullet4_big = pygame.image.load('Pictures\Bullets\Bullet4.png')
    bullet4_big = pygame.transform.scale(bullet4_big, (80, 80))

    textbox = pygame.image.load('Pictures\\textbox.png')
    textbox = pygame.transform.scale(textbox, (750, 130))
    sidebox = pygame.image.load('Pictures\sidebox.png')
    sidebox = pygame.transform.scale(sidebox, (150, 560))
    sideplayer1 = pygame.image.load('Pictures\side_player1.png')
    sideplayer1 = pygame.transform.scale(sideplayer1, (150, 115))
    sideplayer2 = pygame.image.load('Pictures\side_player2.png')
    sideplayer2 = pygame.transform.scale(sideplayer2, (150, 115))

    big_grass = pygame.image.load('Pictures\\BGP\\big_grass.png')
    big_grass = pygame.transform.scale(big_grass, (2400, 1500))
    village = pygame.image.load('Pictures\\BGP\\village.png')
    village = pygame.transform.scale(village, (750,560))

    portal = pygame.image.load('Pictures\portal.png')
    portal = pygame.transform.scale(portal,(100,100))

    auto_playing = pygame.image.load('Pictures\\icons\\auto_playing.png')
    auto_playing = pygame.transform.scale(auto_playing, (25, 25))
    chapter_background = pygame.image.load('Pictures\\icons\\Chapter_background.png')
    chapter_background = pygame.transform.scale(chapter_background, (170, 70))
    level_namebox = pygame.image.load('Pictures\\Level_namebox.png')
    level_namebox = pygame.transform.scale(level_namebox, (700, 110))

    folder_path = 'Pictures\\Walls'
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('png', 'jpg', 'jpeg'))]
    wall_images = [pygame.image.load('Pictures\\Walls' + '\\' + file) for file in image_files]
    for walli in range(len(wall_images)):
        wall_images[walli] = pygame.transform.scale(wall_images[walli], (50,50))

    '''
        wall_images:
        0 - Tree
        1 - air_wall
    '''
