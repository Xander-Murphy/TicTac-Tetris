import pygame

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)


class DataDisplay:
    def __init__(
        self,
        size: tuple[int, int],
        position: tuple[int, int],
    ):
        self.size = size
        self.position = position
        self.surface: pygame.Surface = pygame.Surface(size)
        self.clear()

    def add_surface(
        self,
        surface: pygame.Surface,
        position: tuple[int, int] = (0, 0),
    ) -> pygame.Rect:
        return self.surface.blit(surface, position)

    def display(self, target: pygame.Surface) -> pygame.Rect:
        rect = target.blit(self.surface, self.position)
        # Blue border for testing 
        pygame.draw.rect(target, BLUE, rect, 1)
        return rect

    def clear(self):
        self.surface.fill(WHITE)