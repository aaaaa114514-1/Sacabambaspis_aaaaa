import pygame
import os

class pictures:
    Soul_knight_background = pygame.image.load('Pictures\Soul_knight_background.jpg')
    Soul_knight_background = pygame.transform.scale(Soul_knight_background, (900,560))
    Soul_knight_background2 = pygame.image.load('Pictures\Soul_knight_background2.png')
    Soul_knight_background2 = pygame.transform.scale(Soul_knight_background2, (900,560))
    Title = pygame.image.load('Pictures\Title.png')
    Author = pygame.image.load('Pictures\Author.jpg')
    Author = pygame.transform.scale(Author, (150, 52.5))

    knight1 = pygame.image.load('Pictures\Knight\Knight1.png')
    knight1 = pygame.transform.scale(knight1, (40, 40))
    knight2 = pygame.image.load('Pictures\Knight\Knight2.png')
    knight2 = pygame.transform.scale(knight2, (40, 40))
    knight3 = pygame.image.load('Pictures\Knight\Knight3.png')
    knight3 = pygame.transform.scale(knight3, (40, 40))
    knight4 = pygame.image.load('Pictures\Knight\Knight4.png')
    knight4 = pygame.transform.scale(knight4, (40, 40))
    bullet1 = pygame.image.load('Pictures\Bullets\Bullet1.png')
    bullet1 = pygame.transform.scale(bullet1, (10, 10))

    textbox = pygame.image.load('Pictures\\textbox.png')
    textbox = pygame.transform.scale(textbox, (750, 130))
    sidebox = pygame.image.load('Pictures\sidebox.png')
    sidebox = pygame.transform.scale(sidebox, (150, 560))
    sideplayer1 = pygame.image.load('Pictures\side_player1.png')
    sideplayer1 = pygame.transform.scale(sideplayer1, (150, 115))
    sideplayer2 = pygame.image.load('Pictures\side_player2.png')
    sideplayer2 = pygame.transform.scale(sideplayer2, (150, 115))

    bgp1 = pygame.image.load('Pictures\\BGP\\1.jpeg')
    bgp1 = pygame.transform.scale(bgp1, (900, 560))
    bgp2 = pygame.image.load('Pictures\\BGP\\2.png')
    bgp2 = pygame.transform.scale(bgp2, (900, 560))
    grass = pygame.image.load('Pictures\\BGP\\grass.png')
    grass = pygame.transform.scale(grass, (1280, 720))

    auto_playing = pygame.image.load('Pictures\\icons\\auto_playing.png')
    auto_playing = pygame.transform.scale(auto_playing, (25, 25))
    chapter_background = pygame.image.load('Pictures\\icons\\Chapter_background.png')
    chapter_background = pygame.transform.scale(chapter_background, (170, 70))

    folder_path = 'Pictures\\Walls'
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('png', 'jpg', 'jpeg'))]
    wall_images = [pygame.image.load('Pictures\\Walls' + '\\' + file) for file in image_files]
    for walli in range(len(wall_images)):
        wall_images[walli] = pygame.transform.scale(wall_images[walli], (50,50))

    def __init__(self):
        pass