# TODO: add error screen on exception
# TODO: transition between scenes

import pygame
from pygame.locals import *
from collections import namedtuple
from time import time
from utils import *

from scene import Scene
from test import Test
from game import Game
from menu import Menu
from end import End
from utils import Screen

fonts = namedtuple('Fonts', 'fancy arcade mono')(
    pygame.freetype.Font('fonts/ka1.ttf', 20),
    pygame.freetype.Font('fonts/arcade.ttf', 14),
    pygame.freetype.Font('fonts/firamono.ttf', 12)
)

for font in fonts:
    font.fgcolor = WHITE

class App:
    def __init__(self):
        EventManager.on("quit", self.quit)
        EventManager.on("set mode", self.set_mode)
        EventManager.on("switch scene", self.switch_scene)

        self.done = False
        self.clock = pygame.time.Clock()
        self.max_fps = 40
        self.debug = True
        self.scene = None

        self.scenes = {
            'test': Test,
            'game': Game,
            'menu': Menu,
            'end': End
        }

        Scene.fonts = fonts

        EventManager.emit('set mode', (640, 480))
        EventManager.emit('switch scene', 'menu')

        pygame.key.set_repeat(400, 50)
        pygame.display.set_caption('Pacman')

    def set_mode(self, *args, **kwargs):
        self.window = pygame.display.set_mode(*args, **kwargs)
        Screen.update()

    def switch_scene(self, scene, *args, **kwargs):
        if self.scene is not None:
            self.scene.done()
        self.scene = self.scenes[scene](*args, **kwargs)
        return self.scene
    
    def quit(self):
        self.done = True
    
    def show_debug_infos(self):
        text = f"{self.scene.debug_string()} " \
               f"{classname(self.scene)} " \
               f"{round(self.clock.get_fps()):2} fps"
        rect = fonts.mono.get_rect(text)
        rect.bottomright = Screen.rect.bottomright
        fonts.mono.render_to(Screen.surface, rect, text, fgcolor=WHITE,
                                   bgcolor=BLACK)
    
    def mainloop(self):
        ''' the basic main loop, handling forceful quit (when the user double
        clicks the close button) '''
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
            Screen.surface.fill(BLACK)
            self.scene.update()
            self.scene.render(Screen.surface, Screen.rect)
            if self.debug:
                self.show_debug_infos()
            pygame.display.flip()
    
def main():
    pygame.init()
    App().mainloop()
    pygame.quit()
    
if __name__ == '__main__':
    main()