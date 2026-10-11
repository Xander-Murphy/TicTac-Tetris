import pygame
from .scene import Scene
from ..UI.button import ImageButton
from ..eventManager import EventManager

class StartScene(Scene):
    def __init__(self, screen: pygame.Surface, name: str = "startScene"):
            super().__init__(screen, name)
    
    def enter(self):
        self.SCREEN.fill("blue")

        # Todo 
        # 1. Add this functionality to ImageButton class 
        # 2. Function to center images no matter the window
        
        imageFiles : dict = {
             "Start Button" : 'src/assets/ResizedStartButtonPlaceholder.png',
             "Quit Button" : 'src/assets/QuitButtonPlaceholder.png',
             "Logo" : 'src/assets/Tic-TacTetrisLogoPlaceholder.png'
        }

        imageData : dict = { #(x, y, scale)
             "Start Button" : (50, 300, 6),
             "Quit Button" : (50, 400, 6),
             "Logo" : (250, 50, 10) # Add center function later
        }
        
        self.imageButtons : dict = {}
        imageButtons = self.imageButtons

        # create image button objects and assign them to dictionary
        for imageFile in imageFiles.keys():
             filePath = imageFiles.get(imageFile)
             data = imageData.get(imageFile)
             x = data[0]
             y = data[1]
             scale = data[2]
             
             image = pygame.image.load(filePath).convert_alpha()
             button = ImageButton(x, y, image, self.SCREEN, scale)
             imageButtons[imageFile] = button

        # display all buttons
        for button in imageButtons.values():
             if len(imageButtons) > 0:
                  button : ImageButton
                  button.display()

    def update(self):
        startButton : ImageButton = self.imageButtons.get("Start Button")
        quitButton : ImageButton = self.imageButtons.get("Quit Button")

        if startButton.is_clicked():
            self.EVENTS.append(("change_scene", self, "testScene"))

        if quitButton.is_clicked():
            EventManager.quitGame()

    def exit(self):
        self.SCREEN.fill("white")