import strategies.ghosts
import strategies.pacman

ghosts_strategies = {
    "shortest path": strategies.ghosts.ShortestPath,
    "random": None,
    "blocking": None,
    "lonely": None,
}

pacman_strategies = {
    "user": strategies.pacman.User,
    "farthest": None,
    "greedy": None,
    "joiner": None,
    "adaptive": None
}

