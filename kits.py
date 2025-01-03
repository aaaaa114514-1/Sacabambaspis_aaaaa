import pygame
import pygame_gui
from bgmplayer import BgmPlayer
from account_setter import account_admin
from shopkeeper import shopkeeper
from load_picture import pictures
import sys

'''
Kits:
    manager(UIManager):                     pygame_gui的manager
    bgmplayer(BgmPlayer):                   播放器
    mode(int):                              显示状态: 1-左上角竖排(gal_custom) 2-右下角矩形排列(fight) 3-右下角矩形排列(menu)
    quit_button(UIButton):                  退出界面按钮
    bag_button(UIButton):                   打开背包按钮
    volume_button(UIButton):                调整音量按钮
    volume_slider(UIHorizontalSlider):      调整音量拖条
    volume_slider_visible(bool):            音量拖条是否正在显示
    screen_image(pygame.Surface):           屏幕图像
    onshow(list):                           显示的按钮列表
    font(Font):                             字体
    acer(account_admin):                    账户管理器
    shopkeeper_0(shopkeeper):               商店管理器
    pic(pictures):                          图片加载器
    label_lefttop(tuple):                   标签位置
    Soulstone_b_lefttop(tuple):             灵魂石标签位置
    Soulstone_lefttop(tuple):               灵魂石数字位置

    is_quiting():       -> bool             返回退出按钮是否按下
    check_bagging():                        检查并打开背包
    check_voluming():                       检查并显示/隐藏音量调整拖条
    slider_visible(is_show):                拖条切换为显示/隐藏
        is_show(bool):                          需要切换的目标状态
    check_adjusting_volume():               仅在显示拖条时更新音量
    set_label(text):                        设置标签
        text(str):                              标签内容
    show_Soulstone(username):               显示灵魂石
        username(str):                          用户名
    bag(username):                          打开背包
        username(str):                          用户名

'''
class Kits:
    def __init__(self, screen_image:pygame.Surface, manager:pygame_gui.UIManager, bgmplayer:BgmPlayer, mode:int, onshow:list=None):
        self.screen_image = screen_image
        self.manager = manager
        self.bgmplayer = bgmplayer
        self.mode = mode
        if onshow != None:
            self.onshow = onshow
        else:
            self.onshow = ['quit','bag','volume','logout']
        self.font = pygame.font.SysFont('Arial', 15)
        self.acer = account_admin()
        self.shopkeeper_0 = shopkeeper()
        self.pic = pictures()
        if self.mode == 1:
            button_size = 55
            quit_lefttop = (10,10)
            bag_lefttop = (10,70)
            volume_lefttop = (10,130)
            slide_lefttop = (66,143)
            slide_size = (100,29)
            logout_lefttop = -1
            self.label_lefttop = -1
            self.Soulstone_b_lefttop = (10,190)
            self.Soulstone_lefttop = (10,210)
        elif self.mode == 2:
            button_size = 50
            quit_lefttop = (771,258)
            bag_lefttop = (829,258)
            volume_lefttop = (829,258)
            slide_lefttop = (771,315)
            slide_size = (108,30)
            logout_lefttop = -1
            self.label_lefttop = (767,400)
            self.Soulstone_lefttop = -1
        elif self.mode == 3:
            button_size = 50
            bag_lefttop = (829,258)
            volume_lefttop = (771,312)
            slide_lefttop = (771,366)
            slide_size = (108,30)
            logout_lefttop = (771,258)
            self.label_lefttop = (767,400)
            self.Soulstone_b_lefttop = (767,430)
            self.Soulstone_lefttop = (832,430)
        if 'quit' in self.onshow:
            self.quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(quit_lefttop,(button_size, button_size)),text='Quit',manager=self.manager)
        if 'bag' in self.onshow:
            self.bag_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(bag_lefttop,(button_size, button_size)),text='Bag',manager=self.manager)
        if 'volume' in self.onshow:
            self.volume_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(volume_lefttop, (button_size, button_size)),text='Vol', manager=self.manager)
            self.volume_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(slide_lefttop, slide_size),start_value=self.bgmplayer.get_volume(),value_range=(0.0, 1.0),manager=self.manager)
        if 'logout' in self.onshow:
            self.logout_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(logout_lefttop, (button_size, button_size)),text='Logout',manager=self.manager)
        if self.label_lefttop != -1:
            self.label_text = self.font.render('',True,(0,0,0))
        if self.Soulstone_lefttop != -1:
            self.Soulstone_text_b = self.font.render('Soulstone:',True,(100,100,255))
            self.Soulstone_text = self.font.render('',True,(100,100,255))
        self.volume_slider_visible = False
        self.volume_slider.hide()

    def is_quiting(self):
        return self.quit_button.check_pressed()
    
    def is_logout(self):
        return self.logout_button.check_pressed()
    
    def check_bagging(self,username):
        if self.bag_button.check_pressed():
            self.bag(username)
            return 1
        else:
            return 0
    
    def check_voluming(self):
        if self.volume_button.check_pressed():
            if not self.volume_slider_visible:
                self.slider_visible(1)
            else:
                self.slider_visible(0)

    def slider_visible(self, is_show:bool):
        if is_show == 1:
            self.volume_slider.show()
            self.volume_slider_visible = True
        else:
            self.volume_slider.hide()
            self.volume_slider_visible = False

    def check_adjusting_volume(self):
        if self.volume_slider_visible == True:
            volume = self.volume_slider.get_current_value()
            self.bgmplayer.set_volume(volume)

    def set_label(self, text:str):
        self.label_text = self.font.render(text,True,(0,0,0))
        self.screen_image.blit(self.label_text, self.label_lefttop)

    def show_Soulstone(self, username:str):
        userinfo = self.acer.get_resource(username)
        self.Soulstone_text = self.font.render(str(userinfo["Soulstone"]),True,(100,100,255))
        self.screen_image.blit(self.Soulstone_text_b, self.Soulstone_b_lefttop)
        self.screen_image.blit(self.Soulstone_text, self.Soulstone_lefttop)

    def bag(self, username:str):
        manager = pygame_gui.UIManager((900,560))
        font = pygame.font.Font(None, 15)
        userinfo = self.acer.get_resource(username)
        is_bagging = 1
        rect_surface = pygame.Surface((900, 560), pygame.SRCALPHA)
        rect_surface.fill((0, 0, 0, 150))
        bag_window_b = pygame.Surface((560, 360))
        bag_window_b.fill((0, 0, 0))
        bag_window = pygame.Surface((556,338))
        bag_window.fill((150,150,150))
        quitbag_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((710,90),(20, 20)),text='X',manager=manager)

        rect_width = 90
        rect_height = 130
        default_color = (200, 200, 200)
        selected_color = (100, 100, 100)
        weapons = []
        selected = ['','']
        bullet_pics = {'Original_gun':self.pic.bullet0_big, 'Soul_gun':self.pic.bullet1_big, 'Firing_gun':self.pic.bullet2_big, 'Infinite_magic':self.pic.bullet3_big, 'Infinite_firepower':self.pic.bullet4_big}

        for i in self.shopkeeper_0.pricetable.keys():
            if userinfo[i] != 0 and i in ['Original_gun', 'Soul_gun', 'Firing_gun', 'Infinite_magic', 'Infinite_firepower']:
                weapons.append(i)
                if userinfo[i] == -3:
                    selected = [i,i]
                elif userinfo[i] == -1:
                    selected[0] = i
                elif userinfo[i] == -2:
                    selected[1] = i

        def draw_option(is_selected:bool, rect:pygame.Rect, image:pygame.Surface, text:str):
            textf = font.render(text, True, (0, 0, 0))
            text_rect = textf.get_rect(center=(rect.centerx, rect.bottom-10))
            image_rect = image.get_rect(center=(rect.centerx, rect.bottom-70))
            if is_selected:
                pygame.draw.rect(bag_window, selected_color, rect)
            else:
                pygame.draw.rect(bag_window, default_color, rect)
            bag_window.blit(image, image_rect)
            bag_window.blit(textf, text_rect)

        def exit_bag():
            for weapon in userinfo.keys():
                if weapon in ['Original_gun', 'Soul_gun', 'Firing_gun', 'Infinite_magic', 'Infinite_firepower'] and userinfo[weapon] != 0:
                    if selected[0] == weapon:
                        userinfo[weapon] = -1
                        if selected[1] == weapon:
                            userinfo[weapon] = -3
                    elif selected[1] == weapon:
                        userinfo[weapon] = -2
                    else:
                        userinfo[weapon] = 1
            self.acer.update_resource(username, userinfo)
        
        rects = [[],[]]
        for i in range(len(weapons)):
            rects[0].append(pygame.Rect(80+i*95, 10, rect_width, rect_height))
            rects[1].append(pygame.Rect(80+i*95, 160, rect_width, rect_height))
        

        clock = pygame.time.Clock()
        while is_bagging:
            time_delta = clock.tick(50) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_bag()
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if not pygame.rect.Rect(170,90,560,360).collidepoint(mouse_pos):
                        exit_bag()
                        return 1
                    mouse_pos = (mouse_pos[0]-172,mouse_pos[1]-110)
                    for layer in range(2):
                        for i, rect in enumerate(rects[layer]):
                            if rect.collidepoint(mouse_pos):
                                selected[layer] = weapons[i]

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        exit_bag()
                        return 1
                    if event.key == pygame.K_a:
                        selected[0] = weapons[(weapons.index(selected[0])- 1) % len(rects[0])]
                    elif event.key == pygame.K_d:
                        selected[0] = weapons[(weapons.index(selected[0]) + 1) % len(rects[0])]
                    if event.key == pygame.K_LEFT:
                        selected[1] = weapons[(weapons.index(selected[1])- 1) % len(rects[1])]
                    elif event.key == pygame.K_RIGHT:
                        selected[1] = weapons[(weapons.index(selected[1]) + 1) % len(rects[1])]
                
                manager.process_events(event)
            
            self.screen_image.blit(bag_window_b, (170, 90))
            self.screen_image.blit(bag_window, (172,110))
            bag_window.blit(self.pic.Knight[1][0],(20,50))
            bag_window.blit(self.pic.Knightress[1][0],(20,200))
            for layer in range(2):
                for i in range(len(rects[layer])):
                    draw_option(weapons[i]==selected[layer], rects[layer][i], bullet_pics[weapons[i]], weapons[i])

            manager.update(time_delta)
            manager.draw_ui(self.screen_image)

            pygame.display.flip()

            if quitbag_button.check_pressed():
                exit_bag()
                return 1


