import tkinter
import numpy as np
import math
class Player:
    """
    Player class to be used in the Game obj
    Attributes:
    name: text to distinguish name of player ie player1, player2, computer
    color: hex code to color each player square on click event
    white_pieces_dict: set data structure to keep track of player pieces
    black_pieces_dict: set data structure to keep track of player pieces
    """
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.positions = set()
        # dictionary of white pieces (to be updated regularly)    
        self.white_pieces_dict = \
        {'10':2,'30':4,'50':6,'70':8,\
         '01':10,'21':12,'41':14,'61':16,\
         '12':18,'32':20,'52':22,'72':24}
        # dictionary of black pieces (to be updated regularly)
        self.black_pieces_dict = \
        {'07':2,'27':4,'47':6,'67':8,\
         '16':10,'36':12,'56':14,'76':16,\
         '05':18,'25':20,'45':22,'65':24}
        # dictionary of promoted pieces
        self.white_kings = {}
        self.black_kings = {}
        move_from = [0,0]
        move_to = [0,0]
        
    def remove_piece_from_white_dict(self, key):
        # delete piece from whites dictionary
        del self.white_pieces_dict[key]
        
    def add_piece_to_white_dict(self, key):
        # add piece to whites dictionary
        self.white_pieces_dict[key] = str(key)
        
    def remove_piece_from_black_dict(self, key):
        # delete piece from blacks dictionary
        del self.black_pieces_dict[key]
        
    def add_piece_to_black_dict(self, key):
        # add piece to blacks dictionary
        self.black_pieces_dict[key] = str(key)
    
    def add_to_kings_white(self, key):
        # add piece to white king dict
        self.white_kings[key] = str(key)
    
    def add_to_kings_black(self, key):
        # add piece to white king dict
        self.black_kings[key] = str(key)
        
    def remove_black_king(self, key):
        # delete piece from blacks king dict
        del self.black_kings[key]
    
    def remove_white_king(self, key):
        # delete piece from white king dict
        del self.white_kings[key]
        
class Board:
    """
    Board class to be used in the Game obj
    Attributes:
    sq_size: integer to set size of each squares
    color: hex code to color the board size
    """

    def __init__(self, parent, sq_size, color):
        self.parent = parent   # parent is root
        self.sq_size = sq_size
        self.color = color

        # create a main container for board
        self.container = tkinter.Frame(self.parent)
        self.container.pack()

        # create canvas for container
        self.canvas = tkinter.Canvas(self.container,
                                     width= self.sq_size * 8,
                                     height= self.sq_size * 8)
        # register main canvas
        self.canvas.grid()
        
    
    def draw_board(self):
        # create checkerboard pattern on frame
        for row in range(8):
            for column in range(8):
                if row % 2 == 0 and (row*8 + column) % 2 == 1:
                    color_square = '#769656'
                elif row % 2 == 1 and (row*8 + column) % 2 == 0:
                    color_square = '#769656'
                else:
                    color_square = '#eeeed2'
                self.canvas.create_rectangle(self.sq_size  * column,
                                        self.sq_size  * row,
                                        self.sq_size  * (column + 1),
                                        self.sq_size  * (row + 1),
                                        fill = color_square)
    def set_board(self):
      # draw pieces for initial board position (0,0) position upper left
        for row in range(8):
            for column in range(8):
                if row == 0 and column % 2 == 1 or row == 1 and column % 2 == 0 or \
                                                row == 2 and column % 2 == 1:
                    color_piece = '#ffffff'
                    self.canvas.create_oval(self.sq_size  * column+4.0,
                                            self.sq_size  * row+4.0,
                                            self.sq_size  * (column + 1)-4.0,
                                            self.sq_size  * (row + 1)-4.0,
                                            fill = color_piece)

                if row == 5 and column % 2 == 0 or row == 6 and column % 2 == 1 or \
                                                row == 7 and column % 2 == 0:
                    color_piece = '#000000'
                    self.canvas.create_oval(self.sq_size  * column+4.0,
                                            self.sq_size  * row+4.0,
                                            self.sq_size  * (column + 1)-4.0,
                                            self.sq_size  * (row + 1)-4.0,
                                            fill = color_piece)
            
    def floor_of_row_col(self, col, rw):
        """
        normalize col and row number for all board size by taking
        the floor of event's x and y coords as col and row, respectively
        """
        col_flr = col // self.sq_size
        rw_flr = rw // self.sq_size
        return col_flr, rw_flr

    
    def find_coords_of_selected_sq(self, evt):
        """
        finding coords in a 64-sq grid
        params: event triggered by user's click
        return: tuple of two values for second corner's col, row
        """
        # saves row and col tuple into two variables
        # returns x, y coordinate of event
        column = evt.x; row = evt.y
        # normalize coordinate by square size
        column_floor, row_floor = self.floor_of_row_col(column, row) 

        # convert coordinates to string, use string to locate position in 8x8 grid
        
        rowcol_key_str = str(column_floor) + str(row_floor)

        corner_column = (column_floor * self.sq_size) + self.sq_size
        corner_row =  (row_floor  * self.sq_size) + self.sq_size
        
        return corner_column, corner_row

    def delete_piece(self, evt, second_corner_col, second_corner_row):
        # colour over piece on canvas object

        self.canvas.create_rectangle(
            (evt.x // self.sq_size) * self.sq_size,
            (evt.y // self.sq_size) * self.sq_size,
            second_corner_col,
            second_corner_row,
            fill = '#769656')
        
    def capture_piece(self, capture_col, capture_row):
        # colour over piece on canvas object
        self.canvas.create_rectangle(
            capture_col,
            capture_row,
            capture_col - self.sq_size,
            capture_row - self.sq_size,
            fill = '#769656')

    def place_piece(self, evt, second_corner_col, second_corner_row, player_color):
        
        self.canvas.create_oval(
          (evt.x // self.sq_size) * self.sq_size+4.0,
          (evt.y // self.sq_size) * self.sq_size+4.0,
          second_corner_col-4.0,
          second_corner_row-4.0,
          fill = player_color)
    
    def place_king(self, evt, second_corner_col, second_corner_row, player_color):
        self.canvas.create_oval(
          (evt.x // self.sq_size) * self.sq_size+8.0,
          (evt.y // self.sq_size) * self.sq_size+8.0,
          second_corner_col-4.0,
          second_corner_row-4.0,
          fill = "#dfc024")

        self.canvas.create_oval(
          (evt.x // self.sq_size) * self.sq_size+12.0,
          (evt.y // self.sq_size) * self.sq_size+12.0,
          second_corner_col-8.0,
          second_corner_row-8.0,
          fill = player_color)
        
        
class GameApp(object):
    """
    GameApp class as controller for board and player objects
    Attributes:
    parent: (tkinter.Tk) the root window, parent of the frame
    board: instance of the board class
    unused_squares_dict: keep track of squares left on the board
    player1: instance of player class
    player2: ibid
    computer: ibid
    """

    def __init__(self, parent, board_size):
        self.parent = parent  # parent is root
        self.board_size = board_size
        # create a board object
        self.board = Board(self.parent, board_size, "#ECECEC")  # hex color gray
        self.board.draw_board() # draws board

        # create all players instances
        self.player1 = Player("Player 1", "#000000") # hex black
        self.player2 = Player("Player 2", "#ffffff") # hex white

        self.initialize_buttons()
        # create a menu for game option
        self.start_menu()
    
    def initialize_buttons(self):
        #  --- create buttons for menu ---
        self.two_players_button = tkinter.Button(self.board.container,
                                text = "start game",
                                width = 25,
                                command = self.init_two_players_game)

        self.reset_button = tkinter.Button(self.board.container,
                                           text = "RESET",
                                           width = 25,
                                           command = self.restart)
        
        self.cancel_button = tkinter.Button(self.board.container,
                                           text = "cancel move",
                                           width = 25,
                                           command = self.cancel)

    def start_menu(self):
         # register buttons to board's container
        self.two_players_button.grid()
        
    def init_two_players_game(self):
        # reset board's unused squares
    #    self.board.reset_unused_squares_dict()
        self.board.set_board() # draws pieces on canvas
        # reset players' squares to empty set
        self.player1.selected_sq = set()
        self.player2.selected_sq = set()

        # keep track of turns and turn phases
        self.player_turn = 0 # 0 for black, 1 for white
        self.phase = 0 # 0 for choose
        # show reset button
        self.reset_button.grid()
        self.cancel_button.grid()
        # launch game
        self.board.canvas.bind("<Button-1>", self.play)
        
    """
    Reinitialize the game and board after restart button is pressed 
    """
    def restart(self):        
        self.board.container.destroy()
        # create a new board object and draw board + buttons again
        self.board = Board(self.parent, self.board_size, "#ECECEC")
        self.board.draw_board()
        # create all players instances
        self.player1 = Player("Player 1", "#000000") # hex black
        self.player2 = Player("Player 2", "#ffffff") # hex white
        
        self.initialize_buttons()
        # create a menu for game option
        self.start_menu()
     
    
    def cancel(self):        
        #cancel move by recalling play fn()
        self.play()
        
    def isLegal(self, move_from, move_to, player_turn, is_king):

        # allow jumps if it's capturing a piece
        capturing = [0,0]
        capturing[0] = int(sum([move_from[0],move_to[0]])/2)
        capturing[1] = int(sum([move_from[1],move_to[1]])/2)
        capture_key = str(capturing[0]) + str(capturing[1])
        print("from legality fn : "+str(capture_key)+"\n")
        # allow only single forward diagonal forward moves otherwise
        if player_turn == 0: # player 0 is black pieces
            # movement for standard pieces
            if is_king == False:
                if np.abs(move_from[0]-move_to[0]) == 2 and \
                move_from[1]-move_to[1] == 2 and capture_key in\
                self.player2.white_pieces_dict.values():
                    return capture_key #  move is allowed AND it's a capture
                elif np.abs(move_from[0]-move_to[0]) == 1 and \
                    move_from[1]-move_to[1] == 1 :
                    return True
                else:
                    return False
            # movement for promoted pieces
            elif is_king == True:
                if np.abs(move_from[0]-move_to[0]) == 2 and \
                np.abs(move_from[1]-move_to[1]) == 2 and capture_key in\
                self.player2.white_pieces_dict.values():
                    return capture_key #  move is allowed AND it's a capture
                elif np.abs(move_from[0]-move_to[0]) == 1 and \
                    np.abs(move_from[1]-move_to[1]) == 1 :
                    return True
                else:
                    return False
                
        if player_turn == 1: # player 1 is white pieces
            # movement for standard pieces
            if is_king == False:
                if np.abs(move_from[0]-move_to[0]) == 2 and\
                move_from[1]-move_to[1] == -2 and capture_key in\
                self.player1.black_pieces_dict.values() :
                    return capture_key #  move is allowed AND it's a capture
                elif np.abs(move_from[0]-move_to[0]) == 1 and \
                    move_from[1]-move_to[1] == -1 :
                    return True
                else:
                    return False

            # movement for promoted pieces
            elif is_king == True:
                if np.abs(move_from[0]-move_to[0]) == 2 and \
                np.abs(move_from[1]-move_to[1]) == 2 and capture_key in\
                self.player1.black_pieces_dict.values():
                    return capture_key #  move is allowed AND it's a capture
                elif np.abs(move_from[0]-move_to[0]) == 1 and \
                    np.abs(move_from[1]-move_to[1]) == 1 :
                    return True
                else:
                    return False
        
    def isTrapped(self, move_from, player_turn):
        
        """
        Adding a "cancel move" button is likely a better solution than checking 
        every move like this
        """
        free = True
        target_key = str(move_from[0]+1) + str(move_from[1]+1)
        if player_turn == 0:
            if target_key not in self.player1.black_pieces_dict.values() and \
                target_key not in self.player1.white_pieces_dict.values():
                return True
        target_key = str(move_from[0]+1) + str(move_from[1]-1)
        if player_turn == 0:
            if target_key in self.player1.black_pieces_dict.values() or \
                target_key in self.player1.white_pieces_dict.values():
                free = True
            
    def play(self, event):
        """  method is invoked when the user clicks on a square
        handles click event on UI for player
        Params: event (as mouse click, with x/y coords)
        """
        if self.player_turn == 0:
            print("player 1 turn")
        else:
            print("player 2 turn")
        if self.phase == 0:
            print("select piece to move")
        else:
            print("sure")
        
        # Selecting piece to move from 

        # coordinates for canvas referencing when player click on a square
        target_col, target_row = self.board.find_coords_of_selected_sq(event)
        # coordinates for dictionary management
        col_fl, row_fl = self.board.floor_of_row_col(event.x, event.y)
        rowcol_key = str(col_fl) + str(row_fl)
        
        self.promote = False        

        # PLAYER ONE PHASE ONE
        if self.player_turn == 0 and self.phase == 0:
            #self.add_to_player_sq(rowcol_key, self.player1.selected_sq)
            # remove piece from canvas    
            self.player1.move_from = [col_fl, row_fl]
            # prevent pieces being trapped
            #if self.isTrapped(self.player1.move_from, self.player_turn) == False:
            if rowcol_key in self.player1.black_pieces_dict:
                self.board.delete_piece(event,
                                    target_col,
                                    target_row)
                # check is piece a king?
                if rowcol_key in self.player1.black_kings:
                    self.is_king = True
                    #remove king from dictionary
                    self.player1.remove_black_king(rowcol_key)
                else:
                    self.is_king = False
                #remove piece from dictionary
                self.player1.remove_piece_from_black_dict(rowcol_key)
                print("removed "+str(rowcol_key))
                self.phase = 1      

        # PLAYER ONE PHASE TWO
        elif self.player_turn == 0 and self.phase == 1:        
            self.player1.move_to = [col_fl, row_fl]
            if self.player1.move_to[0] == 0:
                self.promote = True
            
            legality = self.isLegal(self.player1.move_from, self.player1.move_to, self.player_turn, self.is_king)
            print("legality: "+str(legality) )
            if legality == True:
                if rowcol_key not in self.player1.black_pieces_dict and \
                        rowcol_key not in self.player2.white_pieces_dict:
                    # draw piece on canvas
                    print("promote? "+str(self.promote))
                    if self.promote == False:
                        if self.is_king == True:
                            self.board.place_king(event,
                                            target_col,
                                            target_row,
                                            self.player1.color)
                        else: 
                            self.board.place_piece(event,
                                            target_col,
                                            target_row,
                                            self.player1.color)
                    elif self.promote == True:
                        self.board.place_king(event,
                                            target_col,
                                            target_row,
                                            self.player1.color)
                        print("placing king")
                    # add piece to dictionary 
                    self.player1.black_pieces_dict[rowcol_key] = str(rowcol_key)
                    if self.promote == True or self.is_king == True:
                        self.player1.black_kings[rowcol_key] = str(rowcol_key)
                    self.phase = 0
                    # switch turn
                    self.player_turn = 1
            if legality not in [0,1]:
                # if isLegal method returns a string
                # capture the piece given by that string
                
                self.board.capture_piece(target_col-math.copysign(1, self.player1.move_to[0]-\
                            self.player1.move_from[0])*self.board_size, target_row+self.board_size)
                
                #remove piece from dictionary
                self.player2.remove_piece_from_white_dict(legality)
                print("removed "+str(legality))
                # draw piece on canvas
                print("promote? "+str(self.promote))
                if self.promote == False:
                    if self.is_king == False:
                        self.board.place_piece(event,
                                        target_col,
                                        target_row,
                                        self.player1.color)
                    elif self.is_king == True:
                        self.board.place_king(event,
                                        target_col,
                                        target_row,
                                        self.player1.color)

                elif self.promote == True:
                    self.board.place_king(event,
                                        target_col,
                                        target_row,
                                        self.player1.color)
                    print("placing king")
                # add piece to dictionary 
                self.player1.black_pieces_dict[rowcol_key] = str(rowcol_key)
                if self.promote == True:
                    self.player1.black_kings[rowcol_key] = str(rowcol_key)
                self.phase = 0
                # switch turn
                self.player_turn = 1
                
        # PLAYER TWO PHASE ONE
        if self.player_turn == 1 and self.phase == 0:
            
            # remove piece from canvas    
            self.player2.move_from = [col_fl, row_fl]
            # prevent pieces being trapped
            #if self.isTrapped(self.player1.move_from, self.player_turn) == False:
            if rowcol_key in self.player2.white_pieces_dict:
                self.board.delete_piece(event,
                                    target_col,
                                    target_row)
                # check is piece a king?
                if rowcol_key in self.player2.white_kings:
                    self.is_king = True
                    #remove king from dictionary
                    self.player2.remove_white_king(rowcol_key)
                else:
                    self.is_king = False
                #remove piece from dictionary
                self.player2.remove_piece_from_white_dict(rowcol_key)
                print("removed "+str(rowcol_key))
                self.phase = 1      

        # PLAYER TWO PHASE TWO
        elif self.player_turn == 1 and self.phase == 1:        
            self.player2.move_to = [col_fl, row_fl]
            if self.player2.move_to[0] == 7:
                self.promote = True
            
            legality = self.isLegal(self.player2.move_from, self.player2.move_to, self.player_turn, self.is_king)
            if legality == True:
                if rowcol_key not in self.player2.white_pieces_dict and \
                        rowcol_key not in self.player1.black_pieces_dict:
                    # draw piece on canvas
                    print("promote? "+str(self.promote))
                    if self.promote == False:
                        if self.is_king == True:
                            self.board.place_king(event,
                                            target_col,
                                            target_row,
                                            self.player2.color)
                        else: 
                            self.board.place_piece(event,
                                            target_col,
                                            target_row,
                                            self.player2.color)
                    elif self.promote == True:
                        self.board.place_king(event,
                                            target_col,
                                            target_row,
                                            self.player2.color)
                        print("placing king")
                    # add piece to dictionary 
                    self.player2.white_pieces_dict[rowcol_key] = str(rowcol_key)
                    if self.promote == True or self.is_king == True:
                        self.player2.white_kings[rowcol_key] = str(rowcol_key)
                    self.phase = 0
                    # switch turn
                    self.player_turn = 0
            if legality not in [0,1]:
                # if isLegal method returns a string
                # capture the piece given by that string
            
                self.board.capture_piece(target_col-math.copysign(1, self.player2.move_to[0]-\
                            self.player2.move_from[0])*self.board_size, target_row-self.board_size)
                
                print("removed "+str(legality))
                #remove piece from dictionary
                self.player1.remove_piece_from_black_dict(legality)
            
                # draw piece on canvas
                print("promote? "+str(self.promote))
                if self.promote == False:
                    if self.is_king == False:
                        self.board.place_piece(event,
                                        target_col,
                                        target_row,
                                        self.player2.color)
                    elif self.is_king == True:
                        self.board.place_king(event,
                                        target_col,
                                        target_row,
                                        self.player2.color)

                elif self.promote == True:
                    self.board.place_king(event,
                                        target_col,
                                        target_row,
                                        self.player2.color)
                    print("placing king")
                # add piece to dictionary 
                self.player2.white_pieces_dict[rowcol_key] = str(rowcol_key)
                if self.promote == True:
                    self.player2.white_kings[rowcol_key] = str(rowcol_key)
                self.phase = 0
                # switch turn
                self.player_turn = 0

                
def main():
    board_size = 60
    root = tkinter.Tk()
    root.title("draughts")
    tictac_game = GameApp(root, board_size)  # root is parent
    root.mainloop()

if __name__ == '__main__':
    main()
