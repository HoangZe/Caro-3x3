import sys
import pygame
import numpy as np

# initialize pygame: pretty much initializing/ start the game
pygame.init()

# defining colors down here:
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# sizing for the game interface AND its components
WIDTH = 300
HEIGHT = 300
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLUMNS = 3
SQUARE_SIZE = WIDTH // BOARD_COLUMNS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

# create a screen object with pygame, WITH THE WIDTH AND HEIGHT DEFINED
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # a 300x300px screen
pygame.display.set_caption('Tic Tac Toe - Cờ Caro')
screen.fill(BLACK)

board = np.zeros((BOARD_ROWS, BOARD_COLUMNS))  # define a board structure in the size 3x3 with all 0s


# define a function that draws the lines for the game board in the default color of white
def draw_lines(color=WHITE):
    # tu 1 den 3
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, color, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)


def draw_figures(color=WHITE):
    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLUMNS):
            # neu tai vi tri row va column nay co id = 1 thi draw O (player)
            if board[row][column] == 1:
                pygame.draw.circle(screen, color, (
                    int(column * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            # neu tai vi tri nay ma co id = 2 thi draw X (machine)
            elif board[row][column] == 2:
                pygame.draw.line(screen, color,
                                 (column * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), (
                                     column * SQUARE_SIZE + 3 * SQUARE_SIZE // 4,
                                     row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), CROSS_WIDTH)
                pygame.draw.line(screen, color,
                                 (column * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), (
                                     column * SQUARE_SIZE + 3 * SQUARE_SIZE // 4,
                                     row * SQUARE_SIZE + SQUARE_SIZE // 4), CROSS_WIDTH)


# define a function that marks the square at that column and row position as player (1)
def mark_square(row, column, player):
    board[row][column] = player


# this function checks if the square is empty
def available_square(row, column):
    return board[row][column] == 0


# this function checks if the board is full or not
def is_board_full(check_board=board):
    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLUMNS):
            # check if there's any square on the board is 0 (available)
            if check_board[row][column] == 0:
                return False
    return True


# check if someone has won
def check_win(player, check_board=board):
    for column in range(BOARD_COLUMNS):
        # check if 3 squares on a row = player
        if check_board[0][column] == player and check_board[1][column] == player and check_board[2][column] == player:
            return True
    for row in range(BOARD_ROWS):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True
    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True
    if check_board[0][2] == player and check_board[1][1] == player and check_board[2][0] == player:
        return True
    return False


# the minimax function
def minimax (minimax_board, depth, isMaximizing):
    # check if the machine wins (number 2)
    if check_win(2, minimax_board):
        return float('inf') # return the score of infinite: best scenario
    elif check_win(1, minimax_board):
        return float('-inf') # return minus infinite score: worst scenario cuz the machine lost
    elif is_board_full(minimax_board):
        return 0 # if the board is already full but no one wins, return 0 score (a neutral score)

    if isMaximizing:
        best_score = -1000
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                if minimax_board[row][column] == 0:
                    minimax_board[row][column] = 2
                    score = minimax(minimax_board, depth +1, False)
                    minimax_board[row][column] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = 1000
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                if minimax_board[row][column] == 0:
                    minimax_board[row][column] = 1
                    score = minimax(minimax_board, depth + 1, True)
                    minimax_board[row][column] = 0
                    best_score = min(score, best_score)
        return best_score

def best_move():
    best_score = -1000
    move = (-1, 1) # define the default move
    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLUMNS):
            if board[row][column] == 0:
                board[row][column] = 2
                score = minimax(board, 0, False)
                board[row][column] = 0
                if score > best_score:
                    best_score = score
                    move = (row, column)

    if move != (-1, 1):
        mark_square(move[0], move[1], 2)
        return True
    return False


# to restart the game after it ends, refill the screen and redraw the lines
def restart_game():
    screen.fill(BLACK)
    draw_lines(WHITE)
    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLUMNS):
            board[row][column] = 0 # reset moi square tren board ve value 0


draw_lines()
player = 1 # cho player di truoc
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # if we do a click
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] // SQUARE_SIZE
            mouseY = event.pos[1] // SQUARE_SIZE

            # neu square ma ta click vao la o trong thi mark square = 1 (move cua player)
            if available_square(mouseY, mouseX):
                mark_square(mouseY, mouseX, 1)
                # neu move cua player win thi end, con khong thi switch player tu 1 thanh 2 va 2 thanh 1
                if check_win(player):
                    game_over = True
                player = player % 2 + 1 # switch player tu player sang machine

                if not game_over:
                    if best_move():
                       if check_win(2):
                           game_over = True
                       player = player % 2 + 1 # switch player tu machine sang player

                if not game_over:
                    if is_board_full():
                        game_over = True

        # neu event la press R thi restart
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                player = 1

    if not game_over:
        draw_figures()
    else:
        if check_win(1):
            draw_figures(GREEN)
            draw_lines(GREEN)
        elif check_win(2):
            draw_figures(RED)
            draw_lines(RED)
        else:
            draw_figures(YELLOW)
            draw_lines(YELLOW)

    pygame.display.update()