import pygame
from .scene import Scene
from ..UI.button import Button
from ..eventManager import EventManager

class StartScene(Scene):
    def __init__(self, screen: pygame.Surface, name: str = "startScene"):
            super().__init__(screen, name)
    
    def enter(self):
        self.SCREEN.fill("blue")
        self.button = Button(100, 100, 50, 50, "red", self.SCREEN)
        self.button.display()

    def update(self):
        if self.button.is_clicked():
            self.EVENTS.append(("change_scene", self, "testScene"))

    def exit(self):
        self.SCREEN.fill("white")