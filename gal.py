import pygame
from bgmplayer import BgmPlayer
from load_picture import pictures
import sys
import os
import pygetwindow as gw


'''
text:
    font1(Font)             说话人字体(大)
    font2(Font)             对话字体(小)
    screen_image(Surface)   背景板
    chapter_background(Surface) 章节序号背景图
    textfile(str)           文本数据
    textbox(Surface)        文本框图
    progress(int)           文本进度
    speaker([str])          说话人列表
    dialogue([str])         对话列表
    username(str)           用户名
    Chapter(str)            章节名

    push_on() -> Bool               下一句,返回是否还有下一句
    get_text() -> [[str], [str]]    返回历史记录列表[[speaker],[dialogue]]
    show_scene()                    刷新文本框显示
'''
class text:
    pygame.font.init()
    font1 = pygame.font.Font('Text\\xiangfont.ttf', 30)
    font2 = pygame.font.Font('Text\\xiangfont.ttf', 25)
    def __init__(self, screen_image, chapter_background, textfile, textbox, username='I?'):
        self.screen_image = screen_image
        self.chapter_background = chapter_background
        self.textfile = textfile
        self.textbox = textbox
        self.progress = -1
        text_f = open(textfile, "r", encoding="UTF-8")
        self.speaker = []
        self.dialogue = []
        self.username = username
        self.Chapter = ''
        for lines in text_f:
            if lines.strip() != '':
                lines = lines.split()
                if lines[0] == 'Chapter':
                    self.Chapter = str(lines[0]) + ' ' + str(lines[1])
                elif len(lines) == 1:
                    self.speaker.append('')
                    self.dialogue.append(lines[0])
                elif len(lines) == 2:
                    if lines[0] == '0':
                        self.speaker.append(username)
                    else:
                        self.speaker.append(lines[0])
                    self.dialogue.append(lines[1])

    def push_on(self):
        if self.progress < len(self.dialogue) - 1 :
            self.progress += 1
            self.show_scene()
            return 1
        else:
            return 0

    def get_text(self):
        return [self.speaker[:self.progress+1], self.dialogue[:self.progress+1]]

    def show_scene(self):
        self.screen_image.blit(self.textbox, (75,420))
        now_text = self.font1.render(self.speaker[self.progress], True, (0, 0, 0))
        self.screen_image.blit(now_text, (80,421))
        now_text = self.font2.render(self.dialogue[self.progress], True, (0, 0, 0))
        if now_text.get_width() <= 690:
            self.screen_image.blit(now_text, (120,457))
        else:
            text_loca = int(len(self.dialogue[self.progress]) * 690 / now_text.get_width())
            now_text = self.font2.render(self.dialogue[self.progress][:text_loca], True, (0, 0, 0))
            self.screen_image.blit(now_text, (120,457))
            now_text = self.font2.render(self.dialogue[self.progress][text_loca:], True, (0, 0, 0))
            self.screen_image.blit(now_text, (120,490))
        self.screen_image.blit(self.chapter_background, (1,40))
        now_text = self.font1.render(self.Chapter, True, (255,255,255))
        self.screen_image.blit(now_text, (15,55))
        pygame.display.flip()



'''
history:
    screen_image(Surface)   背景板
    background_pic(Surface) 背景图
    font2(Font)             对话字体(小)
    speaker([str])          历史说话人
    dialogue([str])         历史对话
    page(int)               页数(页面顶部对话序号)

    into_history(his_text)      传入列表[[speaker],[dialogue]],初始化并进入历史记录模式
    page_up()                   向上翻页(如可行)
    page_down() -> Bool         向下翻页并返回1; 如不可翻页则退出历史记录模式并返回0
    show_history()              绘制历史记录模式界面
'''
class history:
    pygame.font.init()
    font2 = pygame.font.Font('Text\\xiangfont.ttf', 25)
    def __init__(self, screen_image, background_pic, his_text=[[],[]]):
        self.background_pic = background_pic
        self.screen_image = screen_image
        self.speaker = his_text[0]
        self.dialogue = his_text[1]
        self.page = max(len(self.dialogue) - 4, 0)

    def into_history(self, his_text):
        self.speaker = his_text[0]
        self.dialogue = his_text[1]
        self.page = max(len(self.dialogue) - 4, 0)
        self.show_history()

    def page_up(self):
        if self.page > 0:
            self.page -= 1
            self.show_history()

    def page_down(self):
        if self.page + 4 < len(self.dialogue):
            self.page += 1
            self.show_history()
            return 1
        else:
            return 0

    def show_history(self):
        self.screen_image.blit(self.background_pic, (0,0))
        rect_surface = pygame.Surface((900, 560), pygame.SRCALPHA)
        rect_surface.fill((0, 0, 0, 150))
        self.screen_image.blit(rect_surface, (0, 0))
        for text_i in range(min(len(self.dialogue),4)):
            if self.speaker[self.page + text_i] == '':
                line = self.dialogue[self.page + text_i]
            else:
                line = f'{self.speaker[self.page + text_i]}: {self.dialogue[self.page + text_i]}'
            now_text = self.font2.render(line, True, (255, 255, 255))
            if now_text.get_width() <= 750:
                self.screen_image.blit(now_text, (80, 120*text_i+90))
            else:
                text_loca = int(len(line) * 750 / now_text.get_width())
                now_text = self.font2.render(line[:text_loca], True, (255, 255, 255))
                self.screen_image.blit(now_text, (80, 120*text_i+90))
                now_text = self.font2.render(line[text_loca:], True, (255, 255, 255))
                self.screen_image.blit(now_text, (80, 120*text_i+130))
        pygame.display.flip()







def gal():
    pygame.init()
    screen_image = pygame.display.set_mode((900,560))
    screen_rect = screen_image.get_rect()
    pygame.display.set_caption('Soul Knight')

    pic = pictures()
    screen_image.blit(pic.Soul_knight_background, (0,0))
    screen_image.blit(pic.textbox, (75,420))
    pygame.display.flip()

    bgm = BgmPlayer()
    bgm.play('1.mp3',-1)

    text0 = text(screen_image, pic.chapter_background, 'Text\\Chapter0.txt', pic.textbox, 'aaaaa')
    history0 = history(screen_image, pic.Soul_knight_background)

    def minimize_window():
        window = gw.getWindowsWithTitle('Soul Knight')[0]
        window.minimize()

    def flapper():
        screen_image.blit(pic.Soul_knight_background, (0,0))
        text0.show_scene()
        pygame.display.flip()

    clock = pygame.time.Clock()
    gal_running = 1
    is_history = 0
    is_auto = 0
    timeset = 0
    text0.push_on()
    while gal_running:
        clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and is_history == 0:
                gal_running = text0.push_on()
                if is_auto == 1:
                    timeset = pygame.time.get_ticks()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if is_auto != 0:
                        screen_image.blit(pic.Soul_knight_background, (0,0))
                        text0.show_scene()
                        pygame.display.flip()
                        is_auto = 0
                    elif is_history == 0:
                        bgm.pause()
                        minimize_window()
                        os.startfile('Pictures\K_Boss.pdf')
                    else:
                        is_history = 0
                        flapper()

                elif event.key == pygame.K_SPACE and is_history == 0:
                    gal_running = text0.push_on()
                    if is_auto == 1:
                        timeset = pygame.time.get_ticks()
                elif (event.key == pygame.K_a or event.key == pygame.K_F6) and is_history == 0:
                    if is_auto == 0:
                        screen_image.blit(pic.auto_playing, (10,10))
                        pygame.display.flip()
                        is_auto = 1
                        timeset = pygame.time.get_ticks() - 4000
                    else:
                        flapper()
                        is_auto = 0


            elif event.type == pygame.MOUSEWHEEL:
                if is_history == 0:
                    if event.y > 0 and is_auto == 0:
                        is_history = 1
                        history0.into_history(text0.get_text())
                    elif event.y < 0:
                        gal_running = text0.push_on()
                        if is_auto == 1:
                            timeset = pygame.time.get_ticks()
                else:
                    if event.y > 0:
                        history0.page_up()
                    elif event.y < 0:
                        is_history = history0.page_down()
                        if is_history == 0:
                            flapper()

        if pygame.time.get_ticks() - timeset >= 2500 and is_auto == 1:
            timeset = pygame.time.get_ticks()
            gal_running = text0.push_on()

        if pygame.display.get_active():
            bgm.unpause()
        else:
            bgm.pause()

        keypressed = pygame.key.get_pressed()
        if keypressed[pygame.K_LCTRL] and is_history == 0 and is_auto == 0:
            gal_running = text0.push_on()

if __name__ == '__main__':
    gal()