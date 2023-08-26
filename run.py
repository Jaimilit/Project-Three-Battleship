import random
import time

# Key
# . water
# O part of a ship
# X is a hit
# M is a miss

# Variables
"""
grid_size = 10
num_of_ships = 5
shots_left = 25
game_over = False
num_of_ships_sunk = 0
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ship_positions = []
grid = []
"""
instructions = (
    "Welcome to the Battleships game!\n\n"
    "Instructions:\n"
    "1. You have 25 shots to take down 5 ships of different sizes.\n"
    "2. Your goal is to sink all the ships on the grid.\n"
    "3. Enter your shot's row (A-J) and column (0-9) when prompted.\n"
    "4. '.' is water, 'X' is a hit, and 'M' is a miss.\n"
    "5. Ships will be placed randomly on the grid at the start of the game.\n"
    "6. A ship is sunk when all its parts are hit.\n"
    "7. When all 5 ships are sunk you win the game! \n\n"
    "LET THE BATTLE BEGIN!"
)

class Ship:
    """
    Use class method for items such a ship
    """

    SHIP_TYPES = {
        "Carrier": 5,
        "Battleship": 4,
        "Cruiser": 3,
        "Submarine": 3,
        "Destroyer": 2
    }

    def __init__(self, ship_type, size, board):
        """ 
        Initialize a Ship object with its attributes

        """
        self.ship_type = ship_type
        self.size = size
        self.position = []  
        self.hit_coordinates = set()  
        self.board = board  

    def place(self, start_coordinate, orientation):
            """
            Place the ship on the board with a given starting coordinate and orientation
            It performs checks to ensure that the placement is valid and raises errors 
            if the placement would conflict with existing ship positions or if an invalid orientation is provided
            """
            x, y = start_coordinate
            temp_positions = []

            if orientation == "horizontal":
                for i in range(self.size):
                    temp_positions.append((x + i, y))
            elif orientation == "vertical":
                for i in range(self.size):
                    temp_positions.append((x, y + i))
            else:
                raise ValueError("Invalid orientation. It should be either 'horizontal' or 'vertical'.")

            for coord in temp_positions:
                if coord in self.board.ships_positions():  
                    raise ValueError(f"A ship is already placed at coordinate {coord}")

            self.position = temp_positions

    def is_hit(self, coordinate):
            """
            Checks if a shot hits a ship. If so, mark it and return True.
            """
            if coordinate in self.position and coordinate not in self.hit_coordinates:
                self.hit_coordinates.add(coordinate)
                return True
            return False

    def is_sunk(self):
            """
            Checks whether a ship is sunk by comparing the number of hit coordinates to the size of the ship
            If all coordinates have been hit, the function returns True; otherwise, it returns False
            """
            return len(self.hit_coordinates) == self.size

class Board:
    """
    Use class for board, board size 10x10 as default
    """
    def __init__(self, size=10): 
        self.size = size
        self.grid = [['.' for _ in range(size)] for _ in range(size)]
        self.ships = []
    
    def ships_positions(self):
        """
        Return a list of all ship coordinates on the board
        """
        positions = []
        for ship in self.ships:
            positions.extend(ship.position)
        return positions
    
    def get_ship_at_coordinate(self, coordinate):
        """
        Return the ship at the given coordinate or None if there's no ship
        """
        x, y = coordinate
        for ship in self.ships:
            if (x, y) in ship.position:
                return ship
        return None
    
    def place_ship(self, ship, start_coordinate, orientation):
        """
        Attempt to place a ship on the board
        Ensures coorindates are not out of range of the board for vertical & horizational
        Places ships as an O on the board
        """
        x, y = start_coordinate

        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            raise ValueError(f"Coordinates {start_coordinate} are out of the board's range.")

        if orientation == "horizontal":
            if x + ship.size > self.size:
                raise ValueError(
                    f"Ship cannot be placed at {start_coordinate} in {orientation} orientation. "
                    f"It will go out of the board.")
        elif orientation == "vertical":
            if y + ship.size > self.size:
                raise ValueError(
                    f"Ship cannot be placed at {start_coordinate} in {orientation} orientation. "
                    f"It will go out of the board.")
        else:
            raise ValueError("Invalid orientation. It should be either 'horizontal' or 'vertical'.")

        ship.place(start_coordinate, orientation)
        self.ships.append(ship)

        for coord in ship.position:
            x, y = coord
            self.grid[x][y] = 'O'  

    def random_place_ship(self):
        """
        Randomly chooses a ship type, creates it, and places it on the board without collisions or
        going outside the board
        Uses max attempts to avoid infinite loops in tight scenarios
        Once the ship has been placed successfully, exit the method
        Choose orientation again for each attempt
        """

        ship_name, ship_size = random.choice(list(Ship.SHIP_TYPES.items()))
        ship = Ship(ship_name, ship_size, self)

        attempts = 0
        max_attempts = 1000  

        orientation = random.choice(["horizontal", "vertical"])

        while attempts < max_attempts:
            if orientation == "horizontal":
                x = random.randint(0, self.size - 1)
                y = random.randint(0, self.size - ship_size)
            else:  # vertical
                x = random.randint(0, self.size - ship_size)
                y = random.randint(0, self.size - 1)

            try:
                self.place_ship(ship, (x, y), orientation)
                return  
            except ValueError:
                attempts += 1
                orientation = random.choice(["horizontal", "vertical"])  

        raise RuntimeError("Unable to randomly place the ship after many attempts.")

    def check_hit(self, coordinate):
        """
        Check if a shot hits a ship on the board
        Mark hit on board with 'X'
        Mark miss on board with 'M'
        """
        x, y = coordinate
        for ship in self.ships:
            if ship.is_hit(coordinate):
                self.grid[x][y] = 'X'  
                if ship.is_sunk():
                    print("Yay! A ship was completely sunk!")
                return True
        else:
            if self.check_valid(coordinate):
                self.grid[x][y] = 'M'  
                print("Sorry you missed! No ship was hit.")
            return False
    
    def check_valid(self, coordinate):
        """
        Checks coorindate is valid placement
        """
        x, y = coordinate
        if not (0 <= x < self.size and 0 <= y < self.size):
            return False
        if not (self.grid[x][y] == "." or self.grid[x][y] == "O"):
            return False
        return True
    
    def all_ships_sunk(self):
        """
        Checks if all ships on the board are sunk by iterating through
        is_sunk method
        """
        return all(ship.is_sunk() for ship in self.ships)

    def display(self):
        """
        Displays the board to the console
        Print rows with A-J labels
        Use ASCII method
        """
        print('   ' + ' '.join([str(i) for i in range(self.size)]))

        for i in range(self.size):
            row_label = chr(i + 65)  
            print(f"{row_label}) {' '.join(self.grid[i])}")
    
    @staticmethod
    def print_boards(board1, board2, board1_name="Player 1", board2_name="Player 2"):
        """
        Static method to print two boards side-by-side 
        Board 1 is for player 1
        Board 2 is for player 2
        """
        print(f"{board1_name: <15}{'': <10}{board2_name: <15}")
        print("   " + " ".join(map(str, range(board1.size))) + "        " + " ".join(map(str, range(board2.size))))

        for i in range(board1.size):
            row_letter = chr(65 + i)  
            print(f"{row_letter}) {' '.join(board1.grid[i])}     {row_letter}) {' '.join(board2.grid[i])}")

class Player:
    def __init__(self, name, board_size=10, opponent=None, is_computer=False):
        """ 
        Use init method to store attributes that will later be changed for player
        Own board is where the player places ships
        The Guess board to keep track of shots taken
        """
        self.name = name
        self.own_board = Board(board_size)  
        self.guess_board = Board(board_size)  
        self.is_computer = is_computer
        self.opponent = opponent
        self.number_of_plays = 0
    
    def place_ship(self, ship_name, start_coordinate, orientation):
        """
        Allows player to place a ship on their own game board
        """
        ship_size = Ship.SHIP_TYPES[ship_name]
        new_ship = Ship(ship_name, ship_size, self.own_board)
        self.own_board.place_ship(new_ship, start_coordinate, orientation)
    
    def take_turn(self):
        """
        Represents a player's turn in the game
        Allows a player to choose a coordinate to shoot at opponent's/computer's board
        If the player is the computer, it chooses a random valid coordinate
        If the player is human, it prompts the user to enter a coordinate until a valid one is provided
        It checks if the chosen coordinate is a valid move (not already played and within the board)
        If the move is valid, it takes a shot at the chosen coordinate on the opponent's board
        Finally, it increments the number of plays.
        """
        valid_play = False
        x, y = -1, -1
        while not valid_play:
            if self.is_computer:
                x, y = random.choice([(i, j) for i in range(self.own_board.size) for j in range(self.own_board.size)])
            else:
                good_input = False
                while not good_input:
                    try:
                        x, y = self.coordinate_from_string(input("Please enter row A-J and column 0-9."
                          "\nExample C6: "))
                        good_input = True
                    except ValueError as e:
                        print(f"Invalid input: {e}. Please enter a valid input such as C6.")

            valid_play = self.opponent.own_board.check_valid((x, y))
            if not valid_play:
                print("That coordinate is already played or outside of the board")
        self.take_shot((x, y), self.opponent)
        self.number_of_plays += 1

    def take_shot(self, coordinate, opponent):
        """
        Takes a shot at the opponent's board
        Checks if the shot hits any of the opponent's ships
        Let's the user know if it doesn't hit, mark it as a miss
        """
        x, y = coordinate
        if not self.opponent.own_board.check_valid(coordinate):
            return "Invalid shot"
        if opponent.own_board.check_hit((x, y)):
            msg = "Hit!"
            self.guess_board.grid[x][y] = 'X'
            ship = self.opponent.own_board.get_ship_at_coordinate(coordinate)
            if ship.is_sunk():
                msg += f"{ship.ship_type} is sunk!"
            return msg
       
        self.guess_board.grid[x][y] = 'M'
        return "Sorry you missed! No ship was hit."

    @staticmethod
    def coordinate_from_string(input_str):
        """
        Translates a string input like 'a4' to its corresponding board coordinates.
        Returns a tuple (row, col)
        """
        if len(input_str) < 2 or not input_str[0].isalpha() or not input_str[1:].isdigit():
            raise ValueError("Invalid input format")

        row = ord(input_str[0].upper()) - ord('A')
        col = int(input_str[1:])

        return row, col

class Game:
    def __init__(self, player1, player2):
        """
         Uses class for game and players - 1 and 2
        """
        self.player1 = player1
        self.player2 = player2
        self.player1.opponent = self.player2
        self.player2.opponent = self.player1
    
    def check_win(self):
        """
        Checks if the given player has sunk all opponent's ships
        and can win the game or if player has reached maximum number of plays/shots
        """
        if self.player1.own_board.all_ships_sunk():
            print(f"{self.player2.name} won!")
            return True
        elif self.player2.own_board.all_ships_sunk():
            print(f"{self.player1.name} won!")
            return True
        if self.player1.number_of_plays >= 25 or self.player2.number_of_plays >= 25:
            print(f"Game over... Your 25 shots are up!")
            return True
    
    def place_ships_randomly(self, amount):
        """
        Places a specified number of ships randomly on both players' boards
        """
        for i in range(amount):
            self.player1.own_board.random_place_ship()
            self.player2.own_board.random_place_ship()
    
    def take_turn(self, current_player):
        """
        Player and computer take turns
        Checks if player or computer won
        """
        print(f"{current_player.name} played {current_player.number_of_plays} times!")
        print(f"{current_player.name}'s turn!")

        current_player.take_turn()

        if self.check_win():
            return True
        return False
    
    def play(self):
        """
        Plays the game
        Show person's board and computer's board
        Takes turns
        """
        print(instructions)
        while True:

            Board.print_boards(self.player1.own_board, self.player1.guess_board, "User's board", "Computer's board")
            if self.take_turn(self.player1):
                break
    
            Board.print_boards(self.player1.own_board, self.player1.guess_board, "User's board", "Computer's board")
            time.sleep(2)
            if self.take_turn(self.player2):
                break

        print("Game Over!")

def main():
    """
    Main application that runs the game and its functions
    """

    Ship: Ship(ship_type, size, board)
    
    user = Player("User")
    computer = Player("Computer", is_computer=True)

    battle_ship_game = Game(user, computer)

    battle_ship_game.place_ships_randomly(4)

    battle_ship_game.play()

if __name__ == "__main__":
    main()


"""
def create_grid_and_check_location(start_row, end_row, start_col, end_col, grid_to_check):
    for r in range(start_row, end_row):
        for c in range(start_col, end_col):
            if grid_to_check[r][c] != ".":
                return False
    return True

def place_ships(row, col, direction, length, grid_to_place):
    delta = 1 if direction in {"right", "down"} else -1
    if direction in {"left", "right"}:
        start_col, end_col = col - length + 1, col + delta
        start_row, end_row = row, row + 1
    elif direction in {"up", "down"}:
        start_row, end_row = row - length + 1, row + delta
        start_col, end_col = col, col + 1

    if create_grid_and_check_location(start_row, end_row, start_col, end_col, grid_to_place):
        ship_positions_to_mark = []
        for i in range(length):
            if direction == "left":
                ship_positions_to_mark.append((row, col - i))
            elif direction == "right":
                ship_positions_to_mark.append((row, col + i))
            elif direction == "up":
                ship_positions_to_mark.append((row - i, col))
            else:
                ship_positions_to_mark.append((row + i, col))
        
        if all(0 <= r < grid_size and 0 <= c < grid_size for r, c in ship_positions_to_mark):
            ship_positions.extend(ship_positions_to_mark)
            return True
    return False

def create_grid(size):
    rows, cols = (size, size)
    grid_to_create = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(".")
        grid_to_create.append(row)
    return grid_to_create

def create_computer_grid():
    global computer_grid
    computer_grid = create_grid(computer_grid_size)

def place_computer_ships():
    global computer_ship_positions
    for _ in range(num_of_ships):
        while True:
            random_row = random.randint(0, computer_grid_size - 1)
            random_col = random.randint(0, computer_grid_size - 1)
            direction = random.choice(["left", "right", "up", "down"])
            ship_size = random.randint(3, 5)
            if place_ships(random_row, random_col, direction, ship_size, computer_grid):
                ship_positions_to_mark = []
                for i in range(ship_size):
                    if direction == "left":
                        ship_positions_to_mark.append((random_row, random_col - i))
                    elif direction == "right":
                        ship_positions_to_mark.append((random_row, random_col + i))
                    elif direction == "up":
                        ship_positions_to_mark.append((random_row - i, random_col))
                    else:
                        ship_positions_to_mark.append((random_row + i, random_col))
                
                if all(0 <= row < computer_grid_size and 0 <= col < computer_grid_size for row, col in ship_positions_to_mark):
                    computer_ship_positions.append((random_row, random_col, direction, ship_size))

                    # Mark ship positions on computer_grid
                    for position in ship_positions_to_mark:
                        row, col = position
                        computer_grid[row][col] = "O"
                    break

def print_grids(player_grid, computer_grid, player_ship_positions, computer_ship_positions):
    global grid_size, alphabet
    debug_mode = True
    alphabet = alphabet[:len(player_grid) + 1]

    print("   ", end="")
    for i in range(len(player_grid[0])):
        print(f"{i} ", end="")
    print("      ", end="")
    for i in range(len(computer_grid[0])):
        print(f"{i} ", end="")
    print()

    for row, (player_row, computer_row) in enumerate(zip(player_grid, computer_grid)):
        print(f"{alphabet[row]}) ", end="")
        for col, cell in enumerate(player_row):
            if (row, col) in player_ship_positions:
                print("O", end=" ")
            else:
                print(cell, end=" ")
        print("    ", end="")
        for cell in computer_row:
            print(cell, end=" ")
        print()


def accept_valid_placement():
    
    will get data from user (row & column) to place shot on grid
    writes error to user if input is incorrect
    

    global alphabet
    global grid
    global grid_size

    while True:
        placement = input("Please enter row A-J and column 0-9."
                          "\nExample C6: ").upper()

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

def check_for_ship_sunk(row, col):
    
    Checks if a ship at the given position is completely sunk.
    
    global computer_ship_positions

    for ship_position in computer_ship_positions:
        ship_row, ship_col, ship_direction, ship_size = ship_position
        if ship_direction == "left":
            if (ship_row == row and ship_col - ship_size + 1 <= col <= ship_col):
                return False
        elif ship_direction == "right":
            if (ship_row == row and ship_col <= col <= ship_col + ship_size - 1):
                return False
        elif ship_direction == "up":
            if (ship_col == col and ship_row - ship_size + 1 <= row <= ship_row):
                return False
        elif ship_direction == "down":
            if (ship_col == col and ship_row <= row <= ship_row + ship_size - 1):
                return False
    return True
    
def computer_turn():
    global computer_grid, shots_left_computer
    print("\nComputer's Turn:")
    time.sleep(1)
    while True:
        row = random.randint(0, computer_grid_size - 1)
        col = random.randint(0, computer_grid_size - 1)
        if computer_grid[row][col] in {"M", "X"}:
            continue
        if computer_grid[row][col] in {".", "O"}:
            break
    print(f"Computer shoots at {alphabet[row]}{col}: ", end="")
    if computer_grid[row][col] == ".":
        print("Computer missed!")
        computer_grid[row][col] = "M"
    elif computer_grid[row][col] == "O":
        print("Computer hit!")
        computer_grid[row][col] = "X"  # Update the computer grid to display the hit
    shots_left_computer -= 1
    time.sleep(1)
    
def attempt_shot():
    
    updates grid and ships based on where the shot was located
    tells user if their shot missed, hit a ship, and if a ship was completely
    sunk
    

    global grid
    global num_of_ships_sunk
    global shots_left

    row, col = accept_valid_placement()
    print("")
    print("\n" + "-" * 28)

    if grid[row][col] == ".":
        print("Sorry you missed! No ship was hit.")
        grid[row][col] = "M"
    elif grid[row][col] == "O":
        print("You hit!", end=" ")
        grid[row][col] = "X"
        if check_for_ship_sunk(row, col):
            print("Yay! A ship was completely sunk!")
            num_of_ships_sunk += 1
        else:
            print("Good job! A ship was hit!")

    shots_left -= 1

def check_for_game_over():
    
    game over if all ships have been sunk or if the user has run out of shots
    

    global num_of_ships_sunk
    global num_of_ships
    global shots_left
    global game_over

    if num_of_ships == num_of_ships_sunk:
        print("Congrats! You won the game! You sunk all 5 ships!")
        game_over = True
    elif shots_left <= 0:
        print("Sorry, you lost! You ran out of shots, try again next time!")
        game_over = True



def main():
    global game_over, grid, computer_grid, computer_ship_positions
    print("\n-----Welcome to Battleships-----\n")
    print(instructions)
    grid = create_grid(grid_size)
    create_computer_grid()
    place_computer_ships()

    while not game_over:
        print_grids(grid, computer_grid, ship_positions, computer_ship_positions)
        print("\nYour Turn:")
        print("Ships remaining: " + str(num_of_ships - num_of_ships_sunk))
        print("Shots left: " + str(shots_left))
        attempt_shot()
        check_for_game_over()
        if not game_over:
            print_grids(grid, computer_grid, ship_positions, computer_ship_positions)
            computer_turn()
            check_for_game_over()

if __name__ == "__main__":
    main()

"""