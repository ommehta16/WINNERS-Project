import pygame
class Button:
    def __init__(self,_location:tuple[float],_size:tuple[float]):
        self.location = _location
        self.size = _size
        self.rect = pygame.rect.Rect(_location[0],_location[1],_size[0],_size[1])
        # TODO: add texture
        # TODO: add clicked texture
        # TODO: make it change when hovered
        # TODO: add an action on_click
        # TODO: add an action on_hover
    def draw(self, screen:pygame.Surface):
        pygame.draw.rect(screen,"red",self.rect,10)
    def update(self):
        # TODO: DO THIS!!!
        pass