import pygame
class Button:
    def __init__(self,_location:tuple[float],_size:tuple[float],_on_click,_color="gray",_hover_color="dark gray",_outline_color="black",_text="",_font="Calibri",_fontsize=12):
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
        
    def draw(self, screen:pygame.Surface):
        if self.is_hovered: pygame.draw.rect(screen,self.hover_color,self.rect)
        else: pygame.draw.rect(screen,self.color,self.rect)
        pygame.draw.rect(screen,self.outline_color,self.rect,2)
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
    
    
class TitleBar:
    def __init__(self,_location:tuple[float],_size:tuple[float],_background_color="light gray",_color="gray",_hover_color="dark_gray",_outline_color="black"):
        self.location = _location
        self.size = _size
        self.rect = pygame.rect.Rect(_location[0],_location[1],_size[0],_size[1])
        self.color=_color
        self.background_color = _background_color
        self.hover_color = _hover_color
        self.outline_color = _outline_color
        self.buttons = []
    def add_button(self,_size:tuple[float]=(0,0),_onclick:function=lambda:0,_text:str="",_font:str="Calibri",_font_size:int=12):
        pos = self.location
        if len(self.buttons):
            pos=(self.buttons[-1].rect.right,self.buttons[-1].rect.top)
        tmp_txt:pygame.Surface=pygame.font.SysFont(_font,_font_size).render(_text)
        size = (max(tmp_txt.get_size()[0]+10,100),self.size[1])
        self.buttons.append(Button(pos,size,_onclick,self.color,self.hover_color,self.outline_color,_text,_font,_font_size))
        
        # TODO: check if this works :))