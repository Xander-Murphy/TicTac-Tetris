import pygame

class Texture:
    @classmethod
    def getTileTexture(cls, value : int):
        Colors = (
            (128, 128, 128),  # Default color
            (241, 239, 47),   # Yellow
            (136, 44, 237),   # Purple
            (138, 234, 40),   # Green
            (207, 54, 22),    # Red
            (0, 0, 240),      # Blue
            (221, 164, 34),   # Orange
            (0, 240, 240),    # Cyan
        )
        return Colors[value]

    @classmethod
    def setCellTexture(cls, surface : pygame.Surface, value : int):
        color = cls.getTileTexture(value)
        surface_size = surface.size
        pygame.draw.rect(
            surface,
            color,
            [
                1,
                1,
                surface_size[0] - 2,
                surface_size[1] - 2,
            ],
        )