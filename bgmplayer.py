import pygame

'''
BgmPlayer:
    load(bgmfile(str)):                     加载文件(文件名)
    play(bgmfile(str)=None, loops(int)=0):  播放    bgmfile:文件名    loops: -1:无限循环, n:播放n+1次
    stop():                                 停止播放
    pause():                                暂停播放
    unpause():                              继续播放
    is_playing():                           返回播放状态: 1:正在播放, 0:未在播放
'''

class BgmPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.clock = pygame.time.Clock()

    def load(self, bgmfile):
        pygame.mixer.music.load('BGM\\' + bgmfile)

    def play(self, bgmfile = None, loops = 0):
        if bgmfile != None:
            pygame.mixer.music.load('BGM\\' + bgmfile)
        pygame.mixer.music.play(loops = loops)

    def stop(self):
        pygame.mixer.music.stop()

    def pause(self):
        if self.is_playing():
            pygame.mixer.music.pause()

    def unpause(self):
        if not self.is_playing():
            pygame.mixer.music.unpause()

    def is_playing(self):
        return pygame.mixer.music.get_busy()

    def tick(self):
        self.clock.tick(10)

