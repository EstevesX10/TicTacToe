import sys
import pygame
import random
import copy
from time import sleep
from math import inf
import numpy as np

from Const import *
from Button import Button

pygame.init()
Screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe -> AI')
Icon = pygame.image.load('Extras/Icon.png').convert_alpha()
pygame.display.set_icon(Icon)

class Board:

    def __init__(self):
        self.squares = np.zeros((ROWS,COLS))
        self.empty_squares = self.squares # List of Empty Squares
        self.marked_squares = 0 # Number os Squares Occupied

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
                    Initial_Pos = (col * SQSIZE + SQSIZE // 2, 20)
                    Final_Pos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(Screen, color, Initial_Pos, Final_Pos, LINE_WIDTH)
                
                # Returns Player Number
                return self.squares[0][col]
        
        # Horizontal Wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else X_COLOR
                    Initial_Pos = (20, row * SQSIZE + SQSIZE // 2)
                    Final_Pos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(Screen, color, Initial_Pos, Final_Pos, LINE_WIDTH)
                
                # Returns Player Number
                return self.squares[row][0]

        # Descending Diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else X_COLOR
                Initial_Pos = (20, 20)
                Final_Pos = (WIDTH- 20, HEIGHT - 20)
                pygame.draw.line(Screen, color, Initial_Pos, Final_Pos, X_WIDTH)
            
            return self.squares[1][1]

        # Ascending Diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else X_COLOR
                Initial_Pos = (20, HEIGHT - 20)
                Final_Pos = (WIDTH - 20, 20)
                pygame.draw.line(Screen, color, Initial_Pos, Final_Pos, X_WIDTH)
            
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
                Temp_Board = copy.deepcopy(board)
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
                Temp_Board = copy.deepcopy(board)
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

class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1 # PLayer 1 -> 'X' || Player 2 -> 'O'
        self.Game_Mode = 'AI' # PVP or AI
        self.running = True 
        self.Show_Lines()
    
    def Make_Move(self, row, col):
        self.board.Mark_Square(row, col, self.player)
        self.Draw_Fig(row, col)
        self.Next_Turn()

    def Show_Lines(self):
        # Paint Screen
        Screen.fill(BG_COLOR)
        
        # Vertical Lines
        pygame.draw.line(Screen, LINES_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(Screen, LINES_COLOR, (WIDTH-SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        # Horizontal Lines
        pygame.draw.line(Screen, LINES_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(Screen, LINES_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def Draw_Fig(self, row, col):
        if self.player == 1:
            # Draw 'X (Composed by Ascending and Decending Line)
            # Descending line
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(Screen, X_COLOR, start_desc, end_desc, X_WIDTH)

            # Ascending line
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(Screen, X_COLOR, start_asc, end_asc, X_WIDTH)

        elif(self.player == 2):
            # Draw 'O'
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(Screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

    def Next_Turn(self):
        self.player = 1 if self.player == 2 else 2
        # self.player = self.player % 2 + 1

    def Change_Game_Mode(self):
        self.Game_Mode = 'AI' if self.Game_Mode == 'PVP' else 'PVP'
        # if self.Game_Mode == 'PVP':
        #     self.Game_Mode = 'AI'
        # else:
        #     self.Game_Mode = 'PVP'

    def IsOver(self):
        return self.board.Final_State(show=True) != 0 or self.board.Is_Full()

    def Reset(self):
        self.__init__()

def Main():
    
    game = Game()
    board = game.board
    ai = game.ai
    
    # MAIN LOOP
    while True:

        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                # Press g -> Change Game Mode
                if event.key == pygame.K_g:
                    game.Change_Game_Mode()

                if event.key == pygame.K_r:
                    game.Reset()
                    board = game.board
                    ai = game.ai

                # 0 -> Random AI
                if event.key == pygame.K_0:
                    ai.level = 0

                # 1 -> Expert AI
                if event.key == pygame.K_1:
                    ai.level = 1
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE
                
                if board.Empty_Square(row, col) and game.running:
                    game.Make_Move(row, col)
                    if game.IsOver():
                        game.running = False
        
        if game.Game_Mode == "AI" and game.player == ai.player and game.running:
            # Update the Screen
            pygame.display.update()
            
            # AI Methods
            row, col = ai.Evaluate(board)
            game.Make_Move(row, col)

            if game.IsOver():
                        game.running = False

        pygame.display.update()

def Main_V2(AI_Level, Mode):
    
    game = Game()
    board = game.board
    game.Game_Mode = Mode
    game.ai.level = AI_Level 
    ai = game.ai
    
    # MAIN LOOP
    while True:

        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                # Press g -> Change Game Mode
                if event.key == pygame.K_g:
                    game.Change_Game_Mode()

                if event.key == pygame.K_r:
                    game.Reset()
                    board = game.board
                    game.Game_Mode = Mode
                    game.ai.level = AI_Level 
                    ai = game.ai

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE
                
                if board.Empty_Square(row, col) and game.running:
                    game.Make_Move(row, col)
                    if game.IsOver():
                        game.running = False
        
        if game.Game_Mode == "AI" and game.player == ai.player and game.running:
            # Update the Screen
            pygame.display.update()
            
            # AI Methods
            row, col = ai.Evaluate(board)
            game.Make_Move(row, col)

            if game.IsOver():
                game.running = False

        pygame.display.update()

# Colors
Black = (0,0,0)
White = (255,255,255)

# Letras
Tipo_Letra = pygame.font.SysFont("arialblack", 22)
Tipo_Letra_Grande = pygame.font.SysFont("arialblack", 30)

def Escrever(texto, tipo_letra, cor, x, y, tela):
    img = tipo_letra.render(texto, True, cor)
    tela.blit(img, (x,y))

def Start_Game():
    Run = True
    Menu = "Main"
    
    # Variables
    Main_Menu_BG_IMG = pygame.image.load('Extras/BG_IMG.jpg').convert_alpha()
    Main_Menu_BG = Button(650, -30, Main_Menu_BG_IMG, .6)

    Game_Mode_BG_IMG = pygame.image.load('Extras/BG_IMG_2.jpg').convert_alpha()
    Game_Mode_BG = Button(700, 0, Game_Mode_BG_IMG, .7)

    Play_IMG = pygame.image.load('Extras/Start_3.png').convert_alpha()
    Play_Button = Button(220,200,Play_IMG, .3)

    Back_IMG = pygame.image.load('Extras/Back.png').convert_alpha()
    Back_Button = Button(580,20,Back_IMG, .15)

    PVP_IMG = pygame.image.load('Extras/PVP.png').convert_alpha()
    PVP_Button = Button(250, 130, PVP_IMG, .2)

    AI_IMG = pygame.image.load('Extras/AI.png').convert_alpha()
    AI_Button = Button(450, 130, AI_IMG, .2)

    AI_BG_IMG = pygame.image.load('Extras/BG_IMG_3.jpg').convert_alpha()
    AI_BG = Button(920,0,AI_BG_IMG, .6)

    AI_RANDOM_IMG = pygame.image.load('Extras/Random.png').convert_alpha()
    AI_RANDOM = Button(150, 180, AI_RANDOM_IMG, .2)

    AI_MINIMAX_IMG = pygame.image.load('Extras/MiniMax.png').convert_alpha()
    AI_MINIMAX = Button(575, 180, AI_MINIMAX_IMG, .2)

    EXIT_IMG = pygame.image.load('Extras/Exit.png').convert_alpha()
    EXIT_Button = Button(575, 500, EXIT_IMG, .2)
    
    while Run:

        if Menu == "Main":
            Main_Menu_BG.Show(Screen)
            if Play_Button.Action(Screen):
                Menu = "Game_Mode"

        elif Menu == "Game_Mode":
            Game_Mode_BG.Show(Screen)
            Escrever("GAME MODE", Tipo_Letra_Grande, Black, 200, 50, Screen)
            Escrever("PVP Mode", Tipo_Letra, Black, 140, 250, Screen)
            Escrever("AI Mode", Tipo_Letra, Black, 350, 250, Screen)
            
            if AI_Button.Action(Screen):
                # Activate AI Mode
                Menu = "AI"
                
            if PVP_Button.Action(Screen):
                # Activate PVP Mode
                print("PVP MODE")
                Main_V2(1, "PVP")

            if Back_Button.Action(Screen):
                Menu = "Main"
            
            if EXIT_Button.Action(Screen):
                Run = False

        elif Menu == "AI":
            AI_BG.Show(Screen)
            Escrever("AI MODE", Tipo_Letra_Grande, White, 230, 50, Screen)
            Escrever("Random", Tipo_Letra, White, 48, 300, Screen)
            Escrever("Choice", Tipo_Letra, White, 56, 330, Screen)
            Escrever("MiniMax", Tipo_Letra, White, 475, 300, Screen)

            if AI_RANDOM.Action(Screen):
                print("AI RANDOM")
                Main_V2(0, "AI")

            if AI_MINIMAX.Action(Screen):
                print("AI MINIMAX")
                Main_V2(1, "AI")

            if Back_Button.Action(Screen):
                Menu = "Game_Mode"
            
            if EXIT_Button.Action(Screen):
                Run = False

        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                pass

            if event.type == pygame.QUIT:
                Run = False
        
        pygame.display.update()
    pygame.quit()

# Main()
Start_Game()