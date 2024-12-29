import pygame
import sys
import time
import opening
import login
import gal
import menu

pygame.init()

screen_image = pygame.display.set_mode((900,560))
pygame.display.set_caption('Soul Knight')

opening.opening(screen_image)
username = login.login(screen_image)
user_resource = dict()

with open(f'Text\\Accounts\\{username}\\account_resource.txt', 'r') as f:
    for line in f:
        user_resource[line.split()[0]] = int(line.split()[1])
if user_resource['has_read'] == 0:
    gal.gal(screen_image, username)
    user_resource['has_read'] = 1
    with open (f'Text\\Accounts\\{username}\\account_resource.txt', 'w') as f:
        f.write('Soulstone   100\nhas_read   1')

menu.menu(screen_image)

clock = pygame.time.Clock()


while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
