from termcolor import colored
from copy import deepcopy
from sudoku_generator_0529 import generating_sudoku_grid

'''
collecting "constant" variables used through this program
'''
BOARD_ROWS = 9
BOARD_COLUMNS = 9
BOARD_WIDTH = 37
SQUARES_IN_A_ROW = 3
SQUARES_IN_A_COLUMN = 3

matrix_basic = [[0 for x in range(BOARD_COLUMNS)] for y in range(BOARD_ROWS)]
basic_indices = []
etalon_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]


def choose_difficulty():  # gets random generated sudoku table
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


def print_sudoku(board):
    print("-"*BOARD_WIDTH)
    for row, rows in enumerate(board):
        coloring_numbers = []
        for index, numbers in enumerate(rows):
            if numbers == 0:
                coloring_numbers.append(" ")
            elif [row, index] in basic_indices:
                coloring_numbers.append(colored(numbers, "red"))
            else:
                coloring_numbers.append(numbers)
        print(("|" + " {}   {}   {} |"*SQUARES_IN_A_ROW).format(*coloring_numbers))
        if row == (BOARD_ROWS - 1):
            print("-"*BOARD_WIDTH)
        elif row % SQUARES_IN_A_ROW == 2:
            print("|" + "---+"*(BOARD_COLUMNS - 1) + "---|")
        else:
            print("|" + "   +"*(BOARD_COLUMNS - 1) + "   |")


def user_input(board):
    while True:
        row_number = input("\nPlease give me the number of the row: ")
        if row_number.isnumeric():
            row_number = int(row_number)
        else:
            print("Sorry, you must write numbers!")
            continue
        if row_number not in etalon_list:
            print("Sorry, you must use digits 1 to 9!")
            continue
        else:
            break
    while True:
        column_number = input("Please give me the number of the column: ")
        if column_number.isnumeric():
            column_number = int(column_number)
        else:
            print("Sorry, you must write numbers!")
            continue
        if column_number not in etalon_list:
            print("Sorry, you must use digits 1 to 9!")
            continue
        else:
            break
    while True:
        new_number = input(
            "Please give me the number you want to add (or any letter for deleting): ")
        if new_number.isnumeric():
            new_number = int(new_number)
            if new_number not in etalon_list:
                print("Sorry, you must use digits 1 to 9!")
            elif [(row_number - 1), (column_number - 1)] in basic_indices:
                print("Sorry, this is a basic number that you can't modify!")
                new_number = board[row_number - 1][column_number - 1]
                break
            else:
                break
        elif new_number.isalpha():
            if [(row_number - 1), (column_number - 1)] in basic_indices:
                print("Sorry, this is a basic number that you can't delete!")
                new_number = board[row_number - 1][column_number - 1]
                break
            else:
                new_number = 0
                break
        else:
            print("Sorry, you must write numbers!")
            continue
    board[row_number - 1][column_number - 1] = new_number
    print_sudoku(board)


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
        print_sudoku(matrix_basic)
        matrix = deepcopy(matrix_basic)
        while checking_is_board_full(matrix) is False:
            user_input(matrix)
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
