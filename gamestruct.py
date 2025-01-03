import pygame
import sys
from account_setter import account_admin
from load_picture import pictures
import time
from bgmplayer import BgmPlayer
import opening
import login
import gal
import menu



pygame.init()
acer = account_admin()
pic = pictures

screen_image = pygame.display.set_mode((900,560))
pygame.display.set_caption('Soul Knight')
bgm = BgmPlayer()
bgm.play('Soul_Soil.mp3', -1)

opening.opening(screen_image)

username = login.login(screen_image)

user_resource = acer.get_resource(username)
if user_resource['has_read'] == 0:
    gal.gal(screen_image, username)
    user_resource['has_read'] = 1
    acer.update_resource(username, user_resource)

menu.menu(screen_image, username)


clock = pygame.time.Clock()
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
