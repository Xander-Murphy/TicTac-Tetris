import pygame
from .scene import Scene
from ..UI.button import ImageButton
from ..eventManager import EventManager

def highlight(button: ImageButton):
     pygame.draw.rect(button.screen, "red", button.collisionBox, width=2)

ImageElements = { 
     # Positions are percentage based
     # Positions are concidered from the center
     # If the position is (50, 30) the center of the image is in the center and 30% from the top
     "Start Button": {
          "image" : 'src/assets/ResizedStartButtonPlaceholder.png',
          "position" : (50, 45),
          "scale" : 8,
          "can click" : True,
          "hovering" : highlight,
          "clicked" : lambda scene: EventManager.changeScene(scene, "testScene"),
     },
     "Challenge Button" : {
          "image" : 'src/assets/ChallengeButtonPlaceholder.png',
          "position" : (50, 60),
          "scale" : 8,
          "can click" : True,
          "hovering" : highlight,
          "clicked" : lambda scene: EventManager.changeScene(scene, "endlessTestScene"),
     },
     "Mission Button" : {
          "image" : 'src/assets/MissionButtonPlaceholder.png',
          "position" : (50, 75),
          "scale" : 8,
          "can click" : True,
          "hovering" : highlight,
          "clicked" : lambda scene: EventManager.changeScene(scene, "missionTestScene"),
     },
     "Quit Button" : {
          "image" : 'src/assets/QuitButtonPlaceholder.png',
          "position" : (50, 90),
          "scale" : 8,
          "can click" : True,
          "hovering" : highlight,
          "clicked" : lambda scene: EventManager.quitGame(),
     },
     "Logo" : {
          "image" : 'src/assets/Tic-TacTetrisLogoPlaceholder.png',
          "position" : (50, 20),
          "scale" : 13,
          "can click" : False,
     },
}

class StartScene(Scene):
    def __init__(self, screen: pygame.Surface, name: str = "startScene"):
          super().__init__(screen, name)
    
    def enter(self):
     self.SCREEN.fill("blue")

     self.imageButtons: dict[str, ImageButton] = {}
     screenWidth, screenHeight = self.SCREEN.get_size()

     for name, element in ImageElements.items():
          image = pygame.image.load(element["image"]).convert_alpha()
          position = element["position"]
          scale = element["scale"]
          # Position is perenate based and concidered from the center
          x = int(screenWidth * position[0] / 100 - image.get_width() * scale / 2)
          y = int(screenHeight * position[1] / 100 - image.get_height() * scale / 2)

          button = ImageButton(x, y, image, self.SCREEN, scale)
          
          if element["can click"] and "hovering" in element:
               hoverCallback = element["hovering"]
               button.is_hovering_callback = lambda button=button, callback=hoverCallback: callback(button)
          self.imageButtons[name] = button

        # display all buttons
     for button in self.imageButtons.values():
          if len(self.imageButtons) > 0:
               button : ImageButton
               button.display()

    def update(self):
     # Rendering
     self.SCREEN.fill("blue")
     imageButtons = self.imageButtons
     for button in imageButtons.values():
          if len(imageButtons) > 0:
               button : ImageButton
               button.display()

     for name, element in ImageElements.items():
          if element["can click"] and self.imageButtons[name].is_clicked():
               element["clicked"](self)

    def exit(self):
        self.SCREEN.fill("white")