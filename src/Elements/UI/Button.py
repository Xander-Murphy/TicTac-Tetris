import pygame

class Button:
    def __init__(self, x, y, width, height, color, screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = pygame.Color(color)
        self.screen = screen

    def display(self):
        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

    def is_hovering(self):
        if self.x <= pygame.mouse.get_pos()[0] <= self.x + self.width and self.y <= pygame.mouse.get_pos()[1] <= self.y + self.height:
            return True

    def is_clicked(self):
        if self.is_hovering() and pygame.mouse.get_pressed()[0]:
            return True
        return False