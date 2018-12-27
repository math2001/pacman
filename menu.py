from pygame.locals import *
from scene import Scene
from utils import *
from strategies import ghost_strategies, pacman_strategies
from collections import namedtuple

Sprite = namedtuple('Sprite', 'surf rect')

class Menu(Scene):

    def __init__(self):
        super().__init__()

        text = 'Go!'
        with fontedit(self.fonts.fancy, size=30) as font:
            self.go = Sprite(*font.render(text))
            self.go.rect.bottom = Screen.rect.bottom - 30
            self.go.rect.centerx = Screen.rect.centerx

    def handle_event(self, e):
        super().handle_event(e)
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            if self.go.rect.collidepoint(e.pos):
                # TODO: find out the 2 strategies
                # TODO: no strategy selected = error message
                EventManager.emit('switch scene', 'game')

    def render(self, surface, rect):

        text = 'PACMAN'
        with fontedit(self.fonts.fancy, size=50) as font:
            r = font.get_rect(text)
            r.midtop = rect.midtop
            r.top += 40
            font.render_to(surface, r, text, fgcolor=WHITE)

            title_bottom = r.bottom

        text = 'Pacman strategy'
        column_width = 300
        padding = 20 # between the 2 columns
        with fontedit(self.fonts.arcade, size=30) as font:
            r = font.get_rect(text)
            r.top = title_bottom + 50
            r.centerx = rect.centerx - column_width / 2 - padding / 2
            font.render_to(surface, r, text)
            catego_bottom = r.bottom
            left = r.left

        # pacman strategies
        with fontedit(self.fonts.arcade, size=20) as font:
            bottom = catego_bottom + 20
            for name in pacman_strategies:
                r = font.get_rect(name)
                r.top = bottom
                r.left = left + 10
                font.render_to(surface, r, name)
                bottom += r.height + 10


        text = 'Ghost strategy'
        with fontedit(self.fonts.arcade, size=30) as font:
            r = font.get_rect(text)
            r.top = title_bottom + 50
            r.centerx = rect.centerx + column_width / 2 + padding / 2
            left = r.left
            font.render_to(surface, r, text)

        # ghost strategies
        with fontedit(self.fonts.arcade, size=20) as font:
            bottom = catego_bottom + 20
            for name in ghost_strategies:
                r = font.get_rect(name)
                r.top = bottom
                r.left = left + 10
                font.render_to(surface, r, name)
                bottom += r.height + 10

        surface.blit(*self.go)