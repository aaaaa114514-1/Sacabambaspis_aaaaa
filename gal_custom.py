import pygame
import pygame_gui
import sys
import os
import pygetwindow as gw
from bgmplayer import BgmPlayer
from ai_iosetter import npc_dia
from kits import Kits
from account_setter import account_admin

'''
Inputbox:
    screen_image(Surface):      背景板
    manager(UIManager):         pygame_gui的manager
    input_box(UITextEntryLine): 输入框
    submit_button(UIButton):    提交按钮

    get_and_clear():  -> str    获取输入框信息并返回, 同时清空输入框(若为空则不操作)
    check_empty():              检验输入框是否为空, 并更新提交按钮状态
    is_pressed():   -> bool     返回按钮是否被按下
    set_button(is_able):        设置按钮状态与显示
        is_able(bool):              目标状态: 0-禁用 1-启用
    set_inputbox(is_able):      设置输入框状态
        is_able(bool):              目标状态: 0-禁用 1-启用

'''
class Inputbox:
    pygame.init()

    def __init__(self, screen:pygame.Surface, manager:pygame_gui.UIManager):
        self.screen_image = screen
        self.manager = manager
        self.input_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((75, 515), (645, 40)),manager=self.manager)
        self.submit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((725, 515), (100, 40)),text='Enter',manager=self.manager)
        self.manager.set_focus_set(self.input_box)
        self.set_button(0)

    def get_and_clear(self):
        text = self.input_box.get_text()
        if text != '':
            self.input_box.clear()
            self.manager.set_focus_set(self.input_box)
            self.set_button(0)
            return text
        else:
            return 0

    def check_empty(self):
        if self.input_box.get_text() == '':
            self.set_button(0)
        else:
            self.set_button(1)

    def is_pressed(self):
        return self.submit_button.check_pressed()
    
    def set_button(self, is_able:bool):
        if is_able:
            self.submit_button.is_enabled = True
            self.submit_button.normal_bg_color = (100, 100, 100)
            self.submit_button.hovered_bg_color = (0, 100, 200)
        else:
            self.submit_button.is_enabled = False
            self.submit_button.normal_bg_color = (150, 150, 150)
            self.submit_button.hovered_bg_color = (150, 150, 150)

    def set_inputbox(self, is_able:bool):
        self.input_box.is_enabled = is_able


'''
Textbox:
    content([str]):         内容, 每个元素之间空1行
    textbox(UITextBox):     文本框

    append_text(add_speaker, add_dialogue):     把内容打印在文本框里(说话人和内容之间换行), 并自动翻页至底部
        add_speaker(str):                           说话人
        add_dialogue(str):                          对话内容
'''

class Textbox:
    def __init__(self, content:list[str], manager:pygame_gui.UIManager):
        self.content = [content]
        self.textbox = pygame_gui.elements.UITextBox(html_text=self.content[0], relative_rect=pygame.Rect((75, 10), (750, 500)), manager=manager)

    def append_text(self, add_speaker, add_dialogue):
        self.content.append(f'<font color="grey">{add_speaker}</font>\n>> {add_dialogue}')
        self.textbox.set_text('\n\n'.join(self.content))
        try:
            self.textbox.scroll_bar.set_scroll_from_start_percentage(1)
        except: pass


'''
gal_custom(screen_image, username, npcname, bgm):       实时对话模式
    screen_image(Surface):                                  屏幕图像
    username(str):                                          用户名
    npcname(str):                                           npc名字
    bgm(<BgmPlayer>):                                       bgmplayer
'''
def gal_custom(screen_image:pygame.Surface, username:str, npcname:str, bgm:BgmPlayer):
    pygame.init()
    screen_image.fill((0,0,0))
    manager = pygame_gui.UIManager((900, 560))
    acer = account_admin()

    inputbox_0 = Inputbox(screen_image, manager)
    npc_0 = npc_dia(npcname, username)
    textbox_0 = Textbox(f'Chat with {npc_0.name}\n'+'-'*140, manager)

    kits_0 = Kits(screen_image, manager, bgm, 1)

    clock = pygame.time.Clock()
    pygame.display.flip()
    while True:
        time_delta = clock.tick(30) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                acer.clear_empty_dialogues(username)
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    newtext = inputbox_0.get_and_clear()
                    if newtext:
                        textbox_0.append_text(username, newtext)
                        manager.update(time_delta)
                        manager.draw_ui(screen_image)
                        pygame.display.flip()
                        inputbox_0.set_inputbox(0)
                        textbox_0.append_text(npc_0.name, npc_0.talk(newtext))
                        inputbox_0.set_inputbox(1)


                if event.key == pygame.K_ESCAPE:
                    acer.clear_empty_dialogues(username)
                    return 0
                
            manager.process_events(event)

        if inputbox_0.is_pressed():
            newtext = inputbox_0.get_and_clear()
            if newtext:
                textbox_0.append_text(username, newtext)
                manager.update(time_delta)
                manager.draw_ui(screen_image)
                pygame.display.flip()
                inputbox_0.set_inputbox(0)
                textbox_0.append_text(npc_0.name, npc_0.talk(newtext))
                inputbox_0.set_inputbox(1)

        if kits_0.is_quiting():
            acer.clear_empty_dialogues(username)
            return 0

        inputbox_0.check_empty()
        kits_0.check_bagging(username)
        kits_0.check_voluming()
        kits_0.check_adjusting_volume()
        manager.update(time_delta)
        screen_image.fill((0,0,0))
        manager.draw_ui(screen_image)
        pygame.display.flip()


if __name__ == '__main__':
    screen_image = pygame.display.set_mode((900, 560))
    pygame.display.set_caption('Soul Knight')
    bgm = BgmPlayer()
    bgm.play('Soul_Soil.mp3',-1)
    gal_custom(screen_image,'aaaaa','Bob', bgm)