import pygame
import sys
import time
from load_picture import pictures

def opening():
    pygame.init()

    screen_image = pygame.display.set_mode((900,560))

    pygame.display.set_caption('Soul Knight')

    pic = pictures

    screen_image.blit(pic.Soul_knight_background, (0, 0))

    clock = pygame.time.Clock()
    alpha = 0
    while alpha <= 256:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                alpha = 254
                time.sleep(0.2)
        alpha += 2
        pic.Title.set_alpha(alpha)
        screen_image.blit(pic.Soul_knight_background, (0, 0))
        screen_image.blit(pic.Title, (0, 300))
        pygame.display.flip()

    alpha = 0
    while alpha <= 256:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                alpha = 254
                time.sleep(0.2)
        alpha += 2
        pic.Author.set_alpha(alpha)
        screen_image.blit(pic.Soul_knight_background, (0, 0))
        screen_image.blit(pic.Title, (0, 300))
        screen_image.blit(pic.Author, (20, 0))
        pygame.display.flip()

    pygame.time.wait(1000)
    pygame.draw.rect(screen_image, (0,0,0), (0,0,900,560))
    pygame.display.flip()