import time
import pygame
import sys
from PyQt5.QtWidgets import QApplication, QFileDialog

epsilon = float(0.00000000000001)
class Button:
    def __init__(self,_location:tuple[float,float],_size:tuple[float,float],_on_click,_color="gray",_hover_color="dark gray",_outline_color="black",_text="",_font="Calibri",_fontsize=12,outline_width=1):
        self.rect = pygame.rect.Rect(_location[0],_location[1],_size[0],_size[1])
        self.is_hovered = False
        
        self.colors = {
            "color": _color,
            "hover": _hover_color,
            "outline": _outline_color
        }

        self.on_click = _on_click
        self.text = _text
        self.font = pygame.font.SysFont(_font, _fontsize)
        self.out_size = outline_width
        self.image: pygame.Surface = None
        self.rendered_text = None
        
    def draw(self):
        screen = pygame.display.get_surface()
        if self.is_hovered: pygame.draw.rect(screen,self.colors["hover"],self.rect)
        else: pygame.draw.rect(screen,self.colors["color"],self.rect)
        pygame.draw.rect(screen,self.colors["outline"],self.rect,self.out_size)
        
        if self.image != None:
            if self.image.get_size()[0] > 20 and self.image.get_size()[1] > 20: screen.blit(self.image,(self.rect.centerx-self.image.get_size()[0]/2,self.rect.top))
            if self.rendered_text != None: screen.blit(self.rendered_text,(self.rect.centerx-self.rendered_text.get_size()[0]/2,self.rect.top+self.image.get_size()[1]))
        elif self.rendered_text != None: screen.blit(self.rendered_text,(self.rect.centerx-self.rendered_text.get_size()[0]/2,max(self.rect.centery-self.rendered_text.get_height()/2,self.rect.top)))
        
    def update(self, click:bool):
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = False
        if self.rect.left < mouse_pos[0] and mouse_pos[0] < self.rect.right and self.rect.bottom > mouse_pos[1] and mouse_pos[1] > self.rect.top:
            self.is_hovered = True
            if click:
                self.on_click()
        
        if self.text:
            self.rendered_text = self.font.render(self.text,True,"black")
            if self.rendered_text.get_size()[0] > self.rect.size[0] or self.rendered_text.get_size()[1] > self.rect.size[1]:
                txt_ratio = self.rendered_text.get_size()[1]/self.rendered_text.get_size()[0]
                curr_size = self.rendered_text.get_size()
                target_size = (min(curr_size[0],self.rect.size[0]-10),int(min(curr_size[1],(self.rect.size[0]-10)*txt_ratio)))
                self.rendered_text = pygame.transform.scale(self.rendered_text,target_size)
        else: self.rendered_text = None

        if self.image:
            text_height = 0
            if self.text: text_height = self.rendered_text.get_size()[1]
            img_size = self.orig_image.get_size()
            ratio = img_size[0]/img_size[1]
            max_h = self.rect.height-text_height-10
            max_w = self.rect.width

            target_size = (min(max_w,max_h*ratio),min(max_h,max_w/ratio))
            if target_size[0] < 0 or target_size[1] < 1: self.image = pygame.transform.scale(self.image,(0,0))
            else: self.image = pygame.transform.scale(self.orig_image,target_size)

    def update_font(self,size:int,font_name:str):
        self.font = pygame.font.SysFont(font_name,size)
        self.rendered_text = self.font.render(self.text,True,self.colors["outline"])
    def set_image(self, image_path:str):
        self.orig_image = pygame.image.load(image_path)
        self.image = self.orig_image.copy()
        text_height = 0
        if self.text:
            text_height = self.font.render(self.text,True,"black").get_size()[1]
        img_size = self.image.get_size()
        ratio = img_size[0]/img_size[1]
        max_h = self.rect.height-text_height
        max_w = self.rect.width

        target_size = (min(max_w,max_h*ratio),min(max_h,max_w/ratio))
        self.image = pygame.transform.scale(self.image,target_size)
    
    
class ButtonGrid:
    
    '''
    Create a grid of buttons\n
    `loc` is the top-left, `grid_sz` controls the amount of grid spaces\n
    either `grid_sz[0]` or `grid_sz[1]` **must be > 0**
    '''
    def __init__(self,loc:tuple[float],dims:tuple[float],grid_sz:tuple[int], bg_col="light gray",col="gray",hov_col="dark gray",outline_col="black",outline_width=1,font_size=12):
        if max(grid_sz) <= 0: raise ValueError
        self.rect = pygame.rect.Rect(loc[0],loc[1],dims[0],dims[1])
        self.colors = {
            "color": col,
            "hover": hov_col,
            "outline": outline_col,
            "background": bg_col
        }

        self.outline_width = outline_width
        self.buttons:list[Button] = []
        self.grid_size:list[int] = [max(0,grid_sz[0]),max(0,grid_sz[1])]
        self.font_size = font_size
    def add_button(self, _onclick=lambda: 0, _text: str = "", _font: str = "Calibri", _font_size: int = 12):
        pos = self.rect.topleft
        prev_rect = None
        if len(self.buttons): prev_rect = self.buttons[-1].rect
        if self.grid_size[0] == 0:
            tmp_txt: pygame.Surface = pygame.font.SysFont(_font, _font_size).render(_text, False, "black")
            size = (max(tmp_txt.get_size()[0] + 10, 25), self.rect.height)
            if prev_rect != None: pos = (prev_rect.right, prev_rect.top)
        else:
            size = (self.rect.width / self.grid_size[0], self.rect.width / self.grid_size[1])
            if prev_rect != None and len(self.buttons) % self.grid_size[0] == 0:
                pos = (pos[0], prev_rect.top + size[1])
            elif prev_rect != None:
                pos = (prev_rect.right, prev_rect.top)
        
        self.buttons.append(Button(pos, size, _onclick, self.colors["color"], self.colors["hover"], self.colors["outline"], _text, _font, _font_size, self.outline_width))
        
    def draw(self):
        screen = pygame.display.get_surface()
        
        pygame.draw.rect(screen,self.colors["background"],self.rect)
        
        for button in self.buttons:
            button.draw()
    def update(self,click:bool):
        for i in range(len(self.buttons)):
            self.buttons[i].update(click)
            self.buttons[i].update_font(self.font_size,"calibri")
            pos = self.rect.topleft
            
            prev_rect = None
            if i > 0: prev_rect = self.buttons[i-1].rect
            if self.grid_size[0] == 0:
                size = (max(self.buttons[i].rendered_text.get_size()[0] + 10, 25), self.rect.height)
                if prev_rect != None: pos = (prev_rect.right, prev_rect.top)
            else:
                size = (self.rect.width / self.grid_size[0], self.rect.width / self.grid_size[1])
                if i > 0 and i % self.grid_size[0] == 0:
                    pos = (pos[0], prev_rect.top + size[1])
                elif prev_rect != None:
                    pos = (prev_rect.right, prev_rect.top)
            self.buttons[i].rect.update(pos[0],pos[1],size[0],size[1])
            
                
                
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
    def __init__(self, pos: tuple, size: tuple, initial_val: float, min_val: int, max_val: int) -> None:
        self.pos = pos
        self.size = size

        self.slider_left_pos = self.pos[0] - (size[0] // 2)
        self.slider_right_pos = self.pos[0] + (size[0] // 2)
        self.slider_top_pos = self.pos[1] - (size[1] // 2)

        self.min = min_val
        self.max = max_val
        self.initial_val = (self.slider_right_pos - self.slider_left_pos) * initial_val  # percentage

        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left_pos + self.initial_val - 5, self.slider_top_pos, 10, self.size[1])

        self.dragging = False

    def move_slider(self, mouse_pos):
        new_x = max(self.slider_left_pos, min(mouse_pos[0], self.slider_right_pos))
        self.button_rect.centerx = new_x

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos) or self.container_rect.collidepoint(event.pos):
                self.dragging = True
                self.move_slider(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.move_slider(event.pos)

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), self.container_rect)
        pygame.draw.rect(screen, (100, 100, 100), self.button_rect)
    
    def get_value(self):
        val_range = self.slider_right_pos - self.slider_left_pos
        button_val = self.button_rect.centerx - self.slider_left_pos

        return (button_val / val_range) * (self.max - self.min) + self.min
        
        




        