import pygame
from .scenes import scene
from elements.scenes.testScene import TestScene
from elements.scenes.errorScene import ErrorScene
from elements.scenes.startScene import StartScene

class SceneManager:
    def __init__(self, initScene : str, screen: pygame.Surface):
        self.SCREEN = screen

        # put all scenes here
        self.all_scenes = [
            TestScene(self.SCREEN, "testScene"),
            ErrorScene(self.SCREEN, "errorScene"),
            StartScene(self.SCREEN, "startScene")
        ]
        self.SCENES = self.get_all_scenes()

        # start the init scene
        if initScene not in self.SCENES:
            raise KeyError("Initial scene could not be found")
        self.CURRENT_SCENE : scene = self.SCENES[initScene]

        self.CURRENT_SCENE.enter()

    def get_all_scenes(self):
        myDict = {}

        for scene in self.all_scenes:
            myDict[scene.NAME] = scene
        
        return myDict

    def change_scene(self, current_scene, new_scene = "default"):
        new_scene = self.SCENES.get(new_scene)

        if new_scene is None:
            raise KeyError("New Scene could not be found")

        if current_scene != self.CURRENT_SCENE:
            raise KeyError("Current scene does not match")
        
        self.CURRENT_SCENE.exit()
        self.CURRENT_SCENE = new_scene
        self.CURRENT_SCENE.enter()

    def update(self):
        for event in self.CURRENT_SCENE.EVENTS:
            if event[0] == "change_scene":
                self.change_scene(event[1], event[2])
        
        self.CURRENT_SCENE.update()

        # EXAMPLE - self.EVENTS.append(("change_scene", self, "testScene"))

    def get_screen(self):
        return self.SCREEN