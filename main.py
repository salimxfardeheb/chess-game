import pygame
from data.classes.Board import Board
from data.classes.button import Button
from data.classes.screen import Banner

pygame.init()
WINDOW_SIZE = (1200, 700)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Chess")

board = Board(700, WINDOW_SIZE[1])

button_start_x = 2*(screen.get_width()) / 7
button_start_y = 2 * (screen.get_height()) / 3

pos_start = pygame.Vector2(450, button_start_y)
pos_stop = pygame.Vector2(450, button_start_y + 100)

def draw(display):
    display.fill("#302E2B")
    board.draw_captures(display)
    board.draw_points(display)
    board.draw_turns(display)
    board.draw(display)
    pygame.display.update()

banner = Banner("Welcome to Chess", "Start", "Exit", pos_start, pos_stop)

game = True
running = True
while running:
    pieces = [i.occupying_piece for i in board.squares if i.occupying_piece is not None]
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and mx < 700 and my < 700:
                board.handle_click(mx, my)
                if board.Nulle('black'): 
                    game = True
                    banner.text = 'Draw'
                if board.Nulle('white'): 
                    game = True
                    banner.text = 'Draw'
                if board.is_in_checkmate('black'):
                    game = True
                    banner.text = 'White wins'
                if board.is_in_checkmate('white'):
                    game = True
                    banner.text = 'Black wins'
 
            if banner.button1.is_clicked(pygame.mouse.get_pos()):
                game = False
                if game :
                    board.reset()
                
            if banner.button2.is_clicked(pygame.mouse.get_pos()) and game:
                running = False
        if game:
            banner.draw(screen, game)
        else: 
            draw(screen)      
    pygame.display.flip()

pygame.quit()