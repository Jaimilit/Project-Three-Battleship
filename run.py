# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

# Legend
# X for placing ship and hit battleship
# '  ' for available space
# ' - ' for missed shot

#  "." = water or empty space
#  "O" = part of ship
#  "X" = part of ship that was hit with bullet
#  "#" = water that was shot with bullet, a miss because it hit no ship


from random import randint 
import random
import time

# Global variable for grid
grid = [[]]
# Global variable for grid size
grid_size = 10
# Global variable for number of ships to place
num_of_ships = 3
# Global variable for bullets left
bullets_left = 20
# Global variable for game over
game_over = False
# Global variable for number of ships sunk
num_of_ships_sunk = 0
# Global variable for ship positions
ship_positions = [[]]
# Global variable for alphabet
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

"""
HIDDEN_BOARD = [[' '] * 8 for x in range (8)]
GUESS_BOARD = [[' '] * 8 for x in range (8)]

letters_to_numbers = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7,  }
"""

def validate_grid_and_place_ship(start_row, end_row, start_col, end_col):
    """
    Checks row and column for shipment placement
    Is true or false
    """
    global grid
    global ship_positions

    all_valid = True
    for r in range(start_row, end_row):
        for c in range(start_col, end_col):
            if grid[r][c] !=".":
                all_valid = False
                break
    if all_valid:
        ship_positions.append([start_row, end_row, start_col, end_col])
        for r in range(start_row, end_row):
            for c in range(start_col, end_col):
                grid[r][c] = "O"
    return all_valid

def try_to_place_ship_on_grid(row, col, direction, length):
    """
    Based on direction will call helper method to try and place a ship on the grid.
       Returns validate_grid_and_place_ship which will be True or False.
    """
    global grid_size

    start_row, end_row, start_col, end_col = row, row + 1, col, col + 1
    if direction == "left":
        if col - length < 0:
            return False
        start_col = col - length + 1
    
    elif direction == "right":
        if col + length >= grid_size:
            return False
        end_col = col + length

    elif direction == "up":
        if row - length < 0:
            return False
        start_row = row - length + 1

    elif direction == "down":
        if row + length >= grid_size:
            return False
        end_row = row + length


    return validate_grid_and_place_ship(start_row, end_row, start_col, end_col)


def create_grid():
    """
    Will create a 10x10 grid and randomly place down ships
       of different sizes in different directions.
       Has no Return but will use try_to_place_ship_on_grid.
    """
    global grid
    global grid_size
    global num_of_ships
    global ship_positions

    random.seed(time.time())

    rows, cols = (grid_size, grid_size)

    grid = []
    for r in range(rows):
        row = []
        for c in range (cols):
            row.append(".")
        grod.append(row)

    
    num_of_ships_placed = 0

    ship_positions = []

    while num_of_ships_placed != num_of_ships:
        random_row = random.randint(0, rows - 1)
        random_col - random.randint(0, cols - 1)
        direction = random.choice(["left", "right", "up", "down"])
        ship_size = random.randint(3, 5)
        if try_to_place_ship_on_grid(random_row, random_col, direction, ship_size):
            num_of_ships_placed += 1


def print_grid():
    """
    Will print the grid with rows A-J and columns 0-9.
       Has no Return.
    """
    global grid
    global alphabet

    debug_mode = True

    alphabet = alphabet[0: len(grid) + 1]

    for row in range(len (grid)):
        print(alphabet[row], end=") ")
        for col in range(len (grid[row])):
            if grid [row][col] == "O":
                if debug_mode:
                    print("O", end=" ")
                else:
                    print(".", end=" ")
            else:
                print(grid[row][col], end=" ")
        print(" ")

    print("  ", end=" ")
    for i in range(len(grid[0])):
        print(str(i), end=" ")
    print("")


def accept_valid_bullet_placement():
    """
    Will get valid row and column to place bullet shot.
       Has Return row, col, both are integers.
    """
    global alphabet
    global grid

    is_valid_placement = False
    row = -1
    col = -1
    while is_valid_placement is False:
        placement = input("Enter row A-J and column 0-9  such as C6: ")
        placement = placement.upper()
        if len(placement) <= 0 or len(placement) > 2:
            print("Error: Please enter a valid row and column such as C6")
        continue
        row = placement[0]
        col = placement[1]
        if not row.isalpha() or not col.isnumeric():
            print("Error: Please enter letter A-J for row and 0-9 for column")
            continue
        row = alphabet.find(row)
        if not (-1 < row < grid_size):
            print("Error: Please enter letter A-J for row and 0-9 for column")
            continue
        col = int(col)
        if not (-1 < col < grid_size):
            print("Error: Please enter letter A-J for row and 0-9 for column")
            continue
        if grid[row][col] == "#" or grid[row][col] == "X":
            print("You have already shot a missle here, pick a new location")
            continue
        if grid[row][col] == "." or grid[row][col] =="O":
            is_valid_placement = True


    return row, col

    
def check_for_ship_sunk(row, col):
    """
    If all parts of a shit have been shot it is sunk and we later increment ships sunk.
       Has Return True or False.
    """
    global ship_positions
    global grid

    for position in ship_positions:
        start_row = position[0]
        end_row = position[1]
        start_col = position[2]
        end_col = position[3]
        if start_row <= row <= end_row and start_col <= col <= end_col:
            # ship found, see if sunk
            for r in range(start_row, end_row):
                for c in range(start_col, end_col):
                    if grid[r][c] != "X":
                        return False
    return True




def shoot_bullet():
    """
    Updates grid and ships based on where the bullet was shot.
       Has no Return but will use accept_valid_bullet_placement.
    """
    global grid
    global num_of_ships_sunk
    global bullets_left

    row, col = accept_valid_bullet_placement()
    print("")
    print("-----------------------------------")


    if grid[row][col] == ".":
        print("Missed. You missed a ship")
        grid[row][col] = "#"
    elif grid[row][col] == "O":
        print("Ship hit!", end= " ")
        grid[row][col] = "X"
        if check_for_ship_sunk(row,col):
            print("Congrats! A ship was completely sunk!")
            num_of_ships += 1
        else:
            print("Yay! You shot a ship!")

    bullets_left -= 1


def check_for_game_over():
    """
    If all ships have been sunk or we run out of bullets its game over.
       Has no Return.
    """
    global num_of_ships_sunk
    global num_of_ships
    global bullets_left
    global game_over

    if num_of_ships == num_of_ships_sunk:
        print("Congrats! You won the game!")
        game_over = True
    elif bullets_left <= 0:
        print("Sorry, you ran out of missles. Try again next time!")
        game_over - True


def main():
    """
    Action of all to play game
    """

    global game_over

    print("         Weclome to Battleships          ")
    print("You have 20 shots to take down 3 ships. May the battle begin!")

    create_grid

    while game_over is False:
        print_grid()
        print("Number of ships remaining: " + str(num_of_ships - num_of_ships_sunk))
        print("Number of shots left: " + str(bullets_left))
        shoot_bullet()
        print("-----------------------------------")
        print("")
        check_for_game_over()




"""
def print_board(board):
    print('  A B C D E F G H')
    print('  ---------------')
    row_number = 1
    for row in board:
        print("%d|%s|" % (row_number, "|".join(row)))
        row_number += 1


def create_ships(board):
    
    for ship in range(5):
        ship_row, ship_column = randint(0,7), randint(0,7)
        while board[ship_row][ship_column] == 'X':
            ship_row, ship_column = randint(0,7), randint(0,7)
        board[ship_row][ship_column] = 'X'

def get_ship_location():
    
    # choose ship location, row & column
    
    column = input('Enter a ship column A - H: ').upper()
    while column not in 'ABCDEFGH':
        print('Please print a valid column')
        column = input('Enter a ship column A - H: ').upper()
    row = input('Enter a ship row 1 - 8: ')
    while row not in '12345678':
        print('Please enter a valid row')
        row = input('Enter a ship row 1 - 8: ')
    
    return int(row) - 1, letters_to_numbers[column]

def count_hit_ships(board):
    
   # count the ships hit in order to win/end the game
  #  to check if X exists
     
    count = 0
    for row in board:
        for column in row:
            if column == 'X':
                count += 1
    return count


create_ships(HIDDEN_BOARD)
print_board(HIDDEN_BOARD)
"""
#create ships on hidden/opponent's board
#asks user for row & column
"""
turns = 10
while turns > 0:
    print('Welcome to Battleship!')
    print_board(GUESS_BOARD)
    row, column = get_ship_location()
    if GUESS_BOARD[row][column] == '-':
        print('You already guessed that')
    elif HIDDEN_BOARD [row][column] == 'X':
        print("Congrats! You've hit a battleship!")
        GUESS_BOARD [row][column] = 'X'
        turns -= 1
    else:
        print("Sorry you've missed")
        GUESS_BOARD[row][column] = '-'
        turns -= 1
    if count_hit_ships(GUESS_BOARD) == 5:
        print('Congrats! You sunk all the battleships!')
        break
        print('You have ' + str(turns) + ' turns remaining')
    if turns == 0:
        print('Game Over')
        break
"""