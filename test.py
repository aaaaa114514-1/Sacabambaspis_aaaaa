import pygame
import pygame_gui

class VolumeControl:
    def __init__(self, screen):
        self.screen = screen
        self.manager = pygame_gui.UIManager(screen.get_size())
        
        # 按钮
        self.volume_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 50), (200, 50)),
                                                          text='音量设置', manager=self.manager)

        # 音量拖动条
        self.volume_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((50, 120), (200, 30)),
                                                                   start_value=1.0,
                                                                   value_range=(0.0, 1.0),
                                                                   manager=self.manager)
        self.volume_slider.hide()  # 初始时隐藏拖动条
        
        self.volume_slider_visible = False

    def show_slider(self):
        # 显示音量拖动条
        self.volume_slider.show()
        self.volume_slider_visible = True

    def hide_slider(self):
        # 隐藏音量拖动条
        self.volume_slider.hide()
        self.volume_slider_visible = False

    def adjust_volume(self):
        # 根据拖动条的值调整音量
        volume = self.volume_slider.get_current_value()
        pygame.mixer.music.set_volume(volume)

    def handle_event(self, event):
        self.manager.process_events(event)

    def update(self, time_delta):
        self.manager.update(time_delta)
        
        # 检查按钮是否被点击
        if self.volume_button.check_pressed():
            if not self.volume_slider_visible:
                self.show_slider()
            else:
                self.hide_slider()

        # 如果拖动条的值改变，更新音量
        self.adjust_volume()

    def draw(self):
        self.screen.fill((255, 255, 255))  # 清屏
        self.manager.draw_ui(self.screen)

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            time_delta = clock.tick(60) / 1000.0  # 设置帧率为60 FPS

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_event(event)

            self.update(time_delta)
            self.draw()
            pygame.display.update()

        pygame.quit()


# 初始化 pygame 和 pygame_gui
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('音量控制')
pygame.mixer.init()  # 初始化混音器

volume_control = VolumeControl(screen)
volume_control.run()
