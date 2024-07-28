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
        
    def draw(self):
        screen = pygame.display.get_surface()
        if self.is_hovered: pygame.draw.rect(screen,self.hover_color,self.rect)
        else: pygame.draw.rect(screen,self.color,self.rect)
        pygame.draw.rect(screen,self.outline_color,self.rect,self.outline_width)
        text = self.font.render(self.text,True,self.outline_color)
        screen.blit(text,(self.rect.centerx-text.get_size()[0]/2,self.rect.centery-text.get_size()[1]/2))
        
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
    def add_button(self,_onclick=lambda:0,_text:str="",_font:str="Calibri",_font_size:int=12,_minor_axis_size_spec:float=25):
        pos = self.location
        if self.grid_size[0] == 0:
            tmp_txt:pygame.Surface=pygame.font.SysFont(_font,_font_size).render(_text,False,"black")
            size = (max(tmp_txt.get_size()[0]+10,25),self.size[1])
            if len(self.buttons): pos=(self.buttons[-1].rect.right,self.buttons[-1].rect.top)
            # You get a TEXT-FITTED button if you don't specify the x-grid size
        
        elif self.grid_size[1] == 0:
            size = (self.size[0]/self.grid_size[0],_minor_axis_size_spec)
            if len(self.buttons) and len(self.buttons) % self.grid_size[0] == 0:
                pos=(self.location[0],self.buttons[-1].rect.top+size[1])
            elif len(self.buttons):
                pos=(self.buttons[-1].rect.right,self.buttons[-1].rect.top)
            # You get a SQUARE button if you don't specify the y-grid size
        else:
            size = (self.size[0]/self.grid_size[0],self.size[1]/self.grid_size[1])
            if len(self.buttons) and len(self.buttons) % self.grid_size[0] == 0:
                pos=(self.location[0],self.buttons[-1].rect.top+size[1])
            elif len(self.buttons):
                pos=(self.buttons[-1].rect.right,self.buttons[-1].rect.top)
            # Otherwise, it fits itself to the shape
        
        self.buttons.append(Button(pos,size,_onclick,self.color,self.hover_color,self.outline_color,_text,_font,_font_size,self.outline_width))
        
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
        
        if len(self.buttons):
            self.size[1] = (self.size[1] * 4 + (self.buttons[-1].rect.bottom - self.location[1]) * 1)/5
            
            if abs(self.size[1] - self.buttons[-1].rect.bottom - self.location[1]) <= epsilon:
                self.size[1] = self.buttons[-1].rect.bottom - self.location[1]
                
                
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