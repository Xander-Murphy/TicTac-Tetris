import pygame
from .Scene import Scene

class ErrorScene(Scene):
    def __init__(self, screen: pygame.Surface, name: str = "default"):
        super().__init__(screen, name)

    def enter(self):
        pass

    def update(self):
        raise NotImplementedError("Must have a process")

    def exit(self):
        pass