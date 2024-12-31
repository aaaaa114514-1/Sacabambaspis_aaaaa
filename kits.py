import pygame
import pygame_gui
from bgmplayer import BgmPlayer


'''
Kits:
    manager(UIManager):                     pygame_gui的manager
    bgmplayer(BgmPlayer):                   播放器
    mode(int):                              显示状态: 1-左上角竖排(gal_custom)
    quit_button(UIButton):                  退出界面按钮
    bag_button(UIButton):                   打开背包按钮
    volume_button(UIButton):                调整音量按钮
    volume_slider(UIHorizontalSlider):      调整音量拖条
    volume_slider_visible(bool):            音量拖条是否正在显示

    is_quiting():       -> bool             返回退出按钮是否按下
    check_bagging():                        检查并打开背包
    check_voluming():                       检查并显示/隐藏音量调整拖条
    slider_visible(is_show):                拖条切换为显示/隐藏
        is_show(bool):                      需要切换的目标状态
    check_adjusting_volume():               仅在显示拖条时更新音量

'''
class Kits:
    def __init__(self, manager:pygame_gui.UIManager, bgmplayer:BgmPlayer, mode:int):
        self.manager = manager
        self.bgmplayer = bgmplayer
        self.mode = mode
        if self.mode == 1:
            button_size = 55
            quit_lefttop = (10,10)
            bag_lefttop = (10,70)
            volume_lefttop = (10,130)
            slide_lefttop = (66,143)
            slide_size = (100,29)
        elif self.mode == 2:
            button_size = 50
            quit_lefttop = (771,258)
            bag_lefttop = (829,258)
            volume_lefttop = (771,315)
            slide_lefttop = (771,369)
            slide_size = (108,30)
        self.quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(quit_lefttop,(button_size, button_size)),text='Quit',manager=self.manager)
        self.bag_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(bag_lefttop,(button_size, button_size)),text='Bag',manager=self.manager)
        self.volume_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(volume_lefttop, (button_size, button_size)),text='Vol', manager=self.manager)
        self.volume_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(slide_lefttop, slide_size),start_value=self.bgmplayer.get_volume(),value_range=(0.0, 1.0),manager=self.manager)
        self.volume_slider_visible = False
        self.volume_slider.hide()

    def is_quiting(self):
        return self.quit_button.check_pressed()
    
    def check_bagging(self):
        if self.bag_button.check_pressed():
            pass
    
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




