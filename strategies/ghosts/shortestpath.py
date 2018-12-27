class ShortestPath:

    def __init__(self, tiles, ghosts, pacman):
        self.tiles = tiles
        self.ghosts = ghosts
        self.pacman = pacman

        self.distances = None

    def map_distances(self):
        self.distances = [[float('inf') for _ in range(self.tiles.width)] \
                          for _ in range(self.tiles.height)]

        def map(x, y, distance):
            self.distance_plan[y][x] = distance
            if y > 0 and self.plan[y-1][x] == ' ' \
                and self.distance_plan[y-1][x] > distance + 1:
                map(x, y - 1, distance + 1)
            if y < self.height - 1 and self.plan[y+1][x] == ' ' \
                and self.distance_plan[y+1][x] > distance + 1:
                map(x, y + 1, distance + 1)
            if x > 0 and self.plan[y][x-1] == ' ' \
                and self.distance_plan[y][x-1] > distance + 1:
                map(x - 1, y, distance + 1)
            if x < self.width - 1 and self.plan[y][x+1] == ' ' \
                and self.distance_plan[y][x+1] > distance + 1:
                map(x + 1, y, distance + 1)

        map(x, y, 0)
