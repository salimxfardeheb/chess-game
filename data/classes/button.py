import pygame

class Button:
    def __init__(self, pos, width, height, hover_color, color, text=''):
        self.pos_x = pos.x
        self.pos_y = pos.y
        self.rect = pygame.Rect(self.pos_x, self.pos_y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.font = pygame.font.Font(None, 48)
        self.radius = 10


    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.hover_color, self.rect, border_radius= self.radius)
        else:
            pygame.draw.rect(surface, self.color, self.rect, border_radius= self.radius)
        if self.text != '':
            text_surface = self.font.render(self.text, True, ("#FFFFFF"))
            text_rect = text_surface.get_rect(center= self.rect.center)
            surface.blit(text_surface,text_rect)


    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)