# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

# Legend
# X for placing ship and hit battleship
# '  ' for available space
# ' - ' for missed shot


from random import randint 

HIDDEN_BOARD = [[' '] * 8 for x in range (8)]
GUESS_BOARD = [[' '] * 8 for x in range (8)]

letters_to_numbers = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7,  }

def print_board(board):
    print('     A B C D E F G H')
    print('     ---------------')
    row_number = 1
    for row in board:
        print("%d|%s|" % (row_number, "|".join(row)))
        row_number += 1


def create_ships(board):
    """
create 5 random ships on board
    """
    for ship in range(5):
        ship_row, ship_column = randint(0,7), randint(0,7)
        while board[ship_row][ship_column] == 'X':
            ship_row, ship_column = randint(0,7), randint(0,7)
        board[ship_row][ship_column] = 'X'

def get_ship_location():
    """
    choose ship location, row & column
    """
    row = input('Enter a ship row 1 - 8')
    while row not in '12345678':
        print('Please enter a valid row')
        row = input('Enter a ship row 1 - 8')
    column = input('Enter a ship column A - H').upper()
    while column not in 'ABCDEFGH':
        print('Please print a valid column')
        column = input('Enter a ship column A - H').upper()
    return int(row) - 1, letters_to_numbers[column]

def count_hit_ships(board):
    """
    count the ships hit in order to win/end the game
    to check if X exists
    """ 
    count = 0
    for row in board:
        for column in row:
            if column == 'X':
                count += 1
    return count


create_ships(HIDDEN_BOARD)
"""
create ships on hidden/opponent's board
"""
turns = 10
print_board(HIDDEN_BOARD)
print_board(GUESS_BOARD)
# while turns > 0:
