import pygame
from data.classes.Square import Square
from data.classes.pieces.Rook import Rook
from data.classes.pieces.Bishop import Bishop
from data.classes.pieces.Knight import Knight
from data.classes.pieces.Queen import Queen
from data.classes.pieces.King import King
from data.classes.pieces.Pawn import Pawn

from data.classes.Piece import white_eat
from data.classes.Piece import black_eat

moves_p = []

# Game state checker
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tile_width = width // 8
        self.tile_height = height // 8
        self.selected_piece = None
        self.turn = 'white'
        self.config = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]
        self.squares = self.generate_squares()
        self.setup_board()

    def generate_squares(self):
        output = []
        for y in range(8):
            for x in range(8):
                output.append(
                    Square(x,  y, self.tile_width, self.tile_height)
                )
        return output

    def get_square_from_pos(self, pos):
        for square in self.squares:
            if (square.x, square.y) == (pos[0], pos[1]):
                return square

    def get_piece_from_pos(self, pos):
        return self.get_square_from_pos(pos).occupying_piece
    
    def setup_board(self):
        for y, row in enumerate(self.config):
            for x, piece in enumerate(row):
                if piece != '':
                    square = self.get_square_from_pos((x, y))
                    # looking inside contents, what piece does it have
                    if piece[1] == 'R':
                        square.occupying_piece = Rook(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )
                    # as you notice above, we put `self` as argument, or means our class Board
                    elif piece[1] == 'N':
                        square.occupying_piece = Knight(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )
                    elif piece[1] == 'B':
                        square.occupying_piece = Bishop(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )
                    elif piece[1] == 'Q':
                        square.occupying_piece = Queen(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )
                    elif piece[1] == 'K':
                        square.occupying_piece = King(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )
                    elif piece[1] == 'P':
                        square.occupying_piece = Pawn(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )
    def reset(self):
        self.selected_piece = None
        self.turn = 'white'
        
        self.config = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]
        self.squares = self.generate_squares()
        self.setup_board()
        white_eat.clear()
        black_eat.clear()

    def handle_click(self, mx, my):
        x = mx // self.tile_width
        y = my // self.tile_height
        clicked_square = self.get_square_from_pos((x, y))
        if self.selected_piece is None:
            if clicked_square.occupying_piece is not None:
                if clicked_square.occupying_piece.color == self.turn:
                    self.selected_piece = clicked_square.occupying_piece
        elif self.selected_piece.move(self, clicked_square):
            self.turn = 'white' if self.turn == 'black' else 'black'
        elif clicked_square.occupying_piece is not None:
            if clicked_square.occupying_piece.color == self.turn:
                self.selected_piece = clicked_square.occupying_piece

    # check state checker
    def is_in_check(self, color, board_change=None): # board_change = [(x1, y1), (x2, y2)]
        output = False
        king_pos = None
        changing_piece = None
        old_square = None
        new_square = None
        new_square_old_piece = None
        if board_change is not None:
            for square in self.squares:
                if square.pos == board_change[0]:
                    changing_piece = square.occupying_piece
                    old_square = square
                    old_square.occupying_piece = None
            for square in self.squares:
                if square.pos == board_change[1]:
                    new_square = square
                    new_square_old_piece = new_square.occupying_piece
                    new_square.occupying_piece = changing_piece
        pieces = [
            i.occupying_piece for i in self.squares if i.occupying_piece is not None
        ]
        if changing_piece is not None:
            if changing_piece.notation == 'K':
                king_pos = new_square.pos
        if king_pos == None:
            for piece in pieces:
                if piece.notation == 'K' and piece.color == color:
                        king_pos = piece.pos
        for piece in pieces:
            if piece.color != color:
                for square in piece.attacking_squares(self):
                    if square.pos == king_pos:
                        output = True
        if board_change is not None:
            old_square.occupying_piece = changing_piece
            new_square.occupying_piece = new_square_old_piece
        return output
    
    def is_in_checkmate(self, color):
        output = False
        pieces = [
            i.occupying_piece for i in self.squares if i.occupying_piece is not None
        ]
        for piece in [i.occupying_piece for i in self.squares]:
            if piece != None:
                if piece.notation == 'K' and piece.color == color:
                    king = piece
        if king.get_valid_moves(self) == []: 
            if self.is_in_check(color):
                output = True
            for piece in pieces :
                if piece.color==color:
                    if piece.get_valid_moves(self)!=[]:
                        output=False
                        break
        return output
    
    def draw(self, display):
        if self.selected_piece is not None:
            self.get_square_from_pos(self.selected_piece.pos).highlight = True
            for square in self.selected_piece.get_valid_moves(self):
                square.highlight = True
        for square in self.squares:
            square.draw(display)
    
    def Nulle(self,color):
        pieces = [
            i.occupying_piece for i in self.squares if i.occupying_piece is not None
         ]
        if len(pieces) == 2:
                return True
        elif len(pieces) == 3:
            for piece in pieces :
                if piece.notation== 'B' or piece.notation== 'N':
                    return True
        else:
         for piece in [i.occupying_piece for i in self.squares]:
           if piece != None:
                 if piece.notation == 'K' and piece.color == color:
                    king = piece
         for piece in pieces :
             if piece.color==color:
              if piece.get_valid_moves(self)!=[] :
                return False
         if king.get_valid_moves(self) == []: 
                 return True
         return False
     
    def draw_captures(self, display):
        # Position de départ pour la première pièce
        start_x = 700
        start_x_w = 900
        start_y = 10
        
        # Taille des pièces
        piece_size = (50, 50)
        for i in range(len(black_eat)):
            b_piece = black_eat[i]
            match b_piece:
                case ' ':
                    pawn = pygame.image.load('data/images/w_pawn.png')
                    pawn = pygame.transform.scale(pawn, piece_size)
                    display.blit(pawn, (start_x, start_y + i * (piece_size[1] + 5)))
                case 'R':
                    rook = pygame.image.load('data/images/w_rook.png')
                    rook = pygame.transform.scale(rook, piece_size)
                    display.blit(rook, (start_x, start_y + i * (piece_size[1] + 5)))
                case 'N':
                    knight = pygame.image.load('data/images/w_knight.png')
                    knight = pygame.transform.scale(knight, piece_size)
                    display.blit(knight, (start_x, start_y + i * (piece_size[1] + 5)))
                case 'B':
                    bishop = pygame.image.load('data/images/w_bishop.png')
                    bishop = pygame.transform.scale(bishop, piece_size)
                    display.blit(bishop, (start_x, start_y + i * (piece_size[1] + 5)))
                case 'Q':
                    queen = pygame.image.load('data/images/w_queen.png')
                    queen = pygame.transform.scale(queen, piece_size)
                    display.blit(queen, (start_x, start_y + i * (piece_size[1] + 5)))
        
        for i in range(len(white_eat)):
            w_piece = white_eat[i]
            match w_piece:
                case ' ':
                    pawn = pygame.image.load('data/images/b_pawn.png')
                    pawn = pygame.transform.scale(pawn, piece_size)
                    display.blit(pawn, (start_x_w, start_y + i * (piece_size[1] + 5)))
                case 'R':
                    rook = pygame.image.load('data/images/b_rook.png')
                    rook = pygame.transform.scale(rook, piece_size)
                    display.blit(rook, (start_x_w, start_y + i * (piece_size[1] + 5)))
                case 'N':
                    knight = pygame.image.load('data/images/b_knight.png')
                    knight = pygame.transform.scale(knight, piece_size)
                    display.blit(knight, (start_x_w, start_y + i * (piece_size[1] + 5)))
                case 'B':
                    bishop = pygame.image.load('data/images/b_bishop.png')
                    bishop = pygame.transform.scale(bishop, piece_size)
                    display.blit(bishop, (start_x_w, start_y + i * (piece_size[1] + 5)))
                case 'Q':
                    queen = pygame.image.load('data/images/b_queen.png')
                    queen = pygame.transform.scale(queen, piece_size)
                    display.blit(queen, (start_x_w, start_y + i * (piece_size[1] + 5)))
    

    def Calcul_points(self):
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
    
    def draw_points(self, display):
        wh,blc = self.Calcul_points()
        points_w = "points for white :"+ str(wh) 
        points_b = "points for black :"+ str(blc)
        font = pygame.font.Font(None, 20)
        points_surfaces_white = font.render(points_w, True, (255,255,255))
        points_surfaces_black = font.render(points_b, True,  (255,255,255))
        display.blit(points_surfaces_black, (1000, 650))
        display.blit(points_surfaces_white, (1000, 680))
        
    def draw_turns(self, display):
        font = pygame.font.Font(None, 40)
        turn_text = font.render(self.turn +" to move", True, (255,255,255))
        display.blit(turn_text,(790, 660) )