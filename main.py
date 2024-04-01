import pygame

from data.classes.Board import Board
from data.classes.Piece import white_eat
from data.classes.Piece import black_eat
from data.classes.Piece import white_points
from data.classes.Piece import black_points
pygame.init()

WINDOW_SIZE = (600, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)

board = Board(WINDOW_SIZE[0], WINDOW_SIZE[1])


def draw(display):
	display.fill('white')
	board.draw(display)
	pygame.display.update()


if __name__ == '__main__':
	running = True
	while running:
		mx, my = pygame.mouse.get_pos()
		for event in pygame.event.get():
			# Quit the game if the user presses the close button
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN: 
       			# If the mouse is clicked
				if event.button == 1:
					board.handle_click(mx, my)
		if board.is_in_checkmate('black'): # If black is in checkmate
			print('White wins!')
			print(white_eat,black_eat)
			print("les points de noir :",black_points)
			print("les points de blanc :",white_points)
			running = False
		elif board.is_in_checkmate('white'): # If white is in checkmate
			print('Black wins!')
			print(white_eat,black_eat)
			print("les points de noir :",black_points)
			print("les points de blanc :",white_points)
			running = False
		# Draw the board
		draw(screen)