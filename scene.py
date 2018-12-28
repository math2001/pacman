""" This is a base class from which every scenes inherits from
"""

import pygame
import pygame.freetype
from utils import EventManager
from utils import Screen

pygame.freetype.init()

class Scene:

    fonts = None
  
    def handle_event(self, e):
        """ *pygame* event"""
        if e.type == pygame.QUIT:
            EventManager.emit("quit")
    
    def render(self, surface, rect):
        raise ValueError("No renderer for scene {}".format(self.__class__.__name__))
    
    def update(self):
        pass

    def debug_string(self):
        return ''