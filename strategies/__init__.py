from utils import dotdict
import strategies.ghosts
import strategies.pacman

strategies = dotdict(
    pacman={
        "user": strategies.pacman.User,
        "furthest": strategies.pacman.Furthest,
        # "greedy": None,
        # "joiner": None,
        # "adaptive": None
    },
    ghosts={
        "shortest path": strategies.ghosts.ShortestPath,
        "static": strategies.ghosts.Static,
        # "random": None,
        # "blocking": None,
        # "lonely": None,
    }
)