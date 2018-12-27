from pygame.locals import *
from scene import Scene
from utils import *
from strategies import pacman_strategies, ghosts_strategies
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

        self.strategies_pacman_rects = {}
        self.strategies_ghosts_rects = {}

        self.strategy_combination = dotdict(pacman='user', ghosts='shortest path')

    def handle_event(self, e):
        super().handle_event(e)
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            if self.go.rect.collidepoint(e.pos):
                # TODO: find out the 2 strategies
                # TODO: no strategy selected = error message
                EventManager.emit('switch scene', 'game',
                                  self.strategy_combination.pacman,
                                  self.strategy_combination.ghosts)

            for name, rect in self.strategies_pacman_rects.items():
                if rect.collidepoint(e.pos):
                    self.strategy_combination.pacman = name
                    break
            else:
                # because there cannot be 2 strategies colliding at the same
                # time (none of them are colliding with each other)
                for name, rect in self.strategies_ghosts_rects.items():
                    if rect.collidepoint(e.pos):
                        self.strategy_combination.ghosts = name
                        break


    def render(self, surface, rect):

        text = 'PACMAN'
        with fontedit(self.fonts.fancy, size=50) as font:
            r = font.get_rect(text)
            r.midtop = rect.midtop
            r.top += 40
            font.render_to(surface, r, text, fgcolor=WHITE)
            title_bottom = r.bottom

        padding = 50 # between the 2 columns
        line_height = 20 # between 2 rows

        text = 'Pacman strategy'
        with fontedit(self.fonts.arcade, size=30) as font:
            r = font.get_rect(text)
            r.top = title_bottom + 50
            r.right = rect.centerx - padding / 2
            font.render_to(surface, r, text)
            catego_bottom = r.bottom
            left = r.left
            width = r.width

        # pacman strategies
        with fontedit(self.fonts.arcade, size=20) as font:
            bottom = catego_bottom + 20
            for name in pacman_strategies:
                r = font.get_rect(name)
                r.top = bottom
                r.left = left + 10
                kwargs = dotdict()
                if name == self.strategy_combination.pacman:
                    kwargs.fgcolor = BLACK
                    bg = r.copy()
                    bg.width = width
                    bg.inflate_ip((5, 2))
                    pygame.draw.rect(surface, WHITE, bg)

                font.render_to(surface, r, name, **kwargs)
                self.strategies_pacman_rects[name] = r
                bottom += r.height + line_height

        text = 'Ghost strategy'
        with fontedit(self.fonts.arcade, size=30) as font:
            r = font.get_rect(text)
            r.top = title_bottom + 50
            r.left = rect.centerx + padding / 2
            left = r.left
            font.render_to(surface, r, text)

        # ghost strategies
        with fontedit(self.fonts.arcade, size=20) as font:
            bottom = catego_bottom + 20
            for name in ghosts_strategies:
                r = font.get_rect(name)
                r.top = bottom
                r.left = left + 10
                kwargs = dotdict()
                if name == self.strategy_combination.ghosts:
                    kwargs.fgcolor = BLACK
                    bg = r.copy()
                    bg.width = width
                    bg.inflate_ip((5, 2))
                    pygame.draw.rect(surface, WHITE, bg)

                font.render_to(surface, r, name, **kwargs)
                self.strategies_ghosts_rects[name] = r
                bottom += r.height + line_height

        surface.blit(*self.go)