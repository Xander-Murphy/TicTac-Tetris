import pygame

# refactoring todo
# 1. 


class Button:
    def __init__(self, x, y, width, height, screen : pygame.surface, color = "black"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = pygame.Color(color)
        self.screen = screen
        self.collisionBox : pygame.Rect = pygame.Rect(x, y, width, height)

    def display(self):
        pygame.draw.rect(self.screen, self.color, self.collisionBox)

    def is_hovering(self):
        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]
        collisionBox = self.collisionBox
        
        if collisionBox.x <= mouseX <= collisionBox.x + collisionBox.width and collisionBox.y <= mouseY <= collisionBox.y + collisionBox.height:
            return True

    def is_clicked(self):
        if self.is_hovering() and pygame.mouse.get_pressed()[0]:
            return True
        return False

class ImageButton(Button):
    def __init__(
            self, 
            x, 
            y, 
            image : pygame.Surface, 
            screen : pygame.Surface, 
            scale : int = 1, 
            # displayResolutionWidth = 1, 
            # displayResolutionHeight = 1
            ):
        self.x = x
        self.y = y
        self.coords = (x, y)
        self.screen = screen
        self.scale = scale

        # get dimentions of image and scale it 
        # This assumes the image is properly cropped // the resolution matches the image
        self.width = int(image.get_width() * scale)
        self.height = int(image.get_height() * scale)
        self.image = pygame.transform.scale(image, (self.width, self.height))

        # create the collision box
        rectSize = (self.width, self.height)
        self.collisionBox = pygame.Rect(self.coords, rectSize)


    # override
    def display(self):

        # Draw the image on the screen
        self.screen.blit(self.image, self.coords)

        # # FOR TESTING -- Draw a solid line around the Rect for visualising collisions
        # pygame.draw.rect(
        #     self.screen,
        #     (255, 0, 0),  # Red
        #     self.collisionBox,
        #     width=2
        # )

        