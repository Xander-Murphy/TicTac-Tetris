import pygame

class Texture:
    @classmethod
    def getTileTexture(value : int):
        Colors = (
            (0, 0, 0),        # White
            (241, 239, 47),   # Yellow
            (136, 44, 237),   # Purple
            (138, 234, 40),   # Green
            (207, 54, 22),    # Red
            (0, 0, 240),      # Blue
            (221, 164, 34),   # Orange
            (0, 240, 240),    # Cyan
        )

    @classmethod
    def getCellTexture(cls, surface : pygame.Surface, value : int):
        color = cls.getTileTexture(value)
        new_surface = surface.fill(color)
        return new_surface