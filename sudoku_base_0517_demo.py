import pygame
from copy import deepcopy
from sudoku_generator_0529 import generating_sudoku_grid

'''
collecting "constant" variables used through this program
'''

BLACK = (0,   0,   0)
WHITE = (255, 255, 255, 255)
GREEN = (0, 255, 0, 100)
BLUE = (0, 0, 0, 50)

BOARD_ROWS = 9
BOARD_COLUMNS = 9
BOARD_WIDTH = 37
SQUARES_IN_A_ROW = 3
SQUARES_IN_A_COLUMN = 3

ONE_RECT_SIDE = 30
SIZE = [290, 290]
SIZE_OF_ONE_RECT = (ONE_RECT_SIDE, ONE_RECT_SIDE)

TABLE_LEFT_UPPER_CORNER = [10, 10]
TABLE_LEFT_UNDER_CORNER = [10, 280]
TABLE_RIGHT_UPPER_CORNER = [280, 10]
LINE_NUMBER = 10

matrix_basic = [[0 for x in range(BOARD_COLUMNS)] for y in range(BOARD_ROWS)]
basic_indices = []
etalon_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

number_coordinates = [[0 for x in range(BOARD_COLUMNS)] for y in range(BOARD_ROWS)]


def choose_difficulty():
    while True:
        choose_level = input(
            "Please choose difficulty: (e: easy, m: medium, h: hard, d: demo) ")
        if choose_level == "e":
            generating_sudoku_grid(matrix_basic, 2, checking_is_board_full, etalon_list)
            break
        elif choose_level == "m":
            generating_sudoku_grid(matrix_basic, 5, checking_is_board_full, etalon_list)
            break
        elif choose_level == "h":
            generating_sudoku_grid(matrix_basic, 10, checking_is_board_full, etalon_list)
            break
        elif choose_level == "d":
            read_table_from_file(matrix_basic, "sudoku_demo.txt")
            break
        else:
            print("Please choose from the given levels!")
            continue


def read_table_from_file(board_basic, file_name):
    with open(file_name, "r") as F:
        for i in range(len(board_basic)):
            for j in range(len(board_basic[i])):
                board_basic[i][j] = int(F.readline())


def click(board, pos):
    width = 270
    height = 270
    if pos[0] < width and pos[1] < height:
        gap = width / 9
        x = (pos[0] - 10) // gap
        y = (pos[1] - 10) // gap
        return (int(y), int(x))
    else:
        return None


def print_table(line_number, game_surface):
    x = TABLE_LEFT_UPPER_CORNER.copy()
    y = TABLE_LEFT_UNDER_CORNER.copy()
    for i in range(line_number):
        if i % 3 == 0:
            depth = 3
        else:
            depth = 1
        pygame.draw.line(game_surface, BLACK, x, y, depth)
        x[0] = x[0] + ONE_RECT_SIDE
        y[0] = y[0] + ONE_RECT_SIDE
    m = TABLE_LEFT_UPPER_CORNER.copy()
    n = TABLE_RIGHT_UPPER_CORNER.copy()
    for i in range(line_number):
        if i % 3 == 0:
            depth = 3
        else:
            depth = 1
        pygame.draw.line(game_surface, BLACK, m, n, depth)
        m[1] = m[1] + ONE_RECT_SIDE
        n[1] = n[1] + ONE_RECT_SIDE


def calculate_number_coordinates(cols, rows):
    starting_pos_X = -5

    for j in range(cols):
        starting_pos_X += ONE_RECT_SIDE
        starting_pos_Y = 25
        for i in range(rows):
            number_coordinates[i][j] = (starting_pos_X, starting_pos_Y)
            starting_pos_Y += ONE_RECT_SIDE


def playing_game(basic_grid, grid, board_full_check_func):
    selected = False
    done = False
    indices = None
    key = 0
    pos = (0, 0)

    pygame.init()

    selected_rect = pygame.Surface(SIZE_OF_ONE_RECT, pygame.SRCALPHA)
    pygame.draw.rect(selected_rect, GREEN, selected_rect.get_rect())

    basic_rect = pygame.Surface(SIZE_OF_ONE_RECT, pygame.SRCALPHA)
    pygame.draw.rect(basic_rect, BLUE, basic_rect.get_rect())

    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('$ sudo ku.py')

    clock = pygame.time.Clock()
    screen.fill(WHITE)
    font = pygame.font.SysFont("Arial", 20)

    calculate_number_coordinates(BOARD_COLUMNS, BOARD_ROWS)

    while not done:

        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(10)
        screen.fill(WHITE)
        if board_full_check_func(grid):
            return pygame.display.quit()
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                # done = True  # Flag that we are done so we exit this loop
                return pygame.display.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    key = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                indices = click(grid, pos)

                if event.button == 1 and basic_grid[indices[0]][indices[1]] == 0:
                    selected = True
                    key = None

            if event.type == pygame.MOUSEBUTTONDOWN and basic_grid[indices[0]][indices[1]] != 0:
                selected = False

        if indices and key is not None:
            if basic_grid[indices[0]][indices[1]] == 0:
                grid[indices[0]][indices[1]] = key
                selected = False

            if grid[indices[0]][indices[1]] != 0:
                text = font.render(str(grid[indices[0]][indices[1]]), True, BLACK)
                textRect = text.get_rect()
                textRect.center = number_coordinates[indices[0]][indices[1]]
                screen.blit(text, textRect)
                selected = False

        print_table(LINE_NUMBER, screen)

        for i in range(BOARD_COLUMNS):
            for j in range(BOARD_ROWS):
                if grid[i][j] != 0:
                    text = font.render(str(grid[i][j]), True, BLACK)
                    textRect = text.get_rect()
                    textRect.center = number_coordinates[i][j]
                    screen.blit(text, textRect)
                if basic_grid[i][j] != 0:
                    screen.blit(
                                basic_rect,
                                (
                                    (number_coordinates[i][j][0] - (ONE_RECT_SIDE / 2)),
                                    (number_coordinates[i][j][1] - (ONE_RECT_SIDE / 2)),
                                    ONE_RECT_SIDE,
                                    ONE_RECT_SIDE
                                )
                                )

        if selected:
            screen.blit(
                        selected_rect,
                        (
                            (number_coordinates[indices[0]][indices[1]][0] - (ONE_RECT_SIDE / 2)),
                            (number_coordinates[indices[0]][indices[1]][1] - (ONE_RECT_SIDE / 2)),
                            ONE_RECT_SIDE,
                            ONE_RECT_SIDE
                        )
                        )

        pygame.display.flip()


def checking_is_board_full(board):
    for row in board:
        if 0 in row:
            return False
    return True


def checking_rows(board):
    for row in range(9):
        temp = board[row].copy()
        temp.sort()
        sorted_temp = temp
        if etalon_list != sorted_temp:
            return False
    return True


def checking_columns(board):
    for every_column in range(9):
        temp = []
        for column in range(9):
            temp.append(board[every_column][column])
        temp.sort()
        sorted_temp = temp
        if etalon_list != sorted_temp:
            return False
    return True


def checking_one_square(board, X_indices, Y_indices):
    temp = []
    for i in X_indices:
        for j in Y_indices:
            temp.append(board[i][j])
    temp.sort()
    sorted_temp = temp
    if sorted_temp == etalon_list:
        return True
    if sorted_temp != etalon_list:
        return False


def checking_squares(board):
    A_indices = [0, 1, 2]
    B_indices = [3, 4, 5]
    C_indices = [6, 7, 8]
    indices = [A_indices, B_indices, C_indices]
    for index_list_row in indices:
        for index_list_column in indices:
            if checking_one_square(board, index_list_row, index_list_column) is False:
                return False
    return True


def checking_solution(board):
    win = 0
    if not (checking_rows(board) and checking_columns(board) and checking_squares(board)):
        print("\nSorry, something went wrong here. Try again!")
        return win
    else:
        win = 1
        print('Yay! You won!')
        return win


def generating_basic_indicies(board, board_basic, index_list):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != board_basic[i][j]:
                index_list.append([i, j])
    return index_list


def main():
    choose_difficulty()
    matrix = [[0 for x in range(BOARD_COLUMNS)] for y in range(BOARD_ROWS)]
    generating_basic_indicies(matrix, matrix_basic, basic_indices)
    while True:
        matrix = deepcopy(matrix_basic)
        playing_game(matrix_basic, matrix, checking_is_board_full)
        while True:
            if checking_solution(matrix) == 1:
                new = input("Do you want to play again? y/n ")
                if new == 'y':
                    main()
                elif new == 'n':
                    break
                else:
                    print("Please choose from y and n!")
                    continue
            else:
                new = input("Do you want to try it again? y/n ")
                if new == 'y':
                    break
                elif new == 'n':
                    break
                else:
                    print("Please choose from y and n!")
                    continue
        if not new == 'y':
            break


main()
