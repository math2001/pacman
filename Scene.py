""" This is a base class from which every scenes inherits from
"""
import pygame
from utils import Screen

class Scene:
    def __init__(self, switch_scene, quit, set_mode):
        self.switch_scene = switch_scene
        self.quit = quit
        self.set_mode = set_mode

    def handle_event(self, e):
        """ *pygame* event"""
        if e.type == pygame.QUIT:
            self.quit()
    
    def render(self, surface):
        raise ValueError("No renderer for scene {}".format(self.__class__.__name__))
    
    def update(self):
        pass

    def debug_string(self):
        return self.__class__.__name__