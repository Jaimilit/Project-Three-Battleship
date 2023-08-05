
# Legend
#  "." = water or empty space
#  "O" = part of ship
#  "X" = part of ship that was hit by a shot
#  "M" = a shot that missed and lands in water

import random
import time

# Constant Variables

grid_size = 10
num_of_ships = 5
shots_left = 25
game_over = False
num_of_ships_sunk = 0
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Global Variables
ship_positions = [[]]
grid = [[]]


def create_grid_and_check_location(start_row, end_row, start_col, end_col):
    """
    Checks rows & columns for ship placement and updates the grid and ship positions
    Returns true if ship placement is valid
    """

    global grid
    global ship_positions

    for r in range(start_row, end_row):
        for c in range(start_col, end_col):
            if grid[r][c] != ".":
                return False

    ship_positions.append([start_row, end_row, start_col, end_col])

    for r in range(start_row, end_row):
        for c in range(start_col, end_col):
            grid[r][c] = "O"

    return True

"""
# OLD CODE
    global grid
    global ship_positions

    all_valid = True
    for r in range(start_row, end_row):
        for c in range(start_col, end_col):
            if grid[r][c] != ".":
                all_valid = False
                break
    if all_valid:
        ship_positions.append([start_row, end_row, start_col, end_col])
        for r in range(start_row, end_row):
            for c in range(start_col, end_col):
                grid[r][c] = "O"
    return all_valid

    
"""
def place_ships(row, col, direction, length):
    """
    Place ships on grid - random method
    Ensure there's no other ship there and/or not off the grid
    """
    
    global grid_size

    delta = 1 if direction in {"right", "down"} else -1
    
    if direction in {"left", "right"}:
        start_col, end_col = col - length + 1, col + delta
        start_row, end_row = row, row + 1

    elif direction in {"up", "down"}:
        start_row, end_row = row - length + 1, row + delta
        start_col, end_col = col, col + 1

    return (0 <= start_col < grid_size) and (0 <= start_row < grid_size) and create_grid_and_check_location(start_row, end_row, start_col, end_col)
    
    """
   # OLD CODE
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

    return create_grid_and_check_location(start_row, end_row, start_col, end_col)
    
    """
    
def create_grid():
    """ 
    creates a grid and randomly places ships
    of different sizes in different directions
    """
   
# OLD CODE COME BACK TO THIS ONE
    global grid
    global grid_size
    global num_of_ships
    global ship_positions

    random.seed(time.time())

    rows, cols = (grid_size, grid_size)
    grid = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(".")
        grid.append(row)

    num_of_ships_placed = 0

    ship_positions = []

    while num_of_ships_placed != num_of_ships:
        random_row = random.randint(0, rows - 1)
        random_col = random.randint(0, cols - 1)
        direction = random.choice(["left", "right", "up", "down"])
        ship_size = random.randint(3, 5)
        if place_ships(random_row, random_col, direction, ship_size):
            num_of_ships_placed += 1

    
def print_grid():
    """
    Will print the grid with rows A-J and columns 0-9
    COME BACK TO THIS ONE TOO
    """
    #OLD CODE
    global grid
    global alphabet

    debug_mode = True
    
    alphabet = alphabet[0: len(grid) + 1]

    print("  ", end=" ")
    for i in range(len(grid[0])):
        print(str(i), end=" ")
    print("")

    for row in range(len(grid)):
        print(alphabet[row], end=") ")
        for col in range(len(grid[row])):
            if grid[row][col] == "O":
                if debug_mode:
                    print("O", end=" ")
                else:
                    print(".", end=" ")
            else:
                print(grid[row][col], end=" ")
        print("")
   
    
def accept_valid_placement():
    """
    Will get data from user (row & column) to place shot
    Writes error to user if input is incorrect
    """
    global alphabet
    global grid
    global grid_size

    while True:
        placement = input("Please enter row A-J and column 0-9. Example C6: ").upper()

        if len(placement) != 2:
            print("Error: Please enter a valid input such as C6.")
            continue

        row, col = placement

        if not row.isalpha() or not col.isdigit():
            print("Error: Please enter letter A-J for row and 0-9 for column.")
            continue

        row = alphabet.find(row)
        col = int(col)

        if not (-1 < row < grid_size) or not (-1 < col < grid_size):
            print("Error: Please enter valid row A-J and column 0-9.")
            continue

        if grid[row][col] in {"M", "X"}:
            print("You have already made this shot. Try another location.")
            continue

        if grid[row][col] in {".", "O"}:
            return row, col
    """
   # OLD CODE

    global alphabet
    global grid
    global grid_size

    is_valid_placement = False
    row = -1
    col = -1
    while is_valid_placement is False:
        placement = input("Please enter row A-J and column 0-9. Example C6: ")
        placement = placement.upper()
        if len(placement) <= 0 or len(placement) > 2:
            print("Error: Please enter only one row and column such as C6:")
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
        if grid[row][col] == "M" or grid[row][col] == "X":
            print("You have already made this shot. Try another location")
            continue
        if grid[row][col] == "." or grid[row][col] == "O":
            is_valid_placement = True

    return row, col
    
"""
def check_for_ship_sunk(row, col):
    """
    If all parts of a ship have been shot it is sunk and we count how many ships are sunk
    
    global ship_positions
    global grid
    for start_row, end_row, start_col, end_col in ship_positions:
        if start_row <= row <= end_row and start_col <= col <= end_col:
            if not all(grid[r][c] == "X" for r in range(start_row, end_row + 1) for c in range(start_col, end_col + 1)):
                return False
    return True

"""    
  #  OLD CODE

    global ship_positions
    global grid

    for position in ship_positions:
        start_row = position[0]
        end_row = position[1]
        start_col = position[2]
        end_col = position[3]
        if start_row <= row <= end_row and start_col <= col <= end_col:
            for r in range(start_row, end_row):
                for c in range(start_col, end_col):
                    if grid[r][c] != "X":
                        return False
    return True
    

def attempt_shot():
    """
    Updates grid and ships based on where the shot was located
    Tells user if their shot missed, hit a ship, and if a ship was completely 
    sunk
    
    global grid
    global num_of_ships_sunk
    global shots_left
    
    row, col = accept_valid_placement()
    print("\n----------------------------")

    shot_result = grid[r][c]
    if shot_result == ".":
        print("Sorry, you missed! No ship was shot")
        grid[row][col] = "M"
    elif shot_result == "O":
        print("You hit!", end=" ")
        grid[row][col] = "X"
        if check_for_ship_sunk(row, col):
            print("Yay! A ship was completely sunk!")
            num_of_ships_sunk += 1
        else:
            print("Good job! A ship was shot")

    shots_left -= 1

    """
   # OLD CODE
    global grid
    global num_of_ships_sunk
    global shots_left

    row, col = accept_valid_placement()
    print("")
    print("----------------------------")

    if grid[row][col] == ".":
        print("Sorry you missed! No ship was shot")
        grid[row][col] = "M"
    elif grid[row][col] == "O":
        print("You hit!", end=" ")
        grid[row][col] = "X"
        if check_for_ship_sunk(row, col):
            print("Yay! A ship was completely sunk!")
            num_of_ships_sunk += 1
        else:
            print("Good job! A ship was shot")

    shots_left -= 1
    
    
def check_for_game_over():
    """
    Game over if all ships have been sunk or if the user has run out of shots
    """
    global num_of_ships_sunk
    global num_of_ships
    global shots_left
    global game_over

    if num_of_ships == num_of_ships_sunk:
        print("Congrats you won the game!")
        game_over = True
    elif shots_left <= 0:
        print("Sorry, you lost! You ran out of shots, try again next time!")
        game_over = True


def main():
    """
    Main application that runs the game and its functions
    """
    global game_over

    print()
    print("-----Welcome to Battleships-----")
    print()
    print("You have 25 shots to take down 5 ships. Let the battle begin!")
    print()

    create_grid()

    while game_over is False:
        print_grid()
        print()
        print("Number of ships remaining: " + str(num_of_ships - num_of_ships_sunk))
        print("Number of shots left: " + str(shots_left))
        print()
        attempt_shot()
        print("----------------------------")
        print("")
        check_for_game_over()

main()

