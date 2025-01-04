import pygame
import time
from load_picture import pictures

'''
opening(screen_image):                  开场动画
    screen_image(Surface):                  屏幕图像
'''
def opening(screen_image:pygame.Surface):
    pygame.init()
    pic = pictures()
    screen_image.blit(pic.Soul_knight_background, (0, 0))

    clock = pygame.time.Clock()
    alpha = 0
    while alpha <= 256:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
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
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                alpha = 254
                time.sleep(0.2)
        alpha += 2
        pic.Author.set_alpha(alpha)
        screen_image.blit(pic.Soul_knight_background, (0, 0))
        screen_image.blit(pic.Title, (0, 300))
        screen_image.blit(pic.Author, (20, 0))
        pygame.display.flip()



if __name__ == '__main__':
    screen_image = pygame.display.set_mode((900, 560))
    pygame.display.set_caption('Soul Knight')
    opening(screen_image)