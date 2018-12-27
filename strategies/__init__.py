from utils import dotdict
import strategies.ghosts
import strategies.pacman

strategies = dotdict(
    pacman={
        "user": strategies.pacman.User,
        "farthest": None,
        "greedy": None,
        "joiner": None,
        "adaptive": None
    },
    ghosts={
        "shortest path": strategies.ghosts.ShortestPath,
        "random": None,
        "blocking": None,
        "lonely": None,
    }
)