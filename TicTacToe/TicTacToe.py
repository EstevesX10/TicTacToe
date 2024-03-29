import sys
import pygame
import random
from copy import (deepcopy)
from math import (inf)
import numpy as np
from Button import (Button, Image)
from Constants import (WIDTH,
                       HEIGHT,
                       ROWS,
                       COLS,
                       OFFSET,
                       X_OFFSET,
                       Y_OFFSET,
                       SQSIZE,
                       LINE_WIDTH,
                       BG_COLOR,
                       LINES_COLOR,
                       WHITE,
                       BLUE,
                       BEIGE,
                       CIRC_COLOR,
                       CIRC_WIDTH,
                       RADIUS,
                       X_COLOR,
                       X_WIDTH)

class Board:
    def __init__(self, screen):
        self.screen = screen
        self.squares = np.zeros((ROWS,COLS))
        self.empty_squares = self.squares # List of Empty Squares
        self.marked_squares = 0 # Number os Squares Occupied

    def Copy(self):
        other_board = Board(self.screen)
        other_board.squares = deepcopy(self.squares)
        other_board.empty_squares = deepcopy(self.empty_squares)
        other_board.marked_squares = self.marked_squares
        return other_board

    def Final_State(self, show=False): # Marking Winner Lines 
        '''
        -> return 0 if there is no win yet
        -> return 1 if Player 1 Wins
        -> return 2 if Player 2 Wins
        '''
        
        winner = 0

        # Vertical Wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else X_COLOR
                    Initial_Pos = (col * SQSIZE + X_OFFSET + SQSIZE // 2, 20 + Y_OFFSET)
                    Final_Pos = (col * SQSIZE + X_OFFSET + SQSIZE // 2, 3*SQSIZE - 20 + Y_OFFSET)
                    pygame.draw.line(self.screen, color, Initial_Pos, Final_Pos, LINE_WIDTH)
                
                # Updates Player Number
                winner = self.squares[0][col]
        
        # Horizontal Wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else X_COLOR
                    Initial_Pos = (20 + X_OFFSET, row * SQSIZE + SQSIZE // 2 + Y_OFFSET)
                    Final_Pos = (WIDTH - 20 - X_OFFSET, row * SQSIZE + SQSIZE // 2 + Y_OFFSET)
                    pygame.draw.line(self.screen, color, Initial_Pos, Final_Pos, LINE_WIDTH)
                
                # Updates Player Number
                winner = self.squares[row][0]

        # Descending Diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else X_COLOR
                Initial_Pos = (20 + X_OFFSET, 20 + Y_OFFSET)
                Final_Pos = (X_OFFSET + 3*SQSIZE - 20, Y_OFFSET + 3*SQSIZE - 20)
                pygame.draw.line(self.screen, color, Initial_Pos, Final_Pos, X_WIDTH)
            
            # Updates Winner
            winner = self.squares[1][1]

        # Ascending Diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else X_COLOR
                Initial_Pos = (20 + X_OFFSET, Y_OFFSET + 3*SQSIZE - 20)
                Final_Pos = (X_OFFSET + 3*SQSIZE - 20, 20 + Y_OFFSET)
                pygame.draw.line(self.screen, color, Initial_Pos, Final_Pos, X_WIDTH)
            
            # Updates Winner
            winner = self.squares[1][1]

        # No Win Yet [Initial Value => 0]
        return winner

    def Mark_Square(self, row, col, player):
        self.squares[row][col] = player
        self.marked_squares += 1
    
    def Empty_Square(self, row, col):
        return self.squares[row][col] == 0

    def Get_Empty_Squares(self):
        empty_squares = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.Empty_Square(row, col):
                    empty_squares.append((row, col))
        return empty_squares

    def Is_Full(self):
        return self.marked_squares == 9
    
    def Is_Empty(self):
        return self.marked_squares == 0

class Game:
    def __init__(self, screen):
        self.board = Board(screen)
        self.ai = AI()
        self.player = 1 # Player 1 -> 'X' || Player 2 -> 'O'
        self.game_mode = 'AI' # PVP or AI
        self.screen = screen
        self.winner = 0 # 0 -> Tie || 1 -> 'X' Wins || 2 -> 'O' Wins
    
    def Make_Move(self, row, col):
        self.board.Mark_Square(row, col, self.player)
        self.Draw_Fig(row, col)
        self.Next_Turn()

    def Show_Lines(self):
        # Paint Screen
        self.screen.fill(BLUE)
        
        background_rect = pygame.Rect(X_OFFSET, Y_OFFSET, SQSIZE*COLS, SQSIZE*ROWS)
        pygame.draw.rect(self.screen, BG_COLOR, background_rect, 0, 8)

        # Vertical Lines
        pygame.draw.line(self.screen, LINES_COLOR, (SQSIZE + X_OFFSET, Y_OFFSET), (SQSIZE + X_OFFSET, Y_OFFSET + 3*SQSIZE - 1), LINE_WIDTH)
        pygame.draw.line(self.screen, LINES_COLOR, (2*SQSIZE + X_OFFSET, Y_OFFSET), (2*SQSIZE + X_OFFSET, Y_OFFSET + 3*SQSIZE - 1), LINE_WIDTH)

        # Horizontal Lines
        pygame.draw.line(self.screen, LINES_COLOR, (X_OFFSET, SQSIZE + Y_OFFSET), (X_OFFSET + 3*SQSIZE - 1, SQSIZE + Y_OFFSET), LINE_WIDTH)
        pygame.draw.line(self.screen, LINES_COLOR, (X_OFFSET, Y_OFFSET + 2*SQSIZE), (X_OFFSET + 3*SQSIZE - 1, Y_OFFSET + 2*SQSIZE), LINE_WIDTH)

    def Draw_Fig(self, row, col):
        if self.player == 1:
            # Draw 'X (Composed by Ascending and Decending Line)
            # Descending line
            start_desc = (col * SQSIZE + X_OFFSET + OFFSET, row * SQSIZE + Y_OFFSET + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE + X_OFFSET - OFFSET, row * SQSIZE + SQSIZE + Y_OFFSET - OFFSET)
            pygame.draw.line(self.screen, X_COLOR, start_desc, end_desc, X_WIDTH)

            # Ascending line
            start_asc = (col * SQSIZE + X_OFFSET + OFFSET, row * SQSIZE + SQSIZE + Y_OFFSET - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE + X_OFFSET - OFFSET, row * SQSIZE + Y_OFFSET + OFFSET)
            pygame.draw.line(self.screen, X_COLOR, start_asc, end_asc, X_WIDTH)

        elif(self.player == 2):
            # Draw 'O'
            center = (col * SQSIZE + X_OFFSET + SQSIZE // 2, row * SQSIZE + Y_OFFSET + SQSIZE // 2)
            pygame.draw.circle(self.screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

    def Next_Turn(self):
        self.player = 1 if self.player == 2 else 2

    def Change_Game_Mode(self):
        self.game_mode = 'AI' if self.game_mode == 'PVP' else 'PVP'

    def IsOver(self):
        return self.board.Final_State(show=True) != 0 or self.board.Is_Full()

    def Reset(self, screen):
        self.__init__(screen)

    def Valid_Pos(self, row, col):
        if ((row >= 0 and row < COLS) and (col >= 0 and col < ROWS)):
            return True # Inside the Board
        else:
            return False # Outside of the Board

    def Find_Winner(self):
        final_state = self.board.Final_State(show=True)
        if (final_state != 0):
            return int(final_state)
        return 0

    def Write(self, font, text, size, color, bg_color, bold, pos, screen):
        ''' Writes Text into the Screen '''
        letra = pygame.font.SysFont(font, size, bold)
        frase = letra.render(text, 1, color, bg_color)
        screen.blit(frase, pos)

    def run(self, AI_Level, Mode):
        # Updating Game Parameters
        self.ai.level = AI_Level
        self.game_mode = Mode

        # Displaying the Game Board
        self.Show_Lines()

        # Creating Buttons
        Back_IMG = pygame.image.load('./Assets/Back.png').convert_alpha()
        Back_Button = Button(Back_IMG, 75, 25, .1)
        
        Reset_IMG = pygame.image.load('./Assets/Reset.png').convert_alpha()
        Reset_Button = Button(Reset_IMG, 575, 25, .09)

        # Extra Game Variables
        Game_Over = False
        Run = True

        # MAIN LOOP
        while Run:

            # Buttons
            if (Back_Button.Action(self.screen)):
                Run = False

            if (Reset_Button.Action(self.screen)):
                Game_Over = False
                self.Reset(self.screen)
                self.game_mode = Mode
                self.ai.level = AI_Level
                self.Show_Lines()
            
            if not Game_Over and self.game_mode == "AI" and self.player == self.ai.player and Run:
                # Update the Screen
                pygame.display.update()
                
                # AI Methods
                row, col = self.ai.Evaluate(self.board)
                self.Make_Move(row, col)

                if self.IsOver():
                    self.winner = self.Find_Winner()
                    Game_Over = True

            # Event Loop
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Run = False

                    if event.key == pygame.K_r:
                        Game_Over = False
                        self.Reset(self.screen)
                        self.game_mode = Mode
                        self.ai.level = AI_Level
                        self.Show_Lines()
                    
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if not Game_Over and event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    row = (pos[1] - Y_OFFSET) // SQSIZE
                    col = (pos[0] - X_OFFSET) // SQSIZE

                    if self.Valid_Pos(row, col) and self.board.Empty_Square(row, col) and Run:
                        self.Make_Move(row, col)
                        if self.IsOver():
                            self.winner = self.Find_Winner()
                            Game_Over = True

                if (Game_Over):
                    if (self.game_mode == "PVP"):
                        if (self.winner == 0): # Tie
                            self.Write("Arial", " Tie ", 40, BEIGE, WHITE, True, (1.85*SQSIZE, 35), self.screen)
                        else: # One of the Players Win
                            self.Write("Arial", " Player {} Wins! ".format(self.winner), 40, BEIGE, WHITE, True, (1.22*SQSIZE, 35), self.screen)
                    elif (self.game_mode == "AI"):
                        if (self.winner == 0): # Tie
                            self.Write("Arial", " Tie ", 40, BEIGE, WHITE, True, (1.85*SQSIZE, 35), self.screen)
                        elif (self.winner == 1): # Player 1 Wins
                            self.Write("Arial", " You Won! ".format(self.winner), 40, BEIGE, WHITE, True, (1.48*SQSIZE, 35), self.screen)
                        else: # AI Wins
                            self.Write("Arial", " AI Won! ".format(self.winner), 40, BEIGE, WHITE, True, (1.58*SQSIZE, 35), self.screen)
                        
            pygame.display.update()

class AI:
    def __init__(self, level=1, player=2):
        # level = 0 -> Random AI
        # level = 1 -> AI with MiniMax
        self.level = level
        self.player = player

    def Random_Choice(self, board:Board):
        empty_squares = board.Get_Empty_Squares()
        Rand_Index = random.randrange(0, len(empty_squares))
        # Return a Random Empty Square 
        return empty_squares[Rand_Index]

    def MiniMax(self, board:Board, maximizing:bool):
        
        # Check Terminal Cases
        Case = board.Final_State()

        # Player 1 Wins
        if Case == 1:
            # Evaluation, Move
            return 1, None
        
        # Player 2 Wins - AI
        if Case == 2:
            # Evaluation, Move
            return -1, None
        
        # Draw
        elif(board.Is_Full()):
            # Evaluation, Move
            return 0, None
        
        if maximizing:
            Max_Evaluation = -inf
            Best_Move = None
            Empty_Squares = board.Get_Empty_Squares()

            for (row, col) in Empty_Squares:
                Temp_Board = board.Copy()
                Temp_Board.Mark_Square(row, col, 1)
                Evaluation = self.MiniMax(Temp_Board, False)[0]
                if Evaluation > Max_Evaluation:
                    Max_Evaluation = Evaluation
                    Best_Move = (row,col)
            
            return Max_Evaluation, Best_Move
        
        elif not maximizing:
            Min_Evaluation = inf
            Best_Move = None
            Empty_Squares = board.Get_Empty_Squares()

            for (row, col) in Empty_Squares:
                Temp_Board = board.Copy()
                Temp_Board.Mark_Square(row, col, self.player)
                Evaluation = self.MiniMax(Temp_Board, True)[0]
                if Evaluation < Min_Evaluation:
                    Min_Evaluation = Evaluation
                    Best_Move = (row,col)
            
            return Min_Evaluation, Best_Move

    def Evaluate(self, Main_Board:Board):
        if self.level == 0:
            # Random Choice
            Evaluation = 'random'
            Move = self.Random_Choice(Main_Board)
        else:
            # MiniMax Algorithm Choice
            Evaluation, Move = self.MiniMax(Main_Board, False)
        
        print(f"AI has chosen to mark the square in pos {Move} with an Evaluation of {Evaluation}")
        return Move

class TicTacToe():
    def __init__(self):
        # Initializing Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('TicTacToe [AI]')
        Icon = pygame.image.load('./Assets/Icon.png').convert_alpha()
        pygame.display.set_icon(Icon)

        # Fonts
        self.My_Font = pygame.font.SysFont("arialblack", 22)
        self.My_Big_Font = pygame.font.SysFont("arialblack", 30)

        # Main Application Variables
        self.Run = True
        self.Menu = "Main"
    
    def write(self, font, text, size, color, bg_color, bold, pos, screen):
        ''' Writes Text into the Screen '''
        letra = pygame.font.SysFont(font, size, bold)
        frase = letra.render(text, 1, color, bg_color)
        screen.blit(frase, pos)

    def run(self):
        # Images & Buttons
        Main_Menu_BG_IMG = pygame.image.load('./Assets/BG_IMG.jpg').convert_alpha()
        Main_Menu_BG = Image(Main_Menu_BG_IMG, 650, -30, .6)

        Play_IMG = pygame.image.load('./Assets/Start.png').convert_alpha()
        Play_Button = Button(Play_IMG, 220, 240, .3)

        Back_IMG = pygame.image.load('./Assets/Back.png').convert_alpha()
        Back_Button = Button(Back_IMG, 75, 25, .1)

        PVP_IMG = pygame.image.load('./Assets/PVP.png').convert_alpha()
        PVP_Button = Button(PVP_IMG, 250, 200, .2)

        AI_IMG = pygame.image.load('./Assets/AI.png').convert_alpha()
        AI_Button = Button(AI_IMG, 450, 200, .2)

        AI_RANDOM_IMG = pygame.image.load('./Assets/Random.png').convert_alpha()
        AI_RANDOM_Button = Button(AI_RANDOM_IMG, 250, 200, .2)

        AI_MINIMAX_IMG = pygame.image.load('./Assets/MiniMax.png').convert_alpha()
        AI_MINIMAX_Button = Button(AI_MINIMAX_IMG, 450, 200, .2)

        EXIT_IMG = pygame.image.load('./Assets/Exit.png').convert_alpha()
        EXIT_Button = Button(EXIT_IMG, 575, 520, .2)

        while self.Run:

            if self.Menu == "Main":
                Main_Menu_BG.Display(self.screen)
                if Play_Button.Action(self.screen):
                    self.Menu = "Game_Mode"

            elif self.Menu == "Game_Mode":
                self.screen.fill(BLUE)
                self.write("Arial", " Game Mode ", 40, BEIGE, WHITE, True, (200, 50), self.screen)
                self.write("Arial", " PVP ", 30, BEIGE, WHITE, False, (170, 330), self.screen)
                self.write("Arial", " AI ", 30, BEIGE, WHITE, False, (380, 330), self.screen)

                if AI_Button.Action(self.screen):
                    # Activate AI Mode
                    self.Menu = "AI"
                    
                if PVP_Button.Action(self.screen):
                    game = Game(self.screen)
                    game.run(1, "PVP")

                if Back_Button.Action(self.screen):
                    self.Menu = "Main"
                
                if EXIT_Button.Action(self.screen):
                    self.Run = False

            elif self.Menu == "AI":
                self.screen.fill(BLUE)
                self.write("Arial", " AI Mode ", 40, BEIGE, WHITE, True, (225, 50), self.screen)
                self.write("Arial", " Random ", 30, BEIGE, WHITE, False, (145, 330), self.screen)
                self.write("Arial", " MinMax ", 30, BEIGE, WHITE, False, (349, 330), self.screen)

                if AI_RANDOM_Button.Action(self.screen):
                    game = Game(self.screen)
                    game.run(0, "AI")

                if AI_MINIMAX_Button.Action(self.screen):
                    game = Game(self.screen)
                    game.run(1, "AI")

                if Back_Button.Action(self.screen):
                    self.Menu = "Game_Mode"
                
                if EXIT_Button.Action(self.screen):
                    self.Run = False

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pass

                if event.type == pygame.QUIT:
                    self.Run = False
            
            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    Tic_Tac_Toe = TicTacToe()
    Tic_Tac_Toe.run()