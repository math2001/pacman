from scene import Scene

class Strategy(Scene):

    """A strategy is just like a scene

    It just isn't *activated* as a scene. But in essense, they do the same
    thing: update, render (for debug) and handle events. Hence why they have
    such similar methods.
    """
    def __init__(self, tiles, pacman, ghosts):
        self.tiles = tiles
        self.pacman = pacman
        self.ghosts = ghosts

    def render(self, surface, rect, rfc):
        pass

    def update(self, ufc):
        pass

    def handle_event(self, e):
        pass

    def done(self):
        pass