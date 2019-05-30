import pygame
from copy import deepcopy
from sudoku_generator_0529 import generating_sudoku_grid

'''
collecting "constant" variables used through this program
'''

BLACK = (0,   0,   0)
WHITE = (255, 255, 255, 255)
GREEN = (0, 255, 0, 200)
BLUE = (0, 0, 0, 50)
RED = (255, 0, 0, 200)
YELLOW = (255, 255, 0, 200)
BROWN = (139, 69, 19, 200)

BOARD_ROWS = 9
BOARD_COLUMNS = 9
BOARD_WIDTH = 37
SQUARES_IN_A_ROW = 3
SQUARES_IN_A_COLUMN = 3

ONE_RECT_SIDE = 30
SIZE = [274, 274]
SIZE_OF_ONE_RECT = (ONE_RECT_SIDE, ONE_RECT_SIDE)

TABLE_LEFT_UPPER_CORNER = [2, 2]
TABLE_LEFT_UNDER_CORNER = [2, 272]
TABLE_RIGHT_UPPER_CORNER = [272, 2]
LINE_NUMBER = 10

matrix_basic = [[0 for x in range(BOARD_COLUMNS)] for y in range(BOARD_ROWS)]
etalon_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

number_coordinates = [[0 for x in range(BOARD_COLUMNS)] for y in range(BOARD_ROWS)]


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
    starting_pos_X = -13

    for j in range(cols):
        starting_pos_X += ONE_RECT_SIDE
        starting_pos_Y = 17
        for i in range(rows):
            number_coordinates[i][j] = (starting_pos_X, starting_pos_Y)
            starting_pos_Y += ONE_RECT_SIDE


def choose_difficulty():
    pygame.init()

    easy_rect = pygame.Surface((270, 67.5), pygame.SRCALPHA)
    pygame.draw.rect(easy_rect, GREEN, easy_rect.get_rect(), 10)
    easy_button_rect = easy_rect.get_rect()

    medium_rect = pygame.Surface((270, 67.5), pygame.SRCALPHA)
    pygame.draw.rect(medium_rect, YELLOW, medium_rect.get_rect(), 10)
    medium_button_rect = medium_rect.get_rect()

    hard_rect = pygame.Surface((270, 67.5), pygame.SRCALPHA)
    pygame.draw.rect(hard_rect, RED, hard_rect.get_rect(), 10)
    hard_button_rect = hard_rect.get_rect()

    demo_rect = pygame.Surface((270, 67.5), pygame.SRCALPHA)
    pygame.draw.rect(demo_rect, BROWN, demo_rect.get_rect(), 10)
    demo_button_rect = demo_rect.get_rect()

    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('$ sudo ku.py')

    clock = pygame.time.Clock()
    screen.fill(WHITE)
    screen.blit(easy_rect, (0, 0, 67.5, 270))
    screen.blit(medium_rect, (0, 67.5, 67.5, 270))
    screen.blit(hard_rect, (0, 135, 67.5, 270))
    screen.blit(demo_rect, (0, 202.5, 67.5, 270))

    font = pygame.font.SysFont("Arial", 40)

    easy_text = font.render("EASY", True, BLACK)
    easy_textRect = easy_text.get_rect()
    easy_textRect.center = (easy_button_rect.center[0], easy_button_rect.center[1])
    screen.blit(easy_text, easy_textRect)

    medium_text = font.render("MEDIUM", True, BLACK)
    medium_textRect = medium_text.get_rect()
    medium_textRect.center = (medium_button_rect.center[0], medium_button_rect.center[1] + 67.5)
    screen.blit(medium_text, medium_textRect)

    hard_text = font.render("HARD", True, BLACK)
    hard_textRect = hard_text.get_rect()
    hard_textRect.center = (hard_button_rect.center[0], hard_button_rect.center[1] + 135)
    screen.blit(hard_text, hard_textRect)

    demo_text = font.render("DEMO", True, BLACK)
    demo_textRect = demo_text.get_rect()
    demo_textRect.center = (demo_button_rect.center[0], demo_button_rect.center[1] + 202.5)
    screen.blit(demo_text, demo_textRect)
    while True:

        clock.tick(10)
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                return pygame.display.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if event.button == 1:
                    if pos[0] >= 0 and pos[0] <= 270 and pos[1] >= 0 and pos[1] <= 67.5:
                        generating_sudoku_grid(matrix_basic, 2, checking_is_board_full, etalon_list)
                        return False
                    elif pos[0] >= 0 and pos[0] <= 270 and pos[1] >= 67.5 and pos[1] <= 135:
                        generating_sudoku_grid(matrix_basic, 5, checking_is_board_full, etalon_list)
                        return False
                    elif pos[0] >= 0 and pos[0] <= 270 and pos[1] >= 135 and pos[1] <= 202.5:
                        generating_sudoku_grid(matrix_basic, 10, checking_is_board_full, etalon_list)
                        return False
                    elif pos[0] >= 0 and pos[0] <= 270 and pos[1] >= 202.5 and pos[1] <= 270:
                        read_table_from_file(matrix_basic, "sudoku_demo.txt")
                        return False

        pygame.display.flip()


def playing_game(basic_grid, grid, board_full_check_func):
    selected = False
    indices = []
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

    while True:

        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(10)
        screen.fill(WHITE)
        if board_full_check_func(grid):
            return pygame.display.quit()
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
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


def choosing_continuation(win_condition, restart):
    pygame.init()

    choosen = False

    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('$ sudo ku.py')

    clock = pygame.time.Clock()
    screen.fill(WHITE)
    font = pygame.font.SysFont("Arial", 20)

    message_rect = pygame.Surface((270, 135), pygame.SRCALPHA)
    pygame.draw.rect(message_rect, WHITE, message_rect.get_rect())

    replay_button = pygame.Surface((90, 135), pygame.SRCALPHA)
    pygame.draw.rect(replay_button, YELLOW, replay_button.get_rect())

    new_game_button = pygame.Surface((90, 135), pygame.SRCALPHA)
    pygame.draw.rect(new_game_button, GREEN, new_game_button.get_rect())

    quit_button = pygame.Surface((90, 135), pygame.SRCALPHA)
    pygame.draw.rect(quit_button, RED, quit_button.get_rect())

    win_message = 'You won!'
    lost_message = 'You lost!'
    question = 'Do you want to play again?'

    screen.fill(WHITE)
    screen.blit(message_rect, (0, 0, 135, 270))
    screen.blit(replay_button, (0, 135, 90, 270))
    screen.blit(new_game_button, (90, 135, 180, 270))
    screen.blit(quit_button, (180, 135, 270, 270))

    message_text = (font.render(win_message, True, BLACK) if win_condition == 1 else font.render(lost_message, True, BLACK))
    message_text_rect = message_text.get_rect()
    message_text_rect.center = (135, 45)
    screen.blit(message_text, message_text_rect)

    question_text = (font.render(question, True, BLACK))
    question_text_rect = question_text.get_rect()
    question_text_rect.center = (135, 90)
    screen.blit(question_text, question_text_rect)

    replay_text = font.render('REPLAY', True, BLACK)
    replay_text_rect = replay_text.get_rect()
    replay_text_rect.center = (45, 202.5)
    screen.blit(replay_text, replay_text_rect)

    new_game_text = font.render('NEW', True, BLACK)
    new_game_text_rect = new_game_text.get_rect()
    new_game_text_rect.center = (135, 202.5)
    screen.blit(new_game_text, new_game_text_rect)

    quit_text = font.render('QUIT', True, BLACK)
    quit_text_rect = quit_text.get_rect()
    quit_text_rect.center = (225, 202.5)
    screen.blit(quit_text, quit_text_rect)

    while not choosen:

        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if event.button == 1:
                    if pos[1] > 135 and pos[0] < 90:
                        choosen is True
                        restart[0] = 0
                        return restart[0]
                    elif pos[1] > 135 and pos[0] > 90 and pos[0] < 180:
                        choosen is True
                        restart[0] = 1
                        return restart[0]
                    elif pos[1] > 135 and pos[0] > 180:
                        choosen is True
                        restart[0] = 2
                        return restart[0]

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
        return win
    else:
        win = 1
        return win


def main():
    while True:
        choose_difficulty()
        matrix = [[0 for x in range(BOARD_COLUMNS)] for y in range(BOARD_ROWS)]
        matrix = deepcopy(matrix_basic)
        again = [0]
        while again:
            playing_game(matrix_basic, matrix, checking_is_board_full)
            outcome = checking_solution(matrix)
            again[0] = 1
            again[0] = choosing_continuation(outcome, again)
            if again[0] == 0:
                matrix = deepcopy(matrix_basic)
                continue
            elif again[0] == 1:
                break
            else:
                return


main()
