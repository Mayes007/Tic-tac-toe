import tkinter as tk
import random
import math

# ---------------- CONSTANTS ----------------
PLAYER_X = "X"
PLAYER_O = "O"
EMPTY = ""

X_COLOR = "#1f77b4"
O_COLOR = "#d62728"
WIN_COLOR = "#2ecc71"

LIGHT_BG = "#f0f0f0"
DARK_BG = "#2b2b2b"
LIGHT_TEXT = "#000000"
DARK_TEXT = "#ffffff"

current_bg = LIGHT_BG
current_fg = LIGHT_TEXT

# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("Tic Tac Toe")

# ---------------- GAME STATE ----------------
board = [[EMPTY]*3 for _ in range(3)]
buttons = [[None]*3 for _ in range(3)]

current_player = PLAYER_X
game_over = False

mode = "AI"           # AI or PVP
difficulty = "Hard"   # Easy, Medium, Hard

dark_mode = False

scores = {"X": 0, "O": 0, "Draw": 0}

# ---------------- LABELS ----------------
mode_label = tk.Label(root, text="Mode: Player vs AI", font=("New Time Roman", 12))
mode_label.grid(row=0, column=0, columnspan=3)

difficulty_label = tk.Label(root, text="Difficulty: HARD", font=("New Time Roman", 12))
difficulty_label.grid(row=1, column=0, columnspan=3)

status_label = tk.Label(root, text="Player X's turn", font=("New Time Roman", 14))
status_label.grid(row=2, column=0, columnspan=3, pady=5)

score_label = tk.Label(root, text="X: 0  O: 0  Draws: 0", font=("New Time Roman", 12))
score_label.grid(row=3, column=0, columnspan=3)

# ---------------- GAME LOGIC ----------------
def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0], [(i,0),(i,1),(i,2)]
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i], [(0,i),(1,i),(2,i)]

    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0], [(0,0),(1,1),(2,2)]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2], [(0,2),(1,1),(2,0)]

    if all(board[r][c] != EMPTY for r in range(3) for c in range(3)):
        return "Draw", []

    return None, []

def minimax(is_max):
    result, _ = check_winner()
    if result == PLAYER_O:
        return 1
    if result == PLAYER_X:
        return -1
    if result == "Draw":
        return 0

    if is_max:
        best = -math.inf
        for r in range(3):
            for c in range(3):
                if board[r][c] == EMPTY:
                    board[r][c] = PLAYER_O
                    best = max(best, minimax(False))
                    board[r][c] = EMPTY
        return best
    else:
        best = math.inf
        for r in range(3):
            for c in range(3):
                if board[r][c] == EMPTY:
                    board[r][c] = PLAYER_X
                    best = min(best, minimax(True))
                    board[r][c] = EMPTY
        return best

def ai_move():
    empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == EMPTY]

    if difficulty == "Easy":
        return random.choice(empty_cells)

    if difficulty == "Medium" and random.random() < 0.5:
        return random.choice(empty_cells)

    best_score = -math.inf
    move = None
    for r, c in empty_cells:
        board[r][c] = PLAYER_O
        score = minimax(False)
        board[r][c] = EMPTY
        if score > best_score:
            best_score = score
            move = (r, c)
    return move

# ---------------- GAME FLOW ----------------
def handle_click(r, c):
    global current_player, game_over

    if board[r][c] != EMPTY or game_over:
        return

    board[r][c] = current_player
    buttons[r][c].config(
        text=current_player,
        fg=X_COLOR if current_player == PLAYER_X else O_COLOR
    )

    result, cells = check_winner()
    if result:
        end_game(result, cells)
        return

    switch_turn()

def switch_turn():
    global current_player

    current_player = PLAYER_O if current_player == PLAYER_X else PLAYER_X
    status_label.config(text=f"Player {current_player}'s turn")

    if mode == "AI" and current_player == PLAYER_O:
        root.after(400, ai_turn)

def ai_turn():
    r, c = ai_move()
    handle_click(r, c)

# ---------------- END GAME ----------------
def end_game(result, cells):
    global game_over
    game_over = True

    if result == "Draw":
        scores["Draw"] += 1
        status_label.config(text="It's a draw 🤝")
    else:
        scores[result] += 1
        status_label.config(text=f"Player {result} wins 🏆")
        for r, c in cells:
            buttons[r][c].config(bg=WIN_COLOR)

    update_score()

def update_score():
    score_label.config(
        text=f"X: {scores['X']}  O: {scores['O']}  Draws: {scores['Draw']}"
    )

# ---------------- CONTROLS ----------------
def reset_game():
    global game_over, current_player
    game_over = False
    current_player = PLAYER_X

    for r in range(3):
        for c in range(3):
            board[r][c] = EMPTY
            buttons[r][c].config(text="", bg=current_bg, fg=current_fg)

    status_label.config(text=f"Player X's turn")

def set_mode(new_mode):
    global mode
    mode = new_mode
    mode_label.config(text=f"Mode: {'Player vs Player' if mode == 'PVP' else 'Player vs AI'}")
    reset_game()

def set_difficulty(level):
    global difficulty
    difficulty = level
    difficulty_label.config(text=f"Difficulty: {difficulty.upper()}")
    reset_game()

def toggle_dark_mode():
    global dark_mode, current_bg, current_fg
    dark_mode = not dark_mode
    current_bg = DARK_BG if dark_mode else LIGHT_BG
    current_fg = DARK_TEXT if dark_mode else LIGHT_TEXT

    # update UI colors
    root.config(bg=current_bg)
    for label in [mode_label, difficulty_label, status_label, score_label]:
        label.config(bg=current_bg, fg=current_fg)
    for r in range(3):
        for c in range(3):
            buttons[r][c].config(bg=current_bg, fg=current_fg)

# ---------------- BOARD ----------------
for r in range(3):
    for c in range(3):
        btn = tk.Button(
            root,
            text="",
            font=("New Time Roman", 24),
            width=5,
            height=2,
            bg=current_bg,
            fg=current_fg,
            command=lambda r=r, c=c: handle_click(r, c)
        )
        btn.grid(row=r+4, column=c)
        buttons[r][c] = btn

# ---------------- BUTTONS ----------------
tk.Button(root, text="Restart", command=reset_game).grid(row=7, column=0, columnspan=3, pady=5)
tk.Button(root, text="Toggle Dark/Light Mode", command=toggle_dark_mode).grid(row=8, column=0, columnspan=3)

tk.Button(root, text="Player vs AI", command=lambda: set_mode("AI")).grid(row=9, column=0, columnspan=3)
tk.Button(root, text="Player vs Player", command=lambda: set_mode("PVP")).grid(row=10, column=0, columnspan=3)

tk.Button(root, text="Easy", command=lambda: set_difficulty("Easy")).grid(row=11, column=0)
tk.Button(root, text="Medium", command=lambda: set_difficulty("Medium")).grid(row=11, column=1)
tk.Button(root, text="Hard", command=lambda: set_difficulty("Hard")).grid(row=11, column=2)

root.mainloop()
