import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import random
import time

# --- Constants ---
BASE = 3  # Base size of the Sudoku grid (3x3 sub-grids)
SIZE = BASE**2  # Total size of the grid (9x9)
CELL_SIZE = 50  # Size of each cell in pixels
WIDTH = CELL_SIZE * 20  # Window width
HEIGHT = WIDTH // 16 * 9  # Window height (16:9 aspect ratio)
TITLE = "Sudoku"  # App title

# --- Styles ---
ctk.set_default_color_theme("assets/custom_theme.json")
ctk.set_appearance_mode("light")

# Color Palette
PALETTE = {
    "bg": "#ffffff",
    "fg": "#344861",
    "border": "#344861",
    "primary": "#325aaf",
    "primary-hover": "#7091d5",
    "primary-bg": "#e2ebf3",
    "primary-bg-hover": "#dce3ed",
    "highlight": "#bbdefb",
    "highlight-muted": "#c3d7ea",
    "success": "#6d8265",
    "success-bg": "#def2d6",
    "error": "#b0444f",
    "error-bg": "#ebc8c4",
    "warning": "#baa57c",
    "warning-bg": "#f8f3d6",
}

# --- Application Window ---
root = ctk.CTk()
root.title(TITLE)

# Set window size and center it on the screen
x_position = (root.winfo_screenwidth() - WIDTH) // 2
y_position = (root.winfo_screenheight() - HEIGHT) // 2

root.geometry(f"{WIDTH}x{HEIGHT}+{x_position}+{y_position}")

root.minsize(WIDTH, HEIGHT)


# --- Model ---


def generate_board(difficulty=1):
    """Generate a Sudoku board with numbers pre-filled and empty cells."""

    def pattern(r, c):
        return (BASE * (r % BASE) + r // BASE + c) % SIZE

    def shuffle(s):
        return random.sample(s, len(s))

    # Create a complete board
    rBase = range(BASE)
    rows = [g * BASE + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * BASE + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, SIZE + 1))

    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    # Remove some cells based on difficulty
    squares = SIZE**2
    difficulty_map = {0: 0.2, 1: 0.3, 2: 0.45, 3: 0.6, 4: 0.75}
    empties = int(squares * difficulty_map.get(difficulty, 0.2))

    for p in random.sample(range(squares), empties):
        board[p // SIZE][p % SIZE] = ctk.StringVar(root)

    return board


def get_board_copy(board):
    """Convert a board with tk.StringVar into a plain 2D list with int."""
    return [
        [
            (
                int(cell.get())
                if isinstance(cell, ctk.StringVar) and cell.get() != ""
                else 0 if isinstance(cell, ctk.StringVar) else cell
            )
            for cell in row
        ]
        for row in board
    ]


def select_index(selected, r, c):
    """Update the current selected cell index."""
    selected[0].set(r)
    selected[1].set(c)


def get_selected_index(selected):
    """Get the current selected cell index."""
    return selected[0].get(), selected[1].get()


def write_number(n, index, board):
    """Write a number into the selected modifiable cell."""
    pass


def erase_number(index, board):
    """Erase the number of the selected modifiable cell."""
    pass


def is_board_solved(board):
    """Check if the current Sudoku board is solvable."""
    # if is_board_filled and is_board_valid
    pass


def is_board_filled(board):
    """Check if the current Sudoku board has no empty cells."""
    pass


def is_board_valid(board):
    """Check if the current Sudoku board is valid."""
    pass


def solve_board(board, r=0, c=0):
    """Solve the current Sudoku board using a backtracking algorithm."""
    # Not necessary
    pass


def show_hint(board, solved_board, index):
    """Provide a hint for the selected cell by filling in the correct value."""
    pass


# --- View ---


def create_board_widget(master, board, selected):
    """Create a widget displaying the Sudoku board."""
    frame = ctk.CTkFrame(
        master, fg_color=PALETTE["border"], border_width=2, corner_radius=0
    )

    # 2Dd list to store references to cell labels
    cell_labels = [[None] * SIZE for _ in range(SIZE)]

    # Create 3x3 subgrid frames
    for i in range(0, SIZE, BASE):
        for j in range(0, SIZE, BASE):
            subgrid_frame = ctk.CTkFrame(
                frame, fg_color="white", border_width=3, corner_radius=0
            )

            # Create cells
            for k in range(BASE):
                for l in range(BASE):
                    r, c = k + i, l + j  # Calculate global index
                    value = board[r][c]
                    modifiable = isinstance(
                        value, ctk.StringVar
                    )  # Check if cell is modifiable

                    cell_frame = ctk.CTkFrame(
                        subgrid_frame,
                        fg_color="transparent",
                        border_width=1,
                        corner_radius=0,
                    )
                    label = ctk.CTkLabel(
                        cell_frame,
                        text=str(value.get()) if modifiable else str(value),
                        textvariable=value if modifiable else None,
                        anchor="center",
                        text_color=PALETTE["primary"] if modifiable else None,
                    )

                    cell_labels[r][c] = label

                    # Add click event listener for selection
                    label.bind(
                        "<Button-1>",
                        lambda event, r=r, c=c: [
                            select_index(selected, r, c),
                            update_highlights(selected, board, cell_labels),
                        ],
                    )

                    label.pack(expand=True, fill="both", padx=1, pady=1)
                    cell_frame.grid(row=k, column=l, sticky="news")

            for m in range(BASE):
                subgrid_frame.grid_rowconfigure(m, weight=1, minsize=CELL_SIZE)
                subgrid_frame.grid_columnconfigure(m, weight=1, minsize=CELL_SIZE)

            subgrid_frame.grid(
                row=i // BASE, column=j // BASE, padx=0.5, pady=0.5, sticky="news"
            )

    return frame


def update_highlights(selected, board, cell_labels: list[list[ctk.CTkLabel]]):
    """Update the highlighting for the selected cell, row, column, and sub-grid."""
    board_copy = get_board_copy(board)
    r, c = get_selected_index(selected)
    for i in range(SIZE):
        for j in range(SIZE):
            if (i, j) == (r, c):
                cell_labels[i][j].configure(fg_color=PALETTE["highlight"])
            elif (
                board_copy[r][c]
                and board_copy[i][j]
                and board_copy[r][c] == board_copy[i][j]
            ):
                cell_labels[i][j].configure(fg_color=PALETTE["highlight-muted"])
            elif (
                r == i
                or c == j
                or ((i // BASE == r // BASE) and (j // BASE == c // BASE))
            ):
                cell_labels[i][j].configure(fg_color=PALETTE["primary-bg"])
            else:
                cell_labels[i][j].configure(fg_color="transparent")


def create_numpad_widget(master, selected, board):
    """Create a widget for entering numbers into the board."""
    frame = ctk.CTkFrame(master, fg_color="transparent")

    for i in range(1, SIZE + 1):
        btn = ctk.CTkButton(
            frame,
            text=str(i),
            font=("", 28),
            command=None,  # Implement write command
        )
        btn.grid(
            row=(i - 1) // BASE, column=(i - 1) % BASE, sticky="news", padx=5, pady=5
        )

    for k in range(BASE):
        frame.grid_rowconfigure(k, weight=1, minsize=CELL_SIZE * 2)
        frame.grid_columnconfigure(k, weight=1, minsize=CELL_SIZE * 2)

    return frame


def create_erase_btn(master, selected, board):
    """Create an button to clear the number from a cell."""
    btn = ctk.CTkButton(
        master,
        text="ERASE",
        font=("", 20),
        command=None,  # Implement erase command
    )
    return btn


def create_check_btn(master, board):
    """Create a button to check if the board is solved."""
    btn = ctk.CTkButton(
        master,
        text="CHECK",
        font=("", 20),
        command=None,  # Implement check command
    )
    return btn


def create_hint_btn(master, board, solved_board, selected):
    """Create a button to show hint."""
    btn = ctk.CTkButton(
        master,
        text="HINT",
        font=("", 20),
        command=None,  # Implement hint command
    )
    return btn


def create_timer_widget(master):
    """Create a widget for the timer."""
    frame = ctk.CTkFrame(master, fg_color="transparent")

    timer_label = ctk.CTkLabel(
        frame,
        text="00:00",
        font=("", 20),
        anchor="center",
    )

    timer_label.pack(padx=10, pady=10)

    start_time = None
    elapsed_time = 0

    def update_timer():
        nonlocal start_time, elapsed_time
        # Implement timer
        pass

    update_timer()

    return frame


def create_home_btn(master):
    """Create a button to go back to the homepage."""
    btn = ctk.CTkButton(
        master,
        text="◄",
        font=("", 25),
        fg_color="transparent",
        hover_color=PALETTE["bg"],
        anchor="w",
        command=homepage,
    )
    return btn


def show_message(master, text, type=None, duration=1000):
    """Display a temporary message (toast) on the screen."""
    message_label = ctk.CTkLabel(
        master,
        text=text,
        bg_color="transparent",
        fg_color=PALETTE.get(type + "-bg" if type else "primary-bg"),
        text_color=PALETTE.get(type if type else "primary"),
        padx=10,
        pady=10,
    )
    message_label.place(relx=0.5, rely=0.5, anchor="center")

    # Schedule the message to disappear
    master.after(duration, message_label.destroy)


def reset_ui(master):
    """Resets the UI by destroying all widgets inside master."""
    for widget in master.winfo_children():
        widget.destroy()


# --- Pages ---


def homepage():
    """Displays the homepage."""
    reset_ui(root)

    frame = ctk.CTkFrame(root)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Title
    title_label = ctk.CTkLabel(frame, text=TITLE, font=("", 36, "bold"))
    title_label.pack(padx=25, pady=25)

    # Select difficulty
    difficulties = ["Quickie", "Easy", "Medium", "Hard", "Expert"]
    selected_difficulty = ctk.IntVar(root, value=1)

    def update_difficulty(choice):
        selected_difficulty.set(difficulties.index(choice))

    difficulty_combobox = ctk.CTkComboBox(
        frame,
        values=difficulties,
        command=update_difficulty,
    )
    difficulty_combobox.set("Easy")
    difficulty_combobox.pack(padx=5, pady=5)

    # New game button
    new_game_btn = ctk.CTkButton(
        frame,
        text="New Game",
        fg_color=PALETTE["primary"],
        hover_color=PALETTE["primary-hover"],
        text_color=PALETTE["bg"],
        command=lambda: start_game(selected_difficulty.get()),
    )
    new_game_btn.pack(padx=5, pady=5)

    # Help button
    help_btn = ctk.CTkButton(
        frame,
        text="Help",
        command=help_page,
    )
    help_btn.pack(padx=5, pady=10)


def help_page():
    """Displays the help page."""
    reset_ui(root)

    frame = ctk.CTkFrame(root)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Home button
    home_btn = create_home_btn(frame)
    home_btn.pack(fill="x", anchor="w", padx=5, pady=5)

    # Title
    title_label = ctk.CTkLabel(frame, text="Help", font=("", 36, "bold"))
    title_label.pack(padx=25, pady=25)

    # Instructions
    instructions = (
        "Sudoku is a logic-based number puzzle game.\n" "Further instructions here...\n"
    )

    instructions_label = ctk.CTkLabel(frame, text=instructions, anchor="w")
    instructions_label.pack(padx=25, pady=25)


def start_game(difficulty):
    """Starts a game."""
    reset_ui(root)

    # Initialize variables
    board = generate_board(difficulty)
    solved_board = solve_board(get_board_copy(board))
    selected = (ctk.IntVar(root, value=-1), ctk.IntVar(root, value=-1))

    # Create widgets
    header_frame = ctk.CTkFrame(root)
    home_btn = create_home_btn(header_frame)
    title_label = ctk.CTkLabel(header_frame, text=TITLE, font=("", 24, "bold"))
    timer_widget = create_timer_widget(header_frame)

    board_frame = ctk.CTkFrame(root)
    board_widget = create_board_widget(board_frame, board, selected)

    controls_frame = ctk.CTkFrame(root)
    erase_btn = create_erase_btn(controls_frame, selected, board)
    check_btn = create_check_btn(controls_frame, board)
    hint_btn = create_hint_btn(controls_frame, board, solved_board, selected)
    numpad_widget = create_numpad_widget(controls_frame, selected, board)

    # Place widgets
    # Header
    header_frame.grid_columnconfigure(0, weight=1)
    header_frame.grid_columnconfigure(1, weight=1)
    header_frame.grid_columnconfigure(2, weight=1)
    home_btn.grid(row=0, column=0, sticky="w")
    title_label.grid(row=0, column=1, sticky="nsew")
    timer_widget.grid(row=0, column=2, sticky="e")

    # Board
    board_widget.pack(anchor="e")

    # Controls
    erase_btn.grid(row=0, column=0, padx=5, pady=5)
    check_btn.grid(row=0, column=1, padx=5, pady=5)
    hint_btn.grid(row=0, column=3, padx=5, pady=5)
    numpad_widget.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

    # All
    header_frame.pack(padx=10, pady=10, fill="x")
    board_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)
    controls_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)


def main():
    homepage()
    root.mainloop()


if __name__ == "__main__":
    main()