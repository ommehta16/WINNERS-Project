import time
import pygame
import sys
from PyQt5.QtWidgets import QApplication, QFileDialog

epsilon = float(0.00000000000001)
class Button:
    def __init__(self,_location:tuple[float],_size:tuple[float],_on_click,_color="gray",_hover_color="dark gray",_outline_color="black",_text="",_font="Calibri",_fontsize=12,outline_width=1):
        self.location = _location
        self.size = _size
        self.rect = pygame.rect.Rect(_location[0],_location[1],_size[0],_size[1])
        self.is_hovered = False
        self.color = _color
        self.hover_color = _hover_color
        self.outline_color = _outline_color
        self.on_click = _on_click
        self.text=_text
        self.font = pygame.font.SysFont(_font,_fontsize)
        self.outline_width = outline_width
        self.image:pygame.Surface = None
        
    def draw(self):
        screen = pygame.display.get_surface()
        if self.is_hovered: pygame.draw.rect(screen,self.hover_color,self.rect)
        else: pygame.draw.rect(screen,self.color,self.rect)
        pygame.draw.rect(screen,self.outline_color,self.rect,self.outline_width)
        
        if len(self.text):
            text = self.font.render(self.text,True,self.outline_color)
            screen.blit(text,(self.rect.centerx-text.get_size()[0]/2,self.rect.centery-text.get_size()[1]/2))
        
        if self.image != None:
            screen.blit(self.image,(self.rect.centerx-self.image.get_size()[0]/2,self.rect.centery-self.image.get_size()[1]/2))
        
    def update(self, click:bool):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.left < mouse_pos[0] and mouse_pos[0] < self.rect.right and self.rect.bottom > mouse_pos[1] and mouse_pos[1] > self.rect.top:
            self.is_hovered = True
            if click:
                self.on_click()
            
        else:
            self.is_hovered = False
        
        # TODO: DO THIS!!!
        pass
    
    def set_image(self, image_path:str):
        self.text = ""
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image,(min(self.size[0],self.image.get_size()[0]),min(self.size[1],self.image.get_size()[1])))
        
    
    
class ButtonGrid:
    
    '''
    Create a grid of buttons\n
    `loc` is the top-left, `grid_sz` controls the amount of grid spaces\n
    either `grid_sz[0]` or `grid_sz[1]` **must be > 0**
    '''
    def __init__(self,loc:tuple[float],dims:tuple[float],grid_sz:tuple[int], bg_col="light gray",col="gray",hov_col="dark gray",outline_col="black",outline_width=1):
        if max(grid_sz) <= 0: raise ValueError
        self.location:tuple[float] = loc
        self.size:tuple[float] = dims
        self.rect:pygame.Rect = pygame.rect.Rect(loc[0],loc[1],dims[0],dims[1])
        self.color=col
        self.background_color = bg_col
        self.hover_color = hov_col
        self.outline_color = outline_col
        self.outline_width = outline_width
        self.buttons:list[Button] = []
        self.grid_size:list[int] = [max(0,grid_sz[0]),max(0,grid_sz[1])]
    def add_button(self, _onclick=lambda: 0, _text: str = "", _font: str = "Calibri", _font_size: int = 12, _minor_axis_size_spec: float = 25, _color= "gray"):
        pos = self.location
        if self.grid_size[0] == 0:
            tmp_txt: pygame.Surface = pygame.font.SysFont(_font, _font_size).render(_text, False, "black")
            size = (max(tmp_txt.get_size()[0] + 10, 25), self.size[1])
            if len(self.buttons):
                pos = (self.buttons[-1].rect.right, self.buttons[-1].rect.top)
        elif self.grid_size[1] == 0:
            size = (self.size[0] / self.grid_size[0], _minor_axis_size_spec)
            if len(self.buttons) and len(self.buttons) % self.grid_size[0] == 0:
                pos = (self.location[0], self.buttons[-1].rect.top + self.buttons[-1].size[1])
            elif len(self.buttons):
                pos = (self.buttons[-1].rect.right, self.buttons[-1].rect.top)
        else:
            size = (self.size[0] / self.grid_size[0], self.size[1] / self.grid_size[1])
            if len(self.buttons) and len(self.buttons) % self.grid_size[0] == 0:
                pos = (self.location[0], self.buttons[-1].rect.top + size[1])
            elif len(self.buttons):
                pos = (self.buttons[-1].rect.right, self.buttons[-1].rect.top)
        
        self.buttons.append(Button(pos, size, _onclick, _color, self.hover_color, self.outline_color, _text, _font, _font_size, self.outline_width))
        
    def draw(self):
        screen = pygame.display.get_surface()
        
        pygame.draw.rect(screen,self.background_color,self.rect)
        
        for button in self.buttons:
            button.draw()
    def update(self,click:bool):
        if self.rect.topleft != self.location or self.rect.size != self.size:
            # Update the bounding box/location (idk if/where we need this -- good to have ig?)
            self.rect = pygame.rect.Rect(self.location[0],self.location[1],self.size[0],self.size[1])
        for button in self.buttons:
            button.update(click)
                
                
class Prompt:
    def get_file_open(file_type:str = "All files (*.*)") -> str:
        app = QApplication(sys.argv)
        file_name = QFileDialog.getOpenFileName(None,"Open file",None,file_type)[0]
        app.exit()
        return file_name
    
    def get_file_save(file_type:str = "All files (*.*)") -> str:
        app = QApplication(sys.argv)
        file_name = QFileDialog.getSaveFileName(None,"Save file",None,file_type)[0]
        app.exit()
        return file_name
    
class Slider:
    def __init__(self,pos:tuple,size:tuple,initial_val:float,min:int,max:int) -> None:
        self.pos = pos
        self.size = size

        self.slider_left_pos = self.pos[0] - (size[0]//2)
        self.slider_right_pos = self.pos[0] + (size[0]//2)
        self.slider_top_pos = self.pos[1] - (size[1]//2)

        self.min = min
        self.max = max
        self.initial_val = (self.slider_right_pos - self.slider_left_pos)*initial_val #percentage

        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left_pos + self.initial_val - 5, self.slider_top_pos,10,self.size[1])

        self.dragging = False

    def move_slider(self, mouse_pos):
        if self.dragging:
            new_x = max(self.slider_left_pos, min(mouse_pos[0], self.slider_right_pos))
            self.button_rect.centerx = new_x

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            self.move_slider(event.pos)
    
    def draw(self, screen):
        
        pygame.draw.rect(screen, (200, 200, 200), self.container_rect)  
        pygame.draw.rect(screen, (100, 100, 100), self.button_rect)  
        
        




        