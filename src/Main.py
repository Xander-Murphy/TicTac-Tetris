import pygame
from Elements.SceneManager import SceneManager
from Elements.Scenes.TestScene import TestScene

SCREEN_SIZE = (850, 500)
FPS = 30
WINDOW_NAME = "TicTac-Tetris"
START_SCREEN = "TestScene"

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(WINDOW_NAME)
clock = pygame.time.Clock()
sceneManager = SceneManager(START_SCREEN, screen)

running = True
while running:
    # check for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update the current scene
    sceneManager.update()

    # update display and clock(delta)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()