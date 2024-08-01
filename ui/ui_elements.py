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
        did_action = False

        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = False
        if self.rect.left < mouse_pos[0] and mouse_pos[0] < self.rect.right and self.rect.bottom > mouse_pos[1] and mouse_pos[1] > self.rect.top:
            self.is_hovered = True
            if click:
                did_action = True
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
        return did_action

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
    def __init__(self,loc:tuple[float],dims:tuple[float],grid_sz:tuple[int], bg_col="light gray",col="gray",hov_col="dark gray",outline_col="black",outline_width=1,font_size=12,buttons:list=[]):
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

        for action, image_path, text in buttons:
            self.add_button(_onclick=action,_text=text,_font_size=font_size)
            if len(image_path): self.buttons[-1].set_image(image_path)

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
        ran = False
        for i in range(len(self.buttons)):
            if self.buttons[i].update(click): ran = True
            self.buttons[i].update_font(self.font_size,"calibri")
            pos = self.rect.topleft
            
            prev_rect = None
            if i > 0: prev_rect = self.buttons[i-1].rect
            if self.grid_size[0] == 0:
                size = (max(self.buttons[i].rendered_text.get_size()[0] + 10, 25), self.rect.height)
                if prev_rect != None: pos = (prev_rect.right, prev_rect.top)
            else:
                size = (self.rect.width / self.grid_size[0], self.rect.height / self.grid_size[1])
                if i > 0 and i % self.grid_size[0] == 0:
                    pos = (pos[0], prev_rect.top + size[1])
                elif prev_rect != None:
                    pos = (prev_rect.right, prev_rect.top)
            self.buttons[i].rect.update(pos[0],pos[1],size[0],size[1])
        return ran
            
                
                
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
    def __init__(self, center: tuple, size: tuple, initial_val: float, min_val: int, max_val: int) -> None:
        self.progress:float = float(initial_val)
        self.min:float = min_val
        self.max:float = max_val
        self.rect:pygame.rect.Rect = pygame.rect.Rect(center[0]-size[0]/2,center[1]-size[1]/2,size[0],size[1])
        self.selected:bool = False

    def update(self,clicked:bool,moved:bool):
        if clicked:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.selected = True
        elif moved and self.selected:
            self.selected = True
        else:
            self.selected = False
        
        if self.selected:
            slider_pos = pygame.mouse.get_pos()[0]
            self.progress = min(max((slider_pos-self.rect.left-self.rect.width/40)/(self.rect.width-self.rect.width/20),0),1)

    def draw(self):
        screen = pygame.display.get_surface()
        
        slider_pos = self.progress*(self.rect.width * 19/20) + self.rect.left + self.rect.width/40

        handle = pygame.rect.Rect(slider_pos-self.rect.width/40,self.rect.top,self.rect.width/20,self.rect.height)

        pygame.draw.rect(screen,(200,200,200),self.rect)
        pygame.draw.rect(screen,(100,100,100),handle)

    def get_value(self):
        return self.progress*(self.max-self.min) + self.min

def title_screen(chng_img,BACKGROUND_COLOR):
    on_title = True
    title_font = pygame.font.SysFont("free sans",24)
    text1 = title_font.render('Welcome to Winners Image Data Editor (WIDE), ', True, (0, 0, 0))
    text1_1 = title_font.render('an image editor built in Python using Pygame and Pillow.', True, (0, 0, 0))
    text2 = title_font.render('To continue, please upload a file.', True, (0, 0, 0))
    screen = pygame.display.set_mode((800,600))  # Make window resizable
    def title_img_set():
        nonlocal on_title
        if chng_img():
            on_title = False
    start_up_button = Button((433,348),(80,40),title_img_set,_text="upload",_fontsize=24,_font="free sans")
    while on_title:
        clock = pygame.time.Clock()
        screen.fill(BACKGROUND_COLOR)
        screen.blit(text1, (screen.get_width()/2-text1.get_width()/2,screen.get_height()/2-text1.get_height()/2))
        screen.blit(text1_1, (screen.get_width()/2-text1_1.get_width()/2,screen.get_height()/2+text1.get_height()/2))
        screen.blit(text2, (screen.get_width()/2-text2.get_width()/2,screen.get_height()/2+2*text2.get_height()))
        start_up_button.draw()
        for event in pygame.event.get():
            clicked = False
            if event.type == pygame.QUIT: quit()
            if event.type == pygame.MOUSEBUTTONDOWN: clicked = True
        start_up_button.update(clicked)
        pygame.display.update()
        clock.tick(60)


class adjustmentTile:
    def __init__(self,screen:pygame.Surface,top:int,preview,apply):
        self.hidden = True
        self.owner = None

        self.adjust = ButtonGrid([0, top], [screen.get_size()[0] * 1/4, 20], [3, 1])
        self.adjust.add_button(_text="CANCEL",_onclick=self.hide)
        self.adjust.add_button(_text="PREVIEW",_onclick=preview)
        self.adjust.add_button(_text="APPLY",_onclick=apply)

        self.adjust_bg = pygame.rect.Rect([0, top],[screen.get_size()[0] * 1/4, screen.get_size()[1]-top])

        self.slider_font = pygame.font.SysFont("free sans",30)
        self.slider_color = (0,0,0)
        self.slider = Slider((self.adjust_bg.width // 2, self.adjust_bg.bottom - 150), (self.adjust_bg.width - 40, 20), 0, 0, 100)

    def hide(self):
        pass

    def get_slider_val(self):
        return self.slider.get_value()
    
    def update(self,clicked:bool,moved):
        self.slider_value_text = self.slider_font.render(f'{int(self.slider.get_value())}',1,self.slider_color)
        self.slider.update(clicked,moved)

        click_return = clicked
        if self.slider.selected:
            click_return = False
        self.adjust.update(click_return)
        return click_return

    def update_size(self,screen:pygame.Surface,top):
        self.adjust.rect.update(self.adjust.rect.left,screen.get_size()[1]-max((screen.get_size()[1] - top)/4,20),screen.get_size()[0] * 1/4, max((screen.get_size()[1] - top)/4,20))
        self.adjust_bg.update([0, top],[screen.get_size()[0] * 1/4, screen.get_size()[1]-top])
        self.slider.rect.center = (self.adjust_bg.centerx,self.adjust_bg.centery+self.adjust_bg.height/8)
        self.slider.rect.size = (self.adjust_bg.width-40,20)

    def draw(self):
        screen = pygame.display.get_surface()
        pygame.draw.rect(screen,"dark gray", self.adjust_bg)
        self.adjust.draw()
        self.slider.draw()
        screen.blit(self.slider_value_text, (self.slider.rect.left,self.slider.rect.top - self.slider_value_text.get_height()))

    