import pygame
import sys
import time
import opening
import menu

pygame.init()

screen_image = pygame.display.set_mode((900,560))
screen_rect = screen_image.get_rect()

opening.opening()
menu.menu()

clock = pygame.time.Clock()


while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
