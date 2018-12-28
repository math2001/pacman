from pygame.locals import *
from scene import Scene
from utils import *
from strategies import strategies

class Menu(Scene):

    def __init__(self):
        super().__init__()

        text = 'Go!'
        with fontedit(self.fonts.fancy, size=30) as font:
            self.go = Sprite(*font.render(text))
            self.go.rect.bottom = Screen.rect.bottom - 30
            self.go.rect.centerx = Screen.rect.centerx

        self.selection = dotdict(pacman='user', ghosts='shortest path')

        self.strategies_rects = dotdict(pacman=dotdict(), ghosts=dotdict())
        EventManager.emit('set mode', (640, 480))

    def handle_event(self, e):
        super().handle_event(e)
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            if self.go.rect.collidepoint(e.pos):
                # TODO: find out the 2 strategies
                # TODO: no strategy selected = error message
                EventManager.emit('switch scene', 'game',
                                  self.selection.pacman,
                                  self.selection.ghosts)

            for name, rect in self.strategies_rects.pacman.items():
                if rect.collidepoint(e.pos):
                    self.selection.pacman = name
                    break
            else:
                # because there cannot be 2 strategies colliding at the same
                # time (none of them are colliding with each other)
                for name, rect in self.strategies_rects.ghosts.items():
                    if rect.collidepoint(e.pos):
                        self.selection.ghosts = name
                        break


    def render(self, surface, rect):

        text = 'PACMAN'
        with fontedit(self.fonts.fancy, size=50) as font:
            r = font.get_rect(text)
            r.midtop = rect.midtop
            r.top += 40
            font.render_to(surface, r, text, fgcolor=WHITE)

        padding = 50 # between the 2 columns
        line_height = 20 # between 2 rows

        def display_column(title, top, subject):
            with fontedit(self.fonts.arcade, size=30, underline=True) as font:
                r = font.get_rect(title)
                r.top = top
                if subject == 'pacman':
                    r.right = rect.centerx - padding / 2
                else:
                    r.left = rect.centerx + padding / 2
                font.render_to(surface, r, title)

                left = r.left
                width = r.width

            with fontedit(self.fonts.arcade, size=20) as font:
                bottom = r.bottom + 20
                for name in strategies[subject]:
                    r = font.get_rect(name)
                    r.width = width
                    r.top = bottom
                    r.left = left + 10
                    row = r.inflate((5, 10))
                    kwargs = dotdict()
                    if name == self.selection[subject]:
                        kwargs.fgcolor = BLACK
                        pygame.draw.rect(surface, WHITE, row)

                    font.render_to(surface, r, name, **kwargs)
                    self.strategies_rects[subject][name] = row
                    bottom += r.height + line_height

        display_column('Pacman strategy', r.bottom + 50, 'pacman')
        display_column('Ghosts strategy', r.bottom + 50, 'ghosts')

        surface.blit(*self.go)