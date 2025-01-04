import pygame
from load_picture import pictures

def fade_out(screen_image: pygame.Surface, dt:int=0.3):
    clock = pygame.time.Clock()
    alpha = 0
    fade_surface = pygame.Surface(screen_image.get_size())
    fade_surface.fill((0, 0, 0))
    picture = screen_image.copy()
    while alpha <= 255:
        clock.tick(int(128/dt))
        alpha += 2
        fade_surface.set_alpha(alpha)
        screen_image.blit(picture, (0, 0))
        screen_image.blit(fade_surface, (0, 0))
        pygame.display.flip()

def fade_in(screen_image: pygame.Surface, dt:int=0.3):
    clock = pygame.time.Clock()
    alpha = 255
    fade_surface = pygame.Surface(screen_image.get_size())
    fade_surface.fill((0, 0, 0))
    picture = screen_image.copy()
    while alpha >= 0:
        clock.tick(int(128/dt))
        alpha -= 2
        fade_surface.set_alpha(alpha)
        screen_image.blit(picture, (0, 0))
        screen_image.blit(fade_surface, (0, 0))
        pygame.display.flip()

def level_fade_in(screen_image: pygame.Surface, level_num:int, dt:int=2):
    clock = pygame.time.Clock()
    alpha = 255
    fade_surface = pygame.Surface(screen_image.get_size())
    fade_surface.fill((0, 0, 0))
    pygame.font.init()
    font = pygame.font.Font('Text\\xiangfont.ttf', 60)
    text_surface = font.render('Level ' + str(level_num), True, (255, 255, 255))
    level_namebox = pictures().level_namebox.copy()
    level_namebox.set_alpha(255)
    level_namebox.blit(text_surface, (225, 17))
    picture = screen_image.copy()
    while alpha >= 0:
        clock.tick(int(128/dt))
        alpha -= 2
        fade_surface.set_alpha(alpha)
        screen_image.blit(picture, (0, 0))
        screen_image.blit(level_namebox, (25, 230))
        screen_image.blit(fade_surface, (0, 0))
        pygame.display.flip()
    pygame.time.wait(500)
    alpha = 255
    while alpha >= 0:
        clock.tick(int(128/(dt/3)))
        alpha -= 2
        level_namebox.set_alpha(alpha)
        screen_image.blit(picture, (0, 0))
        screen_image.blit(level_namebox, (25, 230))
        pygame.display.flip()