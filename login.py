import pygame
import pygame_gui
from load_picture import pictures as pic
import hashlib
import os



def login():
    """
    hash_data(data):   -> str       使用SHA-256算法对输入数据进行哈希加密
        data(str):                  需要加密的数据
    """
    def hash_data(data: str) -> str:
        sha256_hash = hashlib.sha256()
        sha256_hash.update(data.encode('utf-8'))
        return sha256_hash.hexdigest()

    pygame.init()
    pygame.display.set_caption("Soul Knight")

    WINDOW_SIZE = (900, 560)
    screen_image = pygame.display.set_mode(WINDOW_SIZE)
    font = pygame.font.Font('Text\\xiangfont.ttf', 60)


    manager = pygame_gui.UIManager(WINDOW_SIZE)

    DXY = [-160,80]
    username_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(150+DXY[0], 200+DXY[1], 200, 50), text="Username:", manager=manager)
    password_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(150+DXY[0], 260+DXY[1], 200, 50), text="Password:", manager=manager)

    username_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(350+DXY[0], 200+DXY[1], 200, 50), manager=manager)
    password_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(350+DXY[0], 260+DXY[1], 200, 50), manager=manager)

    login_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(330+DXY[0], 350+DXY[1], 100, 50), text="Sign in", manager=manager)
    register_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(480+DXY[0], 350+DXY[1], 100, 50), text="Register", manager=manager)

    status_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(250+DXY[0], 410+DXY[1], 400, 50), text="", manager=manager)

    text_f = open('Text\Accounts.txt', "r", encoding="UTF-8")
    user_data = dict()
    for line in text_f:
        user_data[line.split()[0]] = line.split()[1]

    running = True
    clock = pygame.time.Clock()
    while running:
        delta_time = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            manager.process_events(event)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == login_button:
                        username = username_input.get_text()
                        password = password_input.get_text()

                        if username in user_data and user_data[username] == hash_data(password):
                            status_label.set_text(f"Welcome, {username} !")
                        else:
                            status_label.set_text("Incorrect username or password")
                            print(user_data)
                            print(hash_data(password))
                            password_input.clear()

                    elif event.ui_element == register_button:
                        username = username_input.get_text()
                        password = password_input.get_text()

                        if username not in user_data:
                            user_data[username] = hash_data(password)
                            f = open(f'Text\Accounts.txt', "a", encoding="UTF-8")
                            f.write(f'{username}\t{hash_data(password)}\n')
                            f.close()
                            os.mkdir(f'Text\\Accounts\\{username}')
                            password_input.clear()
                            status_label.set_text("Register successfully!")
                        else:
                            status_label.set_text("The username already exists")

        manager.update(delta_time)
        screen_image.blit(pic.Soul_knight_background2,(0,0))
        login_text = font.render('Log in', True, (255, 255, 255))
        screen_image.blit(login_text, (190,170))
        manager.draw_ui(screen_image)

        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    login()