import pygame
from .Scenes import Scene
from Elements.Scenes.TestScene import TestScene
from Elements.Scenes.ErrorScene import ErrorScene

class SceneManager:
    def __init__(self, initScene : str, screen: pygame.Surface):
        self.SCREEN = screen

        # put all scenes here
        self.all_scenes = [
            TestScene(self.SCREEN, "TestScene"),
            ErrorScene(self.SCREEN, "ErrorScene")
        ]
        self.SCENES = self.get_all_scenes()

        # start the init scene
        if initScene not in self.SCENES:
            raise KeyError("Initial scene could not be found")
        self.CURRENT_SCENE : Scene = self.SCENES[initScene]

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
        
        self.CURRENT_SCENE.exit()
        self.CURRENT_SCENE = new_scene
        self.CURRENT_SCENE.enter()

    def update(self):
        for event in self.CURRENT_SCENE.EVENTS:
            if event[0] == "change_scene":
                self.change_scene(event[1], event[2])
        
        self.CURRENT_SCENE.update()

    def get_screen(self):
        return self.SCREEN