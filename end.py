from pygame.locals import *
from scene import Scene
from utils import *

class End(Scene):

    def __init__(self, winner, pacman_strategy, ghosts_strategy):
        super().__init__()
        self.winner = winner
        self.pacman_strategy = pacman_strategy
        self.ghosts_strategy = ghosts_strategy

        EventManager.emit('set mode', (640, 480))

    def handle_event(self, e):
        super().handle_event(e)
        if e.type == KEYDOWN or (e.type == MOUSEBUTTONDOWN and e.button == 1):
            EventManager.emit('switch scene', 'menu')

    def render(self, surf, srect):
        with fontedit(self.fonts.fancy, size=40) as font:
            text = f'the {self.winner} won!'
            r = font.get_rect(text)
            r.center = srect.center
            r.top -= 100
            font.render_to(surf, r, text)
            bottom = r.bottom

        with fontedit(self.fonts.mono, size=15) as font:
            a, b = self.pacman_strategy, self.ghosts_strategy
            if self.winner == 'ghosts':
                a, b = b, a
            text = f'{a!r} seems to beat {b!r}'
            r = font.get_rect(text)
            r.midtop = srect.centerx, bottom + 40
            font.render_to(surf, r, text)

        with fontedit(self.fonts.mono) as font:
            text = 'Click to go back to the menu'
            r = font.get_rect(text)
            r.midbottom = srect.centerx, srect.bottom - 20
            font.render_to(surf, r, text)