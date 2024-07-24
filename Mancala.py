BLOCK_WIDTH = 6
BLOCK_HEIGHT = 5
BLOCK_SEP = "*"
SPACE = ' '
NUM_CUPS = 6
STONES = 'Stones'

def draw_board(top_cups, bottom_cups, mancala_a, mancala_b):
    board = [[SPACE for _ in range((BLOCK_WIDTH + 1) * (len(top_cups) + 2) + 1)] for _ in range(BLOCK_HEIGHT * 2 + 3)
    ]

    for p in range(len(board)):
        board[p][0] = BLOCK_SEP
        board[p][len(board[0]) - 1] = BLOCK_SEP

    for q in range(len(board[0])):
        board[0][q] = BLOCK_SEP
        board[len(board) - 1][q] = BLOCK_SEP

    for p in range(BLOCK_WIDTH + 1, (BLOCK_WIDTH + 1) * (len(top_cups) + 1) + 1):
        board[BLOCK_HEIGHT + 1][p] = BLOCK_SEP

    for i in range(len(top_cups)):
        for p in range(len(board)):
            board[p][(1 + i) * (1 + BLOCK_WIDTH)] = BLOCK_SEP

    for p in range(len(board)):
        board[p][1 + BLOCK_WIDTH] = BLOCK_SEP
        board[p][len(board[0]) - BLOCK_WIDTH - 2] = BLOCK_SEP

    for i in range(len(top_cups)):
        draw_block(board, i, 0, top_cups[i])
        draw_block(board, i, 1, bottom_cups[i])

    draw_mancala(0, mancala_a, board)
    draw_mancala(1, mancala_b, board)

    print('\n'.join([''.join(board[i]) for i in range(len(board))]))

def draw_mancala(fore_or_aft, mancala_data, the_board):
    if fore_or_aft == 0:
        for i in range(len(mancala_data)):
            data = mancala_data[i][0: BLOCK_WIDTH].rjust(BLOCK_WIDTH)
            for j in range(len(mancala_data[0])):
                the_board[1 + i][1 + j] = data[j]
    else:
        for i in range(len(mancala_data)):
            data = mancala_data[i][0: BLOCK_WIDTH].rjust(BLOCK_WIDTH)
            for j in range(len(mancala_data[0])):
                the_board[1 + i][len(the_board[0]) - BLOCK_WIDTH - 1 + j] = data[j]

def draw_block(the_board, pos_x, pos_y, block_data):
    for i in range(BLOCK_HEIGHT):
        data = block_data[i][0:BLOCK_WIDTH].rjust(BLOCK_WIDTH)
        for j in range(BLOCK_WIDTH):
            the_board[1 + pos_y * (BLOCK_HEIGHT + 1) + i][1 + (pos_x + 1) * (BLOCK_WIDTH + 1) + j] = data[j]


# Function to check if the game is over (used to end the game loop)
def dead_game(game):
    # Check if the sum of stones in the first 6 cups or last 6 cups is zero
    if sum(game[:6]) == 0 or sum(game[7:13]) == 0:
        return False
    return True


# Function to check if a given bin number is a player's mancala
def is_player_mancala(bin_num, player_one):
    # Check if the bin number corresponds to a mancala for the player
    return (player_one and bin_num == 6) or (not player_one and bin_num == 13)


# Function to create the initial cup configuration
def create_cups(start, end, initial_stones=None, clockwise=False):
    cups = []

    # Define the range of cup numbers based on the direction
    cup_range = range(start, end + 1) if clockwise else reversed(range(start, end + 1))

    # Loop to create each cup with its initial stone count
    for i in cup_range:
        current_cup = ["Cup", str(i), "Stones"]
        initial_stone = initial_stones[i - start] if initial_stones else "0"
        current_cup.append(str(initial_stone))

        # Fill the cup with spaces for visual alignment
        for _ in range(BLOCK_HEIGHT - 3):
            current_cup.append(" " * BLOCK_WIDTH)

        cups.append(current_cup)

    return cups


# Function to create the mancalas for both players
def create_mancalas(player_one_name, player_two_name, player_one_stones, player_two_stones):
    mancala_a = []
    mancala_b = []

    # Loop to create mancala rows
    for i in range(2 * BLOCK_HEIGHT):
        if i == 2:
            # Add player names to the top of mancalas
            mancala_a.append(player_one_name.ljust(BLOCK_WIDTH))
            mancala_b.append(player_two_name.ljust(BLOCK_WIDTH))
        elif i == 6:
            # Add "Stones" label to the middle of mancalas
            mancala_a.append(STONES.ljust(BLOCK_WIDTH))
            mancala_b.append(STONES.ljust(BLOCK_WIDTH))
        elif i == 7:
            # Add the number of stones in mancalas
            mancala_a.append(player_one_stones.ljust(BLOCK_WIDTH))
            mancala_b.append(player_two_stones.ljust(BLOCK_WIDTH))
        else:
            # Fill the rest with spaces
            mancala_a.append(" " * BLOCK_WIDTH)
            mancala_b.append(" " * BLOCK_WIDTH)
    return mancala_a, mancala_b


# Function to run the Mancala game
def run_game(game, player_one_name, player_two_name, clockwise=False):
    def print_board():
        # Create the cups and mancalas configuration
        if clockwise:
            first_cups = create_cups(1, NUM_CUPS, game[0:6])
            second_cups = create_cups(8, 13, game[7:13], clockwise=True)
        else:
            first_cups = create_cups(1, NUM_CUPS, game[0:6], clockwise=True)
            second_cups = create_cups(8, 13, game[7:13])

        if player_one:
            mancala_one, mancala_two = create_mancalas(player_one_name, player_two_name, str(game[6]), str(game[13]))
        else:
            mancala_one, mancala_two = create_mancalas(player_two_name, player_one_name, str(game[13]), str(game[6]))

        # Draw the game board
        draw_board(first_cups, second_cups, mancala_one, mancala_two)

        # Function to check if a move is valid

    def valid_move(chosen_bin, player_one):
        # Check if the chosen bin is within the valid range for the current player
        if player_one:
            return 1 <= chosen_bin <= 6 and game[chosen_bin - 1] > 0
        else:
            return 8 <= chosen_bin <= 13 and game[chosen_bin - 1] > 0

        # Function to execute a player's move

    def make_move(chosen_bin, player_one):
        stones = game[chosen_bin - 1]
        game[chosen_bin - 1] = 0
        current_bin = chosen_bin

        # Distribute the stones into the cups
        while stones > 0:
            # Determine the next cup to place a stone
            current_bin = (current_bin % 14) + 1

            # Skip the opponent's mancala and continue to the next bin
            if (player_one and current_bin == 13) or (not player_one and current_bin == 6):
                current_bin = (current_bin % 14) + 1

            # Place a stone in the current bin
            game[current_bin - 1] += 1
            stones -= 1

        # Return the last bin where the last stone was placed
        return current_bin
    # Initialize player turn and another_turn flag
    player_one = True
    another_turn = False

    # Main game loop
    while dead_game(game):
        # Print the current game board
        print_board()
        player_name = player_one_name if player_one else player_two_name
        message = f"{player_name}'s turn. Choose a Cup: "
        user_input = input(message)

        chosen_bin = int(user_input)

        # Check if the chosen bin is a valid move
        if valid_move(chosen_bin, player_one):
            # Make the move and get the last bin
            last_bin = make_move(chosen_bin, player_one)

            # Check if the last stone landed in the player's mancala
            if game[last_bin - 1] == 1 and is_player_mancala(last_bin, player_one):
                print("Last stone landed in your mancala. You get another turn.")
                another_turn = True
            else:
                player_one = not player_one
                another_turn = False
        else:
            print("Invalid move. Try again")

    # Print the final game board and declare the game result
    print_board()
    print("The game is over!")

    # Determine the winner or declare a tie
    if game[6] > game[13]:
        print(f"{player_one_name} has won the game!")
    elif game[6] < game[13]:
        print(f"{player_two_name} has won the game!")
    else:
        print("The game ended in a tie")


# Function to get player names
def get_player_names():
    player_one_name = input('Player 1, please tell me your name: ')
    player_two_name = input('Player 2, please tell me your name: ')
    return player_one_name, player_two_name

# Main program entry point
if __name__ == '__main__':
    # Initial game state
    game = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]

    # Get player names
    names = get_player_names()
    player_one_name = names[0]
    player_two_name = names[1]

    # Start the Mancala game
    run_game(game, player_one_name, player_two_name)



