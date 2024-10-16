# Beginning of main.py File
from tkinter import *
import miscellaneous
from cell import *
import Game_ui

#creating the root window
root = Game_ui.create_root()

# Creating start menu frame (will contain sign-in, login, play as guest buttons)
start_menu = Frame(
    root,
    bg='black',
    width=miscellaneous.WIDTH,
    height=miscellaneous.HEIGHT
)
start_menu.place(x=0, y=0)
start_menu.propagate(False)

# creating main menu frame that (will contain play, scores, resume game buttons 
main_menu = Frame(
    root,
    bg='black',
    width=miscellaneous.WIDTH,
    height=miscellaneous.HEIGHT
)
main_menu.propagate(False)

# creating game frame which will contain the game elements (title, board, score counter)
game_frame = Frame(
    root,
    bg='black',
    width=miscellaneous.WIDTH,
    height=miscellaneous.HEIGHT
)
game_frame.propagate(False)

my_score_frame = Frame(
    root,
    bg='black',
    width=miscellaneous.WIDTH,
    height=miscellaneous.HEIGHT
)
my_score_frame.propagate(False)

# creating start menu elements
Game_ui.create_start_menu_elements(main_menu, my_score_frame, game_frame, start_menu, root)

# Program start
root.mainloop()