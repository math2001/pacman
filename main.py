import pygame
from pygame.locals import *
from time import time
from utils import EventManager

from test import Test
from game import Game
from utils import Screen

class App:
    def __init__(self):
        self.set_mode((28 * 20, 31 * 20))
        self.done = False
        self.font = pygame.font.SysFont("Consolas", 14)
        self.clock = pygame.time.Clock()
        self.max_fps = 60
        self.debug = True

        self.scenes = {
            "test": Test,
            "game": Game,
        }

        self.switch_scene("game", "shortest path", "user")

        EventManager.on("quit", self.quit)
        EventManager.on("set mode", self.set_mode)
        EventManager.on("switch scene", self.switch_scene)

    def set_mode(self, *args, **kwargs):
        self.window = pygame.display.set_mode(*args, **kwargs)
        Screen.update()

    def switch_scene(self, scene, *args, **kwargs):
        self.scene = self.scenes[scene](*args, **kwargs)
        return self.scene
    
    def quit(self):
        self.done = True
    
    def show_debug_infos(self):
        fps = round(self.clock.get_fps())
        text = self.font.render(" {} {:2} fps ".format(self.scene.debug_string(), fps), True, pygame.Color("grey"), pygame.Color(0, 0, 0))
        rect = text.get_rect(bottomright=Screen.rect.bottomright)
        Screen.surface.blit(text, rect)
    
    def mainloop(self):
        ''' the basic main loop, handling forceful quit (when the user double
        clicks the close button)'''
        last_quit = 0
        while not self.done:
            self.clock.tick(self.max_fps)
            for event in pygame.event.get():
                if event.type == QUIT:
                    if time() - last_quit < 1:
                        print("Forcefully quiting")
                        return
                    last_quit = time()
                self.scene.handle_event(event)
            Screen.surface.fill(0)
            self.scene.update()
            self.scene.render(Screen.surface)
            if self.debug:
                self.show_debug_infos()
            pygame.display.flip()
    
def main():
    pygame.init()
    App().mainloop()
    pygame.quit()
    
if __name__ == '__main__':
    main()