""" This is a base class from which every scenes inherits from
"""

from utils import EventManager
import pygame
from utils import Screen

class Scene:
    def handle_event(self, e):
        """ *pygame* event"""
        if e.type == pygame.QUIT:
            EventManager.emit("quit")
    
    def render(self, surface):
        raise ValueError("No renderer for scene {}".format(self.__class__.__name__))
    
    def update(self):
        pass

    def debug_string(self):
        return self.__class__.__name__