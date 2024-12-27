import pygame
import pygame_gui
import sys

pygame.init()

class PaginatedTextBox:
    def __init__(self, screen, manager):
        self.screen = screen
        self.manager = manager
        
        # 创建一个文本框来显示长文本
        self.textbox = pygame_gui.elements.UITextBox(
            html_text="This is a long text that will need scrolling. " * 10, 
            relative_rect=pygame.Rect((50, 50), (700, 300)), 
            manager=manager
        )
        
        # 创建滚动条
        self.scrollbar = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((50, 370), (700, 20)),
            start_value=0.0,
            value_range=(0.0, 1.0),
            manager=manager
        )

    def update_scroll(self):
        # 更新文本框的显示区域，通过滚动条的值来调整
        scroll_value = self.scrollbar.get_current_value()
        content_height = self.textbox.get_content_height()
        visible_height = self.textbox.relative_rect.height
        
        # 根据滚动条的值来计算文本框的顶部位置
        offset = (content_height - visible_height) * scroll_value
        self.textbox.set_text_offset((0, -offset))

    def draw(self):
        # 绘制所有 UI 元素
        self.manager.draw_ui(self.screen)

    def process_events(self, event):
        # 处理事件
        self.manager.process_events(event)
    
    def update(self, timedelta):
        # 更新 UI
        self.manager.update(timedelta)

def main():
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Scrollable Text Box Example")
    manager = pygame_gui.UIManager((800, 600))  # 禁用翻译功能
    
    # 创建可翻页的文本框
    paginated_text_box = PaginatedTextBox(screen, manager)
    
    clock = pygame.time.Clock()
    running = True
    while running:
        time_delta = clock.tick(30) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            paginated_text_box.process_events(event)
        
        # 更新滚动条
        paginated_text_box.update_scroll()
        
        # 更新界面
        screen.fill((255, 255, 255))
        paginated_text_box.draw()
        
        pygame.display.flip()
        paginated_text_box.update(time_delta)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
