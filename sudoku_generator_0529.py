# based on: Sudoku Generator Algorithm - www.101computing.net/sudoku-generator-algorithm/
from random import randint, shuffle


def sudoku_solver(grid, board_full_check_func, solution_number):
    '''
    A backtracking/recursive function to check all possible combinations
    of numbers until a solution is found
    '''
    for i in range(0, 81):  # Find next empty cell
        row = i // 9
        col = i % 9
        if grid[row][col] == 0:
            for value in range(1, 10):  # Check that this value has not already be used on this row
                if value not in grid[row]:  # Check that this value has not already be used on this column
                    if value not in (grid[0][col], grid[1][col], grid[2][col],
                                     grid[3][col], grid[4][col], grid[5][col],
                                     grid[6][col], grid[7][col], grid[8][col]):
                        square = []  # Identify which of the 9 squares we are working on
                        if row < 3:
                            if col < 3:
                                square = [grid[i][0:3] for i in range(0, 3)]
                            elif col < 6:
                                square = [grid[i][3:6] for i in range(0, 3)]
                            else:
                                square = [grid[i][6:9] for i in range(0, 3)]
                        elif row < 6:
                            if col < 3:
                                square = [grid[i][0:3] for i in range(3, 6)]
                            elif col < 6:
                                square = [grid[i][3:6] for i in range(3, 6)]
                            else:
                                square = [grid[i][6:9] for i in range(3, 6)]
                        else:
                            if col < 3:
                                square = [grid[i][0:3] for i in range(6, 9)]
                            elif col < 6:
                                square = [grid[i][3:6] for i in range(6, 9)]
                            else:
                                square = [grid[i][6:9] for i in range(6, 9)]
                        if value not in (square[0] + square[1] + square[2]):  # Check that this value has not already be used on this 3x3 square
                            grid[row][col] = value
                            if board_full_check_func(grid):
                                solution_number[0] += 1
                                break
                            else:
                                if sudoku_solver(grid, board_full_check_func, solution_number):
                                    return True
            break
    grid[row][col] = 0


def generating_filled_sudoku_grid(grid, etalon, board_full_check_func):
    '''
    A backtracking/recursive function to check all possible combinations
    of numbers until a solution is found
    '''
    basic_numbers = etalon.copy()
    for i in range(0, 81):  # Find next empty cell
        row = i // 9
        col = i % 9
        if grid[row][col] == 0:
            shuffle(basic_numbers)
            for value in basic_numbers:
                if value not in grid[row]:  # Check that this value has not already be used on this row
                    if value not in (grid[0][col], grid[1][col], grid[2][col],
                                     grid[3][col], grid[4][col], grid[5][col],
                                     grid[6][col], grid[7][col], grid[8][col]):  # Check that this value has not already be used on this column
                        square = []  # Identify which of the 9 squares we are working on
                        if row < 3:
                            if col < 3:
                                square = [grid[i][0:3] for i in range(0, 3)]
                            elif col < 6:
                                square = [grid[i][3:6] for i in range(0, 3)]
                            else:
                                square = [grid[i][6:9] for i in range(0, 3)]
                        elif row < 6:
                            if col < 3:
                                square = [grid[i][0:3] for i in range(3, 6)]
                            elif col < 6:
                                square = [grid[i][3:6] for i in range(3, 6)]
                            else:
                                square = [grid[i][6:9] for i in range(3, 6)]
                        else:
                            if col < 3:
                                square = [grid[i][0:3] for i in range(6, 9)]
                            elif col < 6:
                                square = [grid[i][3:6] for i in range(6, 9)]
                            else:
                                square = [grid[i][6:9] for i in range(6, 9)]
                        if value not in (square[0] + square[1] + square[2]):  # Check that this value has not already be used on this 3x3 square
                            grid[row][col] = value
                            if board_full_check_func(grid):
                                return True
                            else:
                                if generating_filled_sudoku_grid(grid, basic_numbers, board_full_check_func):
                                    return True
            break
    grid[row][col] = 0


def generating_sudoku_grid(grid, level, board_full_check_func, etalon):
    generating_filled_sudoku_grid(grid, etalon, board_full_check_func)
    while level > 0:  # Select a random cell that is not already empty
        row = randint(0, 8)
        col = randint(0, 8)
        while grid[row][col] == 0:
            row = randint(0, 8)
            col = randint(0, 8)

        backup = grid[row][col]  # Remember it's cell value in case we need to put it back
        grid[row][col] = 0

        copy_grid = []  # Take a full copy of the grid
        for r in range(0, 9):
            copy_grid.append([])
            for c in range(0, 9):
                copy_grid[r].append(grid[r][c])

        counter = [0]  # Count the number of solutions that this grid has
        sudoku_solver(copy_grid, board_full_check_func, counter)
        if counter[0] != 1:
            grid[row][col] = backup
            level -= 1
