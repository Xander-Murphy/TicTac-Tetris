import pygame
from .scene import Scene
from ..UI.button import ImageButton
from ..eventManager import EventManager

class StartScene(Scene):
    def __init__(self, screen: pygame.Surface, name: str = "startScene"):
            super().__init__(screen, name)
    
    def enter(self):
        self.SCREEN.fill("blue")

        imageFiles : dict = {
             "Start Button" : 'src/assets/ResizedStartButtonPlaceholder.png'
        }
        imageButtons : list = []

        self.image = pygame.image.load(imageFiles.get("Start Button")).convert_alpha()
        self.button = ImageButton(100, 100, self.image, self.SCREEN, 10)
        self.button.display()

    def update(self):
        if self.button.is_clicked():
            self.EVENTS.append(("change_scene", self, "testScene"))

    def exit(self):
        self.SCREEN.fill("white")