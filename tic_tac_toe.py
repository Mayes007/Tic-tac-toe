# Tic Tac Toe Game

board = [" " for _ in range(9)]

def print_board():
    print()
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print()

def player_move(player):
    while True:
        move = input(f"Player {player}, choose a position (1-9): ")

        if not move.isdigit():
            print("Please enter a number between 1 and 9.")
            continue

        move = int(move) - 1

        if move < 0 or move > 8:
            print("That position is out of range.")
        elif board[move] != " ":
            print("That spot is already taken.")
        else:
            board[move] = player
            break

def check_winner(player):
    win_conditions = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]

    for a, b, c in win_conditions:
        if board[a] == board[b] == board[c] == player:
            return True
    return False

def check_tie():
    return " " not in board

def play_game():
    current_player = "X"

    while True:
        print_board()
        player_move(current_player)

        if check_winner(current_player):
            print_board()
            print(f"🎉 Player {current_player} wins!")
            break

        if check_tie():
            print_board()
            print("🤝 It's a tie!")
            break

        current_player = "O" if current_player == "X" else "X"

play_game()
