import pygame
from .Scene import Scene

class TestScene(Scene):
    def __init__(self, screen: pygame.Surface, name: str = "TestScene"):
        super().__init__(screen, name)

    def enter(self):
        self.SCREEN.fill("purple")
    
    def update(self):
        pass

    def exit(self):
        pass
