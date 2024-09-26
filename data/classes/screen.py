import pygame
from data.classes.button import Button

class Banner():
    def  __init__(self, text, button1, button2, pos_start1, pos_start2):
        self.text = text
        self.button1 = Button(pos_start1, 300, 70, pygame.Color("#A1BF73"), pygame.Color("#5E8F2D"), f"{button1}")
        self.button2 = Button(pos_start2, 300, 70, pygame.Color("#A1BF73"), pygame.Color("#5E8F2D"), f"{button2}")
        self.image = pygame.image.load("data/images/chess_banner.png")
        self.image = pygame.transform.scale(self.image, (400, 350))
        

    def draw(self, display, show):
        if show:
            width_img, height_img = self.image.get_size()
            display.fill(pygame.Color("#302E2B"))
            display.blit(self.image, (600 - ((width_img)/2), 40))
            FONT = pygame.font.Font(None, 80)
            print_text_banner = FONT.render(self.text, True, (255, 255, 255))
            text_width = print_text_banner.get_width()
            display.blit(print_text_banner, (600-(text_width/2), 375))
            self.button1.draw(display)
            self.button2.draw(display)
            pygame.display.update()
        
        
        