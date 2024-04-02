import pygame

from data.classes.Board import Board
from data.classes.Piece import white_eat
from data.classes.Piece import black_eat
pygame.init()

WINDOW_SIZE = (900, 900)
screen = pygame.display.set_mode(WINDOW_SIZE)

board = Board(WINDOW_SIZE[0], WINDOW_SIZE[1])


def draw(display):
	display.fill('white')
	board.draw(display)
	pygame.display.update()

def Calcul_points():
	white_points = 0
	black_points = 0
	for i in range(len(white_eat)):
				if white_eat[i]==' ':
					white_points += 1
				elif white_eat[i] =='N':
					white_points += 3
				elif white_eat[i] =='B':
					white_points += 3
				elif white_eat[i] =='R':
					white_points += 5
				elif white_eat[i] =='Q':
					white_points += 9		
	for i in range(len(black_eat)):
				if black_eat[i]==' ':
					black_points += 1
				elif black_eat[i] =='N':
					black_points += 3
				elif black_eat[i] =='B':
					black_points += 3
				elif black_eat[i] =='R':
					black_points += 5
				elif black_eat[i] =='Q':
					black_points += 9	
	return white_points,black_points	







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
			running = False
		elif board.is_in_checkmate('white'): # If white is in checkmate
			print('Black wins!')
			running = False
		if board.Nulle('black'): # If black is in checkmate
			print('Draw')
			running = False
		if board.Nulle('white'): # If black is in checkmate
			print('Draw')
			running = False
		wh,blc =Calcul_points()
		print(white_eat,black_eat)
		print ("les points de noir",blc)
		print ("les points de blanc",wh)
		# Draw the board
		draw(screen)