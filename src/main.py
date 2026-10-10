import pygame

from elements.sceneManager import SceneManager
from elements.eventManager import EventManager

SIZE = (850, 500)
FPS = 25
STARTING_SCENE = "testScene"


def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    scene_manager = SceneManager(STARTING_SCENE, screen)

    done = False

    def stopPygame():
        nonlocal done
        done = True

    EventManager.onQuitGame.append(stopPygame)

    while not done:

        # update the current scene
        scene_manager.update()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
