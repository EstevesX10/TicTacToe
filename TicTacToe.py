import sys
import pygame
import random
from copy import (copy, deepcopy)
from math import inf
import numpy as np
from Button import (Button, Image)
from Constants import (WIDTH,
                       HEIGHT,
                       ROWS,
                       COLS,
                       X_OFFSET,
                       Y_OFFSET,
                       SQSIZE,
                       LINE_WIDTH,
                       BG_COLOR,
                       LINES_COLOR,
                       BLACK,
                       WHITE,
                       CIRC_COLOR,
                       CIRC_WIDTH,
                       RADIUS,
                       X_COLOR,
                       X_WIDTH,
                       OFFSET)

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

    def Final_State(self, show=False):
        '''
        -> return 0 if there is no win yet
        -> return 1 if Player 1 Wins
        -> return 2 if Player 2 Wins
        '''
        
        # Vertical Wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else X_COLOR
                    Initial_Pos = (col * SQSIZE + X_OFFSET + SQSIZE // 2, 20 + Y_OFFSET)
                    Final_Pos = (col * SQSIZE + X_OFFSET + SQSIZE // 2, HEIGHT - 20 - Y_OFFSET)
                    pygame.draw.line(self.screen, color, Initial_Pos, Final_Pos, LINE_WIDTH)
                
                # Returns Player Number
                return self.squares[0][col]
        
        # Horizontal Wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else X_COLOR
                    Initial_Pos = (20 + X_OFFSET, row * SQSIZE + SQSIZE // 2 + Y_OFFSET)
                    Final_Pos = (WIDTH - 20 - X_OFFSET, row * SQSIZE + SQSIZE // 2 + Y_OFFSET)
                    pygame.draw.line(self.screen, color, Initial_Pos, Final_Pos, LINE_WIDTH)
                
                # Returns Player Number
                return self.squares[row][0]

        # Descending Diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else X_COLOR
                Initial_Pos = (20 + X_OFFSET, 20 + Y_OFFSET)
                Final_Pos = (WIDTH - 20 - X_OFFSET, HEIGHT - 20 - Y_OFFSET)
                pygame.draw.line(self.screen, color, Initial_Pos, Final_Pos, X_WIDTH)
            
            return self.squares[1][1]

        # Ascending Diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else X_COLOR
                Initial_Pos = (20 + X_OFFSET, HEIGHT - 20 - Y_OFFSET)
                Final_Pos = (WIDTH - 20 - X_OFFSET, 20 + Y_OFFSET)
                pygame.draw.line(self.screen, color, Initial_Pos, Final_Pos, X_WIDTH)
            
            return self.squares[1][1]

        # No Win Yet
        return 0

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
        self.player = 1 # PLayer 1 -> 'X' || Player 2 -> 'O'
        self.game_mode = 'AI' # PVP or AI
        self.screen = screen
        self.running = True 
    
    def Make_Move(self, row, col):
        self.board.Mark_Square(row, col, self.player)
        self.Draw_Fig(row, col)
        self.Next_Turn()

    def Show_Lines(self):
        # Paint Screen
        self.screen.fill(BG_COLOR)
        
        """ REPLACE WHITE WITH THE LINES COLOR """
        background_rect = pygame.Rect(X_OFFSET, Y_OFFSET, SQSIZE*COLS, SQSIZE*ROWS)
        
        pygame.draw.rect(self.screen, WHITE, background_rect)

        # Vertical Lines
        pygame.draw.line(self.screen, LINES_COLOR, (SQSIZE + X_OFFSET, Y_OFFSET), (SQSIZE + X_OFFSET, HEIGHT - Y_OFFSET), LINE_WIDTH)
        pygame.draw.line(self.screen, LINES_COLOR, (WIDTH - SQSIZE - X_OFFSET, Y_OFFSET), (WIDTH - SQSIZE - X_OFFSET, HEIGHT - Y_OFFSET), LINE_WIDTH)

        # Horizontal Lines
        pygame.draw.line(self.screen, LINES_COLOR, (X_OFFSET, SQSIZE + Y_OFFSET), (WIDTH - X_OFFSET, SQSIZE + Y_OFFSET), LINE_WIDTH)
        pygame.draw.line(self.screen, LINES_COLOR, (X_OFFSET, HEIGHT - SQSIZE - Y_OFFSET), (WIDTH - X_OFFSET, HEIGHT - SQSIZE - Y_OFFSET), LINE_WIDTH)

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

    def run(self, AI_Level, Mode):
        # Updating Game Parameters
        self.ai.level = AI_Level
        self.game_mode = Mode

        # Displaying the Game Board
        self.Show_Lines()

        # MAIN LOOP
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # Press g -> Change Game Mode
                    if event.key == pygame.K_g:
                        self.Change_Game_Mode()

                    if event.key == pygame.K_r:
                        self.Reset(self.screen)
                        self.game_mode = Mode
                        self.ai.level = AI_Level 
                        self.Show_Lines()
                    
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    row = (pos[1] - Y_OFFSET) // SQSIZE
                    col = (pos[0] - X_OFFSET) // SQSIZE
                    
                    if self.board.Empty_Square(row, col) and self.running:
                        self.Make_Move(row, col)
                        if self.IsOver():
                            self.running = False
            
            if self.game_mode == "AI" and self.player == self.ai.player and self.running:
                # Update the Screen
                pygame.display.update()
                
                # AI Methods
                row, col = self.ai.Evaluate(self.board)
                self.Make_Move(row, col)

                if self.IsOver():
                    self.running = False

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

class TIC_TAC_TOE():
    def __init__(self):
        # Initializing
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('TicTacToe [AI]')
        Icon = pygame.image.load('./Assets/Icon.png').convert_alpha()
        pygame.display.set_icon(Icon)

        # Board & Game Mode Variables
        self.game = Game(self.screen)
        self.board = self.game.board
        self.ai = self.game.ai

        # Fonts
        self.My_Font = pygame.font.SysFont("arialblack", 22)
        self.My_Big_Font = pygame.font.SysFont("arialblack", 30)

        # Main Application Variables
        self.Run = True
        self.Menu = "Main"

    def Write(self, text, my_font, color, x, y, screen):
        img = my_font.render(text, True, color)
        screen.blit(img, (x,y))
    
    def run(self):

        # Images & Buttons
        Main_Menu_BG_IMG = pygame.image.load('./Assets/BG_IMG.jpg').convert_alpha()
        Main_Menu_BG = Image(Main_Menu_BG_IMG, 650, -30, .6)

        Game_Mode_BG_IMG = pygame.image.load('./Assets/BG_IMG_2.jpg').convert_alpha()
        Game_Mode_BG = Image(Game_Mode_BG_IMG, 700, 0, .7)

        Play_IMG = pygame.image.load('./Assets/Start_3.png').convert_alpha()
        Play_Button = Button(Play_IMG, 220, 200, .3)

        Back_IMG = pygame.image.load('./Assets/Back.png').convert_alpha()
        Back_Button = Button(Back_IMG, 580, 20, .15)

        PVP_IMG = pygame.image.load('./Assets/PVP.png').convert_alpha()
        PVP_Button = Button(PVP_IMG, 250, 130, .2)

        AI_IMG = pygame.image.load('./Assets/AI.png').convert_alpha()
        AI_Button = Button(AI_IMG, 450, 130, .2)

        AI_BG_IMG = pygame.image.load('./Assets/BG_IMG_3.jpg').convert_alpha()
        AI_BG = Image(AI_BG_IMG, 920, 0, .6)

        AI_RANDOM_IMG = pygame.image.load('./Assets/Random.png').convert_alpha()
        AI_RANDOM_Button = Button(AI_RANDOM_IMG, 150, 180, .2)

        AI_MINIMAX_IMG = pygame.image.load('./Assets/MiniMax.png').convert_alpha()
        AI_MINIMAX_Button = Button(AI_MINIMAX_IMG, 575, 180, .2)

        EXIT_IMG = pygame.image.load('./Assets/Exit.png').convert_alpha()
        EXIT_Button = Button(EXIT_IMG, 575, 500, .2)

        while self.Run:

            if self.Menu == "Main":
                Main_Menu_BG.Display(self.screen)
                if Play_Button.Action(self.screen):
                    self.Menu = "Game_Mode"

            elif self.Menu == "Game_Mode":
                Game_Mode_BG.Display(self.screen)
                self.Write("GAME MODE", self.My_Big_Font, BLACK, 200, 50, self.screen)
                self.Write("PVP Mode", self.My_Font, BLACK, 140, 250, self.screen)
                self.Write("AI Mode", self.My_Font, BLACK, 350, 250, self.screen)
                
                if AI_Button.Action(self.screen):
                    # Activate AI Mode
                    self.Menu = "AI"
                    
                if PVP_Button.Action(self.screen):
                    # Activate PVP Mode
                    print("PVP MODE")
                    self.game.run(1, "PVP")

                if Back_Button.Action(self.screen):
                    self.Menu = "Main"
                
                if EXIT_Button.Action(self.screen):
                    self.Run = False

            elif self.Menu == "AI":
                AI_BG.Display(self.screen)
                self.Write("AI MODE", self.My_Big_Font, WHITE, 230, 50, self.screen)
                self.Write("Random", self.My_Font, WHITE, 48, 300, self.screen)
                self.Write("Choice", self.My_Font, WHITE, 56, 330, self.screen)
                self.Write("MiniMax", self.My_Font, WHITE, 475, 300, self.screen)

                if AI_RANDOM_Button.Action(self.screen):
                    print("AI RANDOM")
                    self.game.run(0, "AI")

                if AI_MINIMAX_Button.Action(self.screen):
                    print("AI MINIMAX")
                    self.game.run(1, "AI")

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

Tic_Tac_Toe = TIC_TAC_TOE()
Tic_Tac_Toe.run()